# 📚 **API Reference - Agent Cellphone V2**

**Comprehensive API documentation for all modules and components**

---

## 🎯 **Table of Contents**

1. [Core Messaging System](#core-messaging-system)
2. [Backup & Disaster Recovery](#backup--disaster-recovery)
3. [Discord Commander](#discord-commander)
4. [Coordinate Management](#coordinate-management)
5. [Role Management](#role-management)
6. [Analytics & Monitoring](#analytics--monitoring)
7. [Configuration Management](#configuration-management)
8. [Utilities & Helpers](#utilities--helpers)

---

## 🔧 **Core Messaging System**

### **Consolidated Messaging Service**

**Location:** `src/services/consolidated_messaging_service.py`

#### **Classes**

##### **UnifiedMessage**
```python
class UnifiedMessage:
    """Core message structure for unified messaging."""

    def __init__(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: list[UnifiedMessageTag] = None,
        metadata: dict[str, Any] = None,
        message_id: str = None,
        timestamp: str | None = None,
        sender_type: SenderType = SenderType.SYSTEM,
        recipient_type: RecipientType = RecipientType.AGENT,
    ):
        """
        Initialize unified message.

        Args:
            content: Message content
            sender: Sender identifier
            recipient: Recipient identifier
            message_type: Type of message (AGENT_TO_AGENT, BROADCAST, etc.)
            priority: Message priority (REGULAR, URGENT)
            tags: List of message tags
            metadata: Additional metadata
            message_id: Unique message identifier
            timestamp: Message timestamp
            sender_type: Type of sender (AGENT, CAPTAIN, SYSTEM, HUMAN)
            recipient_type: Type of recipient (AGENT, CAPTAIN, SYSTEM, HUMAN)
        """
```

#### **Enums**

##### **UnifiedMessageType**
```python
class UnifiedMessageType(Enum):
    """Message types for unified messaging."""
    TEXT = "text"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"
    AGENT_TO_AGENT = "agent_to_agent"
    CAPTAIN_TO_AGENT = "captain_to_agent"
    SYSTEM_TO_AGENT = "system_to_agent"
    HUMAN_TO_AGENT = "human_to_agent"
```

##### **UnifiedMessagePriority**
```python
class UnifiedMessagePriority(Enum):
    """Message priorities for unified messaging."""
    REGULAR = "regular"
    URGENT = "urgent"
    # Legacy support
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
```

##### **UnifiedMessageTag**
```python
class UnifiedMessageTag(Enum):
    """Message tags for unified messaging."""
    CAPTAIN = "captain"
    ONBOARDING = "onboarding"
    WRAPUP = "wrapup"
    COORDINATION = "COORDINATION"
    SYSTEM = "system"
    # Legacy support
    GENERAL = "GENERAL"
    TASK = "TASK"
    STATUS = "STATUS"
```

#### **Functions**

##### **send_message**
```python
async def send_message(message: UnifiedMessage) -> bool:
    """
    Send message using PyAutoGUI system with inbox fallback.

    Args:
        message: UnifiedMessage object to send

    Returns:
        bool: True if message sent successfully, False otherwise

    Example:
        >>> message = UnifiedMessage(
        ...     content="Hello from system",
        ...     sender="Agent-8",
        ...     recipient="Agent-5",
        ...     message_type=UnifiedMessageType.AGENT_TO_AGENT,
        ...     priority=UnifiedMessagePriority.NORMAL
        ... )
        >>> success = await send_message(message)
        >>> print(f"Message sent: {success}")
    """
```

##### **broadcast_message**
```python
async def broadcast_message(content: str, sender: str) -> bool:
    """
    Broadcast message to all agents.

    Args:
        content: Message content to broadcast
        sender: Sender identifier

    Returns:
        bool: True if broadcast successful, False otherwise

    Example:
        >>> success = await broadcast_message("System maintenance in 5 minutes", "Agent-8")
        >>> print(f"Broadcast sent: {success}")
    """
```

##### **list_agents**
```python
async def list_agents() -> list[str]:
    """
    List all available agents.

    Returns:
        list[str]: List of agent identifiers

    Example:
        >>> agents = await list_agents()
        >>> print(f"Available agents: {agents}")
        # Output: ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5', 'Agent-6', 'Agent-7', 'Agent-8']
    """
```

---

## 💾 **Backup & Disaster Recovery**

### **Backup System Core**

**Location:** `src/core/backup_disaster_recovery/backup_system_core.py`

#### **Classes**

##### **BackupSystemCore**
```python
class BackupSystemCore:
    """Core backup and disaster recovery system."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize backup system with configuration.

        Args:
            config_path: Path to backup configuration file
        """
```

#### **Methods**

##### **create_backup**
```python
async def create_backup(
    self,
    backup_type: str = "incremental",
    source_path: Optional[str] = None,
    custom_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a backup of specified type.

    Args:
        backup_type: Type of backup ('full', 'incremental', 'differential')
        source_path: Path to backup (default: current directory)
        custom_name: Custom name for backup

    Returns:
        Dict[str, Any]: Backup result with metadata

    Example:
        >>> backup_system = BackupSystemCore()
        >>> result = await backup_system.create_backup("full", ".", "system_backup")
        >>> print(f"Backup created: {result['backup_id']}")
    """
```

##### **restore_backup**
```python
async def restore_backup(
    self,
    backup_id: str,
    target_path: str,
    point_in_time: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Restore backup to target path.

    Args:
        backup_id: ID of backup to restore
        target_path: Path to restore to
        point_in_time: Specific point in time to restore to

    Returns:
        Dict[str, Any]: Restoration result

    Example:
        >>> result = await backup_system.restore_backup(
        ...     "full_20240101_020000",
        ...     "/restore/path"
        ... )
        >>> print(f"Restore completed: {result['status']}")
    """
```

##### **list_backups**
```python
async def list_backups(self, backup_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List available backups.

    Args:
        backup_type: Filter by backup type (optional)

    Returns:
        List[Dict[str, Any]]: List of backup metadata

    Example:
        >>> backups = await backup_system.list_backups("full")
        >>> for backup in backups:
        ...     print(f"Backup: {backup['backup_id']} - {backup['timestamp']}")
    """
```

### **Business Continuity Planner**

**Location:** `src/core/backup_disaster_recovery/business_continuity_planner.py`

#### **Classes**

##### **BusinessContinuityPlanner**
```python
class BusinessContinuityPlanner:
    """Business continuity planning and disaster recovery framework."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize business continuity planner.

        Args:
            config_path: Path to BCP configuration file
        """
```

#### **Methods**

##### **create_recovery_plan**
```python
async def create_recovery_plan(
    self,
    disaster_type: DisasterType,
    affected_systems: List[str]
) -> Dict[str, Any]:
    """
    Create a comprehensive recovery plan for a disaster scenario.

    Args:
        disaster_type: Type of disaster (HARDWARE_FAILURE, DATA_CORRUPTION, etc.)
        affected_systems: List of affected system identifiers

    Returns:
        Dict[str, Any]: Complete recovery plan

    Example:
        >>> bcp = BusinessContinuityPlanner()
        >>> plan = await bcp.create_recovery_plan(
        ...     DisasterType.HARDWARE_FAILURE,
        ...     ["messaging_system", "agent_coordination"]
        ... )
        >>> print(f"Recovery plan created: {plan['plan_id']}")
    """
```

##### **test_business_continuity_plan**
```python
async def test_business_continuity_plan(self, plan_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Test the business continuity plan through simulation.

    Args:
        plan_id: Specific plan ID to test (optional)

    Returns:
        Dict[str, Any]: Test results and recommendations

    Example:
        >>> test_result = await bcp.test_business_continuity_plan()
        >>> print(f"BCP test score: {test_result['overall_score']:.2f}")
    """
```

---

## 🤖 **Discord Commander**

### **Discord Agent Bot**

**Location:** `src/discord_commander/discord_agent_bot.py`

#### **Classes**

##### **DiscordAgentBot**
```python
class DiscordAgentBot(commands.Bot):
    """Streamlined Discord bot for V2_SWARM agent coordination."""

    def __init__(self, command_prefix: str = "!", intents=None):
        """
        Initialize Discord agent bot.

        Args:
            command_prefix: Command prefix for Discord commands
            intents: Discord intents configuration
        """
```

#### **Methods**

##### **on_ready**
```python
async def on_ready(self):
    """
    Event handler for bot ready state.
    Called when bot successfully connects to Discord.
    """
```

##### **on_message**
```python
async def on_message(self, message):
    """
    Event handler for incoming messages.

    Args:
        message: Discord message object
    """
```

### **Swarm Command Handlers**

**Location:** `src/discord_commander/handlers_swarm.py`

#### **Classes**

##### **SwarmCommandHandlers**
```python
class SwarmCommandHandlers:
    """Handles swarm-wide commands (broadcast, coordination)."""

    def __init__(self, agent_engine, embed_manager: EmbedManager):
        """
        Initialize swarm command handlers.

        Args:
            agent_engine: Agent communication engine
            embed_manager: Discord embed manager
        """
```

#### **Methods**

##### **handle_swarm_command**
```python
async def handle_swarm_command(self, context: dict[str, Any]) -> dict[str, Any] | None:
    """
    Handle swarm broadcast command.

    Args:
        context: Command context containing author, channel, message, etc.

    Returns:
        dict[str, Any] | None: Response data or None if command should be ignored
    """
```

---

## 📍 **Coordinate Management**

### **Coordinate Loader**

**Location:** `src/core/coordinate_loader.py`

#### **Classes**

##### **CoordinateLoader**
```python
class CoordinateLoader:
    """Single source of truth for agent coordinate management."""

    def __init__(self, config_path: str = "config/coordinates.json"):
        """
        Initialize coordinate loader.

        Args:
            config_path: Path to coordinates configuration file
        """
```

#### **Methods**

##### **get_agent_coordinates**
```python
def get_agent_coordinates(self, agent_id: str) -> tuple[int, int]:
    """
    Get coordinates for a specific agent.

    Args:
        agent_id: Agent identifier (e.g., 'Agent-1')

    Returns:
        tuple[int, int]: (x, y) coordinates

    Raises:
        ValueError: If agent not found or coordinates invalid

    Example:
        >>> loader = CoordinateLoader()
        >>> coords = loader.get_agent_coordinates("Agent-1")
        >>> print(f"Agent-1 coordinates: {coords}")
        # Output: (-1269, 481)
    """
```

##### **get_all_agents**
```python
def get_all_agents(self) -> list[str]:
    """
    Get list of all available agents.

    Returns:
        list[str]: List of agent identifiers

    Example:
        >>> agents = loader.get_all_agents()
        >>> print(f"Available agents: {agents}")
        # Output: ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5', 'Agent-6', 'Agent-7', 'Agent-8']
    """
```

##### **is_agent_active**
```python
def is_agent_active(self, agent_id: str) -> bool:
    """
    Check if agent is active.

    Args:
        agent_id: Agent identifier

    Returns:
        bool: True if agent is active, False otherwise

    Example:
        >>> is_active = loader.is_agent_active("Agent-1")
        >>> print(f"Agent-1 active: {is_active}")
    """
```

---

## 👥 **Role Management**

### **Role Manager**

**Location:** `src/services/role_manager.py`

#### **Classes**

##### **RoleManager**
```python
class RoleManager:
    """Manages agent roles and onboarding processes."""

    def __init__(self):
        """Initialize role manager."""
```

#### **Methods**

##### **get_available_roles**
```python
def get_available_roles(self) -> list[str]:
    """
    Get list of available role modes.

    Returns:
        list[str]: List of available role modes

    Example:
        >>> role_manager = RoleManager()
        >>> roles = role_manager.get_available_roles()
        >>> print(f"Available roles: {roles}")
        # Output: ['bootstrap_cli', 'compliance_refactor_v2', 'memory_nexus', 'production_ready', 'enterprise_deploy', 'live_ops_growth']
    """
```

##### **onboard_agent**
```python
async def onboard_agent(
    self,
    agent_id: str,
    role_mode: str,
    style: str = "friendly"
) -> bool:
    """
    Onboard agent with specific role mode.

    Args:
        agent_id: Agent identifier
        role_mode: Role mode to assign
        style: Onboarding style ('friendly' or 'professional')

    Returns:
        bool: True if onboarding successful, False otherwise

    Example:
        >>> success = await role_manager.onboard_agent(
        ...     "Agent-5",
        ...     "production_ready",
        ...     "professional"
        ... )
        >>> print(f"Onboarding successful: {success}")
    """
```

---

## 📊 **Analytics & Monitoring**

### **Performance Monitoring**

**Location:** `src/core/performance/`

#### **Classes**

##### **PerformanceMonitor**
```python
class PerformanceMonitor:
    """Monitors system performance and metrics."""

    def __init__(self):
        """Initialize performance monitor."""
```

#### **Methods**

##### **get_system_metrics**
```python
async def get_system_metrics(self) -> Dict[str, Any]:
    """
    Get current system performance metrics.

    Returns:
        Dict[str, Any]: System metrics including CPU, memory, disk usage

    Example:
        >>> monitor = PerformanceMonitor()
        >>> metrics = await monitor.get_system_metrics()
        >>> print(f"CPU usage: {metrics['cpu_percent']}%")
    """
```

##### **start_monitoring**
```python
async def start_monitoring(self, interval: int = 60):
    """
    Start continuous performance monitoring.

    Args:
        interval: Monitoring interval in seconds

    Example:
        >>> await monitor.start_monitoring(30)  # Monitor every 30 seconds
    """
```

---

## ⚙️ **Configuration Management**

### **Unified Configuration**

**Location:** `src/core/unified_config.py`

#### **Classes**

##### **UnifiedConfig**
```python
class UnifiedConfig:
    """Unified configuration management system."""

    def __init__(self, config_path: str = "config/unified_config.yaml"):
        """
        Initialize unified configuration.

        Args:
            config_path: Path to configuration file
        """
```

#### **Methods**

##### **get_config**
```python
def get_config(self, key: str, default: Any = None) -> Any:
    """
    Get configuration value by key.

    Args:
        key: Configuration key (supports dot notation)
        default: Default value if key not found

    Returns:
        Any: Configuration value

    Example:
        >>> config = UnifiedConfig()
        >>> db_url = config.get_config("database.url", "sqlite:///default.db")
        >>> print(f"Database URL: {db_url}")
    """
```

##### **set_config**
```python
def set_config(self, key: str, value: Any) -> None:
    """
    Set configuration value.

    Args:
        key: Configuration key (supports dot notation)
        value: Value to set

    Example:
        >>> config.set_config("messaging.timeout", 30)
    """
```

---

## 🛠️ **Utilities & Helpers**

### **Unified Utilities**

**Location:** `src/utils/`

#### **Functions**

##### **get_logger**
```python
def get_logger(name: str) -> logging.Logger:
    """
    Get configured logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        logging.Logger: Configured logger instance

    Example:
        >>> from src.utils.unified_logging_manager import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("System initialized")
    """
```

##### **validate_coordinates**
```python
def validate_coordinates(x: int, y: int) -> bool:
    """
    Validate coordinate values.

    Args:
        x: X coordinate
        y: Y coordinate

    Returns:
        bool: True if coordinates are valid, False otherwise

    Example:
        >>> is_valid = validate_coordinates(-1269, 481)
        >>> print(f"Coordinates valid: {is_valid}")
    """
```

---

## 🚀 **Usage Examples**

### **Complete Messaging Workflow**

```python
import asyncio
from src.services.consolidated_messaging_service import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    UnifiedMessageTag, send_message, broadcast_message
)

async def messaging_example():
    """Complete messaging workflow example."""

    # Create a message
    message = UnifiedMessage(
        content="Hello from Agent-8!",
        sender="Agent-8",
        recipient="Agent-5",
        message_type=UnifiedMessageType.AGENT_TO_AGENT,
        priority=UnifiedMessagePriority.NORMAL,
        tags=[UnifiedMessageTag.COORDINATION]
    )

    # Send the message
    success = await send_message(message)
    print(f"Message sent: {success}")

    # Broadcast to all agents
    broadcast_success = await broadcast_message(
        "System maintenance scheduled for tonight",
        "Agent-8"
    )
    print(f"Broadcast sent: {broadcast_success}")

# Run the example
asyncio.run(messaging_example())
```

### **Backup and Recovery Workflow**

```python
import asyncio
from src.core.backup_disaster_recovery import (
    BackupSystemCore, BusinessContinuityPlanner, DisasterType
)

async def backup_recovery_example():
    """Complete backup and recovery workflow example."""

    # Initialize backup system
    backup_system = BackupSystemCore()

    # Create a full backup
    backup_result = await backup_system.create_backup("full", ".", "system_backup")
    print(f"Backup created: {backup_result['backup_id']}")

    # List available backups
    backups = await backup_system.list_backups()
    print(f"Available backups: {len(backups)}")

    # Create business continuity plan
    bcp = BusinessContinuityPlanner()
    recovery_plan = await bcp.create_recovery_plan(
        DisasterType.HARDWARE_FAILURE,
        ["messaging_system", "agent_coordination"]
    )
    print(f"Recovery plan created: {recovery_plan['plan_id']}")

    # Test business continuity plan
    test_result = await bcp.test_business_continuity_plan()
    print(f"BCP test score: {test_result['overall_score']:.2f}")

# Run the example
asyncio.run(backup_recovery_example())
```

### **Coordinate Management Example**

```python
from src.core.coordinate_loader import get_coordinate_loader

def coordinate_example():
    """Coordinate management example."""

    # Get coordinate loader
    loader = get_coordinate_loader()

    # Get all agents
    agents = loader.get_all_agents()
    print(f"Available agents: {agents}")

    # Get coordinates for each agent
    for agent_id in agents:
        try:
            coords = loader.get_agent_coordinates(agent_id)
            print(f"{agent_id}: {coords}")
        except ValueError as e:
            print(f"Error getting coordinates for {agent_id}: {e}")

    # Check if agent is active
    for agent_id in agents:
        is_active = loader.is_agent_active(agent_id)
        print(f"{agent_id} active: {is_active}")

# Run the example
coordinate_example()
```

---

## 📝 **Error Handling**

### **Common Exceptions**

#### **CoordinateError**
```python
class CoordinateError(Exception):
    """Raised when coordinate operations fail."""
    pass
```

#### **MessagingError**
```python
class MessagingError(Exception):
    """Raised when messaging operations fail."""
    pass
```

#### **BackupError**
```python
class BackupError(Exception):
    """Raised when backup operations fail."""
    pass
```

### **Error Handling Best Practices**

```python
import logging
from src.services.consolidated_messaging_service import send_message, MessagingError
from src.core.coordinate_loader import get_coordinate_loader, CoordinateError

async def robust_messaging_example():
    """Example with proper error handling."""
    logger = logging.getLogger(__name__)

    try:
        # Get coordinates with error handling
        loader = get_coordinate_loader()
        coords = loader.get_agent_coordinates("Agent-1")
        print(f"Agent-1 coordinates: {coords}")

    except CoordinateError as e:
        logger.error(f"Coordinate error: {e}")
        return False

    try:
        # Send message with error handling
        success = await send_message(message)
        return success

    except MessagingError as e:
        logger.error(f"Messaging error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False
```

---

## 🔧 **Configuration Reference**

### **Environment Variables**

| Variable | Description | Default |
|----------|-------------|---------|
| `PYAUTO_PAUSE_S` | PyAutoGUI pause duration | `0.05` |
| `PYAUTO_MOVE_DURATION` | Mouse move duration | `0.4` |
| `PYAUTO_SEND_RETRIES` | Number of send retries | `2` |
| `DISCORD_BOT_TOKEN` | Discord bot token | Required |
| `DISCORD_CHANNEL_ID` | Discord channel ID | Required |

### **Configuration Files**

#### **coordinates.json**
```json
{
  "agents": {
    "Agent-1": {"x": -1269, "y": 481},
    "Agent-2": {"x": -308, "y": 480},
    "Agent-3": {"x": -1269, "y": 1001},
    "Agent-4": {"x": -308, "y": 1000},
    "Agent-5": {"x": 652, "y": 421},
    "Agent-6": {"x": 1612, "y": 419},
    "Agent-7": {"x": 920, "y": 851},
    "Agent-8": {"x": 1611, "y": 941}
  }
}
```

#### **unified_config.yaml**
```yaml
messaging:
  timeout: 30
  retry_attempts: 3
  fallback_enabled: true

coordinates:
  validation_enabled: true
  bounds_check: true

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

---

## 📚 **Additional Resources**

- [Quick Start Guide](QUICK_START.md)
- [Architecture Overview](ARCHITECTURE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
- [Development Workflow](DEVELOPMENT_WORKFLOW.md)
- [API Examples](examples/)

---

**📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory**
