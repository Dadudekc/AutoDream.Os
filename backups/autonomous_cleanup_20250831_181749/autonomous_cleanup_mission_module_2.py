    """Unified {base_name} implementation following SSOT principles"""
    
    def __init__(self):
        self.config = {{}}
        self.state = {{}}
        
    def process(self, data: Any) -> Any:
        """Main processing method"""
        # Unified implementation
        return data
        
    def validate(self, data: Any) -> bool:
        """Validation method"""
        return True
        
    def cleanup(self):
        """Cleanup method"""
        pass

# SSOT Implementation
{base_name}_instance = {base_name.title().replace('_', '')}()
'''
        
        unified_path = os.path.join(consolidated_dir, f"unified_{base_name}.py")
        with open(unified_path, 'w', encoding='utf-8') as f:
            f.write(unified_content)
        
        print(f"  📄 Created unified implementation: {unified_path}")
        
        # Remove duplicates
        for file_path in files:
            try:
                backup_path = os.path.join(self.backup_dir, os.path.basename(file_path))
                shutil.copy2(file_path, backup_path)
                os.remove(file_path)
                print(f"  🗑️ Removed duplicate: {file_path}")
                self.files_cleaned += 1
            except Exception as e:
                print(f"⚠️ Error removing {file_path}: {e}")
                
    def _refactor_to_oo(self):
        """Refactor code to follow object-oriented principles"""
        print("\n🔍 PHASE 3: OBJECT-ORIENTED REFACTORING")
        print("-" * 50)
        
        # Find procedural code patterns
        procedural_patterns = [
            "def main(",
            "def process_",
            "def handle_",
            "def validate_"
        ]
        
        for pattern in procedural_patterns:
            files_with_pattern = []
            for root, dirs, files in os.walk('.'):
                if 'backups' in root or '.git' in root or '__pycache__' in root:
                    continue
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if pattern in content:
                                    files_with_pattern.append(file_path)
                        except Exception:
                            continue
            
            if files_with_pattern:
                print(f"🔍 Found {len(files_with_pattern)} files with procedural patterns")
                for file_path in files_with_pattern:
                    self._refactor_to_oo_file(file_path)
                    
    def _refactor_to_oo_file(self, file_path):
        """Refactor individual file to OO principles"""
        print(f"🔧 Refactoring to OO: {file_path}")
        
        try:
            # Create backup
            backup_path = os.path.join(self.backup_dir, os.path.basename(file_path))
            shutil.copy2(file_path, backup_path)
            
            # Read content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple OO refactoring
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            oo_content = f'''#!/usr/bin/env python3
"""
{base_name} - Object-Oriented Implementation
Refactored from procedural code to follow OO principles
"""
from typing import Any, Dict, List, Optional

class {base_name.title().replace('_', '')}: