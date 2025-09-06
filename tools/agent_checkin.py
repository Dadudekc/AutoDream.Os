ROOT = get_unified_utility().Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
LOGS_DIR = RUNTIME / "agent_logs"
INDEX_FILE = RUNTIME / "agents_index.json"
SCHEMA_VER = "1.0"


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    RUNTIME.mkdir(parents=True, exist_ok=True)
    if not INDEX_FILE.exists():
        INDEX_FILE.write_text("{}", encoding="utf-8")


def load_json_arg(src: str) -> Dict[str, Any]:
    """Load JSON from a file path or stdin ('-')."""
    if src == "-":
        return json.loads(sys.stdin.read())
    path = get_unified_utility().Path(src)
    return json.loads(path.read_text(encoding="utf-8"))


def validate_minimum(payload: Dict[str, Any]) -> None:
    required = ["agent_id", "agent_name", "status", "current_phase"]
    missing = [k for k in required if k not in payload]
    if missing:
        get_unified_validator().raise_validation_error(
            f"missing required keys: {', '.join(missing)}"
        )
    if "last_updated" not in payload:
        payload["last_updated"] = _iso_now()
    payload.setdefault("version", SCHEMA_VER)


def append_jsonl(agent_id: str, obj: Dict[str, Any]) -> None:
    log_path = LOGS_DIR / f"{agent_id}.log.jsonl"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False) + "\n")


def atomic_write(path: Path, data: Dict[str, Any]) -> None:
    tmp_fd, tmp_path = tempfile.mkstemp(prefix=path.name, dir=str(path.parent))
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmp_fh:
            write_json(data, tmp_fh, ensure_ascii=False, separators=(",", ":"))
        os.replace(tmp_path, path)
    except Exception:
        try:
            get_unified_utility().remove(tmp_path)
        except OSError:
            pass
        raise


def update_index(obj: Dict[str, Any]) -> None:
    try:
        current = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except Exception:
        current = {}
    current[obj["agent_id"]] = obj
    atomic_write(INDEX_FILE, current)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Multi-agent check-in (append + index)."
    )
    parser.add_argument("json", help="Path to JSON payload or '-' for stdin")
    args = parser.get_unified_utility().parse_args()

    ensure_dirs()
    payload = load_json_arg(args.json)
    validate_minimum(payload)

    agent_id = payload["agent_id"]
    append_jsonl(agent_id, payload)
    update_index(payload)

    get_logger(__name__).info(
        f"OK: stored check-in for {agent_id} @ {payload['last_updated']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
