#!/usr/bin/env python3
"""
Gaming Integration Core - Practical Examples
=============================================

Real-world usage examples for the SOLID-refactored Gaming Integration Core.

Author: Agent-8 (Operations & Support Specialist)
Date: 2025-10-13
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.integrations.osrs.gaming_integration_core import GameType, GamingIntegrationCore

# ============================================
# EXAMPLE 1: Basic Game Session
# ============================================


def example_basic_session():
    """Example 1: Create and manage a basic game session."""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Game Session")
    print("=" * 60)

    # Initialize core
    core = GamingIntegrationCore()

    # Create session
    session = core.create_game_session(game_type=GameType.STRATEGY, player_id="agent_4")

    print(f"✅ Session created: {session['session_id']}")
    print(f"   Player: {session['player_id']}")
    print(f"   Game Type: {session['game_type']}")
    print(f"   Start Time: {session['start_time']}")

    # Get active sessions
    active = core.get_active_sessions()
    print(f"\n📊 Active sessions: {len(active)}")

    # End session
    success = core.end_game_session(session["session_id"])
    print(f"\n👋 Session ended: {success}")

    return session


# ============================================
# EXAMPLE 2: Multi-Player Gaming
# ============================================


def example_multi_player():
    """Example 2: Multi-player game session management."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Multi-Player Gaming")
    print("=" * 60)

    core = GamingIntegrationCore()

    # Team Beta agents playing together
    players = [
        ("Agent-5", GameType.STRATEGY),
        ("Agent-6", GameType.ACTION),
        ("Agent-7", GameType.PUZZLE),
        ("Agent-8", GameType.SIMULATION),
    ]

    sessions = []
    for player_id, game_type in players:
        session = core.create_game_session(game_type, player_id)
        sessions.append(session)
        print(f"✅ {player_id} joined - Playing {game_type.value}")

    # Check active count
    active = core.get_active_sessions()
    print(f"\n🎮 Total active players: {len(active)}")

    # End all sessions
    print("\n👋 Ending sessions...")
    for session in sessions:
        core.end_game_session(session["session_id"])
        print(f"   {session['player_id']} session ended")

    return sessions


# ============================================
# EXAMPLE 3: Entertainment System Management
# ============================================


def example_entertainment_systems():
    """Example 3: Managing multiple entertainment systems."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Entertainment System Management")
    print("=" * 60)

    core = GamingIntegrationCore()

    # Register various systems
    systems = [
        ("osrs_main", "MMORPG"),
        ("chess_ai", "Strategy"),
        ("arcade_hub", "Action"),
        ("puzzle_master", "Puzzle"),
    ]

    print("📝 Registering systems...")
    for system_id, system_type in systems:
        success = core.register_entertainment_system(system_id, system_type)
        status_icon = "✅" if success else "❌"
        print(f"   {status_icon} {system_id} ({system_type})")

    # Get all systems
    all_systems = core.get_all_entertainment_systems()
    print(f"\n📊 Total systems registered: {len(all_systems)}")

    # Get specific system
    osrs = core.get_entertainment_system("osrs_main")
    if osrs:
        print("\n🎮 OSRS System:")
        print(f"   ID: {osrs['system_id']}")
        print(f"   Type: {osrs['system_type']}")
        print(f"   Status: {osrs['status']}")
        print(f"   Last Activity: {osrs['last_activity']}")

    return all_systems


# ============================================
# EXAMPLE 4: Event-Driven Integration
# ============================================


def example_event_driven():
    """Example 4: Event-driven game management."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Event-Driven Integration")
    print("=" * 60)

    core = GamingIntegrationCore()

    # Create session via event
    create_event = {"type": "create_session", "game_type": "action", "player_id": "agent_3"}

    print("📨 Processing create_session event...")
    result = core.handle_event("session_management", create_event)

    if result["success"]:
        session_id = result["session_id"]
        print(f"   ✅ Session created: {session_id}")

        # Get session via event
        get_event = {"type": "get_session", "session_id": session_id}

        print("\n📨 Processing get_session event...")
        result = core.handle_event("session_management", get_event)
        if result["success"]:
            session = result["session"]
            print(f"   ✅ Session retrieved: {session['player_id']}")

        # End session via event
        end_event = {"type": "end_session", "session_id": session_id}

        print("\n📨 Processing end_session event...")
        result = core.handle_event("session_management", end_event)
        print(f"   ✅ Session ended: {result['success']}")

    return result


# ============================================
# EXAMPLE 5: Custom Event Handler
# ============================================


def example_custom_handler():
    """Example 5: Register and use custom event handler."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Custom Event Handler")
    print("=" * 60)

    # Custom handler for analytics
    class AnalyticsHandler:
        def __init__(self):
            self.events_processed = 0

        def handle_event(self, event):
            self.events_processed += 1
            event_type = event.get("type", "unknown")

            print(f"   📊 Analytics: Processed {event_type} event")

            return {
                "success": True,
                "total_events": self.events_processed,
                "event_type": event_type,
            }

    core = GamingIntegrationCore()

    # Register custom handler
    analytics = AnalyticsHandler()
    core.register_event_handler("analytics", analytics)
    print("✅ Custom analytics handler registered")

    # Use custom handler
    events = [
        {"type": "player_login", "player": "agent_1"},
        {"type": "player_action", "action": "attack"},
        {"type": "player_logout", "player": "agent_1"},
    ]

    print("\n📨 Processing events with custom handler...")
    for event in events:
        result = core.handle_event("analytics", event)
        if result["success"]:
            print(f"   Total events processed: {result['total_events']}")

    return analytics


# ============================================
# EXAMPLE 6: Health Monitoring
# ============================================


def example_health_monitoring():
    """Example 6: Monitor gaming core health."""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Health Monitoring")
    print("=" * 60)

    core = GamingIntegrationCore()

    # Register systems
    core.register_entertainment_system("osrs", "MMORPG")
    core.register_entertainment_system("puzzle", "Puzzle")

    # Create sessions
    core.create_game_session(GameType.STRATEGY, "agent_5")
    core.create_game_session(GameType.ACTION, "agent_6")
    core.create_game_session(GameType.PUZZLE, "agent_7")

    # Get health status
    health = core.get_core_health()

    print("🏥 Gaming Core Health Report:")
    print(f"   Status: {health['status']}")
    print(f"   Initialized: {health['initialized']}")
    print(f"   Active Sessions: {health['session_count']}")
    print(f"   Registered Systems: {health['system_count']}")
    print(f"   Event Handlers: {health['handler_count']}")

    # Check connection
    if core.is_connected():
        print("\n✅ Core is connected and operational")
    else:
        print("\n❌ Core is not connected")

    return health


# ============================================
# EXAMPLE 7: Dependency Injection
# ============================================


def example_dependency_injection():
    """Example 7: Advanced dependency injection."""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Dependency Injection")
    print("=" * 60)

    # Custom session manager with logging
    class LoggingSessionManager:
        def __init__(self):
            self.sessions = {}
            self.operation_log = []

        def create_session(self, game_type, player_id):
            session_id = f"logged_{len(self.sessions)}"
            self.sessions[session_id] = {
                "session_id": session_id,
                "game_type": game_type,
                "player_id": player_id,
                "status": "active",
            }
            self.operation_log.append(f"CREATE: {session_id}")
            return self.sessions[session_id]

        def get_session(self, session_id):
            self.operation_log.append(f"GET: {session_id}")
            return self.sessions.get(session_id)

        def end_session(self, session_id):
            if session_id in self.sessions:
                self.sessions[session_id]["status"] = "ended"
                self.operation_log.append(f"END: {session_id}")
                return True
            return False

        def get_active_sessions(self):
            self.operation_log.append("GET_ACTIVE")
            return [s for s in self.sessions.values() if s["status"] == "active"]

    # Inject custom manager
    logging_manager = LoggingSessionManager()
    core = GamingIntegrationCore(session_manager=logging_manager)

    print("✅ Core initialized with custom logging session manager")

    # Perform operations
    session = core.create_game_session(GameType.STRATEGY, "agent_8")
    active = core.get_active_sessions()
    core.end_game_session(session["session_id"])

    # View operation log
    print(f"\n📝 Operation Log ({len(logging_manager.operation_log)} operations):")
    for operation in logging_manager.operation_log:
        print(f"   {operation}")

    return logging_manager


# ============================================
# RUN ALL EXAMPLES
# ============================================

if __name__ == "__main__":
    print("\n🎮 GAMING INTEGRATION CORE - PRACTICAL EXAMPLES")
    print("=" * 60)
    print("Demonstrating SOLID-compliant gaming integration")
    print("=" * 60)

    try:
        example_basic_session()
        example_multi_player()
        example_entertainment_systems()
        example_event_driven()
        example_custom_handler()
        example_health_monitoring()
        example_dependency_injection()

        print("\n" + "=" * 60)
        print("✅ ALL EXAMPLES EXECUTED SUCCESSFULLY!")
        print("=" * 60)
        print("\n🐝 WE ARE SWARM - Gaming Integration Core operational! ⚡\n")

    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        raise
