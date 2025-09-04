"""
Messaging Delivery Utilities - V2 Compliant Shared Delivery Logic
Eliminates DRY violations across messaging delivery methods
V2 Compliance: Under 300-line limit with focused functionality

@Author: Agent-6 - Gaming & Entertainment Specialist (Coordination & Communication V2 Compliance)
@Version: 1.0.0 - Messaging Delivery DRY Elimination
@License: MIT
"""

from enum import Enum


class DeliveryMethod(Enum):
    """Enumeration of supported delivery methods."""
    PYAUTOGUI = "pyautogui"
    INBOX = "inbox"
    API = "api"


class DeliveryResult:
    """Result of a delivery operation."""
    def __init__(self, success: bool, method: DeliveryMethod, error: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.success = success
        self.method = method
        self.error = error
        self.details = details or {}


class MessagingDeliveryUtils:
    """
    Shared messaging delivery utilities to eliminate DRY violations.
    
    Provides common delivery functionality for:
    - PyAutoGUI delivery
    - Inbox delivery
    - API delivery
    - Delivery orchestration
    """

    @staticmethod
    async def deliver_with_pyautogui(message: UnifiedMessage, coordinates: Dict[str, Any]) -> DeliveryResult:
        """
        Deliver message using PyAutoGUI method.
        
        Args:
            message: Message to deliver
            coordinates: Agent coordinates for delivery
            
        Returns:
            DeliveryResult with success status and details
        """
        try:
            # Import PyAutoGUI delivery logic
            
            delivery_service = PyAutoGUIMessagingDelivery()
            success = await delivery_service.deliver_message(message, coordinates)
            
            return DeliveryResult(
                success=success,
                method=DeliveryMethod.PYAUTOGUI,
                details={"coordinates": coordinates}
            )
            
        except Exception as e:
            return DeliveryResult(
                success=False,
                method=DeliveryMethod.PYAUTOGUI,
                error=f"PyAutoGUI delivery failed: {str(e)}"
            )

    @staticmethod
    async def deliver_with_inbox(message: UnifiedMessage, agent_workspace: str) -> DeliveryResult:
        """
        Deliver message using inbox file method.
        
        Args:
            message: Message to deliver
            agent_workspace: Agent workspace path
            
        Returns:
            DeliveryResult with success status and details
        """
        try:
            
            # Create inbox directory if it doesn't exist
            inbox_dir = get_unified_utility().path.join(agent_workspace, "inbox")
            get_unified_utility().makedirs(inbox_dir, exist_ok=True)
            
            # Create message file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{message.message_id}_{timestamp}.md"
            filepath = get_unified_utility().path.join(inbox_dir, filename)
            
            # Write message to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Message from {message.sender}\n")
                f.write(f"**To:** {message.recipient}\n")
                f.write(f"**Type:** {message.message_type}\n")
                f.write(f"**Priority:** {message.priority}\n")
                f.write(f"**Timestamp:** {message.timestamp}\n")
                f.write(f"**Tags:** {', '.join(message.tags) if message.tags else 'None'}\n\n")
                f.write("## Content\n\n")
                f.write(message.content)
            
            return DeliveryResult(
                success=True,
                method=DeliveryMethod.INBOX,
                details={"filepath": filepath, "filename": filename}
            )
            
        except Exception as e:
            return DeliveryResult(
                success=False,
                method=DeliveryMethod.INBOX,
                error=f"Inbox delivery failed: {str(e)}"
            )

    @staticmethod
    async def deliver_with_api(message: UnifiedMessage, api_endpoint: str) -> DeliveryResult:
        """
        Deliver message using API method.
        
        Args:
            message: Message to deliver
            api_endpoint: API endpoint URL
            
        Returns:
            DeliveryResult with success status and details
        """
        try:
            
            # Prepare message data for API
            message_data = {
                "message_id": message.message_id,
                "sender": message.sender,
                "recipient": message.recipient,
                "message_type": message.message_type.value if get_unified_validator().validate_hasattr(message.message_type, 'value') else str(message.message_type),
                "priority": message.priority.value if get_unified_validator().validate_hasattr(message.priority, 'value') else str(message.priority),
                "content": message.content,
                "tags": message.tags,
                "timestamp": message.timestamp,
                "metadata": message.metadata
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(api_endpoint, json=message_data) as response:
                    if response.status == 200:
                        return DeliveryResult(
                            success=True,
                            method=DeliveryMethod.API,
                            details={"status_code": response.status, "endpoint": api_endpoint}
                        )
                    else:
                        return DeliveryResult(
                            success=False,
                            method=DeliveryMethod.API,
                            error=f"API delivery failed with status {response.status}"
                        )
                        
        except Exception as e:
            return DeliveryResult(
                success=False,
                method=DeliveryMethod.API,
                error=f"API delivery failed: {str(e)}"
            )

    @staticmethod
    async def deliver_message(
        message: UnifiedMessage, 
        method: DeliveryMethod, 
        **kwargs
    ) -> DeliveryResult:
        """
        Deliver message using specified method.
        
        Args:
            message: Message to deliver
            method: Delivery method to use
            **kwargs: Additional parameters for delivery method
            
        Returns:
            DeliveryResult with success status and details
        """
        if method == DeliveryMethod.PYAUTOGUI:
            coordinates = kwargs.get('coordinates', {})
            return await MessagingDeliveryUtils.deliver_with_pyautogui(message, coordinates)
            
        elif method == DeliveryMethod.INBOX:
            agent_workspace = kwargs.get('agent_workspace', '')
            return await MessagingDeliveryUtils.deliver_with_inbox(message, agent_workspace)
            
        elif method == DeliveryMethod.API:
            api_endpoint = kwargs.get('api_endpoint', '')
            return await MessagingDeliveryUtils.deliver_with_api(message, api_endpoint)
            
        else:
            return DeliveryResult(
                success=False,
                method=method,
                error=f"Unsupported delivery method: {method}"
            )

    @staticmethod
    def get_delivery_method_from_string(method_str: str) -> Optional[DeliveryMethod]:
        """
        Convert string to DeliveryMethod enum.
        
        Args:
            method_str: String representation of delivery method
            
        Returns:
            DeliveryMethod enum or None if invalid
        """
        method_map = {
            "pyautogui": DeliveryMethod.PYAUTOGUI,
            "inbox": DeliveryMethod.INBOX,
            "api": DeliveryMethod.API
        }
        
        return method_map.get(method_str.lower())

    @staticmethod
    def format_delivery_result(result: DeliveryResult) -> str:
        """
        Format delivery result for logging or display.
        
        Args:
            result: Delivery result to format
            
        Returns:
            Formatted string
        """
        if result.success:
            return f"✅ {result.method.value} delivery successful"
        else:
            return f"❌ {result.method.value} delivery failed: {result.error}"

    @staticmethod
    def get_available_delivery_methods() -> List[DeliveryMethod]:
        """
        Get list of available delivery methods.
        
        Returns:
            List of available delivery methods
        """
        return [DeliveryMethod.PYAUTOGUI, DeliveryMethod.INBOX, DeliveryMethod.API]


# Export main interface
__all__ = ["MessagingDeliveryUtils", "DeliveryMethod", "DeliveryResult"]
