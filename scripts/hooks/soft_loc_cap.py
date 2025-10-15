import sys, argparse, pathlib
parser = argparse.ArgumentParser(); parser.add_argument("--max", type=int, required=True)
args, paths = parser.parse_known_args()
bad = []
for p in paths:
    if pathlib.Path(p).suffix == ".py":
        n = sum(1 for _ in open(p, "r", encoding="utf-8"))
        if n > args.max:
            bad.append((p, n))
if bad:
    for p, n in bad:
        print(f"{p}: {n} LOC > {args.max}", file=sys.stderr)
    sys.exit(1)


