#!/usr/bin/env python3
"""
Contract Management System - Agent Cellphone V2
==============================================

Comprehensive system for agents to manage contracts from CLI with automated
validation, status updates, and guardrails to ensure contract compliance.

Author: Agent-4 (Captain)
Purpose: Automated contract management with validation
"""

import json
import logging
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    """Task status enumeration"""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW_NEEDED = "REVIEW_NEEDED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BOUNCED_BACK = "BOUNCED_BACK"

class ValidationLevel(Enum):
    """Validation level enumeration"""
    BASIC = "BASIC"
    STANDARD = "STANDARD"
    STRICT = "STRICT"

@dataclass
class ContractRequirement:
    """Individual contract requirement"""
    requirement_id: str
    description: str
    required: bool
    completed: bool = False
    validation_notes: str = ""
    completion_timestamp: Optional[str] = None

@dataclass
class ContractValidation:
    """Contract validation result"""
    is_valid: bool
    missing_requirements: List[str]
    validation_errors: List[str]
    warnings: List[str]
    score: float  # 0.0 to 1.0
    timestamp: str

@dataclass
class ContractStatus:
    """Contract status information"""
    contract_id: str
    agent_id: str
    current_status: TaskStatus
    progress_percentage: float
    last_updated: str
    requirements_completed: int
    total_requirements: int
    validation_result: Optional[ContractValidation] = None

class ContractManager:
    """Main contract management system"""
    
    def __init__(self, contracts_dir: str = "logs"):
        self.contracts_dir = Path(contracts_dir)
        self.contracts_dir.mkdir(exist_ok=True)
        self.status_file = self.contracts_dir / "contract_statuses.json"
        self.contract_statuses: Dict[str, ContractStatus] = {}
        self.load_statuses()
    
    def load_statuses(self):
        """Load existing contract statuses"""
        if self.status_file.exists():
            try:
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for contract_id, status_data in data.items():
                        # Convert string status back to TaskStatus enum
                        if 'current_status' in status_data:
                            try:
                                status_data['current_status'] = TaskStatus(status_data['current_status'])
                            except ValueError:
                                # Fallback to PENDING if status is invalid
                                status_data['current_status'] = TaskStatus.PENDING
                        
                        # Convert back to ContractStatus object
                        validation_data = status_data.get('validation_result')
                        if validation_data:
                            validation = ContractValidation(**validation_data)
                            status_data['validation_result'] = validation
                        self.contract_statuses[contract_id] = ContractStatus(**status_data)
            except Exception as e:
                logger.error(f"Error loading contract statuses: {e}")
                self.contract_statuses = {}
    
    def save_statuses(self):
        """Save contract statuses to file"""
        try:
            data = {}
            for contract_id, status in self.contract_statuses.items():
                status_dict = asdict(status)
                # Convert TaskStatus enum to string for JSON serialization
                status_dict['current_status'] = status.current_status.value
                data[contract_id] = status_dict
            
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving contract statuses: {e}")
    
    def get_contract_requirements(self, contract_file: Path) -> List[ContractRequirement]:
        """Extract requirements from contract file"""
        requirements = []
        
        try:
            with open(contract_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse contract content to extract requirements
            lines = content.split('\n')
            in_requirements = False
            
            for line in lines:
                if "## 📋 **DELIVERABLES REQUIRED**" in line:
                    in_requirements = True
                    continue
                
                if in_requirements and line.startswith("### **"):
                    if "Task Completion" in line:
                        requirements.append(ContractRequirement(
                            requirement_id="task_completion",
                            description="Complete the specific task based on current status",
                            required=True
                        ))
                    elif "Progress Documentation" in line:
                        requirements.append(ContractRequirement(
                            requirement_id="progress_documentation",
                            description="Document current progress and completion",
                            required=True
                        ))
                    elif "Integration Verification" in line:
                        requirements.append(ContractRequirement(
                            requirement_id="integration_verification",
                            description="Verify integration with existing completed systems",
                            required=True
                        ))
                
                if in_requirements and line.startswith("---"):
                    break
            
            # Add standard requirements if none found
            if not requirements:
                requirements = [
                    ContractRequirement(
                        requirement_id="task_completion",
                        description="Complete the specified task",
                        required=True
                    ),
                    ContractRequirement(
                        requirement_id="progress_documentation",
                        description="Document current progress and completion",
                        required=True
                    ),
                    ContractRequirement(
                        requirement_id="integration_verification",
                        description="Verify system integration",
                        required=True
                    )
                ]
                
        except Exception as e:
            logger.error(f"Error parsing contract requirements: {e}")
            # Fallback to standard requirements
            requirements = [
                ContractRequirement(
                    requirement_id="task_completion",
                    description="Complete the specified task",
                    required=True
                ),
                ContractRequirement(
                    requirement_id="progress_documentation",
                    description="Document current progress and completion",
                        required=True
                ),
                ContractRequirement(
                    requirement_id="integration_verification",
                    description="Verify system integration",
                    required=True
                )
            ]
        
        return requirements
    
    def validate_contract_completion(self, contract_id: str, validation_level: ValidationLevel = ValidationLevel.STANDARD) -> ContractValidation:
        """Validate contract completion based on requirements"""
        if contract_id not in self.contract_statuses:
            return ContractValidation(
                is_valid=False,
                missing_requirements=["Contract not found"],
                validation_errors=["Contract ID not found in system"],
                warnings=[],
                score=0.0,
                timestamp=datetime.now().isoformat()
            )
        
        status = self.contract_statuses[contract_id]
        missing_requirements = []
        validation_errors = []
        warnings = []
        
        # Check if contract file exists
        contract_file = self.contracts_dir / f"contracts_{status.agent_id.lower().replace('-', '_')}" / f"{contract_id.lower()}.md"
        
        if not contract_file.exists():
            validation_errors.append(f"Contract file not found: {contract_file}")
            return ContractValidation(
                is_valid=False,
                missing_requirements=["Contract file missing"],
                validation_errors=validation_errors,
                warnings=warnings,
                score=0.0,
                timestamp=datetime.now().isoformat()
            )
        
        # Get requirements and validate
        requirements = self.get_contract_requirements(contract_file)
        completed_count = 0
        total_count = len(requirements)
        
        for req in requirements:
            if not req.completed:
                missing_requirements.append(req.description)
            else:
                completed_count += 1
        
        # Calculate score
        score = completed_count / total_count if total_count > 0 else 0.0
        
        # Additional validation based on level
        if validation_level == ValidationLevel.STRICT:
            # Check for devlog entry
            devlog_dir = self.contracts_dir.parent / "logs"
            devlog_files = list(devlog_dir.glob(f"*{contract_id}*"))
            if not devlog_files:
                validation_errors.append("Devlog entry not found")
                score = max(0.0, score - 0.2)
            
            # Check for completion timestamp
            if not any(req.completion_timestamp for req in requirements if req.completed):
                warnings.append("Some requirements lack completion timestamps")
        
        # Determine if valid
        is_valid = score >= 0.8 and not validation_errors
        
        # Update status
        status.progress_percentage = score * 100
        status.requirements_completed = completed_count
        status.total_requirements = total_count
        status.validation_result = ContractValidation(
            is_valid=is_valid,
            missing_requirements=missing_requirements,
            validation_errors=validation_errors,
            warnings=warnings,
            score=score,
            timestamp=datetime.now().isoformat()
        )
        
        # Auto-update status based on validation
        if is_valid and score >= 0.95:
            status.current_status = TaskStatus.COMPLETED
        elif score >= 0.6:
            status.current_status = TaskStatus.IN_PROGRESS
        elif validation_errors:
            status.current_status = TaskStatus.BOUNCED_BACK
        else:
            status.current_status = TaskStatus.REVIEW_NEEDED
        
        status.last_updated = datetime.now().isoformat()
        self.save_statuses()
        
        return status.validation_result
    
    def update_requirement_status(self, contract_id: str, requirement_id: str, completed: bool, notes: str = "") -> bool:
        """Update individual requirement status"""
        if contract_id not in self.contract_statuses:
            logger.error(f"Contract {contract_id} not found")
            return False
        
        status = self.contract_statuses[contract_id]
        contract_file = self.contracts_dir / f"contracts_{status.agent_id.lower().replace('-', '_')}" / f"{contract_id.lower()}.md"
        
        if not contract_file.exists():
            logger.error(f"Contract file not found: {contract_file}")
            return False
        
        # Update requirements
        requirements = self.get_contract_requirements(contract_file)
        requirement_updated = False
        
        for req in requirements:
            if req.requirement_id == requirement_id:
                req.completed = completed
                req.validation_notes = notes
                if completed:
                    req.completion_timestamp = datetime.now().isoformat()
                requirement_updated = True
                break
        
        if not requirement_updated:
            logger.error(f"Requirement {requirement_id} not found in contract {contract_id}")
            return False
        
        # Re-validate contract
        self.validate_contract_completion(contract_id)
        return True
    
    def get_agent_contracts(self, agent_id: str) -> List[ContractStatus]:
        """Get all contracts for a specific agent"""
        return [status for status in self.contract_statuses.values() if status.agent_id == agent_id]
    
    def create_contract_status(self, contract_id: str, agent_id: str, contract_file: Path) -> ContractStatus:
        """Create new contract status"""
        requirements = self.get_contract_requirements(contract_file)
        
        status = ContractStatus(
            contract_id=contract_id,
            agent_id=agent_id,
            current_status=TaskStatus.PENDING,
            progress_percentage=0.0,
            last_updated=datetime.now().isoformat(),
            requirements_completed=0,
            total_requirements=len(requirements)
        )
        
        self.contract_statuses[contract_id] = status
        self.save_statuses()
        return status
    
    def auto_discover_contracts(self):
        """Automatically discover and register new contracts"""
        for agent_dir in self.contracts_dir.glob("contracts_agent_*"):
            agent_id = agent_dir.name.replace("contracts_", "").replace("_", "-").upper()
            
            for contract_file in agent_dir.glob("*.md"):
                contract_id = contract_file.stem.upper()
                
                if contract_id not in self.contract_statuses:
                    logger.info(f"Auto-discovered new contract: {contract_id} for {agent_id}")
                    self.create_contract_status(contract_id, agent_id, contract_file)

class ContractCLI:
    """CLI interface for contract management"""
    
    def __init__(self):
        self.manager = ContractManager()
        self.manager.auto_discover_contracts()
    
    def show_help(self):
        """Show CLI help"""
        help_text = """
🎯 CONTRACT MANAGEMENT CLI - Agent Cellphone V2

USAGE:
  python contract_cli.py [COMMAND] [OPTIONS]

COMMANDS:
  list [agent_id]           - List all contracts or contracts for specific agent
  status <contract_id>      - Show detailed status of specific contract
  update <contract_id> <requirement_id> <completed> [notes] - Update requirement status
  validate <contract_id>    - Validate contract completion
  complete <contract_id>    - Mark contract as completed
  progress <contract_id>    - Show progress of specific contract
  bounce <contract_id>      - Bounce contract back for review
  help                     - Show this help message

EXAMPLES:
  python contract_cli.py list
  python contract_cli.py list agent-1
  python contract_cli.py status TASK_1B
  python contract_cli.py update TASK_1B task_completion true "Task completed successfully"
  python contract_cli.py validate TASK_1B
  python contract_cli.py complete TASK_1B
  python contract_cli.py progress TASK_1B
  python contract_cli.py bounce TASK_1B

REQUIREMENT IDs:
  - task_completion: Complete the specific task
  - progress_documentation: Document progress and completion
  - integration_verification: Verify system integration
  - devlog_entry: Create devlog entry
  - architecture_compliance: Ensure V2 standards compliance

STATUS VALUES:
  - true/false: For requirement completion
  - 1/0: Alternative for requirement completion
"""
        print(help_text)
    
    def list_contracts(self, agent_id: Optional[str] = None):
        """List contracts"""
        if agent_id:
            contracts = self.manager.get_agent_contracts(agent_id.upper())
            print(f"\n📋 CONTRACTS FOR {agent_id.upper()}:")
        else:
            contracts = list(self.manager.contract_statuses.values())
            print(f"\n📋 ALL CONTRACTS ({len(contracts)} total):")
        
        if not contracts:
            print("No contracts found.")
            return
        
        for contract in contracts:
            status_emoji = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.IN_PROGRESS: "🔄",
                TaskStatus.REVIEW_NEEDED: "🔍",
                TaskStatus.COMPLETED: "✅",
                TaskStatus.FAILED: "❌",
                TaskStatus.BOUNCED_BACK: "🚨"
            }
            
            emoji = status_emoji.get(contract.current_status, "❓")
            print(f"{emoji} {contract.contract_id}: {contract.current_status.value}")
            print(f"   Progress: {contract.progress_percentage:.1f}% ({contract.requirements_completed}/{contract.total_requirements})")
            print(f"   Agent: {contract.agent_id}")
            print(f"   Last Updated: {contract.last_updated}")
            if contract.validation_result:
                print(f"   Validation: {'✅ Valid' if contract.validation_result.is_valid else '❌ Invalid'} (Score: {contract.validation_result.score:.2f})")
            print()
    
    def show_status(self, contract_id: str):
        """Show detailed contract status"""
        if contract_id not in self.manager.contract_statuses:
            print(f"❌ Contract {contract_id} not found")
            return
        
        status = self.manager.contract_statuses[contract_id]
        print(f"\n🎯 CONTRACT STATUS: {contract_id}")
        print(f"Agent: {status.agent_id}")
        print(f"Status: {status.current_status.value}")
        print(f"Progress: {status.progress_percentage:.1f}% ({status.requirements_completed}/{status.total_requirements})")
        print(f"Last Updated: {status.last_updated}")
        
        if status.validation_result:
            print(f"\n📊 VALIDATION RESULTS:")
            print(f"Valid: {'✅ Yes' if status.validation_result.is_valid else '❌ No'}")
            print(f"Score: {status.validation_result.score:.2f}")
            
            if status.validation_result.missing_requirements:
                print(f"\n❌ MISSING REQUIREMENTS:")
                for req in status.validation_result.missing_requirements:
                    print(f"  - {req}")
            
            if status.validation_result.validation_errors:
                print(f"\n🚨 VALIDATION ERRORS:")
                for error in status.validation_result.validation_errors:
                    print(f"  - {error}")
            
            if status.validation_result.warnings:
                print(f"\n⚠️  WARNINGS:")
                for warning in status.validation_result.warnings:
                    print(f"  - {warning}")
    
    def update_requirement(self, contract_id: str, requirement_id: str, completed: str, notes: str = ""):
        """Update requirement status"""
        # Parse completion status
        if completed.lower() in ['true', '1', 'yes', 'y']:
            completed_bool = True
        elif completed.lower() in ['false', '0', 'no', 'n']:
            completed_bool = False
        else:
            print(f"❌ Invalid completion value: {completed}. Use true/false, 1/0, yes/no, or y/n")
            return
        
        if self.manager.update_requirement_status(contract_id, requirement_id, completed_bool, notes):
            print(f"✅ Updated {requirement_id} in {contract_id} to {'completed' if completed_bool else 'not completed'}")
            if notes:
                print(f"Notes: {notes}")
            
            # Auto-validate and show new status
            self.manager.validate_contract_completion(contract_id)
            self.show_status(contract_id)
        else:
            print(f"❌ Failed to update requirement {requirement_id} in {contract_id}")
    
    def validate_contract(self, contract_id: str):
        """Validate contract completion"""
        if contract_id not in self.manager.contract_statuses:
            print(f"❌ Contract {contract_id} not found")
            return
        
        print(f"🔍 Validating contract {contract_id}...")
        validation = self.manager.validate_contract_completion(contract_id)
        
        if validation.is_valid:
            print(f"✅ Contract {contract_id} is VALID (Score: {validation.score:.2f})")
        else:
            print(f"❌ Contract {contract_id} is INVALID (Score: {validation.score:.2f})")
        
        if validation.missing_requirements:
            print(f"\n❌ Missing Requirements:")
            for req in validation.missing_requirements:
                print(f"  - {req}")
        
        if validation.validation_errors:
            print(f"\n🚨 Validation Errors:")
            for error in validation.validation_errors:
                print(f"  - {error}")
        
        if validation.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in validation.warnings:
                print(f"  - {warning}")
    
    def complete_contract(self, contract_id: str):
        """Mark contract as completed"""
        if contract_id not in self.manager.contract_statuses:
            print(f"❌ Contract {contract_id} not found")
            return
        
        # Mark all requirements as completed
        status = self.manager.contract_statuses[contract_id]
        contract_file = self.manager.contracts_dir / f"contracts_{status.agent_id.lower().replace('-', '_')}" / f"{contract_id.lower()}.md"
        
        if contract_file.exists():
            requirements = self.manager.get_contract_requirements(contract_file)
            for req in requirements:
                self.manager.update_requirement_status(contract_id, req.requirement_id, True, "Auto-completed by CLI")
        
        # Validate to update status
        validation = self.manager.validate_contract_completion(contract_id)
        if validation.is_valid:
            print(f"✅ Contract {contract_id} marked as completed successfully!")
        else:
            print(f"⚠️  Contract {contract_id} completed but validation shows issues:")
            for error in validation.validation_errors:
                print(f"  - {error}")
    
    def show_progress(self, contract_id: str):
        """Show contract progress"""
        if contract_id not in self.manager.contract_statuses:
            print(f"❌ Contract {contract_id} not found")
            return
        
        status = self.manager.contract_statuses[contract_id]
        print(f"\n📊 PROGRESS REPORT: {contract_id}")
        print(f"Overall Progress: {status.progress_percentage:.1f}%")
        print(f"Requirements: {status.requirements_completed}/{status.total_requirements}")
        
        # Show progress bar
        bar_length = 30
        filled_length = int(bar_length * status.progress_percentage / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        print(f"Progress Bar: [{bar}] {status.progress_percentage:.1f}%")
        
        # Show status
        status_emoji = {
            TaskStatus.PENDING: "⏳ PENDING",
            TaskStatus.IN_PROGRESS: "🔄 IN PROGRESS",
            TaskStatus.REVIEW_NEEDED: "🔍 REVIEW NEEDED",
            TaskStatus.COMPLETED: "✅ COMPLETED",
            TaskStatus.FAILED: "❌ FAILED",
            TaskStatus.BOUNCED_BACK: "🚨 BOUNCED BACK"
        }
        
        print(f"Status: {status_emoji.get(status.current_status, '❓ UNKNOWN')}")
        print(f"Last Updated: {status.last_updated}")
    
    def bounce_contract(self, contract_id: str):
        """Bounce contract back for review"""
        if contract_id not in self.manager.contract_statuses:
            print(f"❌ Contract {contract_id} not found")
            return
        
        status = self.manager.contract_statuses[contract_id]
        status.current_status = TaskStatus.BOUNCED_BACK
        status.last_updated = datetime.now().isoformat()
        
        # Add bounce reason to validation
        if status.validation_result:
            status.validation_result.validation_errors.append("Contract bounced back for review by agent")
        else:
            status.validation_result = ContractValidation(
                is_valid=False,
                missing_requirements=[],
                validation_errors=["Contract bounced back for review by agent"],
                warnings=[],
                score=0.0,
                timestamp=datetime.now().isoformat()
            )
        
        self.manager.save_statuses()
        print(f"🚨 Contract {contract_id} has been bounced back for review")
        print(f"Agent {status.agent_id} will need to address issues and resubmit")
    
    def run(self, args: List[str]):
        """Run CLI with arguments"""
        if not args or args[0] in ['help', '--help', '-h']:
            self.show_help()
            return
        
        command = args[0].lower()
        
        try:
            if command == 'list':
                agent_id = args[1] if len(args) > 1 else None
                self.list_contracts(agent_id)
            
            elif command == 'status':
                if len(args) < 2:
                    print("❌ Usage: status <contract_id>")
                    return
                self.show_status(args[1])
            
            elif command == 'update':
                if len(args) < 4:
                    print("❌ Usage: update <contract_id> <requirement_id> <completed> [notes]")
                    return
                notes = args[4] if len(args) > 4 else ""
                self.update_requirement(args[1], args[2], args[3], notes)
            
            elif command == 'validate':
                if len(args) < 2:
                    print("❌ Usage: validate <contract_id>")
                    return
                self.validate_contract(args[1])
            
            elif command == 'complete':
                if len(args) < 2:
                    print("❌ Usage: complete <contract_id>")
                    return
                self.complete_contract(args[1])
            
            elif command == 'progress':
                if len(args) < 2:
                    print("❌ Usage: progress <contract_id>")
                    return
                self.show_progress(args[1])
            
            elif command == 'bounce':
                if len(args) < 2:
                    print("❌ Usage: bounce <contract_id>")
                    return
                self.bounce_contract(args[1])
            
            else:
                print(f"❌ Unknown command: {command}")
                self.show_help()
        
        except Exception as e:
            print(f"❌ Error executing command: {e}")
            logger.error(f"CLI error: {e}")

def main():
    """Main CLI entry point"""
    cli = ContractCLI()
    cli.run(sys.argv[1:])

if __name__ == "__main__":
    main()
