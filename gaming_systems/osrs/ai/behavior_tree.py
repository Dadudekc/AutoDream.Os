"""Behavior tree implementation for OSRS AI."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, List, Optional


class OSRSBehaviorNodeType(Enum):
    """Types of nodes used in the behavior tree."""

    ACTION = "action"
    CONDITION = "condition"
    SEQUENCE = "sequence"
    SELECTOR = "selector"
    DECORATOR = "decorator"


@dataclass
class OSRSBehaviorNode:
    """Base class for all behavior tree nodes."""

    name: str
    node_type: OSRSBehaviorNodeType
    children: List["OSRSBehaviorNode"] = field(default_factory=list)

    def add_child(self, child: "OSRSBehaviorNode") -> None:
        """Attach a child node."""
        self.children.append(child)

    def execute(self, player: Any, game_state: Any) -> bool:  # pragma: no cover - abstract
        """Execute the node's behavior.

        Subclasses override this method to provide actual logic.
        """
        raise NotImplementedError


class OSRSActionNode(OSRSBehaviorNode):
    """Leaf node that performs an action."""

    def __init__(self, name: str, action_func: Optional[Callable[[Any, Any], bool]] = None) -> None:
        super().__init__(name, OSRSBehaviorNodeType.ACTION)
        self.action_func = action_func

    def execute(self, player: Any, game_state: Any) -> bool:
        if not self.action_func:
            return True
        try:
            return bool(self.action_func(player, game_state))
        except Exception as e:  # pragma: no cover - defensive
            logging.error(f"Exception in action node '{self.name}': {e}", exc_info=True)
            return False


class OSRSConditionNode(OSRSBehaviorNode):
    """Leaf node that checks a condition."""

    def __init__(self, name: str, condition_func: Callable[[Any, Any], bool]) -> None:
        super().__init__(name, OSRSBehaviorNodeType.CONDITION)
        self.condition_func = condition_func

    def execute(self, player: Any, game_state: Any) -> bool:
        try:
            return bool(self.condition_func(player, game_state))
        except Exception as e:  # pragma: no cover - defensive
            logging.error(f"Exception in condition node '{self.name}': {e}", exc_info=True)
            return False


class OSRSSequenceNode(OSRSBehaviorNode):
    """Composite node that runs children in sequence until one fails."""

    def __init__(self, name: str) -> None:
        super().__init__(name, OSRSBehaviorNodeType.SEQUENCE)

    def execute(self, player: Any, game_state: Any) -> bool:
        for child in self.children:
            if not child.execute(player, game_state):
                return False
        return True


class OSRSSelectorNode(OSRSBehaviorNode):
    """Composite node that succeeds if any child succeeds."""

    def __init__(self, name: str) -> None:
        super().__init__(name, OSRSBehaviorNodeType.SELECTOR)

    def execute(self, player: Any, game_state: Any) -> bool:
        for child in self.children:
            if child.execute(player, game_state):
                return True
        return False


class OSRSDecoratorNode(OSRSBehaviorNode):
    """Node that modifies the result of its single child."""

    def __init__(self, name: str, decorator: Callable[[bool], bool]) -> None:
        super().__init__(name, OSRSBehaviorNodeType.DECORATOR)
        self.decorator = decorator

    def execute(self, player: Any, game_state: Any) -> bool:
        if not self.children:
            return False
        result = self.children[0].execute(player, game_state)
        try:
            return bool(self.decorator(result))
        except Exception as e:  # pragma: no cover - defensive
            logging.error(f"Exception in decorator node '{self.name}': {e}", exc_info=True)
            return False


class OSRSBehaviorTree:
    """Behavior tree container."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.root: Optional[OSRSBehaviorNode] = None

    def set_root(self, node: OSRSBehaviorNode) -> None:
        self.root = node

    def execute(self, player: Any, game_state: Any) -> bool:
        """Execute the behavior tree starting from the root."""
        if not self.root:
            return False
        return bool(self.root.execute(player, game_state))
