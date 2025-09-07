#!/usr/bin/env python3
"""
Constants Consolidation System - Agent-8 Autonomous Cleanup
=========================================================

Automated system to consolidate all scattered constants.py files into the unified constants system.
Part of Agent-8's autonomous cleanup mission to achieve maximum efficiency.

Author: Agent-8 (Integration Enhancement Optimization Manager)
Mission: Autonomous Cleanup & Side Mission Completion
Status: MAXIMUM EFFICIENCY MODE
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import ast
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ConstantDefinition:
    """Represents a constant definition found in a file."""
    name: str
    value: Any
    file_path: str
    line_number: int
    description: str = ""
    category: str = "unknown"


class ConstantsConsolidator:
    """Automated system to consolidate scattered constants into unified system."""
    
    def __init__(self):
        self.consolidated_constants: Dict[str, ConstantDefinition] = {}
        self.duplicate_files: List[str] = []
        self.consolidation_results: Dict[str, Any] = {}
        
    def find_duplicate_constants_files(self) -> List[str]:
        """Find all constants.py files in the repository."""
        logger.info("🔍 Searching for duplicate constants.py files...")
        
        duplicate_files = []
        for root, dirs, files in os.walk("."):
            if "constants.py" in files:
                file_path = os.path.join(root, "constants.py")
                duplicate_files.append(file_path)
                logger.info(f"   Found: {file_path}")
        
        logger.info(f"✅ Found {len(duplicate_files)} duplicate constants.py files")
        return duplicate_files
    
    def extract_constants_from_file(self, file_path: str) -> List[ConstantDefinition]:
        """Extract constant definitions from a Python file."""
        constants = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the file
            tree = ast.parse(content)
            
            # Find all assignments
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            # This is a simple assignment (e.g., CONSTANT = value)
                            constant_name = target.id
                            
                            # Skip if it's not a constant (all caps)
                            if not constant_name.isupper():
                                continue
                            
                            # Try to get the value
                            try:
                                if isinstance(node.value, ast.Constant):
                                    value = node.value.value
                                elif isinstance(node.value, ast.Str):
                                    value = node.value.s
                                elif isinstance(node.value, ast.Num):
                                    value = node.value.n
                                elif isinstance(node.value, ast.NameConstant):
                                    value = node.value.value
                                else:
                                    # For complex expressions, get the source
                                    value = ast.unparse(node.value)
                                
                                constant = ConstantDefinition(
                                    name=constant_name,
                                    value=value,
                                    file_path=file_path,
                                    line_number=node.lineno,
                                    description=f"Extracted from {file_path}"
                                )
                                constants.append(constant)
                                
                            except Exception as e:
                                logger.warning(f"Could not extract value for {constant_name}: {e}")
                                
        except Exception as e:
            logger.error(f"Error extracting constants from {file_path}: {e}")
        
        return constants
    
    def categorize_constant(self, constant: ConstantDefinition) -> str:
        """Categorize a constant based on its name and context."""
        name = constant.name.lower()
        file_path = constant.file_path.lower()
        
        # Categorize based on file path
        if "health" in file_path or "monitoring" in file_path:
            return "health_monitoring"
        elif "decision" in file_path:
            return "decision_making"
        elif "manager" in file_path:
            return "management"
        elif "fsm" in file_path:
            return "fsm"
        elif "baseline" in file_path:
            return "baseline"
        elif "services" in file_path:
            return "services"
        elif "ai_ml" in file_path:
            return "ai_ml"
        elif "financial" in file_path:
            return "financial"
        elif "status" in file_path:
            return "status_monitoring"
        elif "config" in file_path:
            return "configuration"
        else:
            return "general"
    
    def consolidate_constants(self) -> Dict[str, Any]:
        """Main consolidation process."""
        logger.info("🚀 Starting Constants Consolidation Process")
        
        # Find all duplicate files
        duplicate_files = self.find_duplicate_constants_files()
        
        # Extract constants from each file
        all_constants = []
        for file_path in duplicate_files:
            constants = self.extract_constants_from_file(file_path)
            all_constants.extend(constants)
            logger.info(f"   Extracted {len(constants)} constants from {file_path}")
        
        # Categorize and deduplicate constants
        categorized_constants = {}
        duplicates_found = 0
        
        for constant in all_constants:
            category = self.categorize_constant(constant)
            
            if category not in categorized_constants:
                categorized_constants[category] = []
            
            # Check for duplicates
            existing = next((c for c in categorized_constants[category] if c.name == constant.name), None)
            if existing:
                duplicates_found += 1
                logger.info(f"   Duplicate found: {constant.name} in {constant.file_path} and {existing.file_path}")
                # Keep the one from the most specific location
                if len(constant.file_path) < len(existing.file_path):
                    categorized_constants[category].remove(existing)
                    categorized_constants[category].append(constant)
            else:
                categorized_constants[category].append(constant)
        
        # Generate consolidated constants file
        self._generate_consolidated_file(categorized_constants)
        
        # Prepare results
        results = {
            "duplicate_files_found": len(duplicate_files),
            "total_constants_extracted": len(all_constants),
            "duplicates_eliminated": duplicates_found,
            "categories_created": len(categorized_constants),
            "constants_by_category": {cat: len(constants) for cat, constants in categorized_constants.items()},
            "files_to_remove": duplicate_files
        }
        
        logger.info(f"✅ Constants consolidation complete!")
        logger.info(f"   Files processed: {len(duplicate_files)}")
        logger.info(f"   Constants extracted: {len(all_constants)}")
        logger.info(f"   Duplicates eliminated: {duplicates_found}")
        logger.info(f"   Categories created: {len(categorized_constants)}")
        
        return results
    
    def _generate_consolidated_file(self, categorized_constants: Dict[str, List[ConstantDefinition]]):
        """Generate the consolidated constants file."""
        output_file = "src/core/configuration/consolidated_constants.py"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('#!/usr/bin/env python3\n')
            f.write('"""\n')
            f.write('Consolidated Constants - Agent-8 Autonomous Cleanup\n')
            f.write('==================================================\n\n')
            f.write('Automatically consolidated constants from all scattered constants.py files.\n')
            f.write('Generated by Agent-8 during autonomous cleanup mission.\n\n')
            f.write('Author: Agent-8 (Integration Enhancement Optimization Manager)\n')
            f.write('Mission: Autonomous Cleanup & Side Mission Completion\n')
            f.write('Status: MAXIMUM EFFICIENCY MODE\n')
            f.write('"""\n\n')
            
            f.write('from pathlib import Path\n')
            f.write('import os\n\n')
            
            # Add constants by category
            for category, constants in categorized_constants.items():
                f.write(f'# ============================================================================\n')
                f.write(f'# {category.upper().replace("_", " ")} CONSTANTS\n')
                f.write(f'# ============================================================================\n\n')
                
                for constant in constants:
                    f.write(f'# {constant.description}\n')
                    f.write(f'{constant.name} = ')
                    
                    if isinstance(constant.value, str):
                        f.write(f'"{constant.value}"\n')
                    elif isinstance(constant.value, bool):
                        f.write(f'{str(constant.value)}\n')
                    elif isinstance(constant.value, (int, float)):
                        f.write(f'{constant.value}\n')
                    else:
                        f.write(f'{constant.value}\n')
                    
                    f.write('\n')
            
            f.write('# ============================================================================\n')
            f.write('# CONSOLIDATION METADATA\n')
            f.write('# ============================================================================\n\n')
            f.write('CONSOLIDATION_INFO = {\n')
            f.write(f'    "total_constants": {sum(len(constants) for constants in categorized_constants.values())},\n')
            f.write(f'    "categories": {len(categorized_constants)},\n')
            f.write(f'    "consolidated_from_files": {len([c for constants in categorized_constants.values() for c in constants])},\n')
            f.write('    "consolidated_by": "Agent-8",\n')
            f.write('    "mission": "Autonomous Cleanup & Side Mission Completion"\n')
            f.write('}\n')
        
        logger.info(f"✅ Generated consolidated constants file: {output_file}")
    
    def create_migration_guide(self, results: Dict[str, Any]):
        """Create a migration guide for the consolidation."""
        guide_file = "CONSTANTS_CONSOLIDATION_MIGRATION_GUIDE.md"
        
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write('# Constants Consolidation Migration Guide\n\n')
            f.write('**Generated by:** Agent-8 (Integration Enhancement Optimization Manager)\n')
            f.write('**Mission:** Autonomous Cleanup & Side Mission Completion\n')
            f.write('**Status:** MAXIMUM EFFICIENCY MODE\n\n')
            
            f.write('## Consolidation Summary\n\n')
            f.write(f'- **Files Processed:** {results["duplicate_files_found"]}\n')
            f.write(f'- **Constants Extracted:** {results["total_constants_extracted"]}\n')
            f.write(f'- **Duplicates Eliminated:** {results["duplicates_eliminated"]}\n')
            f.write(f'- **Categories Created:** {results["categories_created"]}\n\n')
            
            f.write('## Migration Steps\n\n')
            f.write('1. **Update imports** in all files that import from old constants.py files\n')
            f.write('2. **Replace imports** with: `from src.core.configuration.consolidated_constants import *`\n')
            f.write('3. **Remove old constants.py files** after confirming no breaking changes\n')
            f.write('4. **Test thoroughly** to ensure all constants are accessible\n\n')
            
            f.write('## Files to Remove\n\n')
            for file_path in results["files_to_remove"]:
                f.write(f'- `{file_path}`\n')
            
            f.write('\n## Constants by Category\n\n')
            for category, count in results["constants_by_category"].items():
                f.write(f'- **{category}:** {count} constants\n')
        
        logger.info(f"✅ Created migration guide: {guide_file}")


def main():
    """Main consolidation process."""
    logger.info("🚀 AGENT-8 CONSTANTS CONSOLIDATION MISSION")
    logger.info("=" * 50)
    
    consolidator = ConstantsConsolidator()
    
    # Run consolidation
    results = consolidator.consolidate_constants()
    
    # Create migration guide
    consolidator.create_migration_guide(results)
    
    logger.info("🎯 CONSTANTS CONSOLIDATION MISSION COMPLETE!")
    logger.info("=" * 50)
    
    return results


if __name__ == "__main__":
    main()
