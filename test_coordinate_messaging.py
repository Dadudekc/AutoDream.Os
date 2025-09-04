#!/usr/bin/env python3
"""
Test Coordinate Messaging Functionality
=====================================

Tests the refactored coordinate messaging system to verify it's working properly.
"""


# Add src to path
sys.path.insert(0, 'src')



async def test_coordinate_messaging():
    """Test coordinate messaging functionality."""
    get_logger(__name__).info('🧪 Testing Coordinate Messaging Functionality')
    get_logger(__name__).info('=' * 50)

    try:
        # Initialize messaging core
        core = UnifiedMessagingCore()

        # Test coordinate loading
        get_logger(__name__).info('\n📍 Testing Coordinate Loading:')
        coords = core.load_coordinates_from_config()
        get_logger(__name__).info(f'✅ Loaded coordinates for {len(coords)} agents:')
        for agent, coord in coords.items():
            get_logger(__name__).info(f'  {agent}: {coord}')

        # Test delivery capability
        get_logger(__name__).info('\n🎯 Testing Delivery Capability:')
        for agent in ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4']:
            can_deliver = core.can_deliver_to_agent(agent)
            status = '✅ Available' if can_deliver else '❌ Unavailable'
            get_logger(__name__).info(f'  {agent}: {status}')

        # Test system status
        get_logger(__name__).info('\n📊 Testing System Status:')
        status = core.get_system_status()
        get_logger(__name__).info(f'  System Health: {status.get("system_health", "unknown").upper()}')
        get_logger(__name__).info(f'  Modular Components: {len(status.get("modular_components", {}))} active')

        # Test coordinate display
        get_logger(__name__).info('\n📋 Testing Coordinate Display:')
        coord_info = await core.show_coordinates()
        if coord_info.get('success'):
            get_logger(__name__).info(f'  ✅ Coordinates displayed successfully for {coord_info.get("agent_count", 0)} agents')
        else:
            get_logger(__name__).info(f'  ❌ Coordinate display failed: {coord_info.get("message", "Unknown error")}')

        get_logger(__name__).info('\n✅ Coordinate Messaging Test Complete!')

    except Exception as e:
        get_logger(__name__).info(f'❌ Test failed with error: {e}')
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_coordinate_messaging())

