from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
"""Validate agent workspaces against coordinate SSOT."""
import json
import re
from pathlib import Path


def load_ssot_agents(coord_file: Path) ->set[str]:
    """Return agent IDs defined in the SSOT coordinate file."""
    data = json.loads(coord_file.read_text(encoding='utf-8'))
    return set(data.get('agents', {}).keys())


def list_workspace_agents(workspaces_dir: Path) ->set[str]:
    """Return agent IDs present in agent_workspaces directory."""
    return {p.name for p in workspaces_dir.iterdir() if p.is_dir() and p.
        name.startswith('Agent-')}


def find_coordinate_entries(workspaces_dir: Path) ->dict[str, str]:
    """Find files in workspaces that contain hard-coded coordinates."""
    pattern = re.compile('\\(-?\\d+\\s*,\\s*-?\\d+\\)')
    offenders: dict[str, str] = {}
    for path in workspaces_dir.rglob('*'):
        if path.is_file():
            text = path.read_text(encoding='utf-8', errors='ignore')
            if 'coordinates' in text and pattern.search(text):
                offenders[str(path)] = path.name
    return offenders


def validate_workspaces(workspaces_dir: Path=Path('agent_workspaces'),
    coord_file: Path=Path('cursor_agent_coords.json')) ->bool:
    """Validate workspace directories against coordinate SSOT."""
    agents_in_ssot = load_ssot_agents(coord_file)
    agents_in_ws = list_workspace_agents(workspaces_dir)
    missing = agents_in_ssot - agents_in_ws
    extra = agents_in_ws - agents_in_ssot
    offenders = find_coordinate_entries(workspaces_dir)
    if missing or offenders:
        if missing:
            logger.info(
                f'Agents missing workspace directories: {sorted(missing)}')
        if offenders:
            logger.info('Coordinate entries found in workspaces:')
            for file in offenders:
                logger.info(f' - {file}')
        return False
    if extra:
        logger.info(
            f'Extra workspace directories without SSOT entry: {sorted(extra)}')
    return True


if __name__ == '__main__':
    if not validate_workspaces():
        raise SystemExit(1)
    logger.info('All workspaces match coordinate SSOT.')
