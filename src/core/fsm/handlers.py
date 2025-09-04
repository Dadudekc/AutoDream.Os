"""
FSM Handlers - V2 Compliant State Machine Handlers
Handler implementations for FSM state transitions and actions
V2 COMPLIANCE: Under 300-line limit, modular design, comprehensive error handling

@version 1.0.0 - V2 COMPLIANCE FSM HANDLERS
@license MIT
"""



class StateHandler(ABC):
    """Abstract base class for state handlers"""

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> bool:
        """Execute state handler logic"""
        pass

    @abstractmethod
    def validate(self, context: Dict[str, Any]) -> bool:
        """Validate state conditions"""
        pass


class ConcreteStateHandler(StateHandler):
    """Concrete implementation of state handler"""

    def __init__(
        self,
        action: Callable[[Dict[str, Any]], None],
        check: Callable[[Dict[str, Any]], bool],
    ):
        """Initialize with action and validation functions"""
        self.action = action
        self.check = check

    def execute(self, context: Dict[str, Any]) -> bool:
        """Execute the state action"""
        try:
            self.action(context)
            return True
        except Exception as e:
            context["error"] = str(e)
            return False

    def validate(self, context: Dict[str, Any]) -> bool:
        """Validate state conditions"""
        try:
            return self.check(context)
        except Exception:
            return False


class TransitionHandler:
    """Handler for state transitions"""

    def __init__(self):
        self.handlers: Dict[str, StateHandler] = {}

    def register_handler(self, state_name: str, handler: StateHandler):
        """Register a handler for a specific state"""
        self.handlers[state_name] = handler

    def get_handler(self, state_name: str) -> Optional[StateHandler]:
        """Get handler for a specific state"""
        return self.handlers.get(state_name)

    def execute_transition(
        self, from_state: str, to_state: str, context: Dict[str, Any]
    ) -> bool:
        """Execute transition between states"""
        # Execute exit actions for from_state
        from_handler = self.get_handler(from_state)
        if from_handler and not from_handler.validate(context):
            return False

        # Execute entry actions for to_state
        to_handler = self.get_handler(to_state)
        if to_handler and not to_handler.validate(context):
            return False

        # Execute transition
        if from_handler:
            from_handler.execute(context)
        if to_handler:
            to_handler.execute(context)

        return True


# Factory function for dependency injection
def create_transition_handler() -> TransitionHandler:
    """Factory function to create transition handler instance"""
    return TransitionHandler()


# Export for DI
__all__ = [
    "StateHandler",
    "ConcreteStateHandler",
    "TransitionHandler",
    "create_transition_handler",
]
