#!/usr/bin/env python3
"""
Version Detector
================

Handles version detection for various technologies.
Separates version detection from core technology detection.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import re
import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class VersionDetector:
    """Handles version detection for various technologies"""
    
    def __init__(self):
        """Initialize the version detector"""
        logger.info("Version Detector initialized")

    def detect_versions(self, repo_path: Path, tech_stack: Dict[str, Any]) -> Dict[str, str]:
        """Detect versions of detected technologies"""
        try:
            versions = {}
            
            # Python version detection
            if tech_stack.get("language") == "python":
                python_versions = self._detect_python_versions(repo_path)
                versions.update(python_versions)

            # Node.js version detection
            if tech_stack.get("language") == "javascript" or tech_stack.get("framework"):
                node_versions = self._detect_node_versions(repo_path)
                versions.update(node_versions)

            # Java version detection
            if tech_stack.get("language") == "java":
                java_versions = self._detect_java_versions(repo_path)
                versions.update(java_versions)

            # Go version detection
            if tech_stack.get("language") == "go":
                go_versions = self._detect_go_versions(repo_path)
                versions.update(go_versions)

            # Rust version detection
            if tech_stack.get("language") == "rust":
                rust_versions = self._detect_rust_versions(repo_path)
                versions.update(rust_versions)

            logger.debug(f"Detected versions: {versions}")
            return versions

        except Exception as e:
            logger.error(f"Failed to detect versions: {e}")
            return {}

    def _detect_python_versions(self, repo_path: Path) -> Dict[str, str]:
        """Detect Python package versions"""
        versions = {}
        
        requirements_file = repo_path / "requirements.txt"
        if requirements_file.exists():
            try:
                with open(requirements_file, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            # Extract version info
                            if "==" in line:
                                package, version = line.split("==", 1)
                                versions[f"python_{package}"] = version
                            elif ">=" in line:
                                package, version = line.split(">=", 1)
                                versions[f"python_{package}"] = f">={version}"
                            elif "~=" in line:
                                package, version = line.split("~=", 1)
                                versions[f"python_{package}"] = f"~={version}"
            except Exception as e:
                logger.debug(f"Failed to read requirements.txt: {e}")

        # Check pyproject.toml
        pyproject_file = repo_path / "pyproject.toml"
        if pyproject_file.exists():
            try:
                with open(pyproject_file, "r") as f:
                    content = f.read()
                    # Simple version extraction
                    version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                    if version_match:
                        versions["python_project"] = version_match.group(1)
            except Exception as e:
                logger.debug(f"Failed to read pyproject.toml: {e}")

        return versions

    def _detect_node_versions(self, repo_path: Path) -> Dict[str, str]:
        """Detect Node.js versions"""
        versions = {}
        
        package_file = repo_path / "package.json"
        if package_file.exists():
            try:
                with open(package_file, "r") as f:
                    package_data = json.load(f)
                    
                    # Node.js engine version
                    if "engines" in package_data and "node" in package_data["engines"]:
                        versions["nodejs"] = package_data["engines"]["node"]
                    
                    # Package version
                    if "version" in package_data:
                        versions["package"] = package_data["version"]
                        
                    # Dependencies versions
                    if "dependencies" in package_data:
                        for dep, version in package_data["dependencies"].items():
                            versions[f"npm_{dep}"] = version
                            
            except Exception as e:
                logger.debug(f"Failed to read package.json: {e}")

        return versions

    def _detect_java_versions(self, repo_path: Path) -> Dict[str, str]:
        """Detect Java versions"""
        versions = {}
        
        pom_file = repo_path / "pom.xml"
        if pom_file.exists():
            try:
                with open(pom_file, "r") as f:
                    content = f.read()
                    
                    # Java version
                    java_version_match = re.search(r'<java\.version>([^<]+)</java\.version>', content)
                    if java_version_match:
                        versions["java"] = java_version_match.group(1)
                    
                    # Maven version
                    maven_version_match = re.search(r'<maven\.version>([^<]+)</maven\.version>', content)
                    if maven_version_match:
                        versions["maven"] = maven_version_match.group(1)
                        
            except Exception as e:
                logger.debug(f"Failed to read pom.xml: {e}")

        # Check build.gradle
        gradle_file = repo_path / "build.gradle"
        if gradle_file.exists():
            try:
                with open(gradle_file, "r") as f:
                    content = f.read()
                    # Java version in gradle
                    java_version_match = re.search(r'javaVersion\s*=\s*["\']([^"\']+)["\']', content)
                    if java_version_match:
                        versions["java_gradle"] = java_version_match.group(1)
            except Exception as e:
                logger.debug(f"Failed to read build.gradle: {e}")

        return versions

    def _detect_go_versions(self, repo_path: Path) -> Dict[str, str]:
        """Detect Go versions"""
        versions = {}
        
        go_mod_file = repo_path / "go.mod"
        if go_mod_file.exists():
            try:
                with open(go_mod_file, "r") as f:
                    content = f.read()
                    # Go version
                    go_version_match = re.search(r'go\s+([\d.]+)', content)
                    if go_version_match:
                        versions["go"] = go_version_match.group(1)
            except Exception as e:
                logger.debug(f"Failed to read go.mod: {e}")

        return versions

    def _detect_rust_versions(self, repo_path: Path) -> Dict[str, str]:
        """Detect Rust versions"""
        versions = {}
        
        cargo_file = repo_path / "Cargo.toml"
        if cargo_file.exists():
            try:
                with open(cargo_file, "r") as f:
                    content = f.read()
                    # Rust version
                    rust_version_match = re.search(r'rust-version\s*=\s*["\']([^"\']+)["\']', content)
                    if rust_version_match:
                        versions["rust"] = rust_version_match.group(1)
            except Exception as e:
                logger.debug(f"Failed to read Cargo.toml: {e}")

        return versions

    def get_version_summary(self, versions: Dict[str, str]) -> Dict[str, Any]:
        """Get a summary of detected versions"""
        return {
            "total_versions": len(versions),
            "version_categories": {
                "python": len([k for k in versions.keys() if k.startswith("python")]),
                "nodejs": len([k for k in versions.keys() if k.startswith("npm_") or k == "nodejs"]),
                "java": len([k for k in versions.keys() if k.startswith("java") or k == "maven"]),
                "go": len([k for k in versions.keys() if k == "go"]),
                "rust": len([k for k in versions.keys() if k == "rust"]),
            },
            "versions": versions
        }

