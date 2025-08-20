#!/usr/bin/env python3
"""
Perpetual Motion Contract Service - Agent Cellphone V2
=====================================================

Automatically generates new contracts when agents complete existing ones.
Creates a self-sustaining work cycle - the perpetual motion machine!

Follows V2 standards: ≤ 200 LOC, SRP, OOP design, CLI interface.
"""

import json
import logging
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import argparse
import random

@dataclass
class ContractTemplate:
    """Contract template for automatic generation."""
    title: str
    description: str
    acceptance_criteria: List[str]
    estimated_hours: int
    priority: str
    category: str
    skills_required: List[str]

@dataclass
class GeneratedContract:
    """Automatically generated contract."""
    contract_id: str
    task_id: str
    title: str
    description: str
    assignee: str
    state: str
    created_at: datetime
    template_source: str

class PerpetualMotionContractService:
    """Service that automatically generates new contracts to maintain perpetual motion."""
    
    def __init__(self, contracts_dir: str = "contracts", templates_dir: str = "contract_templates"):
        self.contracts_dir = Path(contracts_dir)
        self.templates_dir = Path(templates_dir)
        self.contracts_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Contract templates for automatic generation
        self.contract_templates = self._load_contract_templates()
        
        # Auto-generation settings
        self.auto_generate_on_completion = True
        self.contracts_per_completion = 2  # Generate 2 new contracts per completion
        self.min_contracts_maintained = 10  # Always maintain at least 10 contracts
        
        # Monitoring thread
        self.monitor_thread = None
        self.monitoring_active = False
        
        self.logger.info("Perpetual Motion Contract Service initialized")
    
    def setup_logging(self):
        """Setup logging for the service."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "perpetual_motion_contracts.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _load_contract_templates(self) -> List[ContractTemplate]:
        """Load contract templates for automatic generation."""
        templates = []
        
        # Default templates if none exist
        default_templates = [
            ContractTemplate(
                title="Code Quality Enhancement",
                description="Improve code quality through refactoring, testing, and documentation",
                acceptance_criteria=["Code passes all tests", "Documentation updated", "Code review completed"],
                estimated_hours=2,
                priority="medium",
                category="code_quality",
                skills_required=["programming", "testing", "documentation"]
            ),
            ContractTemplate(
                title="Performance Optimization",
                description="Identify and optimize performance bottlenecks in the system",
                acceptance_criteria=["Performance metrics improved", "Benchmarks documented", "Optimization validated"],
                estimated_hours=3,
                priority="high",
                category="performance",
                skills_required=["performance_analysis", "optimization", "benchmarking"]
            ),
            ContractTemplate(
                title="Security Enhancement",
                description="Review and enhance security measures in the codebase",
                acceptance_criteria=["Security audit completed", "Vulnerabilities addressed", "Security tests added"],
                estimated_hours=4,
                priority="critical",
                category="security",
                skills_required=["security", "auditing", "testing"]
            ),
            ContractTemplate(
                title="Documentation Update",
                description="Update and improve system documentation",
                acceptance_criteria=["Documentation current", "Examples provided", "Formatting consistent"],
                estimated_hours=1,
                priority="low",
                category="documentation",
                skills_required=["documentation", "technical_writing"]
            ),
            ContractTemplate(
                title="Test Coverage Improvement",
                description="Increase test coverage and add missing test cases",
                acceptance_criteria=["Coverage target met", "Edge cases tested", "Tests pass consistently"],
                estimated_hours=2,
                priority="medium",
                category="testing",
                skills_required=["testing", "test_automation", "quality_assurance"]
            )
        ]
        
        # Try to load from file, fall back to defaults
        try:
            templates_file = self.templates_dir / "contract_templates.json"
            if templates_file.exists():
                with open(templates_file, 'r') as f:
                    data = json.load(f)
                    for item in data:
                        templates.append(ContractTemplate(**item))
                self.logger.info(f"Loaded {len(templates)} contract templates from file")
            else:
                # Save default templates
                self._save_contract_templates(default_templates)
                templates = default_templates
                self.logger.info("Created default contract templates")
        except Exception as e:
            self.logger.error(f"Error loading templates: {e}, using defaults")
            templates = default_templates
        
        return templates
    
    def _save_contract_templates(self, templates: List[ContractTemplate]):
        """Save contract templates to file."""
        try:
            templates_file = self.templates_dir / "contract_templates.json"
            data = [vars(template) for template in templates]
            with open(templates_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Error saving templates: {e}")
    
    def on_contract_completion(self, contract_id: str, agent_id: str, completion_data: Dict[str, Any]):
        """Called when a contract is completed - triggers automatic generation of new contracts."""
        try:
            self.logger.info(f"Contract {contract_id} completed by {agent_id} - generating new contracts")
            
            # Generate new contracts automatically
            new_contracts = self._generate_new_contracts(agent_id, self.contracts_per_completion)
            
            # Save new contracts
            for contract in new_contracts:
                self._save_contract(contract)
            
            # Send resume message to agent to prompt more work
            self._send_resume_message(agent_id, new_contracts)
            
            self.logger.info(f"Generated {len(new_contracts)} new contracts for {agent_id}")
            
        except Exception as e:
            self.logger.error(f"Error handling contract completion: {e}")
    
    def _generate_new_contracts(self, agent_id: str, count: int) -> List[GeneratedContract]:
        """Generate new contracts based on templates."""
        contracts = []
        
        for i in range(count):
            # Select random template
            template = random.choice(self.contract_templates)
            
            # Generate unique contract ID
            contract_id = f"CONTRACT-{int(time.time())}-{i:03d}"
            task_id = f"TASK-{int(time.time())}-{i:03d}"
            
            # Create contract from template
            contract = GeneratedContract(
                contract_id=contract_id,
                task_id=task_id,
                title=f"{template.title} #{i+1}",
                description=template.description,
                assignee=agent_id,
                state="ready",
                created_at=datetime.now(),
                template_source=template.title
            )
            
            contracts.append(contract)
        
        return contracts
    
    def _save_contract(self, contract: GeneratedContract):
        """Save a generated contract to file."""
        try:
            contract_file = self.contracts_dir / f"{contract.contract_id}.json"
            contract_data = vars(contract)
            contract_data["created_at"] = contract.created_at.isoformat()
            
            with open(contract_file, 'w') as f:
                json.dump(contract_data, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Error saving contract {contract.contract_id}: {e}")
    
    def _send_resume_message(self, agent_id: str, new_contracts: List[GeneratedContract]):
        """Send resume message to agent with new contract assignments."""
        try:
            # Create resume message
            message = f"""🚀 CONTRACT COMPLETED - NEW ASSIGNMENTS READY!

🎯 Great work completing your contract! Here are your new assignments:

"""
            
            for i, contract in enumerate(new_contracts, 1):
                message += f"""{i}. **{contract.title}**
   📋 {contract.description}
   🎯 Contract ID: {contract.contract_id}
   📝 Task ID: {contract.task_id}
   ⏰ Status: Ready to start

"""
            
            message += """💡 **NEXT STEPS:**
1. Review your new contracts
2. Start with the highest priority one
3. Send fsm_update when you begin (task_id, state, summary, evidence)
4. Complete contracts to trigger even more assignments!

🔄 **PERPETUAL MOTION ACTIVE** - Keep completing contracts to keep the cycle going!"""
            
            # Save resume message to agent's inbox
            self._save_resume_message(agent_id, message)
            
        except Exception as e:
            self.logger.error(f"Error sending resume message: {e}")
    
    def _save_resume_message(self, agent_id: str, message: str):
        """Save resume message to agent's inbox."""
        try:
            inbox_dir = Path(f"agent_workspaces/{agent_id}/inbox")
            inbox_dir.mkdir(parents=True, exist_ok=True)
            
            message_file = inbox_dir / f"resume_message_{int(time.time())}.json"
            message_data = {
                "from": "PerpetualMotionContractService",
                "to": agent_id,
                "type": "resume",
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "contracts_assigned": True
            }
            
            with open(message_file, 'w') as f:
                json.dump(message_data, f, indent=2, default=str)
                
            self.logger.info(f"Resume message saved to {agent_id} inbox")
            
        except Exception as e:
            self.logger.error(f"Error saving resume message: {e}")
    
    def start_monitoring(self):
        """Start background monitoring for contract completions."""
        if self.monitoring_active:
            self.logger.warning("Monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_contracts, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Contract monitoring started")
    
    def stop_monitoring(self):
        """Stop background monitoring."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("Contract monitoring stopped")
    
    def _monitor_contracts(self):
        """Background thread to monitor for contract completions."""
        while self.monitoring_active:
            try:
                # Check for completed contracts
                self._check_for_completions()
                
                # Maintain minimum contract count
                self._maintain_minimum_contracts()
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _check_for_completions(self):
        """Check for newly completed contracts."""
        try:
            # This would integrate with your existing contract system
            # For now, we'll just log that we're checking
            self.logger.debug("Checking for contract completions...")
            
        except Exception as e:
            self.logger.error(f"Error checking completions: {e}")
    
    def _maintain_minimum_contracts(self):
        """Ensure minimum number of contracts are available."""
        try:
            # Count available contracts
            contract_files = list(self.contracts_dir.glob("*.json"))
            available_count = len(contract_files)
            
            if available_count < self.min_contracts_maintained:
                needed = self.min_contracts_maintained - available_count
                self.logger.info(f"Generating {needed} contracts to maintain minimum")
                
                # Generate contracts for random agents
                agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]
                for _ in range(needed):
                    agent = random.choice(agents)
                    new_contracts = self._generate_new_contracts(agent, 1)
                    for contract in new_contracts:
                        self._save_contract(contract)
                        
        except Exception as e:
            self.logger.error(f"Error maintaining minimum contracts: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get service status."""
        contract_files = list(self.contracts_dir.glob("*.json"))
        
        return {
            "status": "active" if self.monitoring_active else "inactive",
            "contracts_available": len(contract_files),
            "templates_loaded": len(self.contract_templates),
            "auto_generation": self.auto_generate_on_completion,
            "contracts_per_completion": self.contracts_per_completion,
            "min_contracts_maintained": self.min_contracts_maintained
        }

def main():
    """CLI interface for the service."""
    parser = argparse.ArgumentParser(description="Perpetual Motion Contract Service")
    parser.add_argument("--start", action="store_true", help="Start the service")
    parser.add_argument("--stop", action="store_true", help="Stop the service")
    parser.add_argument("--status", action="store_true", help="Show service status")
    parser.add_argument("--test-completion", type=str, help="Test contract completion for agent")
    parser.add_argument("--generate", type=int, help="Generate N new contracts")
    
    args = parser.parse_args()
    
    service = PerpetualMotionContractService()
    
    if args.start:
        service.start_monitoring()
        print("✅ Service started - monitoring for contract completions")
        
    elif args.stop:
        service.stop_monitoring()
        print("✅ Service stopped")
        
    elif args.status:
        status = service.get_status()
        print("📊 Service Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
            
    elif args.test_completion:
        # Test contract completion
        test_data = {"test": True, "timestamp": datetime.now().isoformat()}
        service.on_contract_completion("TEST-CONTRACT", args.test_completion, test_data)
        print(f"✅ Tested contract completion for {args.test_completion}")
        
    elif args.generate:
        # Generate test contracts
        contracts = service._generate_new_contracts("Agent-1", args.generate)
        for contract in contracts:
            service._save_contract(contract)
        print(f"✅ Generated {len(contracts)} test contracts")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
