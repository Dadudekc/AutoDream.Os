#!/usr/bin/env python3
"""Swarm Decision Management System"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from .swarm_communication_enums import (
    SwarmDecision, SwarmDecisionType, DecisionStatus, SwarmCommunicationMetrics
)

logger = logging.getLogger(__name__)


class SwarmDecisionManager:
    """Manages swarm decisions and democratic voting process"""
    
    def __init__(self, voting_timeout_hours: int = 24):
        self.decisions: Dict[str, SwarmDecision] = {}
        self.voting_timeout_hours = voting_timeout_hours
        self.metrics = SwarmCommunicationMetrics()
        logger.info("Swarm Decision Manager initialized")
    
    def create_decision(
        self,
        decision_type: SwarmDecisionType,
        description: str,
        proposer: str,
        deadline_hours: Optional[int] = None
    ) -> SwarmDecision:
        """Create a new swarm decision"""
        decision_id = f"decision_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{decision_type.value}"
        
        deadline = None
        if deadline_hours:
            deadline = datetime.now() + timedelta(hours=deadline_hours)
        
        decision = SwarmDecision(
            decision_id=decision_id,
            decision_type=decision_type,
            description=description,
            proposer=proposer,
            deadline=deadline
        )
        
        self.decisions[decision_id] = decision
        self.metrics.total_decisions += 1
        self.metrics.pending_decisions += 1
        
        logger.info(f"Created decision {decision_id} by {proposer}")
        return decision
    
    def vote_on_decision(self, decision_id: str, agent_id: str, vote: bool) -> bool:
        """Vote on a decision"""
        if decision_id not in self.decisions:
            logger.error(f"Decision {decision_id} not found")
            return False
        
        decision = self.decisions[decision_id]
        
        if decision.status != DecisionStatus.PENDING:
            logger.warning(f"Decision {decision_id} is not in pending status")
            return False
        
        # Start voting if this is the first vote
        if decision.status == DecisionStatus.PENDING:
            decision.status = DecisionStatus.VOTING
        
        decision.votes[agent_id] = vote
        logger.info(f"Agent {agent_id} voted {vote} on decision {decision_id}")
        
        # Check if decision should be finalized
        self._check_decision_finalization(decision_id)
        return True
    
    def _check_decision_finalization(self, decision_id: str) -> None:
        """Check if a decision should be finalized based on votes or deadline"""
        decision = self.decisions[decision_id]
        
        # Check deadline
        if decision.deadline and datetime.now() > decision.deadline:
            self._finalize_decision(decision_id, timeout=True)
            return
        
        # Check if we have enough votes (simple majority for now)
        total_votes = len(decision.votes)
        if total_votes >= 5:  # Majority of 8 agents
            yes_votes = sum(1 for vote in decision.votes.values() if vote)
            no_votes = total_votes - yes_votes
            
            if yes_votes > no_votes:
                decision.status = DecisionStatus.APPROVED
                self.metrics.approved_decisions += 1
                logger.info(f"Decision {decision_id} APPROVED ({yes_votes} yes, {no_votes} no)")
            else:
                decision.status = DecisionStatus.REJECTED
                self.metrics.rejected_decisions += 1
                logger.info(f"Decision {decision_id} REJECTED ({yes_votes} yes, {no_votes} no)")
            
            self.metrics.pending_decisions -= 1
    
    def _finalize_decision(self, decision_id: str, timeout: bool = False) -> None:
        """Finalize a decision (either by timeout or completion)"""
        decision = self.decisions[decision_id]
        
        if timeout:
            decision.status = DecisionStatus.REJECTED
            decision.implementation_notes = "Decision rejected due to timeout"
            self.metrics.rejected_decisions += 1
            logger.warning(f"Decision {decision_id} rejected due to timeout")
        else:
            decision.status = DecisionStatus.IMPLEMENTED
            decision.implementation_notes = "Decision implemented successfully"
            logger.info(f"Decision {decision_id} implemented successfully")
        
        if decision.status in [DecisionStatus.APPROVED, DecisionStatus.REJECTED]:
            self.metrics.pending_decisions -= 1
    
    def get_decision(self, decision_id: str) -> Optional[SwarmDecision]:
        """Get a decision by ID"""
        return self.decisions.get(decision_id)
    
    def get_decisions_by_status(self, status: DecisionStatus) -> List[SwarmDecision]:
        """Get all decisions with a specific status"""
        return [decision for decision in self.decisions.values() if decision.status == status]
    
    def get_pending_decisions(self) -> List[SwarmDecision]:
        """Get all pending decisions"""
        return self.get_decisions_by_status(DecisionStatus.PENDING)
    
    def get_voting_decisions(self) -> List[SwarmDecision]:
        """Get all decisions currently being voted on"""
        return self.get_decisions_by_status(DecisionStatus.VOTING)
    
    def get_decision_summary(self) -> Dict[str, any]:
        """Get a summary of all decisions"""
        return {
            "total_decisions": len(self.decisions),
            "pending_decisions": len(self.get_pending_decisions()),
            "voting_decisions": len(self.get_voting_decisions()),
            "approved_decisions": len(self.get_decisions_by_status(DecisionStatus.APPROVED)),
            "rejected_decisions": len(self.get_decisions_by_status(DecisionStatus.REJECTED)),
            "implemented_decisions": len(self.get_decisions_by_status(DecisionStatus.IMPLEMENTED))
        }
    
    def cleanup_old_decisions(self, days_old: int = 30) -> int:
        """Clean up decisions older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        old_decisions = [
            decision_id for decision_id, decision in self.decisions.items()
            if decision.created_at < cutoff_date
        ]
        
        for decision_id in old_decisions:
            del self.decisions[decision_id]
        
        logger.info(f"Cleaned up {len(old_decisions)} old decisions")
        return len(old_decisions)
    
    def get_metrics(self) -> SwarmCommunicationMetrics:
        """Get current metrics"""
        self.metrics.last_updated = datetime.now()
        return self.metrics



