    """Centralized communication management system."""
    
    def __init__(self):
        self.protocols: Dict[CommunicationType, CommunicationInterface] = {}
        self.message_handlers: Dict[str, callable] = {}
        self.running = False
        self._lock = threading.Lock()
    
    def register_protocol(self, comm_type: CommunicationType, protocol: CommunicationInterface):
        """Register communication protocol."""
        with self._lock:
            self.protocols[comm_type] = protocol
    
    def register_handler(self, message_type: str, handler: callable):
        """Register message handler."""
        self.message_handlers[message_type] = handler
    
    async def start(self):
        """Start communication manager."""
        self.running = True
        for protocol in self.protocols.values():
            await protocol.connect()
    
    async def stop(self):
        """Stop communication manager."""
        self.running = False
        for protocol in self.protocols.values():
            await protocol.disconnect()
    
    async def broadcast(self, message: Message):
        """Broadcast message across all protocols."""
        for protocol in self.protocols.values():
            await protocol.send(message)
    
    async def route_message(self, message: Message):
        """Route message to appropriate handler."""
        if message.type in self.message_handlers:
            handler = self.message_handlers[message.type]
            await handler(message)


class ConsolidatedCommunicationSystem:
    """Main consolidated communication system."""
    
    def __init__(self):
        self.manager = CommunicationManager()
        self.http_comm = None
        self.websocket_comm = None
        self.queue_comm = None
        self._initialized = False
    
    def initialize(self, config: Dict[str, Any]):
        """Initialize communication system with configuration."""
        if self._initialized:
            return
        
        # Initialize HTTP communication
        if 'http' in config:
            self.http_comm = HTTPCommunication(
                config['http']['base_url'],
                config['http'].get('timeout', 30)
            )
            self.manager.register_protocol(CommunicationType.HTTP, self.http_comm)
        
        # Initialize WebSocket communication
        if 'websocket' in config:
            self.websocket_comm = WebSocketCommunication(config['websocket']['url'])
            self.manager.register_protocol(CommunicationType.WEBSOCKET, self.websocket_comm)
        
        # Initialize message queue communication
        if 'queue' in config:
            self.queue_comm = MessageQueue(
                config['queue']['name'],
                config['queue']['broker_url']
            )
            self.manager.register_protocol(CommunicationType.RABBITMQ, self.queue_comm)
        
        self._initialized = True
    
    async def start_system(self):
        """Start the communication system."""
        if not self._initialized:
            raise RuntimeError("Communication system not initialized")
        await self.manager.start()
    
    async def stop_system(self):
        """Stop the communication system."""
        await self.manager.stop()
    
    async def send_message(self, message: Message, protocol: CommunicationType = None):
        """Send message using specified or default protocol."""
        if protocol and protocol in self.manager.protocols:
            await self.manager.protocols[protocol].send(message)
        else:
            await self.manager.broadcast(message)
    
    def register_message_handler(self, message_type: str, handler: callable):
        """Register message handler."""
        self.manager.register_handler(message_type, handler)
    
    async def process_messages(self):
        """Process incoming messages."""
        while self.manager.running:
            for protocol in self.manager.protocols.values():
                message = await protocol.receive()
                if message:
                    await self.manager.route_message(message)
            await asyncio.sleep(0.1)


# Global communication system instance
communication_system = ConsolidatedCommunicationSystem()
