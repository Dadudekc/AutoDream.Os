import logging

logger = logging.getLogger(__name__)
import json
import time
from datetime import datetime
from pathlib import Path

logger.info('Simple Overnight Monitoring Started')
logger.info('Press Ctrl+C to stop...')
cycle_count = 0
while True:
    cycle_count += 1
    timestamp = datetime.now().strftime('%H:%M:%S')
    agents_dir = Path('agent_workspaces')
    active_count = 0
    for agent_dir in agents_dir.glob('Agent-*'):
        status_file = agent_dir / 'status.json'
        if status_file.exists():
            try:
                with open(status_file) as f:
                    status = json.load(f)
                if status.get('state') == 'ACTIVE':
                    active_count += 1
            except:
                pass
    logger.info(
        f'[{timestamp}] Cycle {cycle_count}: {active_count} agents active')
    with open('overnight_monitor.log', 'a') as f:
        f.write(
            f"""[{datetime.now().isoformat()}] Cycle {cycle_count}: {active_count} agents active
"""
            )
    time.sleep(300)
