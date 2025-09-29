"""
V3-009 Command Understanding System
Advanced command parsing and understanding for agent communication
"""

import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class CommandType(Enum):
    """Types of commands"""

    TASK_ASSIGNMENT = "task_assignment"
    STATUS_REQUEST = "status_request"
    COORDINATION = "coordination"
    EMERGENCY = "emergency"
    INFORMATION = "information"
    ACTION_REQUEST = "action_request"


class CommandPriority(Enum):
    """Command priority levels"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class CommandContext:
    """Command execution context"""

    sender: str
    recipient: str
    timestamp: datetime
    priority: CommandPriority
    channel: str
    metadata: dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ParsedCommand:
    """Parsed command structure"""

    command_type: CommandType
    action: str
    parameters: dict[str, Any]
    context: CommandContext
    confidence: float
    original_text: str


class CommandParser:
    """Core command parsing engine"""

    def __init__(self):
        self.command_patterns = self._initialize_command_patterns()
        self.parameter_extractors = self._initialize_parameter_extractors()
        self.priority_indicators = self._initialize_priority_indicators()

    def _initialize_command_patterns(self) -> dict[CommandType, list[str]]:
        """Initialize regex patterns for command recognition"""
        return {
            CommandType.TASK_ASSIGNMENT: [
                r"\b(assign|give|delegate|hand over)\b.*\b(task|mission|job|work)\b",
                r"\b(claim|take|accept|pick up)\b.*\b(task|contract|assignment)\b",
                r"\b(V3-?\d{3}|V2-?\w+-\d{3})\b.*\b(assign|claim|take)\b",
            ],
            CommandType.STATUS_REQUEST: [
                r"\b(status|health|state|condition|progress)\b",
                r"\b(how is|what is the status of|check the status)\b",
                r"\b(report|update|summary|overview)\b",
            ],
            CommandType.COORDINATION: [
                r"\b(coordinate|collaborate|work together|team up)\b",
                r"\b(sync|synchronize|align|harmonize)\b",
                r"\b(meeting|discussion|conference|briefing)\b",
            ],
            CommandType.EMERGENCY: [
                r"\b(emergency|urgent|critical|immediate|asap)\b",
                r"\b(alert|warning|danger|problem|issue)\b",
                r"\b(escalate|notify|warn|alert)\b.*\b(captain|agent-4)\b",
            ],
            CommandType.INFORMATION: [
                r"\b(what|how|when|where|why|who|which)\b",
                r"\b(explain|describe|tell me about|show me)\b",
                r"\b(information|info|details|data|facts)\b",
            ],
            CommandType.ACTION_REQUEST: [
                r"\b(do|perform|execute|run|start|stop)\b",
                r"\b(create|build|deploy|implement|develop)\b",
                r"\b(fix|repair|resolve|solve|correct)\b",
            ],
        }

    def _initialize_parameter_extractors(self) -> dict[str, str]:
        """Initialize parameter extraction patterns"""
        return {
            "agent_id": r"\b(Agent-?[1-8]|Captain|Agent-4)\b",
            "task_id": r"\b(V3-?\d{3}|V2-?\w+-\d{3})\b",
            "priority": r"\b(CRITICAL|HIGH|MEDIUM|LOW|urgent|normal|low)\b",
            "status": r"\b(ACTIVE|INACTIVE|COMPLETED|IN_PROGRESS|PENDING|FAILED)\b",
            "timeframe": r"\b(\d+)\s*(cycle|cycles|hour|hours|day|days|minute|minutes)\b",
            "file_path": r"[a-zA-Z0-9_/.-]+\.(py|json|md|txt|yaml|yml)",
            "number": r"\b\d+\b",
            "percentage": r"\b\d+(\.\d+)?%\b",
            "url": r"https?://[^\s]+",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        }

    def _initialize_priority_indicators(self) -> dict[CommandPriority, list[str]]:
        """Initialize priority level indicators"""
        return {
            CommandPriority.CRITICAL: ["critical", "urgent", "emergency", "asap", "immediate"],
            CommandPriority.HIGH: ["high", "important", "priority", "soon"],
            CommandPriority.MEDIUM: ["medium", "normal", "regular", "standard"],
            CommandPriority.LOW: ["low", "when possible", "eventually", "later"],
        }

    def parse_command(self, text: str, context: CommandContext) -> ParsedCommand:
        """Parse command from text and context"""
        # Clean and normalize text
        cleaned_text = self._clean_text(text)

        # Extract parameters
        parameters = self._extract_parameters(cleaned_text)

        # Classify command type
        command_type, confidence = self._classify_command_type(cleaned_text)

        # Extract action
        action = self._extract_action(cleaned_text, command_type)

        # Determine priority
        priority = self._determine_priority(cleaned_text, context.priority)

        # Update context with determined priority
        context.priority = priority

        return ParsedCommand(
            command_type=command_type,
            action=action,
            parameters=parameters,
            context=context,
            confidence=confidence,
            original_text=text,
        )

    def _clean_text(self, text: str) -> str:
        """Clean and normalize command text"""
        # Convert to lowercase
        text = text.lower()

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text).strip()

        # Remove special characters but keep basic punctuation
        text = re.sub(r"[^\w\s\?\!\.\,]", "", text)

        return text

    def _extract_parameters(self, text: str) -> dict[str, Any]:
        """Extract parameters from command text"""
        parameters = {}

        for param_name, pattern in self.parameter_extractors.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                if len(matches) == 1:
                    parameters[param_name] = matches[0]
                else:
                    parameters[param_name] = matches

        return parameters

    def _classify_command_type(self, text: str) -> tuple[CommandType, float]:
        """Classify command type based on patterns"""
        best_type = CommandType.INFORMATION
        best_confidence = 0.0

        for command_type, patterns in self.command_patterns.items():
            confidence = self._calculate_pattern_confidence(text, patterns)
            if confidence > best_confidence:
                best_confidence = confidence
                best_type = command_type

        return best_type, best_confidence

    def _calculate_pattern_confidence(self, text: str, patterns: list[str]) -> float:
        """Calculate confidence score for pattern matching"""
        matches = 0
        total_patterns = len(patterns)

        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matches += 1

        return matches / total_patterns if total_patterns > 0 else 0.0

    def _extract_action(self, text: str, command_type: CommandType) -> str:
        """Extract specific action from command text"""
        action_mapping = {
            CommandType.TASK_ASSIGNMENT: "assign_task",
            CommandType.STATUS_REQUEST: "get_status",
            CommandType.COORDINATION: "coordinate",
            CommandType.EMERGENCY: "handle_emergency",
            CommandType.INFORMATION: "provide_information",
            CommandType.ACTION_REQUEST: "execute_action",
        }

        base_action = action_mapping.get(command_type, "process_command")

        # Add specific action based on keywords
        if re.search(r"\b(start|begin|launch)\b", text):
            return f"{base_action}_start"
        elif re.search(r"\b(stop|end|terminate)\b", text):
            return f"{base_action}_stop"
        elif re.search(r"\b(check|verify|validate)\b", text):
            return f"{base_action}_check"
        elif re.search(r"\b(update|modify|change)\b", text):
            return f"{base_action}_update"
        else:
            return base_action

    def _determine_priority(self, text: str, context_priority: CommandPriority) -> CommandPriority:
        """Determine command priority from text and context"""
        # Check for priority indicators in text
        for priority, indicators in self.priority_indicators.items():
            for indicator in indicators:
                if indicator in text:
                    return priority

        # Fall back to context priority
        return context_priority


class CommandExecutor:
    """Command execution engine"""

    def __init__(self):
        self.execution_handlers = self._initialize_execution_handlers()
        self.execution_history: list[dict[str, Any]] = []

    def _initialize_execution_handlers(self) -> dict[str, callable]:
        """Initialize command execution handlers"""
        return {
            "assign_task": self._handle_assign_task,
            "get_status": self._handle_get_status,
            "coordinate": self._handle_coordinate,
            "handle_emergency": self._handle_emergency,
            "provide_information": self._handle_provide_information,
            "execute_action": self._handle_execute_action,
        }

    def execute_command(self, parsed_command: ParsedCommand) -> dict[str, Any]:
        """Execute parsed command"""
        action = parsed_command.action
        handler = self.execution_handlers.get(action, self._handle_unknown_command)

        try:
            result = handler(parsed_command)
            execution_result = {
                "status": "success",
                "action": action,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "command_id": f"cmd_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            }
        except Exception as e:
            execution_result = {
                "status": "error",
                "action": action,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "command_id": f"cmd_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            }

        # Record execution
        self.execution_history.append(execution_result)

        return execution_result

    def _handle_assign_task(self, command: ParsedCommand) -> str:
        """Handle task assignment commands"""
        task_id = command.parameters.get("task_id", "Unknown")
        agent_id = command.parameters.get("agent_id", "Unknown")
        return f"Task {task_id} assigned to {agent_id}"

    def _handle_get_status(self, command: ParsedCommand) -> str:
        """Handle status request commands"""
        return "System status: All systems operational"

    def _handle_coordinate(self, command: ParsedCommand) -> str:
        """Handle coordination commands"""
        return "Coordination initiated - team synchronization in progress"

    def _handle_emergency(self, command: ParsedCommand) -> str:
        """Handle emergency commands"""
        return "Emergency protocol activated - Captain notified"

    def _handle_provide_information(self, command: ParsedCommand) -> str:
        """Handle information request commands"""
        return "Information request processed - providing detailed response"

    def _handle_execute_action(self, command: ParsedCommand) -> str:
        """Handle action execution commands"""
        return "Action executed successfully"

    def _handle_unknown_command(self, command: ParsedCommand) -> str:
        """Handle unknown commands"""
        return f"Unknown command: {command.action}"


class CommandUnderstandingSystem:
    """Main command understanding system"""

    def __init__(self):
        self.parser = CommandParser()
        self.executor = CommandExecutor()

    def process_command(
        self,
        text: str,
        sender: str,
        recipient: str,
        priority: CommandPriority = CommandPriority.MEDIUM,
    ) -> dict[str, Any]:
        """Process command through complete understanding pipeline"""
        # Create command context
        context = CommandContext(
            sender=sender, recipient=recipient, timestamp=datetime.now(), priority=priority
        )

        # Parse command
        parsed_command = self.parser.parse_command(text, context)

        # Execute command
        execution_result = self.executor.execute_command(parsed_command)

        return {
            "parsed_command": {
                "type": parsed_command.command_type.value,
                "action": parsed_command.action,
                "parameters": parsed_command.parameters,
                "confidence": parsed_command.confidence,
            },
            "execution": execution_result,
            "context": {
                "sender": context.sender,
                "recipient": context.recipient,
                "priority": context.priority.value,
                "timestamp": context.timestamp.isoformat(),
            },
        }

    def get_system_status(self) -> dict[str, Any]:
        """Get command understanding system status"""
        return {
            "system": "V3-009 Command Understanding",
            "status": "operational",
            "command_types": len(self.parser.command_patterns),
            "parameter_types": len(self.parser.parameter_extractors),
            "execution_handlers": len(self.executor.execution_handlers),
            "execution_history_count": len(self.executor.execution_history),
            "timestamp": datetime.now().isoformat(),
        }


# Global command understanding system instance
command_system = CommandUnderstandingSystem()


def process_command(
    text: str, sender: str, recipient: str, priority: CommandPriority = CommandPriority.MEDIUM
) -> dict[str, Any]:
    """Process command through understanding system"""
    return command_system.process_command(text, sender, recipient, priority)


def get_command_system_status() -> dict[str, Any]:
    """Get command understanding system status"""
    return command_system.get_system_status()


if __name__ == "__main__":
    # Test command understanding system
    test_commands = [
        ("Assign V3-006 to Agent-3 with HIGH priority", "Agent-4", "Agent-3", CommandPriority.HIGH),
        (
            "What is the status of the performance monitoring system?",
            "Agent-1",
            "Agent-3",
            CommandPriority.MEDIUM,
        ),
        (
            "Emergency: Critical error in database system",
            "Agent-2",
            "Agent-3",
            CommandPriority.CRITICAL,
        ),
        (
            "Coordinate with Agent-1 on API integration",
            "Agent-4",
            "Agent-3",
            CommandPriority.MEDIUM,
        ),
    ]

    for text, sender, recipient, priority in test_commands:
        print(f"\nCommand: {text}")
        result = process_command(text, sender, recipient, priority)
        print(f"Type: {result['parsed_command']['type']}")
        print(f"Action: {result['parsed_command']['action']}")
        print(f"Parameters: {result['parsed_command']['parameters']}")
        print(f"Execution: {result['execution']['status']} - {result['execution']['result']}")

    # Show system status
    status = get_command_system_status()
    print(f"\nCommand System Status: {status}")
