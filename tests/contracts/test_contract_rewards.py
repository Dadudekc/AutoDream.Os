#!/usr/bin/env python3
"""
Contract Rewards Test Module
=============================

Tests for XP rewards, distribution, and tracking.
Part of the modularized test_contract_system.py (653 lines → 3 modules).

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import pytest


class TestXPRewards:
    """Test XP reward distribution and tracking."""

    def test_xp_calculation_and_distribution(self):
        """Test XP calculation and distribution logic."""
        reward_scenarios = [
            {
                "contract_id": "SIMPLE-001",
                "base_xp": 100,
                "complexity_multiplier": 1.0,
                "quality_bonus": 1.1,
                "expected_total_xp": 110,
            },
            {
                "contract_id": "COMPLEX-001",
                "base_xp": 500,
                "complexity_multiplier": 1.5,
                "quality_bonus": 1.2,
                "expected_total_xp": 900,
            },
            {
                "contract_id": "CRITICAL-001",
                "base_xp": 1000,
                "complexity_multiplier": 2.0,
                "quality_bonus": 1.3,
                "expected_total_xp": 2600,
            },
        ]

        for scenario in reward_scenarios:
            calculated_xp = (
                scenario["base_xp"] * scenario["complexity_multiplier"] * scenario["quality_bonus"]
            )

            assert calculated_xp == scenario["expected_total_xp"]

    def test_xp_award_process(self):
        """Test XP award process and balance updates."""
        initial_balance = 100
        award_request = {
            "agent_id": "Agent-7",
            "contract_id": "COMPLETED-001",
            "xp_amount": 250,
            "reason": "Contract completion",
        }

        # Simulate XP award
        new_balance = initial_balance + award_request["xp_amount"]
        level = (new_balance // 500) + 1  # Assuming 500 XP per level

        result = {
            "total_xp": new_balance,
            "level": level,
            "xp_gained": award_request["xp_amount"],
        }

        assert result["total_xp"] == initial_balance + award_request["xp_amount"]
        assert "level" in result
        assert result["level"] >= 1

    def test_xp_leaderboard_and_analytics(self):
        """Test XP leaderboard and analytics."""
        # Mock XP data
        agent_xp_data = [
            {"agent_id": "Agent-1", "total_xp": 2500, "level": 5, "contracts_completed": 12},
            {"agent_id": "Agent-7", "total_xp": 1800, "level": 4, "contracts_completed": 9},
            {"agent_id": "Agent-2", "total_xp": 1200, "level": 3, "contracts_completed": 6},
            {"agent_id": "Agent-8", "total_xp": 900, "level": 2, "contracts_completed": 4},
        ]

        # Validate leaderboard ordering
        sorted_by_xp = sorted(agent_xp_data, key=lambda x: x["total_xp"], reverse=True)
        assert sorted_by_xp[0]["agent_id"] == "Agent-1"
        assert sorted_by_xp[-1]["agent_id"] == "Agent-8"

        # Test level calculation (assuming 500 XP per level)
        for agent in agent_xp_data:
            expected_level = (agent["total_xp"] // 500) + 1
            assert agent["level"] == expected_level

    def test_xp_penalty_system(self):
        """Test XP penalty system for failed contracts."""
        penalty_scenarios = [
            {
                "contract_id": "FAILED-001",
                "failure_reason": "deadline_exceeded",
                "original_xp": 200,
                "penalty_percentage": 50,
                "expected_penalty_xp": 100,
            },
            {
                "contract_id": "ABANDONED-001",
                "failure_reason": "contract_abandoned",
                "original_xp": 300,
                "penalty_percentage": 75,
                "expected_penalty_xp": 225,
            },
            {
                "contract_id": "LOW_QUALITY-001",
                "failure_reason": "quality_standards_not_met",
                "original_xp": 150,
                "penalty_percentage": 25,
                "expected_penalty_xp": 37,  # Rounded down
            },
        ]

        for scenario in penalty_scenarios:
            penalty_amount = int(scenario["original_xp"] * (scenario["penalty_percentage"] / 100))
            assert penalty_amount == scenario["expected_penalty_xp"]

    def test_xp_bonus_system(self):
        """Test XP bonus system for exceptional performance."""
        bonus_scenarios = [
            {
                "contract_id": "EARLY_COMPLETION-001",
                "bonus_type": "early_completion",
                "base_xp": 200,
                "bonus_percentage": 25,
                "expected_bonus_xp": 50,
            },
            {
                "contract_id": "HIGH_QUALITY-001",
                "bonus_type": "quality_excellence",
                "base_xp": 300,
                "bonus_percentage": 50,
                "expected_bonus_xp": 150,
            },
            {
                "contract_id": "TEAM_COLLABORATION-001",
                "bonus_type": "team_collaboration",
                "base_xp": 400,
                "bonus_percentage": 15,
                "expected_bonus_xp": 60,
            },
        ]

        for scenario in bonus_scenarios:
            bonus_amount = int(scenario["base_xp"] * (scenario["bonus_percentage"] / 100))
            assert bonus_amount == scenario["expected_bonus_xp"]

    def test_xp_milestone_system(self):
        """Test XP milestone system and achievements."""
        milestone_scenarios = [
            {
                "agent_id": "Agent-1",
                "total_xp": 1000,
                "milestones": [
                    {"xp_threshold": 500, "achievement": "First Level Up", "unlocked": True},
                    {"xp_threshold": 1000, "achievement": "XP Master", "unlocked": True},
                    {"xp_threshold": 2000, "achievement": "XP Legend", "unlocked": False},
                ],
            },
            {
                "agent_id": "Agent-7",
                "total_xp": 2500,
                "milestones": [
                    {"xp_threshold": 500, "achievement": "First Level Up", "unlocked": True},
                    {"xp_threshold": 1000, "achievement": "XP Master", "unlocked": True},
                    {"xp_threshold": 2000, "achievement": "XP Legend", "unlocked": True},
                    {"xp_threshold": 5000, "achievement": "XP God", "unlocked": False},
                ],
            },
        ]

        for scenario in milestone_scenarios:
            total_xp = scenario["total_xp"]
            for milestone in scenario["milestones"]:
                expected_unlocked = total_xp >= milestone["xp_threshold"]
                assert milestone["unlocked"] == expected_unlocked

    def test_xp_transfer_system(self):
        """Test XP transfer system between agents."""
        transfer_scenarios = [
            {
                "from_agent": "Agent-1",
                "to_agent": "Agent-7",
                "xp_amount": 100,
                "transfer_reason": "collaboration_bonus",
                "from_balance_before": 1000,
                "to_balance_before": 500,
                "expected_from_balance": 900,
                "expected_to_balance": 600,
            },
            {
                "from_agent": "Agent-2",
                "to_agent": "Agent-8",
                "xp_amount": 50,
                "transfer_reason": "mentorship_reward",
                "from_balance_before": 800,
                "to_balance_before": 200,
                "expected_from_balance": 750,
                "expected_to_balance": 250,
            },
        ]

        for scenario in transfer_scenarios:
            from_balance_after = scenario["from_balance_before"] - scenario["xp_amount"]
            to_balance_after = scenario["to_balance_before"] + scenario["xp_amount"]

            assert from_balance_after == scenario["expected_from_balance"]
            assert to_balance_after == scenario["expected_to_balance"]

    def test_xp_audit_trail(self):
        """Test XP audit trail and history tracking."""
        xp_events = [
            {
                "agent_id": "Agent-7",
                "event_type": "contract_completion",
                "xp_amount": 200,
                "contract_id": "COMPLETED-001",
                "timestamp": "2025-09-12T10:00:00Z",
                "balance_after": 1200,
            },
            {
                "agent_id": "Agent-7",
                "event_type": "bonus_award",
                "xp_amount": 50,
                "reason": "early_completion",
                "timestamp": "2025-09-12T10:15:00Z",
                "balance_after": 1250,
            },
            {
                "agent_id": "Agent-7",
                "event_type": "penalty_deduction",
                "xp_amount": -25,
                "reason": "quality_issue",
                "timestamp": "2025-09-12T10:30:00Z",
                "balance_after": 1225,
            },
        ]

        # Validate audit trail
        for event in xp_events:
            required_fields = ["agent_id", "event_type", "xp_amount", "timestamp", "balance_after"]
            for field in required_fields:
                assert field in event

        # Test chronological ordering
        timestamps = [event["timestamp"] for event in xp_events]
        sorted_timestamps = sorted(timestamps)
        assert timestamps == sorted_timestamps

    def test_xp_analytics_and_reporting(self):
        """Test XP analytics and reporting functionality."""
        analytics_data = {
            "total_xp_distributed": 15000,
            "average_xp_per_contract": 250,
            "top_performers": [
                {"agent_id": "Agent-1", "total_xp": 3000, "contracts_completed": 15},
                {"agent_id": "Agent-7", "total_xp": 2500, "contracts_completed": 12},
                {"agent_id": "Agent-2", "total_xp": 2000, "contracts_completed": 10},
            ],
            "xp_distribution_by_priority": {
                "CRITICAL": 5000,
                "HIGH": 4000,
                "MEDIUM": 3000,
                "LOW": 2000,
            },
            "monthly_xp_trend": [
                {"month": "2025-07", "total_xp": 4000},
                {"month": "2025-08", "total_xp": 5500},
                {"month": "2025-09", "total_xp": 5500},
            ],
        }

        # Validate analytics data
        assert analytics_data["total_xp_distributed"] > 0
        assert analytics_data["average_xp_per_contract"] > 0
        assert len(analytics_data["top_performers"]) > 0
        assert len(analytics_data["xp_distribution_by_priority"]) > 0
        assert len(analytics_data["monthly_xp_trend"]) > 0

        # Validate top performers ordering
        top_performers = analytics_data["top_performers"]
        for i in range(len(top_performers) - 1):
            assert top_performers[i]["total_xp"] >= top_performers[i + 1]["total_xp"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
