    """WebSocket-based communication implementation."""
    
    def __init__(self, url: str):
        self.url = url
        self.websocket = None
        self._connected = False
    
    async def connect(self) -> bool:
        """Establish WebSocket connection."""
        try:
            import websockets
            self.websocket = await websockets.connect(self.url)
            self._connected = True
            return True
        except ImportError:
            logging.error("websockets not available for WebSocket communication")
            return False
    
    async def disconnect(self) -> bool:
        """Close WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
            self._connected = False
        return True
    
    async def send(self, message: Message) -> bool:
        """Send WebSocket message."""
        if not self._connected:
            return False
        try:
            await self.websocket.send(json.dumps(message.__dict__))
            return True
        except Exception as e:
            logging.error(f"WebSocket send error: {e}")
            return False
    
    async def receive(self) -> Optional[Message]:
        """Receive WebSocket message."""
        if not self._connected:
            return None
        try:
            data = await self.websocket.recv()
            return Message(**json.loads(data))
        except Exception as e:
            logging.error(f"WebSocket receive error: {e}")
        return None


class MessageQueue(CommunicationInterface):
    """Message queue communication implementation."""
    
    def __init__(self, queue_name: str, broker_url: str):
        self.queue_name = queue_name
        self.broker_url = broker_url
        self.connection = None
        self.channel = None
        self._connected = False
    
    async def connect(self) -> bool:
        """Establish queue connection."""
        try:
            import pika
            self.connection = pika.BlockingConnection(pika.URLParameters(self.broker_url))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name)
            self._connected = True
            return True
        except ImportError:
            logging.error("pika not available for message queue communication")
            return False
    
    async def disconnect(self) -> bool:
        """Close queue connection."""
        if self.connection:
            self.connection.close()
            self._connected = False
        return True
    
    async def send(self, message: Message) -> bool:
        """Send queue message."""
        if not self._connected:
            return False
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message.__dict__)
            )
            return True
        except Exception as e:
            logging.error(f"Queue send error: {e}")
            return False
    
    async def receive(self) -> Optional[Message]:
        """Receive queue message."""
        if not self._connected:
            return None
        try:
            method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
            if method_frame:
                self.channel.basic_ack(method_frame.delivery_tag)
                return Message(**json.loads(body))
        except Exception as e:
            logging.error(f"Queue receive error: {e}")
        return None


class CommunicationManager: