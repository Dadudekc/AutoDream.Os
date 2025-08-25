#!/usr/bin/env python3
"""
Generate GitHub Issues for Phase 3 Refactoring

This script reads the contract data and generates all 73 refactoring issues
using the GitHub issue template.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

def load_contract_data(contract_file: str) -> Dict[str, Any]:
    """Load contract data from JSON file."""
    with open(contract_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_contract_file_name(contract_file: str) -> str:
    """Extract the contract file name from the full path."""
    return os.path.basename(contract_file)

def format_field_value(value: Any) -> str:
    """Format contract field values to strings, handling lists and dicts."""
    if isinstance(value, list):
        if all(isinstance(item, str) for item in value):
            return '\n'.join(f"- {item}" for item in value)
        else:
            return '\n'.join(f"- {str(item)}" for item in value)
    elif isinstance(value, dict):
        if 'extract_modules' in value:
            modules = value.get('extract_modules', [])
            return '\n'.join(f"- `{module}`" for module in modules)
        else:
            return '\n'.join(f"- {k}: {v}" for k, v in value.items())
    else:
        return str(value)

def generate_issue_content(contract: Dict[str, Any], template_path: str, contract_file: str) -> str:
    """Generate issue content from contract data and template."""
    
    # Read the template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Extract contract details
    contract_id = contract.get('contract_id', 'UNKNOWN')
    file_path = contract.get('file_path', 'UNKNOWN')
    current_lines = contract.get('current_lines', 0)
    target_lines = contract.get('target_lines', 400)
    reduction_target = contract.get('reduction_target', 0)
    priority = contract.get('priority', 'medium').upper()
    estimated_hours = contract.get('estimated_hours', 0)
    category = contract.get('category', 'General Refactoring')
    
    # Format complex fields
    violations = format_field_value(contract.get('violations', 'Exceeds recommended line count and violates SRP'))
    refactoring_plan = format_field_value(contract.get('refactoring_plan', 'Extract focused modules following SRP'))
    main_class = contract.get('main_class', 'Main class name')
    responsibilities = contract.get('responsibilities', 'Multiple responsibilities identified')
    dependencies = format_field_value(contract.get('dependencies', 'Various dependencies'))
    success_criteria = format_field_value(contract.get('success_criteria', 'Code complies with V2 standards and SRP'))
    
    # Determine phase based on contract file
    if 'phase3a' in contract_file:
        phase = 'Phase 3A (CRITICAL)'
    elif 'phase3b' in contract_file:
        phase = 'Phase 3B (HIGH)'
    elif 'phase3c' in contract_file:
        phase = 'Phase 3C (MEDIUM)'
    elif 'phase3d' in contract_file:
        phase = 'Phase 3D (LOW)'
    elif 'phase3e' in contract_file:
        phase = 'Phase 3E (COMPREHENSIVE)'
    elif 'phase3f' in contract_file:
        phase = 'Phase 3F (REMAINING)'
    elif 'phase3g' in contract_file:
        phase = 'Phase 3G (FINAL)'
    elif 'phase3h' in contract_file:
        phase = 'Phase 3H (COMPLETION)'
    elif 'phase3i' in contract_file:
        phase = 'Phase 3I (ULTIMATE)'
    else:
        phase = 'Phase 3'
    
    # Replace template variables
    content = template.replace('{{ priority }}', priority)
    content = content.replace('{{ estimated_hours }}', str(estimated_hours))
    content = content.replace('{{ category }}', category)
    content = content.replace('{{ file_path }}', file_path)
    content = content.replace('{{ current_lines }}', str(current_lines))
    content = content.replace('{{ target_lines }}', str(target_lines))
    content = content.replace('{{ reduction_target }}', str(reduction_target))
    content = content.replace('{{ violations }}', violations)
    content = content.replace('{{ refactoring_plan }}', refactoring_plan)
    content = content.replace('{{ main_class }}', main_class)
    content = content.replace('{{ responsibilities }}', responsibilities)
    content = content.replace('{{ dependencies }}', dependencies)
    content = content.replace('{{ success_criteria }}', success_criteria)
    content = content.replace('{{ phase }}', phase)
    content = content.replace('{{ contract_id }}', contract_id)
    content = content.replace('{{ contract_file }}', get_contract_file_name(contract_file))
    
    return content

def generate_issue_filename(contract: Dict[str, Any]) -> str:
    """Generate a filename for the issue based on contract details."""
    contract_id = contract.get('contract_id', 'UNKNOWN')
    file_path = contract.get('file_path', 'unknown_file')
    
    # Clean the file path for filename
    clean_path = file_path.replace('/', '_').replace('\\', '_').replace('src_', '')
    clean_path = clean_path.replace('.py', '').replace('.', '_')
    
    return f"issue_{contract_id}_{clean_path}.md"

def main():
    """Main function to generate all refactoring issues."""
    
    # Paths
    contracts_dir = Path("contracts")
    issues_dir = Path(".github/ISSUE_TEMPLATE/refactoring_issues")
    template_path = Path(".github/ISSUE_TEMPLATE/easy_refactoring_issue.md")
    
    # Create issues directory
    issues_dir.mkdir(parents=True, exist_ok=True)
    
    # Contract files to process - now including all new contract files
    contract_files = [
        "contracts/phase3b_moderate_contracts.json",
        "contracts/phase3c_standard_moderate_contracts.json", 
        "contracts/phase3d_remaining_moderate_contracts.json",
        "contracts/phase3e_comprehensive_contracts.json",
        "contracts/phase3f_remaining_contracts.json",
        "contracts/phase3g_final_contracts.json",
        "contracts/phase3h_completion_contracts.json",
        "contracts/phase3i_final_completion.json"
    ]
    
    total_issues = 0
    
    print("🚀 Generating GitHub Issues for Phase 3 Refactoring...")
    print("=" * 60)
    
    for contract_file in contract_files:
        if not os.path.exists(contract_file):
            print(f"⚠️  Contract file not found: {contract_file}")
            continue
            
        print(f"\n📁 Processing: {contract_file}")
        
        try:
            # Load contract data
            contracts_data = load_contract_data(contract_file)
            contracts = contracts_data.get('contracts', [])
            
            print(f"   Found {len(contracts)} contracts")
            print(f"   Total contracts field: {len(contracts)}")
            
            for i, contract in enumerate(contracts):
                try:
                    print(f"     Processing contract {i+1}/{len(contracts)}: {contract.get('contract_id', 'UNKNOWN')}")
                    
                    # Generate issue content
                    issue_content = generate_issue_content(contract, template_path, contract_file)
                    
                    # Generate filename
                    issue_filename = generate_issue_filename(contract)
                    issue_path = issues_dir / issue_filename
                    
                    # Write issue file
                    with open(issue_path, 'w', encoding='utf-8') as f:
                        f.write(issue_content)
                    
                    total_issues += 1
                    print(f"       ✅ Generated: {issue_filename}")
                    
                except Exception as e:
                    print(f"       ❌ Error generating issue for {contract.get('contract_id', 'UNKNOWN')}: {e}")
                    import traceback
                    traceback.print_exc()
                    
        except Exception as e:
            print(f"   ❌ Error processing {contract_file}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"🎉 Successfully generated {total_issues} refactoring issues!")
    print(f"📁 Issues saved to: {issues_dir}")
    print("\n📋 Next Steps:")
    print("1. Review generated issues in the .github/ISSUE_TEMPLATE/refactoring_issues/ directory")
    print("2. Copy issues to GitHub repository issues manually or use GitHub CLI")
    print("3. Assign issues to contributors")
    print("4. Track progress using the contract system")

if __name__ == "__main__":
    main()
