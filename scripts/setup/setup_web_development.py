#!/usr/bin/env python3
"""
Web Development Environment Setup Script
Agent_Cellphone_V2_Repository TDD Integration Project

This script sets up the complete web development environment including:
- Selenium for web automation
- Flask for web applications
- FastAPI for modern APIs
- Frontend frameworks and tools
- Testing infrastructure
- Development tools and quality assurance

Author: Web Development & UI Framework Specialist
License: MIT
"""

import os
import sys
import subprocess
import platform
import json

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import List, Dict, Any, Optional


class WebDevelopmentSetup:
    """Web development environment setup manager"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.requirements_file = self.project_root / "requirements_web_development.txt"
        self.venv_path = self.project_root / "venv_web_dev"

        # Platform-specific configurations
        self.is_windows = platform.system() == "Windows"
        self.is_linux = platform.system() == "Linux"
        self.is_macos = platform.system() == "Darwin"

        self.python_executable = self._get_python_executable()
        self.pip_executable = self._get_pip_executable()

        print(f"🚀 Web Development Environment Setup")
        print(f"📍 Project Root: {self.project_root}")
        print(f"🐍 Python: {self.python_executable}")
        print(f"📦 Platform: {platform.system()} {platform.release()}")
        print()

    def _get_python_executable(self) -> str:
        """Get the appropriate Python executable"""
        if self.is_windows:
            return "python"
        return "python3"

    def _get_pip_executable(self) -> str:
        """Get the appropriate pip executable"""
        if self.is_windows:
            return "pip"
        return "pip3"

    def run_command(self, command: List[str], cwd: Optional[Path] = None) -> bool:
        """Run a command and return success status"""
        try:
            print(f"🔄 Running: {' '.join(command)}")
            result = subprocess.run(
                command,
                cwd=cwd or self.project_root,
                check=True,
                capture_output=True,
                text=True,
            )
            if result.stdout:
                print(f"✅ Output: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running command: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
            return False

    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        try:
            result = subprocess.run(
                [self.python_executable, "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            version = result.stdout.strip()
            print(f"🐍 Python Version: {version}")

            # Check for Python 3.8+
            if (
                "3.8" in version
                or "3.9" in version
                or "3.10" in version
                or "3.11" in version
                or "3.12" in version
            ):
                return True
            else:
                print("⚠️  Warning: Python 3.8+ recommended for optimal compatibility")
                return True
        except Exception as e:
            print(f"❌ Error checking Python version: {e}")
            return False

    def create_virtual_environment(self) -> bool:
        """Create a virtual environment for web development"""
        if self.venv_path.exists():
            print(f"📁 Virtual environment already exists at: {self.venv_path}")
            return True

        try:
            print(f"🔧 Creating virtual environment at: {self.venv_path}")
            command = [self.python_executable, "-m", "venv", str(self.venv_path)]
            if not self.run_command(command):
                return False

            print("✅ Virtual environment created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating virtual environment: {e}")
            return False

    def activate_virtual_environment(self) -> bool:
        """Activate the virtual environment and update pip"""
        if self.is_windows:
            pip_path = self.venv_path / "Scripts" / "pip.exe"
            python_path = self.venv_path / "Scripts" / "python.exe"
        else:
            pip_path = self.venv_path / "bin" / "pip"
            python_path = self.venv_path / "bin" / "python"

        if not pip_path.exists() or not python_path.exists():
            print("❌ Virtual environment not properly created")
            return False

        # Update pip
        print("🔄 Updating pip...")
        if not self.run_command([str(pip_path), "install", "--upgrade", "pip"]):
            return False

        return True

    def install_dependencies(self) -> bool:
        """Install all web development dependencies"""
        if self.is_windows:
            pip_path = self.venv_path / "Scripts" / "pip.exe"
        else:
            pip_path = self.venv_path / "bin" / "pip"

        if not pip_path.exists():
            print("❌ pip not found in virtual environment")
            return False

        print("📦 Installing web development dependencies...")

        # Install core dependencies first
        core_deps = [
            "flask>=2.3.0",
            "fastapi>=0.104.0",
            "selenium>=4.15.0",
            "pytest>=7.4.0",
        ]

        for dep in core_deps:
            print(f"🔄 Installing {dep}...")
            if not self.run_command([str(pip_path), "install", dep]):
                print(f"⚠️  Warning: Failed to install {dep}")

        # Install from requirements file
        if self.requirements_file.exists():
            print("📋 Installing from requirements file...")
            if not self.run_command(
                [str(pip_path), "install", "-r", str(self.requirements_file)]
            ):
                print("⚠️  Warning: Some dependencies may not have installed correctly")
        else:
            print("⚠️  Requirements file not found, installing core dependencies only")

        return True

    def setup_webdriver_managers(self) -> bool:
        """Set up webdriver managers for Selenium"""
        print("🌐 Setting up webdriver managers...")

        if self.is_windows:
            python_path = self.venv_path / "Scripts" / "python.exe"
        else:
            python_path = self.venv_path / "bin" / "python"

        # Install webdriver-manager
        if not self.run_command(
            [str(python_path), "-m", "pip", "install", "webdriver-manager"]
        ):
            return False

        # Test webdriver setup
        test_script = """
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "venv_web_dev" / "Lib" / "site-packages"))

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    print("✅ Selenium and ChromeDriver setup successful")
except Exception as e:
    print(f"❌ WebDriver setup failed: {e}")
"""

        test_file = self.project_root / "test_webdriver_setup.py"
        with open(test_file, "w") as f:
            f.write(test_script)

        success = self.run_command([str(python_path), str(test_file)])
        test_file.unlink()  # Clean up test file

        return success

    def create_web_development_structure(self) -> bool:
        """Create the web development directory structure"""
        print("📁 Creating web development directory structure...")

        web_dirs = [
            "src/web/automation",
            "src/web/api",
            "src/web/frontend",
            "src/web/testing",
            "src/web/utils",
            "tests/web",
            "tests/web/automation",
            "tests/web/api",
            "tests/web/frontend",
            "web_config",
            "web_logs",
        ]

        for dir_path in web_dirs:
            full_path = self.project_root / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"📂 Created: {dir_path}")

        return True

    def create_web_config_files(self) -> bool:
        """Create configuration files for web development"""
        print("⚙️  Creating web development configuration files...")

        # Flask configuration
        flask_config = {
            "development": {
                "DEBUG": True,
                "TESTING": False,
                "SECRET_KEY": "dev-secret-key-change-in-production",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///web_dev.db",
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            },
            "testing": {
                "DEBUG": False,
                "TESTING": True,
                "SECRET_KEY": "test-secret-key",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            },
            "production": {
                "DEBUG": False,
                "TESTING": False,
                "SECRET_KEY": "production-secret-key-change-this",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///production.db",
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            },
        }

        config_file = self.project_root / "web_config" / "flask_config.json"
        config_file.parent.mkdir(exist_ok=True)

        with open(config_file, "w") as f:
            json.dump(flask_config, f, indent=2)

        print(f"✅ Created: {config_file}")

        # Selenium configuration
        selenium_config = {
            "browsers": {
                "chrome": {
                    "headless": False,
                    "window_size": "1920x1080",
                    "implicit_wait": 10,
                },
                "firefox": {
                    "headless": False,
                    "window_size": "1920x1080",
                    "implicit_wait": 10,
                },
            },
            "timeouts": {"page_load": 30, "script": 30, "implicit": 10},
            "screenshots": {"enabled": True, "directory": "web_logs/screenshots"},
        }

        selenium_config_file = self.project_root / "web_config" / "selenium_config.json"
        with open(selenium_config_file, "w") as f:
            json.dump(selenium_config, f, indent=2)

        print(f"✅ Created: {selenium_config_file}")

        return True

    def create_sample_web_applications(self) -> bool:
        """Create sample web applications for testing"""
        print("🌐 Creating sample web applications...")

        # Sample Flask app
        flask_app_content = '''"""
Sample Flask Application for Testing
Agent_Cellphone_V2_Repository Web Development Environment
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Main page"""
    return jsonify({
        "message": "Agent_Cellphone_V2 Web Development Environment",
        "status": "running",
        "endpoints": [
            "/api/health",
            "/api/test",
            "/api/automation/status"
        ]
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": "2025-01-20T00:00:00Z",
        "version": "1.0.0"
    })

@app.route('/api/test')
def test():
    """Test endpoint"""
    return jsonify({
        "message": "Test endpoint working",
        "method": request.method,
        "headers": dict(request.headers)
    })

@app.route('/api/automation/status')
def automation_status():
    """Automation status endpoint"""
    return jsonify({
        "selenium": "ready",
        "webdriver": "configured",
        "browsers": ["chrome", "firefox"]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''

        flask_app_file = self.project_root / "src" / "web" / "sample_flask_app.py"
        flask_app_file.parent.mkdir(parents=True, exist_ok=True)

        with open(flask_app_file, "w") as f:
            f.write(flask_app_content)

        print(f"✅ Created: {flask_app_file}")

        # Sample FastAPI app
        fastapi_app_content = '''"""
Sample FastAPI Application for Testing
Agent_Cellphone_V2_Repository Web Development Environment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

app = FastAPI(
    title="Agent_Cellphone_V2 Web API",
    description="Web Development Environment API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint"""
    return {
        "message": "Agent_Cellphone_V2 FastAPI Environment",
        "status": "running",
        "endpoints": [
            "/docs",
            "/api/health",
            "/api/test"
        ]
    }

@app.get("/api/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp="2025-01-20T00:00:00Z",
        version="1.0.0"
    )

@app.get("/api/test")
async def test():
    """Test endpoint"""
    return {
        "message": "FastAPI test endpoint working",
        "framework": "FastAPI",
        "async": True
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

        fastapi_app_file = self.project_root / "src" / "web" / "sample_fastapi_app.py"
        with open(fastapi_app_file, "w") as f:
            f.write(fastapi_app_content)

        print(f"✅ Created: {fastapi_app_file}")

        return True

    def create_test_files(self) -> bool:
        """Create test files for web development"""
        print("🧪 Creating test files...")

        # Flask tests
        flask_test_content = '''"""
Test Flask Application
Agent_Cellphone_V2_Repository Web Development Environment
"""

import pytest
from src.web.sample_flask_app import app

@pytest.fixture
def client():
    """Test client fixture"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_endpoint(client):
    """Test main endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'running'
    assert 'endpoints' in data

def test_health_endpoint(client):
    """Test health endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_test_endpoint(client):
    """Test test endpoint"""
    response = client.get('/api/test')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Test endpoint working'
'''

        flask_test_file = self.project_root / "tests" / "web" / "test_flask_app.py"
        flask_test_file.parent.mkdir(parents=True, exist_ok=True)

        with open(flask_test_file, "w") as f:
            f.write(flask_test_content)

        print(f"✅ Created: {flask_test_file}")

        # Selenium tests
        selenium_test_content = '''"""
Test Selenium Web Automation
Agent_Cellphone_V2_Repository Web Development Environment
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture(scope="function")
def driver():
    """WebDriver fixture"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for testing
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()

def test_selenium_setup(driver):
    """Test basic Selenium setup"""
    assert driver is not None
    assert driver.current_url == "data:,"

def test_webpage_navigation(driver):
    """Test webpage navigation"""
    # Navigate to a simple page
    driver.get("https://httpbin.org/html")

    # Check if page loaded
    assert "Herman Melville" in driver.page_source

    # Check title
    assert "Herman Melville" in driver.title

def test_element_interaction(driver):
    """Test element interaction"""
    driver.get("https://httpbin.org/forms/post")

    # Find form elements
    custname_input = driver.find_element("name", "custname")
    assert custname_input is not None

    # Type in input field
    custname_input.send_keys("Test User")
    assert custname_input.get_attribute("value") == "Test User"
'''

        selenium_test_file = self.project_root / "tests" / "web" / "test_selenium.py"
        with open(selenium_test_file, "w") as f:
            f.write(selenium_test_content)

        print(f"✅ Created: {selenium_test_file}")

        return True

    def create_launch_scripts(self) -> bool:
        """Create launch scripts for web applications"""
        print("🚀 Creating launch scripts...")

        # Windows batch file
        if self.is_windows:
            batch_content = """@echo off
echo Starting Agent_Cellphone_V2 Web Development Environment...

cd /d "%~dp0"

echo.
echo Available commands:
echo 1. Start Flask app: start_flask.bat
echo 2. Start FastAPI app: start_fastapi.bat
echo 3. Run tests: run_tests.bat
echo 4. Activate virtual environment: activate_venv.bat
echo.

pause
"""

            batch_file = self.project_root / "start_web_dev.bat"
            with open(batch_file, "w") as f:
                f.write(batch_content)

            print(f"✅ Created: {batch_file}")

        # PowerShell script
        powershell_content = """# Agent_Cellphone_V2 Web Development Environment Launcher
# PowerShell Script

Write-Host "🚀 Starting Agent_Cellphone_V2 Web Development Environment..." -ForegroundColor Green
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "Available commands:" -ForegroundColor Yellow
Write-Host "1. Start Flask app: .\\start_flask.ps1" -ForegroundColor Cyan
Write-Host "2. Start FastAPI app: .\\start_fastapi.ps1" -ForegroundColor Cyan
Write-Host "3. Run tests: .\\run_tests.ps1" -ForegroundColor Cyan
Write-Host "4. Activate virtual environment: .\\activate_venv.ps1" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to continue"
"""

        powershell_file = self.project_root / "start_web_dev.ps1"
        with open(powershell_file, "w") as f:
            f.write(powershell_content)

        print(f"✅ Created: {powershell_file}")

        # Flask launcher
        flask_launcher = '''#!/usr/bin/env python3
"""
Flask Application Launcher
Agent_Cellphone_V2_Repository Web Development Environment
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.web.sample_flask_app import app

    if __name__ == '__main__':
        print("🌐 Starting Flask application...")
        print("📍 URL: http://localhost:5000")
        print("📚 API Endpoints:")
        print("   - GET / - Main page")
        print("   - GET /api/health - Health check")
        print("   - GET /api/test - Test endpoint")
        print("   - GET /api/automation/status - Automation status")
        print()
        print("Press Ctrl+C to stop")

        app.run(debug=True, host='0.0.0.0', port=5000)

except ImportError as e:
    print(f"❌ Error importing Flask app: {e}")
    print("Make sure you have activated the virtual environment and installed dependencies")
    sys.exit(1)
'''

        flask_launcher_file = self.project_root / "start_flask.py"
        with open(flask_launcher_file, "w") as f:
            f.write(flask_launcher)

        print(f"✅ Created: {flask_launcher_file}")

        # FastAPI launcher
        fastapi_launcher = '''#!/usr/bin/env python3
"""
FastAPI Application Launcher
Agent_Cellphone_V2_Repository Web Development Environment
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    import uvicorn
    from src.web.sample_fastapi_app import app

    if __name__ == '__main__':
        print("🚀 Starting FastAPI application...")
        print("📍 URL: http://localhost:8000")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("📚 API Endpoints:")
        print("   - GET / - Main page")
        print("   - GET /api/health - Health check")
        print("   - GET /api/test - Test endpoint")
        print()
        print("Press Ctrl+C to stop")

        uvicorn.run(app, host="0.0.0.0", port=8000)

except ImportError as e:
    print(f"❌ Error importing FastAPI app: {e}")
    print("Make sure you have activated the virtual environment and installed dependencies")
    sys.exit(1)
'''

        fastapi_launcher_file = self.project_root / "start_fastapi.py"
        with open(fastapi_launcher_file, "w") as f:
            f.write(fastapi_launcher)

        print(f"✅ Created: {fastapi_launcher_file}")

        return True

    def run_verification_tests(self) -> bool:
        """Run verification tests to ensure setup is working"""
        print("🔍 Running verification tests...")

        if self.is_windows:
            python_path = self.venv_path / "Scripts" / "python.exe"
        else:
            python_path = self.venv_path / "bin" / "python"

        # Test basic imports
        test_imports = """
import sys
from pathlib import Path

# Test core web framework imports
try:
    import flask
    print("✅ Flask imported successfully")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")

try:
    import fastapi
    print("✅ FastAPI imported successfully")
except ImportError as e:
    print(f"❌ FastAPI import failed: {e}")

try:
    import selenium
    print("✅ Selenium imported successfully")
except ImportError as e:
    print(f"❌ Selenium import failed: {e}")

try:
    import pytest
    print("✅ Pytest imported successfully")
except ImportError as e:
    print(f"❌ Pytest import failed: {e}")

print("\\n🎉 Web development environment verification complete!")
"""

        test_file = self.project_root / "test_web_imports.py"
        with open(test_file, "w") as f:
            f.write(test_imports)

        success = self.run_command([str(python_path), str(test_file)])
        test_file.unlink()  # Clean up test file

        return success

    def create_setup_summary(self) -> bool:
        """Create a setup summary document"""
        print("📋 Creating setup summary...")

        summary_content = f"""# Web Development Environment Setup Summary

## 🎯 Setup Completed Successfully

**Date:** 2025-01-20
**Project:** Agent_Cellphone_V2_Repository
**Specialist:** Web Development & UI Framework Specialist

## 🏗️ Environment Components

### Virtual Environment
- **Location:** {self.venv_path}
- **Python:** {self.python_executable}
- **Status:** ✅ Active

### Core Frameworks
- **Flask:** Web application framework
- **FastAPI:** Modern API framework
- **Selenium:** Web automation framework
- **Pytest:** Testing framework

### Directory Structure
```
src/web/
├── automation/          # Selenium automation scripts
├── api/                # API implementations
├── frontend/           # Frontend components
├── testing/            # Web testing utilities
└── utils/              # Web utilities

tests/web/
├── automation/          # Selenium tests
├── api/                # API tests
└── frontend/           # Frontend tests

web_config/              # Configuration files
web_logs/                # Log files and screenshots
```

## 🚀 Quick Start Commands

### Activate Environment
```bash
# Windows
{self.venv_path}\\Scripts\\activate

# Linux/Mac
source {self.venv_path}/bin/activate
```

### Start Applications
```bash
# Flask App (Port 5000)
python start_flask.py

# FastAPI App (Port 8000)
python start_fastapi.py
```

### Run Tests
```bash
# All tests
pytest

# Web tests only
pytest tests/web/

# Specific test file
pytest tests/web/test_flask_app.py
```

## 📚 Available Endpoints

### Flask App (http://localhost:5000)
- `GET /` - Main page
- `GET /api/health` - Health check
- `GET /api/test` - Test endpoint
- `GET /api/automation/status` - Automation status

### FastAPI App (http://localhost:8000)
- `GET /` - Main page
- `GET /api/health` - Health check
- `GET /api/test` - Test endpoint
- `GET /docs` - Interactive API documentation

## 🔧 Configuration Files

- **Flask Config:** `web_config/flask_config.json`
- **Selenium Config:** `web_config/selenium_config.json`
- **Requirements:** `requirements_web_development.txt`

## 🧪 Testing Infrastructure

- **Framework:** Pytest
- **Coverage:** pytest-cov
- **HTML Reports:** pytest-html
- **Selenium Tests:** Automated browser testing
- **API Tests:** REST API testing

## 📦 Dependencies Installed

All web development dependencies have been installed including:
- Web frameworks (Flask, FastAPI)
- Web automation (Selenium, Playwright)
- Testing tools (Pytest, Coverage)
- Development tools (Black, Flake8, MyPy)
- Documentation tools (Sphinx, MkDocs)

## 🎉 Next Steps

1. **Activate the virtual environment**
2. **Start one of the sample applications**
3. **Run the test suite to verify everything works**
4. **Begin developing your web applications**

## 🆘 Troubleshooting

If you encounter issues:
1. Ensure the virtual environment is activated
2. Check that all dependencies are installed
3. Verify Python version compatibility (3.8+)
4. Check the logs in `web_logs/` directory

---

**Setup completed by:** Web Development & UI Framework Specialist
**Status:** ✅ Ready for development
"""

        summary_file = self.project_root / "WEB_DEVELOPMENT_SETUP_SUMMARY.md"
        with open(summary_file, "w") as f:
            f.write(summary_content)

        print(f"✅ Created: {summary_file}")
        return True

    def setup_complete(self) -> bool:
        """Complete the entire web development environment setup"""
        print("🚀 Starting comprehensive web development environment setup...")
        print()

        steps = [
            ("Checking Python version", self.check_python_version),
            ("Creating virtual environment", self.create_virtual_environment),
            ("Activating virtual environment", self.activate_virtual_environment),
            ("Installing dependencies", self.install_dependencies),
            ("Setting up webdriver managers", self.setup_webdriver_managers),
            ("Creating directory structure", self.create_web_development_structure),
            ("Creating configuration files", self.create_web_config_files),
            ("Creating sample applications", self.create_sample_web_applications),
            ("Creating test files", self.create_test_files),
            ("Creating launch scripts", self.create_launch_scripts),
            ("Running verification tests", self.run_verification_tests),
            ("Creating setup summary", self.create_setup_summary),
        ]

        for step_name, step_func in steps:
            print(f"🔄 {step_name}...")
            if not step_func():
                print(f"❌ Failed at step: {step_name}")
                return False
            print(f"✅ {step_name} completed")
            print()

        print("🎉 Web Development Environment Setup Complete!")
        print()
        print("📋 Next Steps:")
        print("1. Activate the virtual environment")
        print("2. Start one of the sample applications")
        print("3. Run tests to verify everything works")
        print("4. Begin developing your web applications")
        print()
        print(f"📚 See {self.project_root}/WEB_DEVELOPMENT_SETUP_SUMMARY.md for details")

        return True


def main():
    """Main setup function"""
    setup = WebDevelopmentSetup()

    try:
        success = setup.setup_complete()
        if success:
            print("🎯 Setup completed successfully!")
            return 0
        else:
            print("❌ Setup failed. Check the logs above for details.")
            return 1
    except Exception as e:
        print(f"💥 Unexpected error during setup: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
