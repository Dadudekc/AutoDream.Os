"""
Agent-6 V2 Compliance Test Suite
Tests for Coordination & Communication V2 Compliance implementation
V2 Compliance: Under 300-line limit with comprehensive test coverage

@Author: Agent-6 - Gaming & Entertainment Specialist (Coordination & Communication V2 Compliance)
@Version: 1.0.0 - V2 Compliance Test Suite
@License: MIT
"""


# Import V2 compliant modules
    SSOTCoordinationManagerEnhanced,
    create_enhanced_coordination_manager
)
    VectorDatabaseStrategicOversightV2,
    create_strategic_oversight_v2
)
    UnifiedAgentCoordinatorV2,
    create_unified_agent_coordinator_v2,
    AgentType
)


class TestSSOTCoordinationManagerEnhanced:
    """Test suite for enhanced SSOT coordination manager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_vector_db = Mock()
        self.coordinator = create_enhanced_coordination_manager(self.mock_vector_db)

    def test_initialization(self):
        """Test coordinator initialization."""
        assert self.coordinator is not None
        assert self.coordinator.vector_db_service == self.mock_vector_db
        assert not self.coordinator.coordination_active
        assert len(self.coordinator.coordination_threads) == 0

    def test_v2_compliance_line_count(self):
        """Test V2 compliance - line count under 300."""
        source_lines = len(inspect.getsource(SSOTCoordinationManagerEnhanced).split('\n'))
        assert source_lines < 300, f"File exceeds V2 line limit: {source_lines} lines"

    def test_dependency_injection(self):
        """Test dependency injection pattern."""
        # Test with vector database service
        coordinator_with_db = create_enhanced_coordination_manager(self.mock_vector_db)
        assert coordinator_with_db.vector_db_service == self.mock_vector_db
        
        # Test without vector database service
        coordinator_without_db = create_enhanced_coordination_manager(None)
        assert coordinator_without_db.vector_db_service is None

    def test_coordination_initialization(self):
        """Test coordination system initialization."""
        self.coordinator.initialize_coordination()
        assert self.coordinator.coordination_active
        assert len(self.coordinator.coordination_threads) == 2

    def test_intelligent_message_sending(self):
        """Test intelligent coordination message sending."""
        self.coordinator.initialize_coordination()
        
        message_id = self.coordinator.send_intelligent_coordination_message(
            recipient="Agent-1",
            message_type="coordination_request",
            content={"task": "integration"},
            use_vector_insights=True
        )
        
        assert message_id is not None
        assert message_id.startswith("msg_")

    def test_agent_recommendations(self):
        """Test intelligent agent recommendations."""
        # Mock agent capabilities
        self.coordinator.agent_capabilities = {
            "Agent-1": {
                "skills": ["integration", "core_systems"],
                "performance_score": 90.0,
                "availability": "active"
            },
            "Agent-7": {
                "skills": ["web_development", "react"],
                "performance_score": 85.0,
                "availability": "active"
            }
        }
        
        task_requirements = {
            "required_skills": ["integration"],
            "task_type": "integration"
        }
        
        recommendations = self.coordinator.get_intelligent_agent_recommendations(task_requirements)
        
        assert len(recommendations) > 0
        assert recommendations[0]["agent_id"] == "Agent-1"
        assert recommendations[0]["match_score"] > 0.7

    def test_enhanced_status(self):
        """Test enhanced coordination status."""
        self.coordinator.initialize_coordination()
        
        status = self.coordinator.get_enhanced_coordination_status()
        
        assert status["active"] is True
        assert status["vector_database_connected"] is True
        assert "coordination_metrics" in status


class TestVectorDatabaseStrategicOversightV2:
    """Test suite for V2 compliant strategic oversight."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = get_unified_config().get_config()"ssot_config": {}, "enable_messaging": False}
        self.oversight = create_strategic_oversight_v2(self.config)

    def test_initialization(self):
        """Test strategic oversight initialization."""
        assert self.oversight is not None
        assert self.oversight.config == self.config
        assert self.oversight.ssot_indexer is not None
        assert self.oversight.context_retrieval is not None
        assert self.oversight.pattern_analysis is not None

    def test_v2_compliance_line_count(self):
        """Test V2 compliance - line count under 300."""
        source_lines = len(inspect.getsource(VectorDatabaseStrategicOversightV2).split('\n'))
        assert source_lines < 300, f"File exceeds V2 line limit: {source_lines} lines"

    def test_dependency_injection(self):
        """Test dependency injection pattern."""
        custom_config = get_unified_config().get_config()"custom_setting": "value"}
        oversight = create_strategic_oversight_v2(custom_config)
        assert oversight.config == custom_config

    @pytest.mark.asyncio
    async def test_ssot_data_initialization(self):
        """Test SSOT data initialization."""
        # Mock the ssot_indexer methods
        self.oversight.ssot_indexer.index_captain_handbook = Mock()
        self.oversight.ssot_indexer.index_v2_compliance_standards = Mock()
        
        await self.oversight.initialize_ssot_data()
        
        # Verify methods were called
        self.oversight.ssot_indexer.index_captain_handbook.assert_called_once()
        self.oversight.ssot_indexer.index_v2_compliance_standards.assert_called_once()

    @pytest.mark.asyncio
    async def test_strategic_oversight_report(self):
        """Test strategic oversight report generation."""
        # Mock agent capabilities
        self.oversight.agent_capabilities = {
            "Agent-1": Mock(skills=["integration"], performance_score=90.0, availability="active")
        }
        
        # Mock active missions
        self.oversight.active_missions = {
            "mission_1": Mock(status="active", progress=0.5, objectives=["obj1"], deadline=None)
        }
        
        report = await self.oversight.generate_strategic_oversight_report("mission_1")
        
        assert report is not None
        assert report.report_id is not None
        assert "mission_status" in report.mission_status
        assert len(report.agent_capabilities) > 0

    @pytest.mark.asyncio
    async def test_swarm_coordination_insights(self):
        """Test swarm coordination insights."""
        # Mock context retrieval
        self.oversight.context_retrieval.get_context_insights = AsyncMock(return_value=[
            {
                "type": "coordination",
                "content": "Test insight",
                "confidence": 0.8,
                "actions": ["action1"],
                "impact": "high"
            }
        ])
        
        insights = await self.oversight.get_swarm_coordination_insights("test_context")
        
        assert len(insights) > 0
        assert insights[0].insight_type == "coordination"
        assert insights[0].confidence_level == 0.8

    @pytest.mark.asyncio
    async def test_agent_recommendations(self):
        """Test intelligent agent recommendations."""
        # Mock agent capabilities
        self.oversight.agent_capabilities = {
            "Agent-1": AgentCapability(
                skills=["integration", "core_systems"],
                specializations=["system_integration"],
                performance_score=90.0,
                availability="active"
            )
        }
        
        task_requirements = {
            "required_skills": ["integration"],
            "task_type": "integration"
        }
        
        recommendations = await self.oversight.get_agent_recommendations(task_requirements)
        
        assert len(recommendations) > 0
        assert recommendations[0]["agent_id"] == "Agent-1"
        assert recommendations[0]["match_score"] > 0.7


class TestUnifiedAgentCoordinatorV2:
    """Test suite for V2 compliant unified agent coordinator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_vector_db = Mock()
        self.coordinator = create_unified_agent_coordinator_v2(self.mock_vector_db)

    def test_initialization(self):
        """Test coordinator initialization."""
        assert self.coordinator is not None
        assert self.coordinator.vector_db_service == self.mock_vector_db
        assert len(self.coordinator.strategies) == 3  # Agent-1, Agent-6, Agent-7
        assert AgentType.AGENT_1 in self.coordinator.strategies
        assert AgentType.AGENT_6 in self.coordinator.strategies
        assert AgentType.AGENT_7 in self.coordinator.strategies

    def test_v2_compliance_line_count(self):
        """Test V2 compliance - line count under 300."""
        source_lines = len(inspect.getsource(UnifiedAgentCoordinatorV2).split('\n'))
        assert source_lines < 300, f"File exceeds V2 line limit: {source_lines} lines"

    def test_dependency_injection(self):
        """Test dependency injection pattern."""
        # Test with vector database service
        coordinator_with_db = create_unified_agent_coordinator_v2(self.mock_vector_db)
        assert coordinator_with_db.vector_db_service == self.mock_vector_db
        
        # Test without vector database service
        coordinator_without_db = create_unified_agent_coordinator_v2(None)
        assert coordinator_without_db.vector_db_service is None

    @pytest.mark.asyncio
    async def test_agent_coordination(self):
        """Test agent coordination."""
        agent_data = {
            "integration_targets": ["target1", "target2"],
            "task_type": "integration"
        }
        
        result = await self.coordinator.coordinate_agent(
            AgentType.AGENT_1, 
            agent_data, 
            use_vector_insights=True
        )
        
        assert result is not None
        assert result.agent_type == AgentType.AGENT_1
        assert result.status == "coordinated"
        assert result.execution_time > 0
        assert len(result.recommendations) > 0

    @pytest.mark.asyncio
    async def test_intelligent_agent_recommendations(self):
        """Test intelligent agent recommendations."""
        task_requirements = {
            "required_skills": ["integration"],
            "task_type": "integration"
        }
        
        recommendations = await self.coordinator.get_intelligent_agent_recommendations(task_requirements)
        
        assert len(recommendations) > 0
        assert recommendations[0]["agent_type"] == AgentType.AGENT_1
        assert recommendations[0]["match_score"] > 0.7

    @pytest.mark.asyncio
    async def test_coordination_analytics(self):
        """Test coordination analytics."""
        # Perform some coordinations first
        await self.coordinator.coordinate_agent(AgentType.AGENT_1, {"test": "data"})
        await self.coordinator.coordinate_agent(AgentType.AGENT_6, {"test": "data"})
        
        analytics = await self.coordinator.get_coordination_analytics()
        
        assert analytics["total_coordinations"] >= 2
        assert analytics["successful_coordinations"] >= 2
        assert analytics["success_rate"] >= 0
        assert "agent_type_distribution" in analytics
        assert "performance_metrics" in analytics


class TestV2ComplianceIntegration:
    """Integration tests for V2 compliance across all systems."""

    def setup_method(self):
        """Set up integration test fixtures."""
        self.mock_vector_db = Mock()
        self.coordination_manager = create_enhanced_coordination_manager(self.mock_vector_db)
        self.strategic_oversight = create_strategic_oversight_v2({})
        self.agent_coordinator = create_unified_agent_coordinator_v2(self.mock_vector_db)

    def test_v2_compliance_across_all_systems(self):
        """Test V2 compliance across all coordination systems."""
        
        # Test line count compliance
        coordination_lines = len(inspect.getsource(SSOTCoordinationManagerEnhanced).split('\n'))
        oversight_lines = len(inspect.getsource(VectorDatabaseStrategicOversightV2).split('\n'))
        agent_coord_lines = len(inspect.getsource(UnifiedAgentCoordinatorV2).split('\n'))
        
        assert coordination_lines < 300, f"Coordination manager exceeds V2 limit: {coordination_lines} lines"
        assert oversight_lines < 300, f"Strategic oversight exceeds V2 limit: {oversight_lines} lines"
        assert agent_coord_lines < 300, f"Agent coordinator exceeds V2 limit: {agent_coord_lines} lines"

    def test_dependency_injection_consistency(self):
        """Test dependency injection consistency across systems."""
        # All systems should support dependency injection
        assert get_unified_validator().validate_hasattr(self.coordination_manager, 'vector_db_service')
        assert get_unified_validator().validate_hasattr(self.strategic_oversight, 'config')
        assert get_unified_validator().validate_hasattr(self.agent_coordinator, 'vector_db_service')

    @pytest.mark.asyncio
    async def test_integrated_coordination_workflow(self):
        """Test integrated coordination workflow."""
        # Initialize coordination manager
        self.coordination_manager.initialize_coordination()
        
        # Generate strategic oversight report
        report = await self.strategic_oversight.generate_strategic_oversight_report()
        
        # Coordinate agents
        agent_result = await self.agent_coordinator.coordinate_agent(
            AgentType.AGENT_6, 
            {"coordination_systems": ["system1", "system2"]}
        )
        
        # Verify integration
        assert self.coordination_manager.coordination_active
        assert report is not None
        assert agent_result.status == "coordinated"

    def test_performance_metrics_tracking(self):
        """Test performance metrics tracking across systems."""
        # All systems should track performance metrics
        assert get_unified_validator().validate_hasattr(self.coordination_manager, 'coordination_metrics')
        assert get_unified_validator().validate_hasattr(self.agent_coordinator, 'performance_metrics')
        
        # Initialize and check metrics
        self.coordination_manager.initialize_coordination()
        status = self.coordination_manager.get_enhanced_coordination_status()
        
        assert "coordination_metrics" in status
        assert "vector_database_connected" in status


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
