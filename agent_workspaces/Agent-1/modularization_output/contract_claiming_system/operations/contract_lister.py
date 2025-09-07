"""
Contract listing operations for the contract claiming system.
"""

from typing import Dict, List, Any, Optional
from ..core.contract_manager import ContractManager


class ContractLister:
    """Handles contract listing and filtering operations."""
    
    def __init__(self, contract_manager: ContractManager):
        self.contract_manager = contract_manager
    
    def list_available_contracts(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all available contracts, optionally filtered by category."""
        available = []
        contracts = self.contract_manager.get_all_contracts()
        contracts_section = contracts.get("contracts", {})
        
        for contract_type, contract_data in contracts_section.items():
            if isinstance(contract_data, dict) and 'contracts' in contract_data:
                contracts_list = contract_data.get('contracts', [])
                if isinstance(contracts_list, list):
                    for contract in contracts_list:
                        if isinstance(contract, dict) and contract.get('status') == 'AVAILABLE':
                            if category is None or contract.get('category') == category:
                                available.append(contract)
            elif isinstance(contract_data, list):
                for contract in contract_data:
                    if isinstance(contract, dict) and contract.get('status') == 'AVAILABLE':
                        if category is None or contract.get('category') == category:
                            available.append(contract)
        
        return available
    
    def list_contracts_by_status(self, status: str) -> List[Dict[str, Any]]:
        """List contracts by specific status."""
        contracts_by_status = []
        contracts = self.contract_manager.get_all_contracts()
        contracts_section = contracts.get("contracts", {})
        
        for contract_type, contract_data in contracts_section.items():
            if isinstance(contract_data, dict) and 'contracts' in contract_data:
                contracts_list = contract_data.get('contracts', [])
                if isinstance(contracts_list, list):
                    for contract in contracts_list:
                        if isinstance(contract, dict) and contract.get('status') == status:
                            contracts_by_status.append(contract)
            elif isinstance(contract_data, list):
                for contract in contract_data:
                    if isinstance(contract, dict) and contract.get('status') == status:
                        contracts_by_status.append(contract)
        
        return contracts_by_status
    
    def list_contracts_by_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """List contracts claimed by a specific agent."""
        agent_contracts = []
        contracts = self.contract_manager.get_all_contracts()
        contracts_section = contracts.get("contracts", {})
        
        for contract_type, contract_data in contracts_section.items():
            if isinstance(contract_data, dict) and 'contracts' in contract_data:
                contracts_list = contract_data.get('contracts', [])
                if isinstance(contracts_list, list):
                    for contract in contracts_list:
                        if isinstance(contract, dict) and contract.get('agent_id') == agent_id:
                            agent_contracts.append(contract)
            elif isinstance(contract_data, list):
                for contract in contract_data:
                    if isinstance(contract, dict) and contract.get('agent_id') == agent_id:
                        agent_contracts.append(contract)
        
        return agent_contracts
    
    def list_contracts_by_category(self, category: str) -> List[Dict[str, Any]]:
        """List all contracts in a specific category."""
        category_contracts = []
        contracts = self.contract_manager.get_all_contracts()
        contracts_section = contracts.get("contracts", {})
        
        for contract_type, contract_data in contracts_section.items():
            if isinstance(contract_data, dict) and 'contracts' in contract_data:
                contracts_list = contract_data.get('contracts', [])
                if isinstance(contracts_list, list):
                    for contract in contracts_list:
                        if isinstance(contract, dict) and contract.get('category') == category:
                            category_contracts.append(contract)
            elif isinstance(contract_data, list):
                for contract in contract_data:
                    if isinstance(contract, dict) and contract.get('category') == category:
                        category_contracts.append(contract)
        
        return category_contracts
    
    def search_contracts(self, search_term: str) -> List[Dict[str, Any]]:
        """Search contracts by title or description."""
        matching_contracts = []
        search_term_lower = search_term.lower()
        contracts = self.contract_manager.get_all_contracts()
        contracts_section = contracts.get("contracts", {})
        
        for contract_type, contract_data in contracts_section.items():
            if isinstance(contract_data, dict) and 'contracts' in contract_data:
                contracts_list = contract_data.get('contracts', [])
                if isinstance(contracts_list, list):
                    for contract in contracts_list:
                        if isinstance(contract, dict):
                            title = contract.get('title', '').lower()
                            description = contract.get('description', '').lower()
                            if search_term_lower in title or search_term_lower in description:
                                matching_contracts.append(contract)
            elif isinstance(contract_data, list):
                for contract in contract_data:
                    if isinstance(contract, dict):
                        title = contract.get('title', '').lower()
                        description = contract.get('description', '').lower()
                        if search_term_lower in title or search_term_lower in description:
                            matching_contracts.append(contract)
        
        return matching_contracts
    
    def get_contract_summary(self) -> Dict[str, Any]:
        """Get a summary of all contracts by category and status."""
        summary = {}
        contracts = self.contract_manager.get_all_contracts()
        contracts_section = contracts.get("contracts", {})
        
        for contract_type, contract_data in contracts_section.items():
            if isinstance(contract_data, dict) and 'contracts' in contract_data:
                contracts_list = contract_data.get('contracts', [])
                if isinstance(contracts_list, list):
                    for contract in contracts_list:
                        if isinstance(contract, dict):
                            category = contract.get('category', 'Unknown')
                            status = contract.get('status', 'Unknown')
                            
                            if category not in summary:
                                summary[category] = {}
                            if status not in summary[category]:
                                summary[category][status] = 0
                            summary[category][status] += 1
            elif isinstance(contract_data, list):
                for contract in contract_data:
                    if isinstance(contract, dict):
                        category = contract.get('category', 'Unknown')
                        status = contract.get('status', 'Unknown')
                        
                        if category not in summary:
                            summary[category] = {}
                        if status not in summary[category]:
                            summary[category][status] = 0
                        summary[category][status] += 1
        
        return summary
    
    def format_contract_list(self, contracts: List[Dict[str, Any]], show_details: bool = False) -> str:
        """Format a list of contracts for display."""
        if not contracts:
            return "No contracts found."
        
        formatted_lines = []
        for contract in contracts:
            contract_id = contract.get('contract_id', 'Unknown')
            title = contract.get('title', 'No Title')
            category = contract.get('category', 'Unknown')
            points = contract.get('points', 0)
            status = contract.get('status', 'Unknown')
            
            line = f"📋 {contract_id}: {title} ({points} pts) - {category} [{status}]"
            formatted_lines.append(line)
            
            if show_details:
                description = contract.get('description', 'No description')
                agent_id = contract.get('agent_id', 'Unclaimed')
                progress = contract.get('progress', '0%')
                
                formatted_lines.append(f"   Description: {description}")
                formatted_lines.append(f"   Agent: {agent_id}")
                formatted_lines.append(f"   Progress: {progress}")
                formatted_lines.append("")
        
        return "\n".join(formatted_lines)
