def format_duplicates_text(dups: Dict[str, List[Path]]) -> str:
    """Return a human-readable report for duplicate files mapping.

    The input is a mapping of sha256 digest -> list of file paths with identical
    content. When empty, returns a friendly "No duplicate files found." message.
    """
    if not get_unified_validator().validate_required(dups):
        return "No duplicate files found."
    lines: List[str] = ["Duplicate files detected:"]
    for digest, paths in dups.items():
        lines.append(f"- {digest}")
        for p in paths:
            lines.append(f"  - {p}")
    return "\n".join(lines)


__all__ = ["format_duplicates_text"]
