"""
Register Command Handler

Handles test registration commands for the testing framework CLI.
"""

import os
import glob
from pathlib import Path
from typing import List, Dict, Any


class RegisterCommandHandler:
    """Handles test registration commands"""
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
    
    def handle(self, args) -> int:
        """Handle the register command"""
        if args.test_file:
            print(f"📝 Registering tests from file: {args.test_file}")
            return self._register_tests_from_file(args.test_file)
        elif args.test_dir:
            print(f"📝 Registering tests from directory: {args.test_dir}")
            return self._register_tests_from_directory(args.test_dir)
        else:
            print("No registration source specified. Use --test-file or --test-dir")
            return 1
        
        return 0
    
    def _register_tests_from_file(self, file_path: str) -> int:
        """Register tests from a specific file"""
        try:
            if not os.path.exists(file_path):
                print(f"❌ Error: File not found: {file_path}")
                return 1
            
            # Parse the test file and extract test information
            test_info = self._parse_test_file(file_path)
            
            if test_info:
                # Register with orchestrator
                success = self.orchestrator.register_test_file(file_path, test_info)
                if success:
                    print(f"✅ Successfully registered {len(test_info.get('tests', []))} tests from {file_path}")
                    return 0
                else:
                    print(f"❌ Failed to register tests from {file_path}")
                    return 1
            else:
                print(f"⚠️  No tests found in {file_path}")
                return 0
                
        except Exception as e:
            print(f"❌ Error registering tests from file {file_path}: {e}")
            return 1
    
    def _register_tests_from_directory(self, dir_path: str) -> int:
        """Register tests from a directory"""
        try:
            if not os.path.exists(dir_path):
                print(f"❌ Error: Directory not found: {dir_path}")
                return 1
            
            if not os.path.isdir(dir_path):
                print(f"❌ Error: Path is not a directory: {dir_path}")
                return 1
            
            # Find all test files in directory
            test_files = self._find_test_files(dir_path)
            
            if not test_files:
                print(f"⚠️  No test files found in directory: {dir_path}")
                return 0
            
            total_tests = 0
            successful_registrations = 0
            
            for test_file in test_files:
                try:
                    test_info = self._parse_test_file(test_file)
                    if test_info and test_info.get('tests'):
                        success = self.orchestrator.register_test_file(test_file, test_info)
                        if success:
                            successful_registrations += 1
                            total_tests += len(test_info['tests'])
                        else:
                            print(f"⚠️  Failed to register tests from {test_file}")
                except Exception as e:
                    print(f"⚠️  Error processing {test_file}: {e}")
            
            print(f"✅ Successfully registered {total_tests} tests from {successful_registrations}/{len(test_files)} files")
            return 0
            
        except Exception as e:
            print(f"❌ Error registering tests from directory {dir_path}: {e}")
            return 1
    
    def _find_test_files(self, dir_path: str) -> List[str]:
        """Find all test files in a directory"""
        test_files = []
        
        # Common test file patterns
        test_patterns = [
            "test_*.py",
            "*_test.py",
            "tests.py"
        ]
        
        for pattern in test_patterns:
            test_files.extend(glob.glob(os.path.join(dir_path, pattern)))
            test_files.extend(glob.glob(os.path.join(dir_path, "**", pattern), recursive=True))
        
        # Remove duplicates and sort
        test_files = list(set(test_files))
        test_files.sort()
        
        return test_files
    
    def _parse_test_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a test file and extract test information"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            test_info = {
                "file_path": file_path,
                "file_size": len(content),
                "tests": [],
                "imports": [],
                "classes": [],
                "functions": []
            }
            
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # Extract imports
                if line.startswith('import ') or line.startswith('from '):
                    test_info["imports"].append(line)
                
                # Extract test functions
                elif line.startswith('def test_') or line.startswith('def test'):
                    test_name = line.split('def ')[1].split('(')[0]
                    test_info["tests"].append({
                        "name": test_name,
                        "type": "function",
                        "line": line_num,
                        "signature": line
                    })
                
                # Extract test classes
                elif line.startswith('class Test') or line.startswith('class test'):
                    class_name = line.split('class ')[1].split('(')[0]
                    test_info["classes"].append({
                        "name": class_name,
                        "line": line_num,
                        "signature": line
                    })
                
                # Extract functions
                elif line.startswith('def '):
                    func_name = line.split('def ')[1].split('(')[0]
                    if not func_name.startswith('test'):
                        test_info["functions"].append({
                            "name": func_name,
                            "line": line_num,
                            "signature": line
                        })
            
            return test_info
            
        except Exception as e:
            print(f"⚠️  Error parsing test file {file_path}: {e}")
            return None
