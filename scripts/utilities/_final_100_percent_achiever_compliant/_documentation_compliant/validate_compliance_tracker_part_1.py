"""
validate_compliance_tracker_part_1.py
Module: validate_compliance_tracker_part_1.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:36:48
"""

# Part 1 of validate_compliance_tracker.py
# Original file: .\scripts\utilities\validate_compliance_tracker.py

        
        for py_file in self.repo_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                
                relative_path = str(py_file.relative_to(self.repo_root))
                
                if lines >= 800:
                    violations["critical"].append((relative_path, lines, str(py_file)))
                elif lines >= 500:
                    violations["major"].append((relative_path, lines, str(py_file)))
                elif lines >= 300:
                    violations["moderate"].append((relative_path, lines, str(py_file)))
                else:
                    violations["compliant"].append((relative_path, lines, str(py_file)))
                    
            except Exception as e:
                print(f"Error reading {py_file}: {e}")
                
        return violations
    
    def validate_tracker_consistency(self) -> Dict[str, any]:
        """Validate consistency between tracker files"""
        results = {
            "status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        # Check if root file exists (master file is required)
        if not self.tracker_files[0].exists():
            results["status"] = "error"
            results["issues"].append("Master tracker file missing")
            return results
            
        # Check if docs file exists (will be created if missing)
        if not self.tracker_files[1].exists():
            results["status"] = "warning"
            results["issues"].append("Docs tracker file missing - will be created")
            results["recommendations"].append("Synchronize tracker files")
            return results
            
        # Read root file (master file)
        try:
            with open(self.tracker_files[0], 'r', encoding='utf-8') as f:
                root_content = f.read()
        except Exception as e:
            results["status"] = "error"
            results["issues"].append(f"Error reading master tracker file: {e}")

