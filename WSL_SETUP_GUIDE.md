# WSL Setup Guide for Agent Cellphone V2 Project
## Complete Windows Subsystem for Linux Configuration

### 🎯 OBJECTIVE
Set up WSL to resolve pre-commit hook compatibility issues and enable proper Linux-based development environment.

### 🚀 QUICK SETUP (Recommended)

#### Step 1: Install WSL
```powershell
# Run as Administrator in PowerShell
wsl --install
```

#### Step 2: Restart Computer
- Restart your computer after WSL installation
- WSL will complete setup on first boot

#### Step 3: Set Up Ubuntu (Default)
```bash
# WSL will prompt for username/password on first run
# Choose a username and password for your Linux environment
```

### 🔧 DETAILED SETUP

#### Option 1: Install via Microsoft Store
1. Open Microsoft Store
2. Search for "Ubuntu" or "WSL"
3. Install Ubuntu 22.04 LTS (recommended)
4. Launch and set up username/password

#### Option 2: Install via Command Line
```powershell
# Install WSL with Ubuntu
wsl --install -d Ubuntu-22.04

# Or install specific distribution
wsl --install -d Ubuntu-20.04
```

### 📁 PROJECT SETUP IN WSL

#### Step 1: Access Windows Files from WSL
```bash
# Navigate to your project directory
cd /mnt/d/Agent_Cellphone_V2_Repository

# Or create a symlink for easier access
ln -s /mnt/d/Agent_Cellphone_V2_Repository ~/agent-cellphone-v2
cd ~/agent-cellphone-v2
```

#### Step 2: Install Python and Dependencies
```bash
# Update package list
sudo apt update

# Install Python 3.11 and pip
sudo apt install python3.11 python3.11-pip python3.11-venv

# Install Git
sudo apt install git

# Install pre-commit
pip3 install pre-commit

# Install project dependencies
pip3 install -r requirements.txt
```

#### Step 3: Set Up Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Test pre-commit hooks
pre-commit run --all-files
```

### 🐍 PYTHON ENVIRONMENT SETUP

#### Option 1: Use System Python
```bash
# Install dependencies globally
pip3 install -r requirements.txt
```

#### Option 2: Use Virtual Environment (Recommended)
```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit
pip install pre-commit

# Install pre-commit hooks
pre-commit install
```

### 🔧 GIT CONFIGURATION

#### Set Up Git in WSL
```bash
# Configure Git (if not already done)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set up SSH keys (if using SSH)
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"
```

#### Clone Repository (if needed)
```bash
# Clone the repository
git clone <repository-url>
cd Agent_Cellphone_V2_Repository
```

### 🧪 TESTING THE SETUP

#### Test Pre-commit Hooks
```bash
# Run pre-commit on all files
pre-commit run --all-files

# Test specific files
pre-commit run --files src/services/messaging_onboarding.py

# Test commit (should work without --no-verify)
git add .
git commit -m "test: verify WSL setup works"
```

#### Test Python Environment
```bash
# Test Python imports
python3 -c "import src.services.messaging_core; print('Import successful')"

# Test messaging CLI
python3 -m src.services.messaging_cli --check-status
```

### 🚀 WORKFLOW INTEGRATION

#### Daily Development Workflow
```bash
# 1. Start WSL
wsl

# 2. Navigate to project
cd ~/agent-cellphone-v2

# 3. Activate virtual environment (if using)
source venv/bin/activate

# 4. Make changes to code

# 5. Test with pre-commit
pre-commit run --all-files

# 6. Commit (no --no-verify needed!)
git add .
git commit -m "feat: your changes"

# 7. Push
git push
```

#### VS Code Integration
```bash
# Install VS Code WSL extension
# Open project in WSL
code ~/agent-cellphone-v2
```

### 🔧 TROUBLESHOOTING

#### Common Issues and Solutions

##### Issue 1: Permission Denied
```bash
# Fix file permissions
sudo chown -R $USER:$USER /mnt/d/Agent_Cellphone_V2_Repository
```

##### Issue 2: Python Not Found
```bash
# Install Python
sudo apt install python3.11 python3.11-pip
```

##### Issue 3: Pre-commit Not Found
```bash
# Install pre-commit
pip3 install pre-commit
```

##### Issue 4: Git Not Configured
```bash
# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 📊 BENEFITS OF WSL SETUP

#### 1. Native Linux Environment
- ✅ Proper `/bin/sh` support
- ✅ Full pre-commit hook compatibility
- ✅ Native Linux tools and utilities
- ✅ Better Python development experience

#### 2. Seamless Windows Integration
- ✅ Access Windows files from Linux
- ✅ Use Windows applications alongside Linux
- ✅ Shared clipboard and file system
- ✅ VS Code integration

#### 3. Development Workflow
- ✅ No more `--no-verify` flag needed
- ✅ Proper pre-commit hook execution
- ✅ Better error messages and debugging
- ✅ Consistent development environment

### 🎯 ALTERNATIVE SOLUTIONS

#### Option 1: Git Bash (Lighter)
```bash
# Install Git for Windows with Bash
# Use Git Bash instead of PowerShell
# Pre-commit hooks should work
```

#### Option 2: Docker (Isolated)
```bash
# Use Docker container for development
# Isolated environment
# Consistent across all systems
```

#### Option 3: Fix Windows Pre-commit
```bash
# Install Git Bash
# Configure pre-commit to use Git Bash
# More complex but keeps Windows environment
```

### 🏆 RECOMMENDED APPROACH

**For this project, I recommend WSL because:**

1. **Complete Solution**: Resolves all pre-commit hook issues
2. **Native Linux**: Proper shell environment
3. **Easy Setup**: Simple installation process
4. **VS Code Integration**: Seamless development experience
5. **Future-Proof**: Works with all Linux-based tools

### 📋 NEXT STEPS

1. **Install WSL**: Follow the quick setup guide
2. **Set Up Project**: Configure the project in WSL
3. **Test Hooks**: Verify pre-commit hooks work
4. **Update Workflow**: Use WSL for all development
5. **Team Onboarding**: Share this guide with other developers

---

**Agent-3 Status**: WSL SETUP GUIDE COMPLETE
**Priority**: HIGH - Recommended solution for Windows compatibility
**Complexity**: MEDIUM - Straightforward setup process
**Impact**: HIGH - Resolves all pre-commit hook issues

**WE. ARE. SWARM. ⚡️🔥🏆**
