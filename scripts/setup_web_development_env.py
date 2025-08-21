#!/usr/bin/env python3
"""
Web Development Environment Setup Script
Agent_Cellphone_V2_Repository TDD Integration Project

This script sets up the complete web development environment including:
- Selenium WebDriver setup
- Flask and FastAPI configuration
- TDD testing infrastructure
- Code quality tools
- Development environment configuration

Author: Web Development & UI Framework Specialist
License: MIT
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path
from typing import List, Dict, Any

class WebDevelopmentEnvironmentSetup:
    """Setup and configure web development environment for TDD integration"""
    
    def __init__(self, repo_root: str = None):
        self.repo_root = Path(repo_root) if repo_root else Path(__file__).parent.parent
        self.scripts_dir = self.repo_root / "scripts"
        self.src_dir = self.repo_root / "src"
        self.tests_dir = self.repo_root / "tests"
        self.web_dir = self.src_dir / "web"
        self.config_dir = self.repo_root / "config"
        
        # Environment configuration
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.os_platform = platform.system().lower()
        self.is_windows = self.os_platform == "windows"
        
        print(f"🚀 Setting up Web Development Environment")
        print(f"📍 Repository: {self.repo_root}")
        print(f"🐍 Python Version: {self.python_version}")
        print(f"💻 Platform: {self.os_platform}")
        print("-" * 60)
    
    def setup_dependencies(self) -> bool:
        """Install all web development dependencies"""
        print("📦 Installing Web Development Dependencies...")
        
        try:
            # Install core requirements
            requirements_file = self.repo_root / "requirements_web_development.txt"
            if requirements_file.exists():
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
                ], check=True, capture_output=True)
                print("✅ Core dependencies installed successfully")
            else:
                print("❌ requirements_web_development.txt not found")
                return False
            
            # Install additional development tools
            dev_tools = [
                "pip-tools",
                "pipdeptree",
                "safety"
            ]
            
            for tool in dev_tools:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", tool
                ], check=True, capture_output=True)
                print(f"✅ {tool} installed")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
    
    def setup_selenium_webdriver(self) -> bool:
        """Setup Selenium WebDriver for web automation"""
        print("🌐 Setting up Selenium WebDriver...")
        
        try:
            # Install webdriver-manager for automatic driver management
            subprocess.run([
                sys.executable, "-m", "pip", "install", "webdriver-manager"
            ], check=True, capture_output=True)
            
            # Create Selenium configuration
            selenium_config = {
                "webdriver": {
                    "chrome": {
                        "driver_path": "auto",
                        "options": [
                            "--headless",
                            "--no-sandbox",
                            "--disable-dev-shm-usage",
                            "--disable-gpu"
                        ]
                    },
                    "firefox": {
                        "driver_path": "auto",
                        "options": ["--headless"]
                    },
                    "edge": {
                        "driver_path": "auto",
                        "options": ["--headless"]
                    }
                },
                "timeouts": {
                    "implicit_wait": 10,
                    "page_load": 30,
                    "script": 30
                },
                "retry_attempts": 3
            }
            
            config_file = self.config_dir / "selenium_config.json"
            config_file.parent.mkdir(exist_ok=True)
            
            with open(config_file, 'w') as f:
                json.dump(selenium_config, f, indent=2)
            
            print("✅ Selenium WebDriver configured successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up Selenium: {e}")
            return False
    
    def setup_flask_environment(self) -> bool:
        """Setup Flask development environment"""
        print("🔥 Setting up Flask Environment...")
        
        try:
            # Create Flask configuration
            flask_config = {
                "development": {
                    "DEBUG": True,
                    "TESTING": False,
                    "SECRET_KEY": "dev-secret-key-change-in-production",
                    "DATABASE_URI": "sqlite:///dev.db",
                    "LOG_LEVEL": "DEBUG"
                },
                "testing": {
                    "DEBUG": False,
                    "TESTING": True,
                    "SECRET_KEY": "test-secret-key",
                    "DATABASE_URI": "sqlite:///test.db",
                    "LOG_LEVEL": "INFO"
                },
                "production": {
                    "DEBUG": False,
                    "TESTING": False,
                    "SECRET_KEY": "change-this-in-production",
                    "DATABASE_URI": "sqlite:///prod.db",
                    "LOG_LEVEL": "WARNING"
                }
            }
            
            config_file = self.config_dir / "flask_config.json"
            config_file.parent.mkdir(exist_ok=True)
            
            with open(config_file, 'w') as f:
                json.dump(flask_config, f, indent=2)
            
            print("✅ Flask environment configured successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up Flask: {e}")
            return False
    
    def setup_fastapi_environment(self) -> bool:
        """Setup FastAPI development environment"""
        print("⚡ Setting up FastAPI Environment...")
        
        try:
            # Create FastAPI configuration
            fastapi_config = {
                "app": {
                    "title": "Agent_Cellphone_V2 API",
                    "description": "TDD Integration Web API",
                    "version": "2.0.0",
                    "docs_url": "/docs",
                    "redoc_url": "/redoc"
                },
                "server": {
                    "host": "0.0.0.0",
                    "port": 8000,
                    "reload": True
                },
                "database": {
                    "url": "sqlite:///./fastapi.db",
                    "echo": False
                },
                "cors": {
                    "origins": ["*"],
                    "methods": ["GET", "POST", "PUT", "DELETE"],
                    "headers": ["*"]
                }
            }
            
            config_file = self.config_dir / "fastapi_config.json"
            config_file.parent.mkdir(exist_ok=True)
            
            with open(config_file, 'w') as f:
                json.dump(fastapi_config, f, indent=2)
            
            print("✅ FastAPI environment configured successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up FastAPI: {e}")
            return False
    
    def setup_tdd_infrastructure(self) -> bool:
        """Setup TDD testing infrastructure"""
        print("🧪 Setting up TDD Testing Infrastructure...")
        
        try:
            # Create pytest configuration
            pytest_config = f"""
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-report=xml
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    web: marks tests as web tests
    selenium: marks tests as selenium tests
    flask: marks tests as flask tests
    fastapi: marks tests as fastapi tests
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
"""
            
            pytest_file = self.repo_root / "pytest.ini"
            with open(pytest_file, 'w') as f:
                f.write(pytest_config)
            
            # Create test configuration
            test_config = {
                "test_environment": {
                    "base_url": "http://localhost:5000",
                    "api_base_url": "http://localhost:8000",
                    "selenium": {
                        "browser": "chrome",
                        "headless": True,
                        "timeout": 30
                    },
                    "database": {
                        "test_db": "sqlite:///test.db",
                        "cleanup_after_tests": True
                    }
                },
                "test_data": {
                    "fixtures_dir": "tests/fixtures",
                    "mocks_dir": "tests/mocks",
                    "test_users": [
                        {"username": "test_user", "password": "test_pass"},
                        {"username": "admin_user", "password": "admin_pass"}
                    ]
                }
            }
            
            test_config_file = self.config_dir / "test_config.json"
            test_config_file.parent.mkdir(exist_ok=True)
            
            with open(test_config_file, 'w') as f:
                json.dump(test_config, f, indent=2)
            
            print("✅ TDD infrastructure configured successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up TDD infrastructure: {e}")
            return False
    
    def setup_development_tools(self) -> bool:
        """Setup development tools and pre-commit hooks"""
        print("🛠️ Setting up Development Tools...")
        
        try:
            # Create pre-commit configuration
            precommit_config = {
                "repos": [
                    {
                        "repo": "https://github.com/pre-commit/pre-commit-hooks",
                        "rev": "v4.4.0",
                        "hooks": [
                            {"id": "trailing-whitespace"},
                            {"id": "end-of-file-fixer"},
                            {"id": "check-yaml"},
                            {"id": "check-added-large-files"},
                            {"id": "check-merge-conflict"}
                        ]
                    },
                    {
                        "repo": "https://github.com/psf/black",
                        "rev": "23.11.0",
                        "hooks": [{"id": "black"}]
                    },
                    {
                        "repo": "https://github.com/pycqa/isort",
                        "rev": "5.12.0",
                        "hooks": [{"id": "isort"}]
                    },
                    {
                        "repo": "https://github.com/pycqa/flake8",
                        "rev": "6.1.0",
                        "hooks": [{"id": "flake8"}]
                    }
                ]
            }
            
            precommit_file = self.repo_root / ".pre-commit-config.yaml"
            with open(precommit_file, 'w') as f:
                import yaml
                yaml.dump(precommit_config, f, default_flow_style=False)
            
            # Install pre-commit hooks
            subprocess.run([
                sys.executable, "-m", "pre_commit", "install"
            ], check=True, capture_output=True)
            
            print("✅ Development tools configured successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up development tools: {e}")
            return False
    
    def create_web_structure(self) -> bool:
        """Create enhanced web development directory structure"""
        print("📁 Creating Web Development Structure...")
        
        try:
            # Web source directories
            web_dirs = [
                "web/controllers",
                "web/models", 
                "web/services",
                "web/utils",
                "web/middleware",
                "web/static/css",
                "web/static/js",
                "web/static/images",
                "web/templates/base",
                "web/templates/components",
                "web/templates/pages"
            ]
            
            for dir_path in web_dirs:
                full_path = self.src_dir / dir_path
                full_path.mkdir(parents=True, exist_ok=True)
                (full_path / "__init__.py").touch()
            
            # Test directories
            test_dirs = [
                "tests/web",
                "tests/web/unit",
                "tests/web/integration",
                "tests/web/e2e",
                "tests/web/selenium",
                "tests/web/fixtures",
                "tests/web/mocks"
            ]
            
            for dir_path in test_dirs:
                full_path = self.repo_root / dir_path
                full_path.mkdir(parents=True, exist_ok=True)
                (full_path / "__init__.py").touch()
            
            print("✅ Web development structure created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating web structure: {e}")
            return False
    
    def run_verification_tests(self) -> bool:
        """Run basic verification tests to ensure setup is correct"""
        print("🔍 Running Verification Tests...")
        
        try:
            # Test basic imports
            test_imports = [
                "flask",
                "fastapi", 
                "selenium",
                "pytest",
                "pytest_flask",
                "pytest_fastapi"
            ]
            
            for module in test_imports:
                try:
                    __import__(module)
                    print(f"✅ {module} imported successfully")
                except ImportError:
                    print(f"❌ {module} import failed")
                    return False
            
            # Test basic Flask app creation
            try:
                from flask import Flask
                app = Flask(__name__)
                print("✅ Flask app creation successful")
            except Exception as e:
                print(f"❌ Flask app creation failed: {e}")
                return False
            
            # Test basic FastAPI app creation
            try:
                from fastapi import FastAPI
                app = FastAPI()
                print("✅ FastAPI app creation successful")
            except Exception as e:
                print(f"❌ FastAPI app creation failed: {e}")
                return False
            
            print("✅ All verification tests passed")
            return True
            
        except Exception as e:
            print(f"❌ Error during verification: {e}")
            return False
    
    def setup_complete(self) -> bool:
        """Complete setup process"""
        print("\n🚀 Starting Web Development Environment Setup...")
        
        steps = [
            ("Installing Dependencies", self.setup_dependencies),
            ("Setting up Selenium WebDriver", self.setup_selenium_webdriver),
            ("Setting up Flask Environment", self.setup_flask_environment),
            ("Setting up FastAPI Environment", self.setup_fastapi_environment),
            ("Setting up TDD Infrastructure", self.setup_tdd_infrastructure),
            ("Setting up Development Tools", self.setup_development_tools),
            ("Creating Web Structure", self.create_web_structure),
            ("Running Verification Tests", self.run_verification_tests)
        ]
        
        for step_name, step_func in steps:
            print(f"\n📋 {step_name}...")
            if not step_func():
                print(f"❌ Setup failed at: {step_name}")
                return False
        
        print("\n🎉 Web Development Environment Setup Complete!")
        print("\n📚 Next Steps:")
        print("1. Activate your virtual environment")
        print("2. Run: python -m pytest tests/ -v")
        print("3. Start Flask app: python scripts/run_flask_dev.py")
        print("4. Start FastAPI app: python scripts/run_fastapi_dev.py")
        print("5. Run Selenium tests: python -m pytest tests/web/selenium/ -v")
        
        return True

def main():
    """Main setup function"""
    setup = WebDevelopmentEnvironmentSetup()
    success = setup.setup_complete()
    
    if success:
        print("\n✅ Setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
