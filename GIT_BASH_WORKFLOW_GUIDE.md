# 🎯 Git Bash Workflow for Pre-commit Hooks

## The Problem
- Pre-commit hooks require `/bin/sh` (Unix shell)
- Windows CMD/PowerShell don't provide this
- Using `--no-verify` bypasses quality checks ❌
- Need proper solution that maintains code quality ✅

## The Solution: Git Bash
Git Bash provides a Unix-like environment on Windows with all the tools pre-commit hooks need.

---

## 🚀 Quick Setup (2 Minutes)

### Step 1: Verify Git Bash
```bash
# Check if Git Bash is available
where git-bash.exe
# OR check common locations
ls "C:\Program Files\Git\bin\bash.exe"
```

### Step 2: Open Git Bash in Project
```bash
# Method 1: Right-click in project folder
Right-click in D:\Agent_Cellphone_V2_Repository
Select "Git Bash Here"

# Method 2: Open manually
"C:\Program Files\Git\bin\bash.exe" --cd="D:\Agent_Cellphone_V2_Repository"
```

### Step 3: Test Pre-commit
```bash
# In Git Bash, test pre-commit hooks
pre-commit run --all-files
```

---

## 📋 Your New Workflow

### ✅ **Instead of this (bad):**
```cmd
# Windows CMD/PowerShell
git add .
git commit --no-verify -m "feat: new feature"
git push --no-verify origin main
```

### ✅ **Do this (good):**
```bash
# Git Bash
git add .
git commit -m "feat: new feature"
git push origin main
```

---

## 🛠️ Git Bash Commands Reference

### Basic Git Operations
```bash
# Status and staging
git status
git add .
git add specific-file.py

# Committing
git commit -m "feat: add new feature"
git commit --amend  # Fix last commit

# Pushing
git push origin agent
git push origin main
```

### Pre-commit Operations
```bash
# Test all files
pre-commit run --all-files

# Test specific files
pre-commit run --files src/new_file.py

# Test staged files only
pre-commit run

# Auto-fix issues (where possible)
pre-commit run --all-files && pre-commit run --all-files
```

### Quality Checks
```bash
# Run individual tools
python -m black src/
python -m isort src/
python -m flake8 src/
python -m mypy src/

# Run tests
python -m pytest tests/
```

---

## 🎯 Project Quality Standards

### Code Formatting (Black)
- Line length: 88 characters
- Python versions: 3.8, 3.9, 3.10, 3.11
- Follows PEP 8 with modern improvements

### Import Organization (isort)
- Uses Black profile
- Sections: stdlib, third-party, local
- Consistent import ordering

### Linting (Flake8)
- Max line length: 88
- Ignores: E203, W503, E501
- Catches common Python issues

### Type Checking (MyPy)
- Ignores missing imports
- No strict optional checking
- Validates type annotations

### Security (Bandit)
- Skips: B101, B601
- Checks for security vulnerabilities

### Documentation (Docformatter)
- Wraps summaries at 88 chars
- Wraps descriptions at 88 chars
- Consistent docstring formatting

---

## 🐛 Troubleshooting

### Pre-commit Still Failing?
```bash
# Check pre-commit installation
which pre-commit
pre-commit --version

# Reinstall pre-commit
pip install --upgrade pre-commit
pre-commit install
```

### Git Bash Not Found?
```bash
# Install Git with Git Bash
# Download from: https://git-scm.com/
# During installation:
# - Select "Git Bash Here" option
# - Choose "Use Git from Windows Command Prompt"
```

### Environment Issues?
```bash
# Check PATH
echo $PATH

# Check Python
python --version
which python

# Check pip packages
pip list | grep pre-commit
```

---

## 📈 Benefits of Git Bash Solution

### ✅ **Immediate Benefits**
- **No more --no-verify** bypasses ✅
- **Proper code quality enforcement** ✅
- **Consistent with project standards** ✅
- **Team collaboration friendly** ✅

### ✅ **Long-term Benefits**
- **Maintains code quality** over time ✅
- **Prevents regressions** ✅
- **Professional development standards** ✅
- **CI/CD compatibility** ✅

---

## 🚀 Advanced Usage

### Custom Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: custom-check
        name: Custom project check
        entry: python scripts/custom_check.py
        language: system
        files: \.py$
```

### Selective Hook Running
```bash
# Run only specific hooks
pre-commit run black --all-files
pre-commit run flake8 --all-files

# Skip specific hooks
SKIP=flake8,mypy pre-commit run --all-files
```

### Auto-fixing
```bash
# Let pre-commit auto-fix what it can
pre-commit run --all-files

# Then run again to check remaining issues
pre-commit run --all-files
```

---

## 📋 Checklist for New Developers

- [ ] Install Git with Git Bash
- [ ] Clone repository
- [ ] Open Git Bash in project directory
- [ ] Run `pre-commit install`
- [ ] Test with `pre-commit run --all-files`
- [ ] Make changes and commit normally
- [ ] Never use `--no-verify`

---

## 🎉 Success!

**You're now using Git Bash for all git operations!**

- ✅ No more `--no-verify` flags
- ✅ Pre-commit hooks work perfectly
- ✅ Code quality is maintained
- ✅ Professional development standards
- ✅ Team collaboration friendly

**Happy coding! 🚀**
