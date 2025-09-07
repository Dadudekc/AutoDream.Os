#!/usr/bin/env python3
"""
Captain Contract Instruction Service - Agent Cellphone V2
=======================================================

Instructs the Captain to create specific, meaningful contracts when agents complete work.
This creates a perpetual motion system where the Captain is prompted to create new contracts.
"""

import json
import time
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
log = logging.getLogger("captain_contract_instruction_service")


@dataclass
class ContractCompletion:
    """Contract completion event"""

    contract_id: str
    agent_id: str
    completion_time: str
    quality_score: float
    actual_effort: str
    notes: str = ""


@dataclass
class CaptainInstruction:
    """Instruction for Captain to create new contracts"""

    instruction_id: str
    agent_id: str
    completed_contract: str
    instruction_type: str
    priority: str
    suggested_contracts: List[Dict[str, str]]
    reasoning: str
    created_time: str


class CaptainContractInstructionService:
    """Service that instructs the Captain to create new contracts"""

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[3]
        self.contract_pool_file = self.project_root / "contracts" / "contract_pool.json"
        self.completion_log_file = (
            self.project_root / "contracts" / "completion_log.json"
        )
        self.captain_inbox_file = (
            self.project_root
            / "agent_workspaces"
            / "Captain-5"
            / "inbox"
            / "contract_instructions.json"
        )

        # Ensure Captain inbox directory exists
        self.captain_inbox_file.parent.mkdir(parents=True, exist_ok=True)

        # Load existing data
        self.contract_pool = self._load_contract_pool()
        self.completion_log = self._load_completion_log()

        log.info("Captain Contract Instruction Service initialized")

    def _load_contract_pool(self) -> Dict[str, Any]:
        """Load contract pool from file"""
        try:
            if self.contract_pool_file.exists():
                with open(self.contract_pool_file, "r") as f:
                    return json.load(f)
            return {"contract_pool": {}, "contract_stats": {}}
        except Exception as e:
            log.error(f"Error loading contract pool: {e}")
            return {"contract_pool": {}, "contract_stats": {}}

    def _load_completion_log(self) -> List[ContractCompletion]:
        """Load completion log from file"""
        try:
            if self.completion_log_file.exists():
                with open(self.completion_log_file, "r") as f:
                    data = json.load(f)
                    return [
                        ContractCompletion(**item)
                        for item in data.get("completions", [])
                    ]
            return []
        except Exception as e:
            log.error(f"Error loading completion log: {e}")
            return []

    def _save_captain_instruction(self, instruction: CaptainInstruction):
        """Save instruction to Captain's inbox"""
        try:
            # Ensure Captain inbox directory exists
            self.captain_inbox_file.parent.mkdir(parents=True, exist_ok=True)

            # Load existing instructions
            instructions = []
            if self.captain_inbox_file.exists():
                with open(self.captain_inbox_file, "r") as f:
                    data = json.load(f)
                    instructions = data.get("instructions", [])

            # Add new instruction
            instructions.append(asdict(instruction))

            # Save updated instructions
            with open(self.captain_inbox_file, "w") as f:
                json.dump({"instructions": instructions}, f, indent=2)

            log.info(f"Captain instruction saved: {instruction.instruction_id}")

        except Exception as e:
            log.error(f"Error saving captain instruction: {e}")

    def process_contract_completion(
        self,
        contract_id: str,
        agent_id: str,
        quality_score: float = 100.0,
        actual_effort: str = "",
        notes: str = "",
    ) -> bool:
        """Process contract completion and create Captain instruction"""
        try:
            log.info(f"Processing completion of contract {contract_id} by {agent_id}")

            # Create completion record
            completion = ContractCompletion(
                contract_id=contract_id,
                agent_id=agent_id,
                completion_time=datetime.now().isoformat(),
                quality_score=quality_score,
                actual_effort=actual_effort,
                notes=notes,
            )

            # Add to completion log
            self.completion_log.append(completion)
            self._save_completion_log()

            # Create Captain instruction
            instruction = self._create_captain_instruction(completion)
            self._save_captain_instruction(instruction)

            log.info(f"Captain instruction created for {agent_id} completion")
            return True

        except Exception as e:
            log.error(f"Error processing contract completion: {e}")
            return False

    def _create_captain_instruction(
        self, completion: ContractCompletion
    ) -> CaptainInstruction:
        """Create instruction for Captain to create new contracts"""
        try:
            # Generate instruction ID
            instruction_id = f"INSTRUCTION-{int(time.time())}"

            # Determine instruction type based on agent and contract
            instruction_type = self._determine_instruction_type(
                completion.agent_id, completion.contract_id
            )

            # Determine priority based on quality score and agent
            priority = self._determine_priority(
                completion.quality_score, completion.agent_id
            )

            # Generate suggested contracts based on completion
            suggested_contracts = self._generate_suggested_contracts(completion)

            # Create reasoning for the instruction
            reasoning = self._create_reasoning(completion, instruction_type)

            instruction = CaptainInstruction(
                instruction_id=instruction_id,
                agent_id=completion.agent_id,
                completed_contract=completion.contract_id,
                instruction_type=instruction_type,
                priority=priority,
                suggested_contracts=suggested_contracts,
                reasoning=reasoning,
                created_time=datetime.now().isoformat(),
            )

            return instruction

        except Exception as e:
            log.error(f"Error creating captain instruction: {e}")
            # Return default instruction
            return CaptainInstruction(
                instruction_id=f"INSTRUCTION-{int(time.time())}",
                agent_id=completion.agent_id,
                completed_contract=completion.contract_id,
                instruction_type="GENERAL",
                priority="MEDIUM",
                suggested_contracts=[],
                reasoning="Default instruction due to error",
                created_time=datetime.now().isoformat(),
            )

    def _determine_instruction_type(self, agent_id: str, contract_id: str) -> str:
        """Determine the type of instruction based on agent and contract"""
        try:
            # Get contract details
            contract_details = self._get_contract_details(contract_id)
            if not contract_details:
                return "GENERAL"

            category = contract_details.get("category", "general")

            # Map categories to instruction types
            category_mapping = {
                "standards_enforcement": "STANDARDS_IMPROVEMENT",
                "quality_assurance": "QUALITY_ENHANCEMENT",
                "integration_and_ecosystem": "INTEGRATION_EXPANSION",
                "documentation_and_tracking": "DOCUMENTATION_EXTENSION",
                "performance_optimization": "PERFORMANCE_SCALING",
                "security": "SECURITY_STRENGTHENING",
                "automation": "AUTOMATION_ADVANCEMENT",
                "monitoring": "MONITORING_ENHANCEMENT",
                "innovation": "INNOVATION_DEVELOPMENT",
                "scalability": "SCALABILITY_IMPROVEMENT",
            }

            return category_mapping.get(category, "GENERAL")

        except Exception as e:
            log.error(f"Error determining instruction type: {e}")
            return "GENERAL"

    def _determine_priority(self, quality_score: float, agent_id: str) -> str:
        """Determine priority based on quality score and agent"""
        try:
            if quality_score >= 95:
                return "HIGH"  # Excellent work, create challenging contracts
            elif quality_score >= 85:
                return "MEDIUM"  # Good work, create balanced contracts
            else:
                return "LOW"  # Needs improvement, create supportive contracts

        except Exception as e:
            log.error(f"Error determining priority: {e}")
            return "MEDIUM"

    def _generate_suggested_contracts(
        self, completion: ContractCompletion
    ) -> List[Dict[str, str]]:
        """Generate suggested contracts for the Captain to create"""
        try:
            contract_details = self._get_contract_details(completion.contract_id)
            if not contract_details:
                return []

            category = contract_details.get("category", "general")
            agent_id = completion.agent_id

            # Generate suggestions based on category and agent
            suggestions = []

            if category == "standards_enforcement":
                suggestions.extend(
                    [
                        {
                            "title": f"Enhanced {agent_id} Standards Compliance",
                            "description": f"Build upon {agent_id}'s successful standards work with advanced compliance features",
                            "estimated_effort": "3-4 hours",
                            "category": "standards_enforcement",
                        },
                        {
                            "title": f"{agent_id} Standards Automation",
                            "description": f"Automate standards checking processes based on {agent_id}'s expertise",
                            "estimated_effort": "4-5 hours",
                            "category": "automation",
                        },
                    ]
                )

            elif category == "quality_assurance":
                suggestions.extend(
                    [
                        {
                            "title": f"{agent_id} Quality Framework Extension",
                            "description": f"Extend the quality framework based on {agent_id}'s successful implementation",
                            "estimated_effort": "3-4 hours",
                            "category": "quality_assurance",
                        },
                        {
                            "title": f"{agent_id} Quality Metrics Dashboard",
                            "description": f"Create comprehensive quality metrics dashboard leveraging {agent_id}'s QA expertise",
                            "estimated_effort": "4-5 hours",
                            "category": "monitoring",
                        },
                    ]
                )

            elif category == "integration_and_ecosystem":
                suggestions.extend(
                    [
                        {
                            "title": f"{agent_id} Ecosystem Integration",
                            "description": f"Expand ecosystem integration based on {agent_id}'s successful work",
                            "estimated_effort": "4-6 hours",
                            "category": "integration_and_ecosystem",
                        },
                        {
                            "title": f"{agent_id} External API Development",
                            "description": f"Develop external APIs leveraging {agent_id}'s integration experience",
                            "estimated_effort": "5-6 hours",
                            "category": "integration_advanced",
                        },
                    ]
                )

            elif category == "documentation_and_tracking":
                suggestions.extend(
                    [
                        {
                            "title": f"{agent_id} Documentation Standards",
                            "description": f"Establish comprehensive documentation standards based on {agent_id}'s work",
                            "estimated_effort": "3-4 hours",
                            "category": "documentation",
                        },
                        {
                            "title": f"{agent_id} Knowledge Base Creation",
                            "description": f"Create knowledge base leveraging {agent_id}'s documentation expertise",
                            "estimated_effort": "4-5 hours",
                            "category": "documentation",
                        },
                    ]
                )

            else:
                # Generic suggestions for other categories
                suggestions.extend(
                    [
                        {
                            "title": f"{agent_id} Advanced {category.title()}",
                            "description": f"Build upon {agent_id}'s successful {category} work with advanced features",
                            "estimated_effort": "3-5 hours",
                            "category": category,
                        },
                        {
                            "title": f"{agent_id} {category.title()} Innovation",
                            "description": f"Develop innovative solutions in {category} based on {agent_id}'s expertise",
                            "estimated_effort": "4-6 hours",
                            "category": "innovation",
                        },
                    ]
                )

            return suggestions

        except Exception as e:
            log.error(f"Error generating suggested contracts: {e}")
            return []

    def _create_reasoning(
        self, completion: ContractCompletion, instruction_type: str
    ) -> str:
        """Create reasoning for why the Captain should create new contracts"""
        try:
            agent_id = completion.agent_id
            quality_score = completion.quality_score
            actual_effort = completion.actual_effort

            reasoning = f"Agent {agent_id} has successfully completed a contract with a quality score of {quality_score}/100 "
            reasoning += f"in {actual_effort}. "

            if quality_score >= 95:
                reasoning += f"This exceptional performance demonstrates {agent_id}'s expertise and readiness for more challenging work. "
                reasoning += f"Creating new contracts will capitalize on this momentum and push {agent_id} to even greater achievements."
            elif quality_score >= 85:
                reasoning += f"This solid performance shows {agent_id} is ready to expand their capabilities. "
                reasoning += f"New contracts will help {agent_id} grow while maintaining quality standards."
            else:
                reasoning += f"While there's room for improvement, {agent_id} has completed the work and is ready for the next challenge. "
                reasoning += f"New contracts will provide opportunities for {agent_id} to enhance their skills and quality."

            reasoning += f" The {instruction_type.lower().replace('_', ' ')} instruction type suggests focusing on areas where {agent_id} "
            reasoning += f"has demonstrated competence, ensuring continued success and team momentum toward our 50-contract goal."

            return reasoning

        except Exception as e:
            log.error(f"Error creating reasoning: {e}")
            return f"Agent {completion.agent_id} completed a contract and is ready for new challenges."

    def _get_contract_details(self, contract_id: str) -> Optional[Dict[str, Any]]:
        """Get contract details from pool"""
        try:
            for category, contracts in self.contract_pool.get(
                "contract_pool", {}
            ).items():
                for contract in contracts:
                    if contract.get("contract_id") == contract_id:
                        return contract
            return None

        except Exception as e:
            log.error(f"Error getting contract details: {e}")
            return None

    def _save_completion_log(self):
        """Save completion log to file"""
        try:
            data = {
                "completions": [
                    asdict(completion) for completion in self.completion_log
                ]
            }
            with open(self.completion_log_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            log.error(f"Error saving completion log: {e}")

    def get_captain_instructions(self) -> List[CaptainInstruction]:
        """Get all pending instructions for the Captain"""
        try:
            if not self.captain_inbox_file.exists():
                return []

            with open(self.captain_inbox_file, "r") as f:
                data = json.load(f)
                instructions = data.get("instructions", [])
                return [CaptainInstruction(**item) for item in instructions]

        except Exception as e:
            log.error(f"Error getting captain instructions: {e}")
            return []

    def get_completion_summary(self) -> Dict[str, Any]:
        """Get summary of contract completions"""
        try:
            total_completions = len(self.completion_log)
            today_completions = len(
                [
                    c
                    for c in self.completion_log
                    if c.completion_time.startswith(datetime.now().date().isoformat())
                ]
            )

            agent_completions = {}
            for completion in self.completion_log:
                agent_id = completion.agent_id
                if agent_id not in agent_completions:
                    agent_completions[agent_id] = 0
                agent_completions[agent_id] += 1

            return {
                "total_completions": total_completions,
                "today_completions": today_completions,
                "agent_completions": agent_completions,
                "completion_rate": f"{(total_completions/50*100):.1f}%"
                if total_completions > 0
                else "0%",
            }

        except Exception as e:
            log.error(f"Error getting completion summary: {e}")
            return {}


def main():
    """CLI interface for Captain Contract Instruction Service"""
    import argparse

    parser = argparse.ArgumentParser(description="Captain Contract Instruction Service")
    parser.add_argument(
        "--complete",
        nargs=4,
        metavar=("CONTRACT_ID", "AGENT_ID", "QUALITY_SCORE", "EFFORT"),
        help="Process contract completion and create Captain instruction",
    )
    parser.add_argument(
        "--instructions", action="store_true", help="Show pending Captain instructions"
    )
    parser.add_argument("--status", action="store_true", help="Show completion status")

    args = parser.parse_args()

    service = CaptainContractInstructionService()

    if args.complete:
        contract_id, agent_id, quality_score, effort = args.complete
        success = service.process_contract_completion(
            contract_id, agent_id, float(quality_score), effort
        )
        if success:
            print(
                f"✅ Contract completion processed and Captain instruction created for {agent_id}"
            )
        else:
            print(f"❌ Failed to process contract completion for {agent_id}")

    elif args.instructions:
        instructions = service.get_captain_instructions()
        if instructions:
            print(f"📋 Pending Captain Instructions ({len(instructions)}):")
            for instruction in instructions:
                print(f"\n🔑 {instruction.instruction_id}")
                print(f"   Agent: {instruction.agent_id}")
                print(f"   Type: {instruction.instruction_type}")
                print(f"   Priority: {instruction.priority}")
                print(f"   Completed: {instruction.completed_contract}")
                print(
                    f"   Suggestions: {len(instruction.suggested_contracts)} contracts"
                )
        else:
            print("📋 No pending Captain instructions")

    elif args.status:
        summary = service.get_completion_summary()
        print(json.dumps(summary, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
