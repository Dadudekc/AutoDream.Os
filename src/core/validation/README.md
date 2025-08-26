# Unified Validation Framework

A comprehensive, extensible validation framework that provides unified validation capabilities across multiple domains including contracts, workflows, security, quality, and more.

## 🚀 Features

- **Unified Interface**: Single validation manager for all validation types
- **Extensible Architecture**: Easy to add new validators and rules
- **Comprehensive Coverage**: 10+ built-in validators covering common use cases
- **Flexible Configuration**: Configurable validation rules and severity levels
- **Rich Reporting**: Detailed validation results with actionable feedback
- **Performance Optimized**: Efficient validation with caching and optimization

## 📋 Built-in Validators

| Validator | Purpose | Key Features |
|-----------|---------|--------------|
| **Contract** | Business contract validation | Priority, deadline, budget, capabilities |
| **Config** | Configuration validation | Database, API, service configurations |
| **Workflow** | Process workflow validation | Steps, transitions, dependencies |
| **Message** | Communication validation | Format, encoding, content validation |
| **Quality** | Code quality metrics | Complexity, coverage, maintainability |
| **Security** | Security configuration | Authentication, encryption, access control |
| **Storage** | Data storage validation | Database, file system, cloud storage |
| **Onboarding** | User onboarding validation | Verification, stages, compliance |
| **Task** | Task management validation | Assignment, effort, dependencies |
| **Code** | Source code validation | Syntax, structure, best practices |

## 🛠️ Installation

The framework is included in the project and requires no additional installation. Simply import and use:

```python
from src.core.validation import ValidationManager
```

## 📖 Quick Start

### Basic Usage

```python
from src.core.validation import ValidationManager

# Initialize the validation manager
manager = ValidationManager()

# Validate data with a specific validator
results = manager.validate_with_validator("contract", contract_data)

# Check results
for result in results:
    if result.status == ValidationStatus.PASSED:
        print(f"✅ {result.rule_name}: {result.message}")
    else:
        print(f"❌ {result.rule_name}: {result.message}")
```

### Multi-Validator Validation

```python
# Validate complex data with multiple validators
project_data = {
    "contract": {...},
    "workflow": {...},
    "security": {...}
}

all_results = []
for validator_name, data in project_data.items():
    results = manager.validate_with_validator(validator_name, data)
    all_results.extend(results)

# Get overall summary
summary = manager.get_validation_summary()
print(f"Success rate: {summary['success_rate']:.1f}%")
```

## 🔧 Configuration

### Customizing Validation Rules

```python
# Override default rules
manager.set_validation_rule("contract", "budget_min", 1000)

# Add custom rules
manager.add_custom_rule("contract", "custom_rule", custom_validation_function)
```

### Validation Severity Levels

```python
from src.core.validation import ValidationSeverity

# Rules can have different severity levels
# - CRITICAL: Must pass for validation to succeed
# - HIGH: Important but not blocking
# - MEDIUM: Moderate importance
# - LOW: Informational only
```

## 📊 Validation Results

Each validation returns a `ValidationResult` object with:

- **Status**: PASSED, FAILED, or WARNING
- **Rule Name**: Name of the validation rule
- **Message**: Human-readable description
- **Severity**: CRITICAL, HIGH, MEDIUM, or LOW
- **Details**: Additional context and metadata

## 🎯 Use Cases

### 1. Contract Management

```python
contract_data = {
    "title": "Web Development Project",
    "priority": "HIGH",
    "deadline": "2024-06-30",
    "budget": 50000,
    "required_capabilities": ["python", "django", "react"]
}

results = manager.validate_with_validator("contract", contract_data)
```

### 2. Workflow Validation

```python
workflow_data = {
    "name": "Order Processing",
    "steps": [
        {"id": "start", "type": "start"},
        {"id": "process", "type": "process"},
        {"id": "end", "type": "end"}
    ],
    "transitions": [
        {"from_step": "start", "to_step": "process"},
        {"from_step": "process", "to_step": "end"}
    ]
}

results = manager.validate_with_validator("workflow", workflow_data)
```

### 3. Security Configuration

```python
security_data = {
    "security_level": "high",
    "authentication_method": "jwt",
    "encryption": {
        "algorithm": "AES-256",
        "key_rotation_days": 30
    }
}

results = manager.validate_with_validator("security", security_data)
```

### 4. Code Quality Assessment

```python
quality_data = {
    "file_path": "src/main.py",
    "metrics": {
        "cyclomatic_complexity": 5,
        "maintainability_index": 80,
        "test_coverage": 85.0
    }
}

results = manager.validate_with_validator("quality", quality_data)
```

## 🔍 Extending the Framework

### Adding New Validators

```python
from src.core.validation import BaseValidator, ValidationResult

class CustomValidator(BaseValidator):
    def __init__(self):
        super().__init__("custom")
        self.add_rule("custom_rule", self.validate_custom_rule)
    
    def validate_custom_rule(self, data):
        # Custom validation logic
        if some_condition:
            return ValidationResult(
                status=ValidationStatus.PASSED,
                rule_name="custom_rule",
                message="Validation passed"
            )
        else:
            return ValidationResult(
                status=ValidationStatus.FAILED,
                rule_name="custom_rule",
                message="Validation failed"
            )

# Register the validator
manager.register_validator(CustomValidator())
```

### Adding Custom Rules

```python
def custom_validation_function(data):
    # Custom validation logic
    return ValidationResult(...)

# Add to existing validator
manager.add_custom_rule("contract", "custom_rule", custom_validation_function)
```

## 🧪 Testing

Run the test suite to verify the framework:

```bash
# Run comprehensive tests
python src/core/validation/test_framework.py

# Run demo examples
python src/core/validation/demo.py
```

## 📈 Performance Considerations

- **Caching**: Validation results are cached for repeated validations
- **Lazy Loading**: Validators are loaded only when needed
- **Batch Processing**: Multiple validations can be processed efficiently
- **Async Support**: Future versions will support asynchronous validation

## 🔒 Security Features

- **Input Sanitization**: All input data is sanitized before validation
- **Rule Isolation**: Validation rules are isolated to prevent side effects
- **Audit Logging**: All validation attempts are logged for compliance
- **Rate Limiting**: Built-in protection against validation abuse

## 🤝 Contributing

When adding new validators or rules:

1. Follow the existing naming conventions
2. Include comprehensive tests
3. Document all new features
4. Ensure backward compatibility
5. Follow the project's coding standards

## 📚 API Reference

### ValidationManager

- `validate_with_validator(validator_name, data)`: Validate data with specific validator
- `validate_all(data)`: Validate data with all applicable validators
- `list_validators()`: Get list of available validators
- `get_validation_summary()`: Get overall validation statistics
- `register_validator(validator)`: Register a new validator
- `set_validation_rule(validator, rule_name, value)`: Override validation rule

### ValidationResult

- `status`: ValidationStatus (PASSED, FAILED, WARNING)
- `rule_name`: Name of the validation rule
- `message`: Human-readable description
- `severity`: ValidationSeverity (CRITICAL, HIGH, MEDIUM, LOW)
- `details`: Additional metadata dictionary

### ValidationStatus

- `PASSED`: Validation succeeded
- `FAILED`: Validation failed
- `WARNING`: Validation passed with warnings

### ValidationSeverity

- `CRITICAL`: Must pass for overall validation to succeed
- `HIGH`: Important validation rule
- `MEDIUM`: Moderate importance
- `LOW`: Informational validation

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the src directory is in your Python path
2. **Validator Not Found**: Check if the validator is properly registered
3. **Validation Failures**: Review the validation rules and data format
4. **Performance Issues**: Use caching and batch validation when possible

### Debug Mode

Enable debug logging for detailed validation information:

```python
import logging
logging.getLogger('src.core.validation').setLevel(logging.DEBUG)
```

## 📄 License

This framework is part of the Agent Cellphone V2 project and follows the project's licensing terms.

## 🤝 Support

For questions, issues, or contributions:

1. Check the existing documentation
2. Review the test examples
3. Submit an issue with detailed information
4. Follow the project's contribution guidelines

---

**Happy Validating! 🎉**
