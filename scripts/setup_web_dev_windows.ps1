# Web Development Environment Setup Script for Windows
# Agent_Cellphone_V2_Repository TDD Integration Project
#
# Author: Web Development & UI Framework Specialist
# License: MIT

param(
    [switch]$SkipDependencies,
    [switch]$SkipTests,
    [switch]$Verbose
)

# Set execution policy for current session
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

Write-Host "🚀 Setting up Web Development Environment for Windows" -ForegroundColor Green
Write-Host "📍 Repository: $PSScriptRoot\.." -ForegroundColor Cyan
Write-Host "🐍 Python Version: $(python --version)" -ForegroundColor Cyan
Write-Host "💻 Platform: Windows" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

# Function to check if command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Function to install Python package
function Install-PythonPackage($package) {
    try {
        Write-Host "📦 Installing $package..." -ForegroundColor Yellow
        python -m pip install $package --quiet
        Write-Host "✅ $package installed successfully" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Failed to install $package: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to create directory structure
function New-DirectoryStructure {
    Write-Host "📁 Creating directory structure..." -ForegroundColor Yellow

    $directories = @(
        "src\web\controllers",
        "src\web\models",
        "src\web\services",
        "src\web\utils",
        "src\web\middleware",
        "src\web\static\css",
        "src\web\static\js",
        "src\web\static\images",
        "src\web\templates\base",
        "src\web\templates\components",
        "src\web\templates\pages",
        "tests\web\unit",
        "tests\web\integration",
        "tests\web\e2e",
        "tests\web\selenium",
        "tests\web\fixtures",
        "tests\web\mocks",
        "config",
        "test_results"
    )

    foreach ($dir in $directories) {
        $fullPath = Join-Path $PSScriptRoot\.. $dir
        if (!(Test-Path $fullPath)) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
            Write-Host "✅ Created: $dir" -ForegroundColor Green
        }
    }
}

# Function to install dependencies
function Install-Dependencies {
    if ($SkipDependencies) {
        Write-Host "⏭️ Skipping dependency installation" -ForegroundColor Yellow
        return
    }

    Write-Host "📦 Installing Web Development Dependencies..." -ForegroundColor Yellow

    # Check if requirements file exists
    $requirementsFile = Join-Path $PSScriptRoot\.. "requirements_web_development.txt"
    if (Test-Path $requirementsFile) {
        Write-Host "📋 Installing from requirements file..." -ForegroundColor Cyan
        python -m pip install -r $requirementsFile --quiet
        Write-Host "✅ Core dependencies installed" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️ Requirements file not found, installing core packages..." -ForegroundColor Yellow

        # Install core packages individually
        $corePackages = @(
            "Flask>=2.3.0",
            "FastAPI>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "selenium>=4.15.0",
            "webdriver-manager>=4.0.0",
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-flask>=1.3.0",
            "pytest-fastapi>=0.1.0"
        )

        foreach ($package in $corePackages) {
            Install-PythonPackage $package
        }
    }

    # Install additional development tools
    $devTools = @("pip-tools", "pipdeptree", "safety")
    foreach ($tool in $devTools) {
        Install-PythonPackage $tool
    }
}

# Function to setup Selenium WebDriver
function Setup-SeleniumWebDriver {
    Write-Host "🌐 Setting up Selenium WebDriver..." -ForegroundColor Yellow

    try {
        # Install webdriver-manager
        Install-PythonPackage "webdriver-manager"

        # Create Selenium configuration
        $seleniumConfig = @{
            webdriver = @{
                chrome = @{
                    driver_path = "auto"
                    options = @("--headless", "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu")
                }
                firefox = @{
                    driver_path = "auto"
                    options = @("--headless")
                }
            }
            timeouts = @{
                implicit_wait = 10
                page_load = 30
                script = 30
            }
            retry_attempts = 3
        }

        $configDir = Join-Path $PSScriptRoot\.. "config"
        $configFile = Join-Path $configDir "selenium_config.json"

        if (!(Test-Path $configDir)) {
            New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        }

        $seleniumConfig | ConvertTo-Json -Depth 10 | Set-Content $configFile
        Write-Host "✅ Selenium WebDriver configured" -ForegroundColor Green

    }
    catch {
        Write-Host "❌ Error setting up Selenium: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Function to setup Flask environment
function Setup-FlaskEnvironment {
    Write-Host "🔥 Setting up Flask Environment..." -ForegroundColor Yellow

    try {
        $flaskConfig = @{
            development = @{
                DEBUG = $true
                TESTING = $false
                SECRET_KEY = "dev-secret-key-change-in-production"
                DATABASE_URI = "sqlite:///dev.db"
                LOG_LEVEL = "DEBUG"
                HOST = "0.0.0.0"
                PORT = 5000
            }
            testing = @{
                DEBUG = $false
                TESTING = $true
                SECRET_KEY = "test-secret-key"
                DATABASE_URI = "sqlite:///test.db"
                LOG_LEVEL = "INFO"
            }
            production = @{
                DEBUG = $false
                TESTING = $false
                SECRET_KEY = "change-this-in-production"
                DATABASE_URI = "sqlite:///prod.db"
                LOG_LEVEL = "WARNING"
            }
        }

        $configDir = Join-Path $PSScriptRoot\.. "config"
        $configFile = Join-Path $configDir "flask_config.json"

        if (!(Test-Path $configDir)) {
            New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        }

        $flaskConfig | ConvertTo-Json -Depth 10 | Set-Content $configFile
        Write-Host "✅ Flask environment configured" -ForegroundColor Green

    }
    catch {
        Write-Host "❌ Error setting up Flask: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Function to setup FastAPI environment
function Setup-FastAPIEnvironment {
    Write-Host "⚡ Setting up FastAPI Environment..." -ForegroundColor Yellow

    try {
        $fastapiConfig = @{
            app = @{
                title = "Agent_Cellphone_V2 API"
                description = "TDD Integration Web API"
                version = "2.0.0"
                docs_url = "/docs"
                redoc_url = "/redoc"
            }
            server = @{
                host = "0.0.0.0"
                port = 8000
                reload = $true
            }
            database = @{
                url = "sqlite:///./fastapi.db"
                echo = $false
            }
            cors = @{
                origins = @("*")
                methods = @("GET", "POST", "PUT", "DELETE")
                headers = @("*")
            }
        }

        $configDir = Join-Path $PSScriptRoot\.. "config"
        $configFile = Join-Path $configDir "fastapi_config.json"

        if (!(Test-Path $configDir)) {
            New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        }

        $fastapiConfig | ConvertTo-Json -Depth 10 | Set-Content $configFile
        Write-Host "✅ FastAPI environment configured" -ForegroundColor Green

    }
    catch {
        Write-Host "❌ Error setting up FastAPI: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Function to setup TDD infrastructure
function Setup-TDDInfrastructure {
    Write-Host "🧪 Setting up TDD Testing Infrastructure..." -ForegroundColor Yellow

    try {
        # Create pytest configuration
        $pytestConfig = @"
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
"@

        $pytestFile = Join-Path $PSScriptRoot\.. "pytest.ini"
        $pytestConfig | Set-Content $pytestFile

        # Create test configuration
        $testConfig = @{
            test_environment = @{
                base_url = "http://localhost:5000"
                api_base_url = "http://localhost:8000"
                selenium = @{
                    browser = "chrome"
                    headless = $true
                    timeout = 30
                }
                database = @{
                    test_db = "sqlite:///test.db"
                    cleanup_after_tests = $true
                }
            }
            test_data = @{
                fixtures_dir = "tests/fixtures"
                mocks_dir = "tests/mocks"
                test_users = @(
                    @{username = "test_user"; password = "test_pass"},
                    @{username = "admin_user"; password = "admin_pass"}
                )
            }
        }

        $configDir = Join-Path $PSScriptRoot\.. "config"
        $testConfigFile = Join-Path $configDir "test_config.json"

        if (!(Test-Path $configDir)) {
            New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        }

        $testConfig | ConvertTo-Json -Depth 10 | Set-Content $testConfigFile
        Write-Host "✅ TDD infrastructure configured" -ForegroundColor Green

    }
    catch {
        Write-Host "❌ Error setting up TDD infrastructure: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Function to run verification tests
function Test-Environment {
    if ($SkipTests) {
        Write-Host "⏭️ Skipping environment verification" -ForegroundColor Yellow
        return
    }

    Write-Host "🔍 Running Environment Verification Tests..." -ForegroundColor Yellow

    try {
        # Test basic imports
        $testImports = @("flask", "fastapi", "selenium", "pytest")

        foreach ($module in $testImports) {
            try {
                python -c "import $module; print('✅ $module imported successfully')"
            }
            catch {
                Write-Host "❌ $module import failed" -ForegroundColor Red
                return $false
            }
        }

        # Test basic Flask app creation
        try {
            python -c "from flask import Flask; app = Flask(__name__); print('✅ Flask app creation successful')"
        }
        catch {
            Write-Host "❌ Flask app creation failed" -ForegroundColor Red
            return $false
        }

        # Test basic FastAPI app creation
        try {
            python -c "from fastapi import FastAPI; app = FastAPI(); print('✅ FastAPI app creation successful')"
        }
        catch {
            Write-Host "❌ FastAPI app creation failed" -ForegroundColor Red
            return $false
        }

        Write-Host "✅ All verification tests passed" -ForegroundColor Green
        return $true

    }
    catch {
        Write-Host "❌ Error during verification: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main setup function
function Start-WebDevelopmentSetup {
    Write-Host "🚀 Starting Web Development Environment Setup..." -ForegroundColor Green

    try {
        # Create directory structure
        New-DirectoryStructure

        # Install dependencies
        Install-Dependencies

        # Setup Selenium WebDriver
        Setup-SeleniumWebDriver

        # Setup Flask environment
        Setup-FlaskEnvironment

        # Setup FastAPI environment
        Setup-FastAPIEnvironment

        # Setup TDD infrastructure
        Setup-TDDInfrastructure

        # Verify environment
        $verificationSuccess = Test-Environment

        if ($verificationSuccess) {
            Write-Host "🎉 Web Development Environment Setup Complete!" -ForegroundColor Green
            Write-Host ""
            Write-Host "📚 Next Steps:" -ForegroundColor Cyan
            Write-Host "1. Activate your virtual environment (if using one)" -ForegroundColor White
            Write-Host "2. Run: python scripts/run_tdd_tests.py" -ForegroundColor White
            Write-Host "3. Start Flask app: python scripts/run_flask_dev.py" -ForegroundColor White
            Write-Host "4. Start FastAPI app: python scripts/run_fastapi_dev.py" -ForegroundColor White
            Write-Host "5. Run Selenium tests: python -m pytest tests/web/selenium/ -v" -ForegroundColor White
            Write-Host ""
            Write-Host "🌐 Flask will be available at: http://localhost:5000" -ForegroundColor Yellow
            Write-Host "⚡ FastAPI will be available at: http://localhost:8000" -ForegroundColor Yellow
            Write-Host "📚 FastAPI docs at: http://localhost:8000/docs" -ForegroundColor Yellow
        }
        else {
            Write-Host "⚠️ Setup completed with verification issues" -ForegroundColor Yellow
            Write-Host "Please review the errors above and run verification again" -ForegroundColor Yellow
        }

    }
    catch {
        Write-Host "❌ Setup failed: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# Run setup if script is executed directly
if ($MyInvocation.InvocationName -ne ".") {
    Start-WebDevelopmentSetup
}
