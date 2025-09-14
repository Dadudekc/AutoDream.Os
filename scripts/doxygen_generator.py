#!/usr/bin/env python3
"""
@file doxygen_generator.py
@brief Automated Doxygen documentation generator for Agent Cellphone V2
@author Agent-4 Captain
@date 2025-09-12
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional
import json
from datetime import datetime


class DoxygenGenerator:
    """
    @brief Manages automated Doxygen documentation generation.
    
    This class handles the complete documentation generation process
    for the Agent Cellphone V2 swarm coordination system.
    """
    
    def __init__(self, project_root: str = "."):
        """
        @brief Initialize the Doxygen generator.
        
        @param project_root Root directory of the project
        """
        self.project_root = Path(project_root).resolve()
        self.doxyfile_path = self.project_root / "Doxyfile"
        self.output_dir = self.project_root / "docs" / "doxygen"
        self.html_dir = self.output_dir / "html"
        
    def check_dependencies(self) -> Dict[str, bool]:
        """
        @brief Check if required dependencies are available.
        
        @return Dictionary with dependency availability status
        """
        dependencies = {
            "doxygen": False,
            "graphviz": False,
            "doxyfile": self.doxyfile_path.exists()
        }
        
        # Check Doxygen
        try:
            result = subprocess.run(
                ["doxygen", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            dependencies["doxygen"] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            dependencies["doxygen"] = False
            
        # Check Graphviz (dot command)
        try:
            result = subprocess.run(
                ["dot", "-V"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            dependencies["graphviz"] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            dependencies["graphviz"] = False
            
        return dependencies
    
    def install_instructions(self) -> str:
        """
        @brief Generate installation instructions for missing dependencies.
        
        @return Formatted installation instructions
        """
        instructions = []
        instructions.append("🔧 **DOXYGEN DEPENDENCY INSTALLATION**")
        instructions.append("")
        
        instructions.append("### **Windows Installation**")
        instructions.append("1. **Doxygen**: Download from https://www.doxygen.nl/download.html")
        instructions.append("2. **Graphviz**: Download from https://graphviz.org/download/")
        instructions.append("3. **Add to PATH**: Ensure both tools are in your system PATH")
        instructions.append("")
        
        instructions.append("### **Alternative: Chocolatey**")
        instructions.append("```bash")
        instructions.append("choco install doxygen")
        instructions.append("choco install graphviz")
        instructions.append("```")
        instructions.append("")
        
        instructions.append("### **Verification**")
        instructions.append("```bash")
        instructions.append("doxygen --version")
        instructions.append("dot -V")
        instructions.append("```")
        
        return "\n".join(instructions)
    
    def generate_documentation(self) -> Dict[str, any]:
        """
        @brief Generate Doxygen documentation.
        
        @return Dictionary with generation results and statistics
        """
        if not self.doxyfile_path.exists():
            return {
                "success": False,
                "error": "Doxyfile not found",
                "files_generated": 0
            }
        
        try:
            # Create output directory
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Run Doxygen
            result = subprocess.run(
                ["doxygen", str(self.doxyfile_path)],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            # Count generated files
            files_generated = 0
            if self.html_dir.exists():
                files_generated = len(list(self.html_dir.rglob("*")))
            
            return {
                "success": result.returncode == 0,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "files_generated": files_generated,
                "output_dir": str(self.output_dir)
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Doxygen generation timed out",
                "files_generated": 0
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "files_generated": 0
            }
    
    def create_documentation_index(self) -> str:
        """
        @brief Create a comprehensive documentation index.
        
        @return Path to the created index file
        """
        index_content = f"""# Agent Cellphone V2 - Documentation Index

## 🐝 **SWARM DOCUMENTATION SYSTEM** 🐝

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Project**: Agent Cellphone V2 - Swarm Coordination System
**Version**: 2.0.0

## 📋 **Documentation Sections**

### **1. API Documentation**
- **HTML Documentation**: [View Online](html/index.html)
- **Class Reference**: Complete class and method documentation
- **Function Reference**: All function signatures and descriptions

### **2. System Architecture**
- **Swarm Coordination**: 8-agent positioning and communication
- **PyAutoGUI Integration**: Real-time automation protocols
- **Multi-Monitor Support**: Dual-screen agent distribution

### **3. Development Tools**
- **Consolidation Scripts**: File consolidation and optimization
- **Performance Monitoring**: System health and optimization
- **Quality Assurance**: Code quality enforcement

### **4. Integration Guides**
- **Messaging Systems**: Inter-agent communication protocols
- **Discord Integration**: Bot communication and management
- **Status Management**: Agent status tracking and reporting

## 🚀 **Quick Navigation**

### **Core Components**
- [Agent Coordination](html/class_agent_coordinator.html)
- [Messaging System](html/class_messaging_service.html)
- [Performance Monitor](html/class_performance_monitor.html)
- [Consolidation Tools](html/class_consolidation_manager.html)

### **Utility Scripts**
- [Doxygen Generator](html/doxygen__generator_8py.html)
- [Project Scanner](html/project__scanner_8py.html)
- [Performance Audit](html/performance__audit_8py.html)

## 📊 **Documentation Statistics**

- **Total Files Documented**: {self._count_documented_files()}
- **Classes Documented**: {self._count_documented_classes()}
- **Functions Documented**: {self._count_documented_functions()}
- **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🔧 **Maintenance**

This documentation is automatically generated and maintained as part of the
swarm coordination system. Updates are triggered by:

- Code changes in documented files
- New class or function additions
- Documentation comment updates
- System architecture changes

---

**WE ARE SWARM** - Comprehensive documentation for the most advanced
multi-agent coordination system! 🚀🐝
"""
        
        index_path = self.output_dir / "README.md"
        index_path.write_text(index_content, encoding='utf-8')
        return str(index_path)
    
    def _count_documented_files(self) -> int:
        """Count documented source files."""
        try:
            return len(list(self.project_root.rglob("*.py")))
        except:
            return 0
    
    def _count_documented_classes(self) -> int:
        """Count documented classes (approximate)."""
        try:
            count = 0
            for py_file in self.project_root.rglob("*.py"):
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                count += content.count("class ")
            return count
        except:
            return 0
    
    def _count_documented_functions(self) -> int:
        """Count documented functions (approximate)."""
        try:
            count = 0
            for py_file in self.project_root.rglob("*.py"):
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                count += content.count("def ")
            return count
        except:
            return 0
    
    def run_full_generation(self) -> Dict[str, any]:
        """
        @brief Run complete documentation generation process.
        
        @return Comprehensive generation results
        """
        print("🐝 **SWARM DOXYGEN GENERATOR ACTIVATED** 🐝")
        print("")
        
        # Check dependencies
        print("📋 Checking dependencies...")
        deps = self.check_dependencies()
        
        if not deps["doxygen"]:
            print("❌ Doxygen not found!")
            print(self.install_instructions())
            return {"success": False, "error": "Doxygen not installed"}
        
        if not deps["doxyfile"]:
            print("❌ Doxyfile not found!")
            return {"success": False, "error": "Doxyfile not found"}
        
        print("✅ Dependencies check passed")
        print("")
        
        # Generate documentation
        print("🚀 Generating documentation...")
        result = self.generate_documentation()
        
        if result["success"]:
            print(f"✅ Documentation generated successfully!")
            print(f"📁 Output directory: {result['output_dir']}")
            print(f"📄 Files generated: {result['files_generated']}")
            
            # Create index
            index_path = self.create_documentation_index()
            print(f"📋 Documentation index created: {index_path}")
            
            # Open documentation if possible
            html_index = self.html_dir / "index.html"
            if html_index.exists():
                print(f"🌐 Open documentation: {html_index}")
        else:
            print(f"❌ Documentation generation failed: {result.get('error', 'Unknown error')}")
            if result.get('stderr'):
                print(f"Error details: {result['stderr']}")
        
        return result


def main():
    """
    @brief Main entry point for Doxygen generation.
    
    @return Exit code (0 for success, 1 for failure)
    """
    generator = DoxygenGenerator()
    result = generator.run_full_generation()
    
    if result["success"]:
        print("")
        print("🎉 **DOXYGEN GENERATION COMPLETE** 🎉")
        print("📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory")
        return 0
    else:
        print("")
        print("❌ **DOXYGEN GENERATION FAILED** ❌")
        return 1


if __name__ == "__main__":
    exit(main())
