#!/usr/bin/env python3
"""
Test-Driven Development for Messaging System - Agent Cellphone V2
================================================================

TDD Test Suite for identifying and fixing messaging system issues.
Following the failures identified in the logs, we'll write tests first,
then fix the issues.

Issues to address:
1. Lock acquisition errors with time variable
2. Atomic write failures
3. 'NoneType' object has no attribute 'sender'
4. Message queuing issues
5. PyAutoGUI fallback not working properly

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
"""


# Import messaging components
    UnifiedMessage as Message,
    UnifiedMessageType as MessageType,
    UnifiedMessagePriority as MessagePriority,
    DeliveryMethod
)


class TestMessagingSystemTDD:
    """TDD test suite for messaging system fixes."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.inbox_paths = {
            'Agent-1': get_unified_utility().path.join(self.temp_dir, 'agent_workspaces', 'Agent-1', 'inbox'),
            'Agent-2': get_unified_utility().path.join(self.temp_dir, 'agent_workspaces', 'Agent-2', 'inbox'),
            'Agent-3': get_unified_utility().path.join(self.temp_dir, 'agent_workspaces', 'Agent-3', 'inbox'),
            'Agent-4': get_unified_utility().path.join(self.temp_dir, 'agent_workspaces', 'Agent-4', 'inbox'),
        }

        # Create inbox directories
        for path in self.inbox_paths.values():
            get_unified_utility().makedirs(path, exist_ok=True)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @pytest.mark.asyncio
    async def test_message_creation_with_valid_data(self):
        """Test 1: Message creation should work with valid data."""
        # Given: Valid message parameters
        recipient = "Agent-1"
        content = "Test message"
        message_type = MessageType.TEXT
        priority = MessagePriority.REGULAR

        # When: Creating a message
        service = UnifiedMessagingCore()
        result = await service.send_message(
            recipient=recipient,
            content=content,
            message_type=message_type,
            priority=priority
        )

        # Then: Should succeed and return valid result
        assert result['success'] is True
        assert 'message_id' in result
        assert result['message_id'] is not None

    @pytest.mark.asyncio
    async def test_pyautogui_fallback_to_inbox_delivery(self):
        """Test 2: PyAutoGUI should fallback to inbox when coordinates unavailable."""
        # Given: Service with inbox paths configured
        service = UnifiedMessagingCore(inbox_paths=self.inbox_paths)

        # When: Sending message with PyAutoGUI mode (should fallback)
        result = await service.send_message(
            recipient="Agent-1",
            content="Test fallback message",
            delivery_method=DeliveryMethod.PYAUTOGUI
        )

        # Debug: Print result
        get_logger(__name__).info(f"DEBUG: Result = {result}")

        # Debug: Check if inbox paths are set
        get_logger(__name__).info(f"DEBUG: Service inbox_paths = {service.delivery_manager.inbox_paths if get_unified_validator().validate_hasattr(service, 'delivery_manager') else 'No delivery_manager'}")

        # Then: Should succeed via fallback and create inbox file
        assert result['success'] is True
        inbox_files = list(get_unified_utility().Path(self.inbox_paths['Agent-1']).glob("CAPTAIN_MESSAGE_*.md"))
        get_logger(__name__).info(f"DEBUG: Found inbox files = {inbox_files}")
        assert len(inbox_files) > 0

        # Verify file content
        with open(inbox_files[0], 'r') as f:
            content = f.read()
            assert "CAPTAIN MESSAGE" in content
            assert "Test fallback message" in content
            assert "Delivery Method: inbox" in content

    @pytest.mark.asyncio
    async def test_message_delivery_with_lock_handling(self):
        """Test 3: Message delivery should handle locks properly."""
        # Given: Service with proper configuration
        service = UnifiedMessagingCore()
        service.inbox_paths = self.inbox_paths

        # When: Sending multiple messages concurrently
        tasks = []
        for i in range(5):
            task = service.send_message(
                recipient="Agent-1",
                content=f"Concurrent message {i}",
                message_type=MessageType.TEXT,
                priority=MessagePriority.REGULAR
            )
            tasks.append(task)

        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Then: All should succeed without lock errors
        for result in results:
            if get_unified_validator().validate_type(result, Exception):
                pytest.fail(f"Concurrent delivery failed: {result}")
            assert result['success'] is True

        # Verify all messages delivered
        inbox_files = list(get_unified_utility().Path(self.inbox_paths['Agent-1']).glob("CAPTAIN_MESSAGE_*.md"))
        assert len(inbox_files) == 5

    @pytest.mark.asyncio
    async def test_message_validation_prevents_invalid_data(self):
        """Test 4: Message validation should prevent invalid data."""
        # Given: Service instance
        service = UnifiedMessagingCore()

        # When: Sending message with invalid recipient
        result = await service.send_message(
            recipient="",  # Invalid: empty recipient
            content="Test message"
        )

        # Then: Should fail validation
        assert result['success'] is False
        assert 'error' in result

    @pytest.mark.asyncio
    async def test_coordinates_loading_from_config(self):
        """Test 5: Coordinates should load properly from config."""
        # Given: Service instance
        service = UnifiedMessagingCore()

        # When: Loading coordinates
        result = await service.show_coordinates()

        # Then: Should return coordinate information
        assert 'status' in result
        if result['status'] == 'success':
            assert 'coordinates' in result
            assert 'pyautogui_config' in result
            assert get_unified_validator().validate_type(result['coordinates'], dict)

    @pytest.mark.asyncio
    async def test_message_with_metadata_tracking(self):
        """Test 6: Messages should track delivery metadata."""
        # Given: Service with inbox paths
        service = UnifiedMessagingCore()
        service.inbox_paths = self.inbox_paths

        # When: Sending message
        result = await service.send_message(
            recipient="Agent-1",
            content="Metadata test message",
            delivery_method=DeliveryMethod.PYAUTOGUI
        )

        # Then: Should track delivery method in metadata
        assert result['success'] is True
        assert 'method' in result
        assert result['method'] in ['pyautogui', 'inbox_fallback']

        # Verify inbox file created with proper metadata
        inbox_files = list(get_unified_utility().Path(self.inbox_paths['Agent-1']).glob("CAPTAIN_MESSAGE_*.md"))
        assert len(inbox_files) > 0

        with open(inbox_files[0], 'r') as f:
            content = f.read()
            assert "Delivery Method:" in content

    @pytest.mark.asyncio
    async def test_bulk_onboarding_creates_multiple_messages(self):
        """Test 7: Bulk onboarding should create messages for all agents."""
        # Given: Service instance
        service = UnifiedMessagingCore()
        service.inbox_paths = self.inbox_paths

        # When: Running bulk onboarding
        result = await service.send_bulk_onboarding()

        # Then: Should return results for all 8 agents
        assert get_unified_validator().validate_type(result, dict)
        assert len(result) == 8  # Agent-1 through Agent-8

        # Each agent should have a result
        for agent_id in [f"Agent-{i}" for i in range(1, 9)]:
            assert agent_id in result
            assert 'status' in result[agent_id]

    @pytest.mark.asyncio
    async def test_inbox_delivery_creates_proper_file_format(self):
        """Test 8: Inbox delivery should create properly formatted files."""
        # Given: Service with inbox paths
        service = UnifiedMessagingCore()
        service.inbox_paths = self.inbox_paths

        # When: Sending message directly to inbox
        result = await service.send_message(
            recipient="Agent-2",
            content="Formatted file test",
            delivery_method=DeliveryMethod.INBOX
        )

        # Then: Should create properly formatted file
        assert result['success'] is True

        inbox_files = list(get_unified_utility().Path(self.inbox_paths['Agent-2']).glob("CAPTAIN_MESSAGE_*.md"))
        assert len(inbox_files) > 0

        with open(inbox_files[0], 'r') as f:
            content = f.read()

            # Check required sections
            assert "# 🚨 CAPTAIN MESSAGE" in content
            assert "**From:**" in content
            assert "**To:**" in content
            assert "**Priority:**" in content
            assert "**Timestamp:**" in content
            assert "**Delivery Method:** inbox" in content
            assert "Formatted file test" in content
            assert "**WE. ARE. SWARM.**" in content

    @pytest.mark.asyncio
    async def test_error_handling_for_missing_inbox_paths(self):
        """Test 9: Should handle missing inbox paths gracefully."""
        # Given: Service without inbox paths configured
        service = UnifiedMessagingCore()
        # Don't set inbox_paths

        # When: Sending message
        result = await service.send_message(
            recipient="Agent-1",
            content="Missing inbox test"
        )

        # Then: Should handle gracefully (may succeed via PyAutoGUI or fail gracefully)
        assert 'success' in result
        # Either succeeds or fails with proper error message
        if not result['success']:
            assert 'error' in result

    @pytest.mark.asyncio
    async def test_message_id_generation_is_unique(self):
        """Test 10: Generated message IDs should be unique."""
        # Given: Service instance
        service = UnifiedMessagingCore()

        # When: Generating multiple message IDs
        ids = set()
        for _ in range(100):
            msg_id = service._generate_message_id()
            ids.add(msg_id)

        # Then: All IDs should be unique
        assert len(ids) == 100


if __name__ == "__main__":
    # Run the TDD tests
    pytest.main([__file__, "-v", "--tb=short"])
