# 🚀 V2 Code Quality Standards - Agent Cellphone V2

## 📋 Overview

This document defines the comprehensive code quality standards for Agent Cellphone V2, ensuring V2 compliance through automated tools, consistent formatting, and rigorous quality checks.

## 🎯 Compliance Levels

| Level | Score Range | Description | Status |
|-------|-------------|-------------|---------|
| **V2 COMPLIANT - EXCELLENT** | 95.0% - 100% | Full compliance achieved | 🎯 Target |
| **V2 COMPLIANT - GOOD** | 90.0% - 94.9% | Good compliance, minor issues | ✅ Acceptable |
| **V2 COMPLIANT - ACCEPTABLE** | 80.0% - 89.9% | Basic compliance, needs improvement | ⚠️ Warning |
| **V2 COMPLIANT - NEEDS IMPROVEMENT** | 70.0% - 79.9% | Below standard, action required | ❌ Action Required |
| **V2 NON-COMPLIANT** | < 70.0% | Critical issues, immediate action | 🚨 Critical |

## 🔧 Quality Tools

### **1. Code Formatting**

#### **Black - Code Formatter**
- **Purpose**: Automatic code formatting to PEP 8 standards
- **Configuration**: 88 character line length, Python 3.8+ compatibility
- **Usage**: `black .` (format all files) or `black --check .` (check only)
- **Integration**: Pre-commit hook, CI/CD pipeline

#### **isort - Import Sorting**
- **Purpose**: Automatic import organization and sorting
- **Configuration**: Black-compatible profile, 88 character line length
- **Usage**: `isort .` (sort all files) or `isort --check-only .` (check only)
- **Integration**: Pre-commit hook, CI/CD pipeline

#### **Autopep8 - PEP 8 Compliance**
- **Purpose**: Additional PEP 8 compliance fixes
- **Configuration**: Aggressive mode, 88 character line length
- **Usage**: `autopep8 --in-place --aggressive --aggressive .`
- **Integration**: Pre-commit hook

### **2. Linting & Analysis**

#### **Flake8 - Style Guide Enforcement**
- **Purpose**: PEP 8 style guide enforcement
- **Configuration**: 88 character line length, extended ignore patterns
- **Usage**: `flake8`
- **Integration**: Pre-commit hook, CI/CD pipeline
- **Extensions**: docstrings, import-order, bugbear, comprehensions, simplify

#### **Pylint - Comprehensive Analysis**
- **Purpose**: Code analysis, error detection, and style checking
- **Configuration**: 88 character line length, balanced rule set
- **Usage**: `pylint`
- **Integration**: Pre-commit hook, CI/CD pipeline
- **Threshold**: Minimum score 8.0/10.0

#### **MyPy - Static Type Checking**
- **Purpose**: Static type checking and validation
- **Configuration**: Strict mode, Python 3.8+ compatibility
- **Usage**: `mypy`
- **Integration**: Pre-commit hook, CI/CD pipeline
- **Threshold**: 90% type coverage

### **3. Security & Safety**

#### **Bandit - Security Linting**
- **Purpose**: Security vulnerability detection
- **Configuration**: JSON output, excluded test directories
- **Usage**: `bandit -r . -f json`
- **Integration**: Pre-commit hook, CI/CD pipeline
- **Threshold**: Zero security issues

#### **Safety - Dependency Scanning**
- **Purpose**: Known vulnerability detection in dependencies
- **Configuration**: JSON output, full report
- **Usage**: `safety check --json`
- **Integration**: Pre-commit hook, CI/CD pipeline
- **Threshold**: Zero vulnerabilities

## 📁 Configuration Files

### **pyproject.toml**
Central configuration for all quality tools:
- Black formatting settings
- isort import sorting
- Flake8 linting rules
- Pylint analysis settings
- MyPy type checking
- Bandit security scanning
- Pytest testing configuration
- Coverage reporting

### **.pre-commit-config.yaml**
Pre-commit hooks configuration:
- Automatic quality checks on commit
- Quality gates enforcement
- Tool execution order
- Failure handling

## 🚦 Quality Gates

### **Gate 1: Code Formatting (Required)**
- Black formatting check
- isort import sorting
- Autopep8 compliance

### **Gate 2: Linting (Required)**
- Flake8 violations
- Pylint score threshold
- Style guide compliance

### **Gate 3: Type Checking (Optional)**
- MyPy type coverage
- Type annotation quality

### **Gate 4: Security (Required)**
- Bandit security issues
- Safety vulnerability scan

### **Gate 5: Import Management (Required)**
- Autoflake unused import removal
- Import organization

## 🔄 Workflow Integration

### **Pre-commit Hooks**
```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
```

### **CI/CD Pipeline**
```yaml
# GitHub Actions example
- name: Code Quality Check
  run: |
    python scripts/code_quality_enforcer.py
    python -m black --check .
    python -m isort --check-only .
    flake8
    pylint
    mypy
    bandit -r . -f json
    safety check --json
```

### **Local Development**
```bash
# Run quality checks locally
python scripts/code_quality_enforcer.py

# Fix formatting issues
black .
isort .
autopep8 --in-place --aggressive --aggressive .

# Check specific tools
flake8
pylint
mypy
bandit -r .
safety check
```

## 📊 Quality Metrics

### **Code Quality Score Calculation**
```
Overall Score = (Tool1_Score + Tool2_Score + ... + ToolN_Score) / N

Where:
- Black: 100% (pass) or partial score based on formatting issues
- isort: 100% (pass) or partial score based on import issues
- Flake8: 100% (pass) or partial score based on violations
- Pylint: Score from 0-10 converted to percentage
- MyPy: 100% (pass) or partial score based on type errors
- Bandit: 100% (pass) or 0% (fail) based on security issues
- Safety: 100% (pass) or 0% (fail) based on vulnerabilities
```

### **Thresholds by Tool**
| Tool | Threshold | Scoring Method |
|------|-----------|----------------|
| Black | 100% | Pass/Fail with partial scoring |
| isort | 100% | Pass/Fail with partial scoring |
| Flake8 | 95% | Violation count based |
| Pylint | 8.0/10.0 | Score based |
| MyPy | 90% | Error count based |
| Bandit | 0 issues | Pass/Fail |
| Safety | 0 vulnerabilities | Pass/Fail |

## 🛠️ Troubleshooting

### **Common Issues & Solutions**

#### **Black Formatting Issues**
```bash
# Check what would be formatted
black --check --diff .

# Format all files
black .

# Format specific file
black path/to/file.py
```

#### **isort Import Issues**
```bash
# Check import organization
isort --check-only --diff .

# Sort imports automatically
isort .

# Sort specific file
isort path/to/file.py
```

#### **Flake8 Violations**
```bash
# Run with specific file
flake8 path/to/file.py

# Show error codes
flake8 --show-source --statistics .

# Ignore specific errors
flake8 --extend-ignore=E203,W503 .
```

#### **Pylint Score Issues**
```bash
# Run on specific file
pylint path/to/file.py

# Show detailed report
pylint --reports=y path/to/file.py

# Generate configuration
pylint --generate-rcfile > .pylintrc
```

#### **MyPy Type Issues**
```bash
# Check specific file
mypy path/to/file.py

# Show error details
mypy --show-error-codes path/to/file.py

# Ignore missing imports
mypy --ignore-missing-imports path/to/file.py
```

## 📈 Continuous Improvement

### **Quality Monitoring**
- Regular quality audits (weekly)
- Trend analysis and reporting
- Tool configuration optimization
- Rule set refinement

### **Performance Optimization**
- Tool execution time monitoring
- Parallel execution where possible
- Caching and incremental checks
- Selective file checking

### **Team Training**
- Quality standards workshops
- Tool usage training
- Best practices documentation
- Code review guidelines

## 🔗 Resources

### **Official Documentation**
- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Pylint Documentation](https://pylint.pycqa.org/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Safety Documentation](https://pyup.io/safety/)

### **Best Practices**
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [PEP 257 Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

### **Integration Examples**
- [Pre-commit Framework](https://pre-commit.com/)
- [GitHub Actions](https://github.com/features/actions)
- [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)

---

**Last Updated**: 2025-08-30  
**Version**: 2.0.0  
**Maintainer**: Agent-2 - V2 Compliance Team  
**Status**: ACTIVE - V2 Standards Implementation
