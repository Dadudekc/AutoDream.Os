#!/usr/bin/env python3
"""
Intelligent Repository Scanner & Discovery System
================================================

Enterprise-grade repository discovery with:
- Automatic repository discovery
- Technology stack detection
- Market readiness evaluation
- Dependency analysis
- Architecture assessment
- Performance profiling

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import os
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import re
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TechnologyStack:
    """Detected technology stack information"""
    language: str = "unknown"
    version: str = "unknown"
    framework: Optional[str] = None
    database: Optional[str] = None
    frontend: Optional[str] = None
    backend: Optional[str] = None
    cloud: Optional[str] = None
    container: Optional[str] = None
    ci_cd: Optional[str] = None
    testing: Optional[str] = None
    documentation: Optional[str] = None
    confidence: float = 0.0


@dataclass
class RepositoryMetadata:
    """Repository metadata and analysis results"""
    repository_id: str
    name: str
    path: str
    size_bytes: int = 0
    file_count: int = 0
    language_count: int = 0
    last_modified: datetime = field(default_factory=datetime.now)
    technology_stack: TechnologyStack = field(default_factory=TechnologyStack)
    health_score: float = 0.0
    market_readiness: float = 0.0
    dependencies: List[str] = field(default_factory=list)
    architecture_patterns: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    security_analysis: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class DiscoveryConfig:
    """Discovery configuration settings"""
    scan_depth: int = 3
    max_file_size_mb: int = 10
    excluded_patterns: List[str] = field(default_factory=lambda: [
        "*.pyc", "*.pyo", "__pycache__", ".git", ".svn", "node_modules", 
        "*.log", "*.tmp", "*.cache", ".DS_Store", "Thumbs.db"
    ])
    included_extensions: List[str] = field(default_factory=lambda: [
        ".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".cs", ".go", 
        ".rs", ".php", ".rb", ".swift", ".kt", ".scala", ".html", ".css",
        ".xml", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf"
    ])
    technology_patterns: Dict[str, List[str]] = field(default_factory=lambda: {
        "python": ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile"],
        "javascript": ["package.json", "yarn.lock", "package-lock.json"],
        "java": ["pom.xml", "build.gradle", "gradle.properties"],
        "go": ["go.mod", "go.sum", "Gopkg.toml"],
        "rust": ["Cargo.toml", "Cargo.lock"],
        "php": ["composer.json", "composer.lock"],
        "ruby": ["Gemfile", "Gemfile.lock", "Rakefile"],
        "dotnet": ["*.csproj", "*.vbproj", "*.sln", "packages.config"]
    })


class IntelligentRepositoryScanner:
    """
    Intelligent repository scanning and discovery system
    
    Features:
    - Automatic repository discovery
    - Technology stack detection
    - Market readiness evaluation
    - Dependency analysis
    - Architecture assessment
    - Performance profiling
    """
    
    def __init__(self, config: Optional[DiscoveryConfig] = None):
        """Initialize the intelligent repository scanner"""
        self.config = config or DiscoveryConfig()
        self.discovered_repositories: Dict[str, RepositoryMetadata] = {}
        self.scan_cache: Dict[str, Any] = {}
        self.scan_history: List[Dict[str, Any]] = []
        self.technology_database = self._load_technology_database()
        
        logger.info("Intelligent Repository Scanner initialized")
    
    def _load_technology_database(self) -> Dict[str, Any]:
        """Load technology detection patterns and rules"""
        return {
            "languages": {
                "python": {
                    "extensions": [".py", ".pyw", ".pyx"],
                    "files": ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile"],
                    "patterns": [r"import\s+\w+", r"from\s+\w+\s+import", r"def\s+\w+\s*\("]
                },
                "javascript": {
                    "extensions": [".js", ".jsx", ".ts", ".tsx"],
                    "files": ["package.json", "yarn.lock", "package-lock.json"],
                    "patterns": [r"import\s+.*\s+from", r"require\s*\(", r"export\s+"]
                },
                "java": {
                    "extensions": [".java", ".class", ".jar"],
                    "files": ["pom.xml", "build.gradle", "gradle.properties"],
                    "patterns": [r"import\s+\w+", r"public\s+class", r"@\w+"]
                },
                "go": {
                    "extensions": [".go"],
                    "files": ["go.mod", "go.sum", "Gopkg.toml"],
                    "patterns": [r"package\s+\w+", r"import\s+\(", r"func\s+\w+\s*\("]
                },
                "rust": {
                    "extensions": [".rs"],
                    "files": ["Cargo.toml", "Cargo.lock"],
                    "patterns": [r"use\s+\w+", r"fn\s+\w+\s*\(", r"struct\s+\w+"]
                }
            },
            "frameworks": {
                "django": {"patterns": [r"from\s+django", r"INSTALLED_APPS", r"MIDDLEWARE"]},
                "flask": {"patterns": [r"from\s+flask", r"Flask\(", r"@app\.route"]},
                "react": {"patterns": [r"import\s+React", r"useState", r"useEffect"]},
                "angular": {"patterns": [r"@Component", r"@Injectable", r"@NgModule"]},
                "spring": {"patterns": [r"@SpringBootApplication", r"@RestController", r"@Service"]}
            },
            "databases": {
                "postgresql": {"patterns": [r"psycopg2", r"postgresql", r"postgres"]},
                "mysql": {"patterns": [r"mysql-connector", r"mysqldb", r"mysql"]},
                "mongodb": {"patterns": [r"pymongo", r"mongodb", r"mongoose"]},
                "redis": {"patterns": [r"redis", r"redis-py", r"ioredis"]}
            }
        }
    
    def discover_repositories(self, root_path: str, recursive: bool = True) -> List[str]:
        """Discover repositories in the given path"""
        try:
            discovered = []
            root = Path(root_path)
            
            if not root.exists():
                logger.error(f"Root path does not exist: {root_path}")
                return discovered
            
            # Look for common repository indicators
            repository_indicators = [
                ".git", ".svn", ".hg", "package.json", "requirements.txt", 
                "pom.xml", "build.gradle", "Cargo.toml", "go.mod", "*.sln"
            ]
            
            if recursive:
                # Recursive discovery
                for indicator in repository_indicators:
                    if "*" in indicator:
                        # Pattern matching
                        for path in root.rglob(indicator.replace("*", "*")):
                            repo_path = path.parent if path.is_file() else path
                            if str(repo_path) not in discovered:
                                discovered.append(str(repo_path))
                                logger.info(f"Discovered repository: {repo_path}")
                    else:
                        # Exact file/directory matching
                        for path in root.rglob(indicator):
                            repo_path = path.parent if path.is_file() else path
                            if str(repo_path) not in discovered:
                                discovered.append(str(repo_path))
                                logger.info(f"Discovered repository: {repo_path}")
            else:
                # Non-recursive discovery (only immediate subdirectories)
                for item in root.iterdir():
                    if item.is_dir():
                        for indicator in repository_indicators:
                            indicator_path = item / indicator
                            if indicator_path.exists():
                                if str(item) not in discovered:
                                    discovered.append(str(item))
                                    logger.info(f"Discovered repository: {item}")
                                break
            
            logger.info(f"Discovered {len(discovered)} repositories in {root_path}")
            return discovered
            
        except Exception as e:
            logger.error(f"Failed to discover repositories: {e}")
            return []
    
    def scan_repository(self, repository_path: str, deep_scan: bool = False) -> Optional[RepositoryMetadata]:
        """Scan a single repository for comprehensive analysis"""
        try:
            repo_path = Path(repository_path)
            if not repo_path.exists():
                logger.error(f"Repository path does not exist: {repository_path}")
                return None
            
            # Check cache first
            cache_key = f"{repository_path}_{deep_scan}"
            if cache_key in self.scan_cache:
                logger.info(f"Using cached scan results for {repository_path}")
                return self.scan_cache[cache_key]
            
            logger.info(f"Scanning repository: {repository_path}")
            
            # Create repository metadata
            metadata = RepositoryMetadata(
                repository_id=f"repo_{hash(str(repository_path))}",
                name=repo_path.name,
                path=str(repository_path)
            )
            
            # Basic repository analysis
            self._analyze_basic_metadata(metadata, repo_path)
            
            # Technology stack detection
            self._detect_technology_stack(metadata, repo_path)
            
            # Dependency analysis
            self._analyze_dependencies(metadata, repo_path)
            
            # Architecture patterns
            self._detect_architecture_patterns(metadata, repo_path)
            
            # Performance metrics
            self._analyze_performance(metadata, repo_path)
            
            # Security analysis
            self._analyze_security(metadata, repo_path)
            
            # Calculate scores
            self._calculate_scores(metadata)
            
            # Generate recommendations
            self._generate_recommendations(metadata)
            
            # Cache results
            self.scan_cache[cache_key] = metadata
            
            # Update discovered repositories
            self.discovered_repositories[metadata.repository_id] = metadata
            
            # Record scan history
            self.scan_history.append({
                "timestamp": datetime.now().isoformat(),
                "repository_id": metadata.repository_id,
                "scan_type": "deep" if deep_scan else "basic",
                "duration": time.time()
            })
            
            logger.info(f"Repository scan completed: {repository_path}")
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to scan repository {repository_path}: {e}")
            return None
    
    def _analyze_basic_metadata(self, metadata: RepositoryMetadata, repo_path: Path):
        """Analyze basic repository metadata"""
        try:
            # Calculate repository size
            total_size = 0
            file_count = 0
            language_files = {}
            
            for file_path in repo_path.rglob("*"):
                if file_path.is_file():
                    # Check if file should be excluded
                    if self._should_exclude_file(file_path):
                        continue
                    
                    # Check file size
                    try:
                        file_size = file_path.stat().st_size
                        if file_size <= self.config.max_file_size_mb * 1024 * 1024:
                            total_size += file_size
                            file_count += 1
                            
                            # Count files by extension
                            ext = file_path.suffix.lower()
                            if ext in self.config.included_extensions:
                                language_files[ext] = language_files.get(ext, 0) + 1
                    except (OSError, PermissionError):
                        continue
            
            metadata.size_bytes = total_size
            metadata.file_count = file_count
            metadata.language_count = len(language_files)
            
            # Get last modified time
            try:
                metadata.last_modified = datetime.fromtimestamp(repo_path.stat().st_mtime)
            except (OSError, PermissionError):
                pass
            
            logger.debug(f"Basic metadata: size={total_size}, files={file_count}, languages={len(language_files)}")
            
        except Exception as e:
            logger.error(f"Failed to analyze basic metadata: {e}")
    
    def _should_exclude_file(self, file_path: Path) -> bool:
        """Check if a file should be excluded from analysis"""
        for pattern in self.config.excluded_patterns:
            if "*" in pattern:
                # Wildcard pattern matching
                if file_path.match(pattern):
                    return True
            else:
                # Exact name matching
                if file_path.name == pattern or file_path.name.endswith(pattern):
                    return True
        
        return False
    
    def _detect_technology_stack(self, metadata: RepositoryMetadata, repo_path: Path):
        """Detect technology stack and versions"""
        try:
            detected_languages = set()
            detected_frameworks = set()
            detected_databases = set()
            
            # Scan for language-specific files and patterns
            for language, config in self.technology_database["languages"].items():
                # Check for language-specific files
                for file_name in config["files"]:
                    if (repo_path / file_name).exists():
                        detected_languages.add(language)
                        break
                
                # Check for language-specific patterns in code files
                if language in detected_languages:
                    continue
                
                for ext in config["extensions"]:
                    for file_path in repo_path.rglob(f"*{ext}"):
                        if self._should_exclude_file(file_path):
                            continue
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                for pattern in config["patterns"]:
                                    if re.search(pattern, content, re.IGNORECASE):
                                        detected_languages.add(language)
                                        break
                                if language in detected_languages:
                                    break
                        except (OSError, UnicodeDecodeError):
                            continue
            
            # Detect frameworks
            for framework, config in self.technology_database["frameworks"].items():
                for file_path in repo_path.rglob("*"):
                    if file_path.is_file() and not self._should_exclude_file(file_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                for pattern in config["patterns"]:
                                    if re.search(pattern, content, re.IGNORECASE):
                                        detected_frameworks.add(framework)
                                        break
                                if framework in detected_frameworks:
                                    break
                        except (OSError, UnicodeDecodeError):
                            continue
            
            # Detect databases
            for database, config in self.technology_database["databases"].items():
                for file_path in repo_path.rglob("*"):
                    if file_path.is_file() and not self._should_exclude_file(file_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                for pattern in config["patterns"]:
                                    if re.search(pattern, content, re.IGNORECASE):
                                        detected_databases.add(database)
                                        break
                                if database in detected_databases:
                                    break
                        except (OSError, UnicodeDecodeError):
                            continue
            
            # Update metadata
            if detected_languages:
                primary_language = list(detected_languages)[0]
                metadata.technology_stack.language = primary_language
                metadata.technology_stack.confidence = 0.8
            
            if detected_frameworks:
                metadata.technology_stack.framework = ", ".join(detected_frameworks)
            
            if detected_databases:
                metadata.technology_stack.database = ", ".join(detected_databases)
            
            logger.debug(f"Technology stack: {detected_languages}, {detected_frameworks}, {detected_databases}")
            
        except Exception as e:
            logger.error(f"Failed to detect technology stack: {e}")
    
    def _analyze_dependencies(self, metadata: RepositoryMetadata, repo_path: Path):
        """Analyze project dependencies"""
        try:
            dependencies = []
            
            # Python dependencies
            requirements_file = repo_path / "requirements.txt"
            if requirements_file.exists():
                try:
                    with open(requirements_file, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#"):
                                dependencies.append(f"python:{line}")
                except Exception as e:
                    logger.debug(f"Failed to read requirements.txt: {e}")
            
            # Node.js dependencies
            package_file = repo_path / "package.json"
            if package_file.exists():
                try:
                    with open(package_file, 'r') as f:
                        package_data = json.load(f)
                        if "dependencies" in package_data:
                            for dep, version in package_data["dependencies"].items():
                                dependencies.append(f"nodejs:{dep}@{version}")
                        if "devDependencies" in package_data:
                            for dep, version in package_data["devDependencies"].items():
                                dependencies.append(f"nodejs:{dep}@{version} (dev)")
                except Exception as e:
                    logger.debug(f"Failed to read package.json: {e}")
            
            # Java dependencies
            pom_file = repo_path / "pom.xml"
            if pom_file.exists():
                try:
                    with open(pom_file, 'r') as f:
                        content = f.read()
                        # Simple dependency extraction (in real implementation, use XML parser)
                        deps = re.findall(r'<artifactId>([^<]+)</artifactId>', content)
                        for dep in deps:
                            dependencies.append(f"java:{dep}")
                except Exception as e:
                    logger.debug(f"Failed to read pom.xml: {e}")
            
            metadata.dependencies = dependencies
            logger.debug(f"Dependencies: {len(dependencies)} found")
            
        except Exception as e:
            logger.error(f"Failed to analyze dependencies: {e}")
    
    def _detect_architecture_patterns(self, metadata: RepositoryMetadata, repo_path: Path):
        """Detect common architecture patterns"""
        try:
            patterns = []
            
            # Check for common directory structures
            if (repo_path / "src").exists():
                patterns.append("src-based-structure")
            
            if (repo_path / "app").exists():
                patterns.append("app-based-structure")
            
            if (repo_path / "lib").exists():
                patterns.append("library-structure")
            
            if (repo_path / "tests").exists() or (repo_path / "test").exists():
                patterns.append("test-separation")
            
            if (repo_path / "docs").exists() or (repo_path / "documentation").exists():
                patterns.append("documentation-separation")
            
            if (repo_path / "config").exists() or (repo_path / "conf").exists():
                patterns.append("configuration-separation")
            
            # Check for specific architecture files
            if (repo_path / "docker-compose.yml").exists() or (repo_path / "Dockerfile").exists():
                patterns.append("containerized")
            
            if (repo_path / ".github").exists() or (repo_path / "Jenkinsfile").exists():
                patterns.append("ci-cd-integration")
            
            if (repo_path / "api").exists() or (repo_path / "routes").exists():
                patterns.append("api-focused")
            
            metadata.architecture_patterns = patterns
            logger.debug(f"Architecture patterns: {patterns}")
            
        except Exception as e:
            logger.error(f"Failed to detect architecture patterns: {e}")
    
    def _analyze_performance(self, metadata: RepositoryMetadata, repo_path: Path):
        """Analyze performance characteristics"""
        try:
            performance_metrics = {}
            
            # File size distribution
            file_sizes = []
            for file_path in repo_path.rglob("*"):
                if file_path.is_file() and not self._should_exclude_file(file_path):
                    try:
                        size = file_path.stat().st_size
                        file_sizes.append(size)
                    except (OSError, PermissionError):
                        continue
            
            if file_sizes:
                performance_metrics["total_files"] = len(file_sizes)
                performance_metrics["average_file_size"] = sum(file_sizes) / len(file_sizes)
                performance_metrics["largest_file_size"] = max(file_sizes)
                performance_metrics["file_size_distribution"] = {
                    "small": len([s for s in file_sizes if s < 1024]),
                    "medium": len([s for s in file_sizes if 1024 <= s < 10240]),
                    "large": len([s for s in file_sizes if s >= 10240])
                }
            
            # Language complexity (simple heuristic)
            code_files = 0
            for ext in [".py", ".js", ".java", ".cpp", ".c", ".cs", ".go", ".rs"]:
                code_files += len(list(repo_path.rglob(f"*{ext}")))
            
            performance_metrics["code_files"] = code_files
            performance_metrics["complexity_score"] = min(100, code_files * 2)  # Simple heuristic
            
            metadata.performance_metrics = performance_metrics
            logger.debug(f"Performance metrics: {performance_metrics}")
            
        except Exception as e:
            logger.error(f"Failed to analyze performance: {e}")
    
    def _analyze_security(self, metadata: RepositoryMetadata, repo_path: Path):
        """Analyze security characteristics"""
        try:
            security_analysis = {}
            
            # Check for security-related files
            security_files = []
            for pattern in [".env", ".env.*", "*.key", "*.pem", "*.p12", "secrets.*", "config.*"]:
                for file_path in repo_path.rglob(pattern):
                    if not self._should_exclude_file(file_path):
                        security_files.append(str(file_path.relative_to(repo_path)))
            
            security_analysis["security_files"] = security_files
            security_analysis["has_secrets"] = len(security_files) > 0
            
            # Check for common security issues
            security_issues = []
            
            # Check for hardcoded secrets in code
            for ext in [".py", ".js", ".java", ".cpp", ".c", ".cs", ".go", ".rs"]:
                for file_path in repo_path.rglob(f"*{ext}"):
                    if self._should_exclude_file(file_path):
                        continue
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            # Check for hardcoded secrets
                            if re.search(r'password\s*=\s*["\'][^"\']+["\']', content, re.IGNORECASE):
                                security_issues.append("hardcoded_password")
                            
                            if re.search(r'api_key\s*=\s*["\'][^"\']+["\']', content, re.IGNORECASE):
                                security_issues.append("hardcoded_api_key")
                            
                            if re.search(r'secret\s*=\s*["\'][^"\']+["\']', content, re.IGNORECASE):
                                security_issues.append("hardcoded_secret")
                    except (OSError, UnicodeDecodeError):
                        continue
            
            security_analysis["security_issues"] = list(set(security_issues))
            security_analysis["security_score"] = max(0, 100 - len(security_issues) * 20)
            
            metadata.security_analysis = security_analysis
            logger.debug(f"Security analysis: {security_analysis}")
            
        except Exception as e:
            logger.error(f"Failed to analyze security: {e}")
    
    def _calculate_scores(self, metadata: RepositoryMetadata):
        """Calculate health and market readiness scores"""
        try:
            # Health score calculation
            health_factors = []
            
            # File organization (25%)
            if metadata.architecture_patterns:
                health_factors.append(25)
            else:
                health_factors.append(10)
            
            # Testing presence (20%)
            if "test-separation" in metadata.architecture_patterns:
                health_factors.append(20)
            else:
                health_factors.append(5)
            
            # Documentation (20%)
            if "documentation-separation" in metadata.architecture_patterns:
                health_factors.append(20)
            else:
                health_factors.append(5)
            
            # Configuration management (15%)
            if "configuration-separation" in metadata.architecture_patterns:
                health_factors.append(15)
            else:
                health_factors.append(5)
            
            # CI/CD integration (20%)
            if "ci-cd-integration" in metadata.architecture_patterns:
                health_factors.append(20)
            else:
                health_factors.append(5)
            
            metadata.health_score = sum(health_factors)
            
            # Market readiness score calculation
            readiness_factors = []
            
            # Technology stack completeness (30%)
            if metadata.technology_stack.language:
                readiness_factors.append(30)
            if metadata.technology_stack.framework:
                readiness_factors.append(20)
            if metadata.technology_stack.database:
                readiness_factors.append(10)
            
            # Architecture maturity (40%)
            if len(metadata.architecture_patterns) >= 3:
                readiness_factors.append(40)
            elif len(metadata.architecture_patterns) >= 2:
                readiness_factors.append(25)
            elif len(metadata.architecture_patterns) >= 1:
                readiness_factors.append(15)
            
            # Security posture (30%)
            if metadata.security_analysis.get("security_score", 0) >= 80:
                readiness_factors.append(30)
            elif metadata.security_analysis.get("security_score", 0) >= 60:
                readiness_factors.append(20)
            elif metadata.security_analysis.get("security_score", 0) >= 40:
                readiness_factors.append(10)
            
            metadata.market_readiness = min(100, sum(readiness_factors))
            
            logger.debug(f"Scores: health={metadata.health_score}, readiness={metadata.market_readiness}")
            
        except Exception as e:
            logger.error(f"Failed to calculate scores: {e}")
    
    def _generate_recommendations(self, metadata: RepositoryMetadata):
        """Generate improvement recommendations"""
        try:
            recommendations = []
            
            # Health score recommendations
            if metadata.health_score < 50:
                recommendations.append("Critical: Repository needs significant restructuring")
            elif metadata.health_score < 70:
                recommendations.append("High: Repository needs moderate improvements")
            elif metadata.health_score < 85:
                recommendations.append("Medium: Repository could benefit from minor improvements")
            else:
                recommendations.append("Low: Repository is in good health")
            
            # Specific recommendations based on missing patterns
            if "test-separation" not in metadata.architecture_patterns:
                recommendations.append("Add dedicated test directory and testing framework")
            
            if "documentation-separation" not in metadata.architecture_patterns:
                recommendations.append("Create documentation directory with README and guides")
            
            if "configuration-separation" not in metadata.architecture_patterns:
                recommendations.append("Separate configuration from code")
            
            if "ci-cd-integration" not in metadata.architecture_patterns:
                recommendations.append("Integrate CI/CD pipeline for automated testing and deployment")
            
            if "containerized" not in metadata.architecture_patterns:
                recommendations.append("Consider containerization for consistent deployment")
            
            # Security recommendations
            if metadata.security_analysis.get("has_secrets", False):
                recommendations.append("Move secrets to environment variables or secure configuration")
            
            if metadata.security_analysis.get("security_score", 100) < 80:
                recommendations.append("Review and fix security issues identified in analysis")
            
            # Technology stack recommendations
            if not metadata.technology_stack.framework:
                recommendations.append("Consider adding a framework for better structure and features")
            
            if not metadata.technology_stack.database:
                recommendations.append("Evaluate if database integration would benefit the project")
            
            metadata.recommendations = recommendations
            logger.debug(f"Generated {len(recommendations)} recommendations")
            
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
    
    def scan_multiple_repositories(self, repository_paths: List[str], 
                                 max_workers: int = 4) -> List[RepositoryMetadata]:
        """Scan multiple repositories in parallel"""
        try:
            results = []
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_path = {
                    executor.submit(self.scan_repository, path): path 
                    for path in repository_paths
                }
                
                for future in future_to_path:
                    try:
                        metadata = future.result()
                        if metadata:
                            results.append(metadata)
                    except Exception as e:
                        path = future_to_path[future]
                        logger.error(f"Failed to scan repository {path}: {e}")
            
            logger.info(f"Completed scanning {len(results)} repositories")
            return results
            
        except Exception as e:
            logger.error(f"Failed to scan multiple repositories: {e}")
            return []
    
    def get_discovery_summary(self) -> Dict[str, Any]:
        """Get a summary of all discovered repositories"""
        try:
            summary = {
                "total_repositories": len(self.discovered_repositories),
                "total_size_mb": sum(r.size_bytes for r in self.discovered_repositories.values()) / (1024 * 1024),
                "average_health_score": sum(r.health_score for r in self.discovered_repositories.values()) / len(self.discovered_repositories) if self.discovered_repositories else 0,
                "average_market_readiness": sum(r.market_readiness for r in self.discovered_repositories.values()) / len(self.discovered_repositories) if self.discovered_repositories else 0,
                "technology_distribution": {},
                "architecture_patterns": {},
                "scan_history": self.scan_history[-10:] if self.scan_history else []
            }
            
            # Technology distribution
            for repo in self.discovered_repositories.values():
                lang = repo.technology_stack.language
                if lang:
                    summary["technology_distribution"][lang] = summary["technology_distribution"].get(lang, 0) + 1
            
            # Architecture patterns
            for repo in self.discovered_repositories.values():
                for pattern in repo.architecture_patterns:
                    summary["architecture_patterns"][pattern] = summary["architecture_patterns"].get(pattern, 0) + 1
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get discovery summary: {e}")
            return {"error": str(e)}
    
    def export_discovery_report(self, output_path: str = None) -> str:
        """Export discovery results to JSON report"""
        try:
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"repository_discovery_report_{timestamp}.json"
            
            report_data = {
                "scan_timestamp": datetime.now().isoformat(),
                "discovery_summary": self.get_discovery_summary(),
                "repositories": [
                    {
                        "repository_id": repo.repository_id,
                        "name": repo.name,
                        "path": repo.path,
                        "size_bytes": repo.size_bytes,
                        "file_count": repo.file_count,
                        "technology_stack": {
                            "language": repo.technology_stack.language,
                            "framework": repo.technology_stack.framework,
                            "database": repo.technology_stack.database
                        },
                        "health_score": repo.health_score,
                        "market_readiness": repo.market_readiness,
                        "architecture_patterns": repo.architecture_patterns,
                        "dependencies": repo.dependencies,
                        "recommendations": repo.recommendations
                    }
                    for repo in self.discovered_repositories.values()
                ]
            }
            
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            logger.info(f"Discovery report exported to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to export discovery report: {e}")
            return ""


def main():
    """Main function for standalone testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Intelligent Repository Scanner")
    parser.add_argument("--discover", type=str, help="Discover repositories in path")
    parser.add_argument("--scan", type=str, help="Scan specific repository")
    parser.add_argument("--scan-all", type=str, help="Scan all repositories in path")
    parser.add_argument("--export", action="store_true", help="Export discovery report")
    
    args = parser.parse_args()
    
    scanner = IntelligentRepositoryScanner()
    
    try:
        if args.discover:
            print(f"🔍 Discovering repositories in: {args.discover}")
            repositories = scanner.discover_repositories(args.discover)
            print(f"✅ Discovered {len(repositories)} repositories:")
            for repo in repositories[:10]:  # Show first 10
                print(f"  - {repo}")
            if len(repositories) > 10:
                print(f"  ... and {len(repositories) - 10} more")
        
        elif args.scan:
            print(f"🔍 Scanning repository: {args.scan}")
            metadata = scanner.scan_repository(args.scan, deep_scan=True)
            if metadata:
                print(f"✅ Repository scan completed:")
                print(f"  Name: {metadata.name}")
                print(f"  Language: {metadata.technology_stack.language}")
                print(f"  Framework: {metadata.technology_stack.framework}")
                print(f"  Health Score: {metadata.health_score}/100")
                print(f"  Market Readiness: {metadata.market_readiness}/100")
                print(f"  Architecture Patterns: {', '.join(metadata.architecture_patterns)}")
                print(f"  Dependencies: {len(metadata.dependencies)}")
                print(f"  Recommendations: {len(metadata.recommendations)}")
            else:
                print("❌ Repository scan failed")
        
        elif args.scan_all:
            print(f"🔍 Scanning all repositories in: {args.scan_all}")
            repositories = scanner.discover_repositories(args.scan_all)
            if repositories:
                results = scanner.scan_multiple_repositories(repositories)
                print(f"✅ Scanned {len(results)} repositories")
                
                # Show summary
                summary = scanner.get_discovery_summary()
                print(f"📊 Discovery Summary:")
                print(f"  Total Repositories: {summary['total_repositories']}")
                print(f"  Average Health Score: {summary['average_health_score']:.1f}/100")
                print(f"  Average Market Readiness: {summary['average_market_readiness']:.1f}/100")
                print(f"  Total Size: {summary['total_size_mb']:.1f} MB")
            else:
                print("❌ No repositories found to scan")
        
        elif args.export:
            if scanner.discovered_repositories:
                output_file = scanner.export_discovery_report()
                print(f"📄 Discovery report exported to: {output_file}")
            else:
                print("❌ No repositories to export. Run discovery first.")
        
        else:
            print("🔍 Intelligent Repository Scanner ready")
            print("Use --discover <path> to discover repositories")
            print("Use --scan <path> to scan a specific repository")
            print("Use --scan-all <path> to scan all repositories in a path")
            print("Use --export to export discovery report")
        
    except Exception as e:
        print(f"❌ Operation failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
