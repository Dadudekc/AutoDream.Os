#!/usr/bin/env python3
"""Status enums for decision coordination system."""

from enum import Enum


class CoordinationMode(Enum):
    """Decision coordination modes."""

    CONSENSUS = "consensus"
    MAJORITY = "majority"
    EXPERT_OPINION = "expert_opinion"
    HIERARCHICAL = "hierarchical"
    COLLABORATIVE = "collaborative"


class CoordinationStatus(Enum):
    """Status values for coordination sessions."""

    ACTIVE = "active"
    GATHERING_INPUTS = "gathering_inputs"
    INPUTS_GATHERED = "inputs_gathered"
    DELIBERATING = "deliberating"
    DELIBERATION_COMPLETE = "deliberation_complete"
    BUILDING_CONSENSUS = "building_consensus"
    CONSENSUS_REACHED = "consensus_reached"
    CONSENSUS_FAILED = "consensus_failed"
    FINALIZING = "finalizing"
    NO_CONSENSUS = "no_consensus"
    RETRYING = "retrying"
    FAILED = "failed"
    COMPLETED = "completed"
