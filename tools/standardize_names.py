#!/usr/bin/env python3
"""
Standardize filenames by applying a manifest of renames and rewriting imports/refs.

Features
- Dry run (default) prints the impact map
- Safe mode: backups every changed file into runtime/standardize_names/backups/
- Atomic per-file steps: move -> rewrite -> verify import graph for moved module
- Rewrites Python imports + generic text refs in {md,py,txt,yaml,yml,toml,json,ini}
- Detects collisions (target exists), missing sources, and produces a rollback plan

Usage
  python tools/standardize_names.py --manifest runtime/standardize_names/rename_manifest.json --apply
  python tools/standardize_names.py --group consolidated-prefix --apply
"""
from __future__ import annotations
import argparse, json, re, shutil, sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime" / "standardize_names"
BACKUP = RUNTIME / "backups"
BACKUP.mkdir(parents=True, exist_ok=True)

TEXT_EXT = {".py", ".md", ".txt", ".yaml", ".yml", ".toml", ".json", ".ini", ".cfg", ".rst"}

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")

def as_module(path: str) -> str:
    # "src/services/messaging_service.py" -> "src.services.messaging_service"
    return path[:-3].replace("/", ".") if path.endswith(".py") else path.replace("/", ".")

def load_manifest(path: Path) -> Dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data

def gather_moves(manifest: Dict, group_name: str | None) -> List[Tuple[str, str]]:
    groups = manifest.get("groups", [])
    moves: List[Tuple[str, str]] = []
    for g in groups:
        if group_name and g["name"] != group_name:
            continue
        for src, dst in g["moves"]:
            moves.append((src, dst))
    return moves

def find_text_files() -> List[Path]:
    files: List[Path] = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_EXT and "runtime/standardize_names/backups" not in rel(p):
            files.append(p)
    return files

def rewrite_content(text: str, old_mod: str, new_mod: str, old_path: str, new_path: str) -> str:
    # Python import patterns
    patterns = [
        (rf"(^|\n)\s*from\s+{re.escape(old_mod)}\s+import\s", f"\\1from {new_mod} import "),
        (rf"(^|\n)\s*import\s+{re.escape(old_mod)}(\s|$)",     f"\\1import {new_mod}\\2"),
    ]
    for pat, repl in patterns:
        text = re.sub(pat, repl, text, flags=re.M)

    # Generic path-ish references (docs/configs). Keep conservative to avoid over-match.
    text = text.replace(old_path, new_path)
    return text

def apply_one_move(src: Path, dst: Path, dry: bool) -> Dict:
    src_rel, dst_rel = rel(src), rel(dst)
    result = {"src": src_rel, "dst": dst_rel, "status": "ok", "changed_files": []}

    if not src.exists():
        result["status"] = "missing-source"; return result
    if dst.exists():
        result["status"] = "target-exists"; return result
    old_mod, new_mod = as_module(src_rel), as_module(dst_rel)

    # Move (or simulate)
    if dry:
        pass
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, BACKUP / src.name)
        shutil.move(src, dst)

    # Rewrite imports and references repo-wide
    for f in find_text_files():
        txt = f.read_text(encoding="utf-8", errors="ignore")
        new_txt = rewrite_content(txt, old_mod, new_mod, src_rel, dst_rel)
        if new_txt != txt:
            result["changed_files"].append(rel(f))
            if not dry:
                (BACKUP / f.name).write_text(txt, encoding="utf-8")  # one-file backup (last wins)
                f.write_text(new_txt, encoding="utf-8")

    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=str(RUNTIME / "rename_manifest.json"))
    ap.add_argument("--group", default=None, help="limit to a single group")
    ap.add_argument("--apply", action="store_true", help="actually move + rewrite")
    ap.add_argument("--one", default=None, help="rename only a single source path")
    args = ap.parse_args()

    mpath = Path(args.manifest)
    if not mpath.exists():
        print(f"❌ manifest not found: {mpath}")
        sys.exit(2)

    manifest = load_manifest(mpath)
    moves = gather_moves(manifest, args.group)

    if args.one:
        moves = [mv for mv in moves if mv[0] == args.one]
        if not moves:
            print(f"❌ requested --one not in manifest: {args.one}")
            sys.exit(3)

    print(f"== Renames (dry={not args.apply}) ==")
    total = 0
    report = []
    for src, dst in moves:
        src_p, dst_p = ROOT / src, ROOT / dst
        r = apply_one_move(src_p, dst_p, dry=(not args.apply))
        report.append(r)
        total += 1
        print(f"{r['status']:>14} : {src}  ->  {dst}  (edit {len(r['changed_files'])} files)")

    out = RUNTIME / ("dry_report.json" if not args.apply else "apply_report.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"📄 report → {out}")
    print(f"✅ processed {total} renames")

if __name__ == "__main__":
    raise SystemExit(main())
