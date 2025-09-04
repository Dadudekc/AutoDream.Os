#!/usr/bin/env python3
"""
Coordinate System Debug Script
==============================

Debugs and validates the coordinate system used by the messaging system.
Shows which coordinate files are being used and their values.
"""


def debug_coordinate_system():
    """Debug the coordinate system configuration."""
    get_logger(__name__).info("🔍 COORDINATE SYSTEM DEBUG")
    get_logger(__name__).info("=" * 50)

    # Check available coordinate files
    get_logger(__name__).info("\n📁 Available Coordinate Files:")

    # Discord coordinates
    discord_coords_file = get_unified_utility().Path("src/discord_commander_coordinates.json")
    if discord_coords_file.exists():
        get_logger(__name__).info(f"  ✅ {discord_coords_file} (Discord Commander)")
        with open(discord_coords_file, 'r') as f:
            discord_data = read_json(f)
        discord_coords = {}
        for agent, data in discord_data.get('agents', {}).items():
            coord = data.get('coordinates', [])
            if coord:
                discord_coords[agent] = tuple(coord)
    else:
        get_logger(__name__).info(f"  ❌ {discord_coords_file} (Discord Commander)")
        discord_coords = {}

    # Messaging config coordinates
    messaging_config_file = get_unified_utility().Path("config/messaging.yml")
    if messaging_config_file.exists():
        get_logger(__name__).info(f"  ✅ {messaging_config_file} (Messaging System)")
        with open(messaging_config_file, 'r') as f:
            config = yaml.safe_load(f)
        messaging_coords = config.get('coordinates', {})
    else:
        get_logger(__name__).info(f"  ❌ {messaging_config_file} (Messaging System)")
        messaging_coords = {}

    # Test actual loading from messaging system
    get_logger(__name__).info("\n🔧 Messaging System Coordinate Loading:")

    try:
        sys.path.insert(0, 'src')

        coord_delivery = CoordinateMessagingDelivery()
        loaded_coords = coord_delivery.load_coordinates()

        if loaded_coords:
            # Determine source
            has_negative = any(coord[0] < 0 for coord in loaded_coords.values())
            source = "Discord coordinates (screen-relative)" if has_negative else "Config coordinates (grid-based)"

            get_logger(__name__).info(f"  ✅ Successfully loaded {len(loaded_coords)} agents")
            get_logger(__name__).info(f"  📍 Source: {source}")
            get_logger(__name__).info("\n  📋 Loaded Coordinates:")

            for agent in sorted(loaded_coords.keys()):
                coord = loaded_coords[agent]
                discord_coord = discord_coords.get(agent)
                config_coord = messaging_coords.get(agent)

                status = "✅"
                if discord_coord and tuple(coord) == discord_coord:
                    status += " [FROM DISCORD]"
                elif config_coord and tuple(coord) == tuple(config_coord):
                    status += " [FROM CONFIG]"
                else:
                    status += " [UNKNOWN SOURCE]"

                get_logger(__name__).info(f"    {agent}: {coord} {status}")
        else:
            get_logger(__name__).info("  ❌ No coordinates loaded by messaging system")

    except Exception as e:
        get_logger(__name__).info(f"  ❌ Failed to load coordinates: {e}")
        traceback.print_exc()

    # Summary
    get_logger(__name__).info("\n📊 SUMMARY:")
    get_logger(__name__).info("=" * 30)

    discord_count = len(discord_coords)
    config_count = len(messaging_coords)

    get_logger(__name__).info(f"  Discord coordinates file: {discord_count} agents")
    get_logger(__name__).info(f"  Config coordinates file: {config_count} agents")

    if loaded_coords:
        loaded_count = len(loaded_coords)
        has_negative = any(coord[0] < 0 for coord in loaded_coords.values())
        source = "Discord (screen-relative)" if has_negative else "Config (grid-based)"
        get_logger(__name__).info(f"  Messaging system loaded: {loaded_count} agents from {source}")

        # Check for mismatches
        discord_keys = set(discord_coords.keys())
        config_keys = set(messaging_coords.keys())
        loaded_keys = set(loaded_coords.keys())

        if discord_keys == loaded_keys:
            get_logger(__name__).info("  ✅ Messaging system is using Discord coordinates")
        elif config_keys == loaded_keys:
            get_logger(__name__).info("  ⚠️ Messaging system is using Config coordinates (fallback)")
        else:
            get_logger(__name__).info("  ❌ Coordinate mismatch detected")
    else:
        get_logger(__name__).info("  ❌ Messaging system failed to load coordinates")

if __name__ == "__main__":
    debug_coordinate_system()

