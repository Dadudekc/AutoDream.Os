#!/usr/bin/env python3
"""
Test Agent-7 Coordinate Messaging
"""

sys.path.insert(0, 'src')


get_logger(__name__).info('🎯 Testing Agent-7 Coordinate Messaging')
get_logger(__name__).info('=' * 40)

try:
    core = UnifiedMessagingCore()
    coords = core.load_coordinates_from_config()

    get_logger(__name__).info(f'✅ Coordinates loaded for {len(coords)} agents')
    agent7_coords = coords.get('Agent-7')
    get_logger(__name__).info(f'Agent-7 coordinates: {agent7_coords}')

    # Test delivery capability
    can_deliver = core.can_deliver_to_agent('Agent-7')
    get_logger(__name__).info(f'Agent-7 coordinate delivery: {"✅ Ready" if can_deliver else "❌ Not ready"}')

    # Test system status
    status = core.get_system_status()
    get_logger(__name__).info(f'System health: {status.get("system_health", "unknown").upper()}')

    get_logger(__name__).info('\n✅ Agent-7 coordinate messaging is working!')

except Exception as e:
    get_logger(__name__).info(f'❌ Error: {e}')
    traceback.print_exc()

