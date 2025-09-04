/**
 * Chart State Validation Module - V2 Compliant
 * Chart state validation functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// CHART STATE VALIDATION MODULE
// ================================

/**
 * Chart state validation functionality
 */
export class ChartStateValidationModule {
    constructor() {
        this.logger = {
            log: (message) => {
                // V2 Compliance: Use structured logging without console
                const timestamp = new Date().toISOString();
                const logEntry = `[${timestamp}] CHART-VALIDATION: ${message}`;
                // Store in memory for debugging if needed
                if (!this._logs) this._logs = [];
                this._logs.push(logEntry);
            },
            error: (message, error) => {
                const timestamp = new Date().toISOString();
                const errorEntry = `[${timestamp}] CHART-VALIDATION ERROR: ${message}`;
                if (!this._logs) this._logs = [];
                this._logs.push(errorEntry);
                this._logs.push(`Error details: ${error}`);
            }
        };
        this.validationRules = new Map([
            ['currentSymbol', { type: 'string', minLength: 1, maxLength: 10, pattern: /^[A-Z]+$/ }],
            ['timeframe', { type: 'string', enum: ['1m', '5m', '15m', '1h', '1d', '1w'] }],
            ['chartType', { type: 'string', enum: ['candlestick', 'line', 'bar', 'area'] }],
            ['indicators', { type: 'array', maxLength: 10 }],
            ['zoomLevel', { type: 'number', min: 0.1, max: 5 }],
            ['panOffset', { type: 'number', min: -1000, max: 1000 }],
            ['isInitialized', { type: 'boolean' }]
        ]);
    }

    /**
     * Validate state property
     */
    validateProperty(property, value) {
        const rule = this.validationRules.get(property);
        if (!rule) {
            return { valid: true, warning: `No validation rule for property: ${property}` };
        }

        return this.validateValue(value, rule, property);
    }

    /**
     * Validate value against rule
     */
    validateValue(value, rule, propertyName = 'value') {
        // Type validation first
        const typeResult = this.validateType(value, rule, propertyName);
        if (!typeResult.valid) return typeResult;

        // Specific validations based on type
        const specificResult = this.validateSpecificType(value, rule, propertyName);
        if (!specificResult.valid) return specificResult;

        // Enum validation
        const enumResult = this.validateEnum(value, rule, propertyName);
        if (!enumResult.valid) return enumResult;

        return { valid: true };
    }

    /**
     * Validate type
     */
    validateType(value, rule, propertyName) {
        if (rule.type && typeof value !== rule.type) {
            return {
                valid: false,
                error: `Property '${propertyName}' must be of type ${rule.type}, got ${typeof value}`
            };
        }
        return { valid: true };
    }

    /**
     * Validate type-specific constraints
     */
    validateSpecificType(value, rule, propertyName) {
        switch (rule.type) {
            case 'string':
                return this.validateStringConstraints(value, rule, propertyName);
            case 'number':
                return this.validateNumberConstraints(value, rule, propertyName);
            case 'array':
                return this.validateArrayConstraints(value, rule, propertyName);
            default:
                return { valid: true };
        }
    }

    /**
     * Validate string constraints
     */
    validateStringConstraints(value, rule, propertyName) {
        if (rule.minLength && value.length < rule.minLength) {
            return {
                valid: false,
                error: `Property '${propertyName}' must be at least ${rule.minLength} characters`
            };
        }
        if (rule.maxLength && value.length > rule.maxLength) {
            return {
                valid: false,
                error: `Property '${propertyName}' must be at most ${rule.maxLength} characters`
            };
        }
        if (rule.pattern && !rule.pattern.test(value)) {
            return {
                valid: false,
                error: `Property '${propertyName}' does not match required pattern`
            };
        }
        return { valid: true };
    }

    /**
     * Validate number constraints
     */
    validateNumberConstraints(value, rule, propertyName) {
        if (rule.min !== undefined && value < rule.min) {
            return {
                valid: false,
                error: `Property '${propertyName}' must be at least ${rule.min}`
            };
        }
        if (rule.max !== undefined && value > rule.max) {
            return {
                valid: false,
                error: `Property '${propertyName}' must be at most ${rule.max}`
            };
        }
        return { valid: true };
    }

    /**
     * Validate array constraints
     */
    validateArrayConstraints(value, rule, propertyName) {
        if (!Array.isArray(value)) {
            return {
                valid: false,
                error: `Property '${propertyName}' must be an array`
            };
        }
        if (rule.maxLength && value.length > rule.maxLength) {
            return {
                valid: false,
                error: `Property '${propertyName}' must have at most ${rule.maxLength} items`
            };
        }
        return { valid: true };
    }

    /**
     * Validate enum constraints
     */
    validateEnum(value, rule, propertyName) {
        if (rule.enum && !rule.enum.includes(value)) {
            return {
                valid: false,
                error: `Property '${propertyName}' must be one of: ${rule.enum.join(', ')}`
            };
        }
        return { valid: true };
    }

    /**
     * Validate entire state object
     */
    validateState(state) {
        const errors = [];
        const warnings = [];

        for (const [property, value] of Object.entries(state)) {
            const result = this.validateProperty(property, value);
            if (!result.valid) {
                errors.push(result.error);
            } else if (result.warning) {
                warnings.push(result.warning);
            }
        }

        return {
            valid: errors.length === 0,
            errors,
            warnings,
            propertyCount: Object.keys(state).length
        };
    }

    /**
     * Validate state transition
     */
    validateStateTransition(oldState, newState) {
        const errors = [];

        // Check for invalid transitions
        if (oldState.isInitialized && !newState.isInitialized) {
            errors.push('Cannot uninitialize an initialized state');
        }

        if (newState.zoomLevel < 0.1 && newState.zoomLevel !== oldState.zoomLevel) {
            errors.push('Zoom level cannot be less than 0.1');
        }

        if (Math.abs(newState.panOffset) > 1000) {
            errors.push('Pan offset cannot exceed 1000 in magnitude');
        }

        return {
            valid: errors.length === 0,
            errors,
            transition: {
                from: oldState,
                to: newState
            }
        };
    }

    /**
     * Sanitize state value
     */
    sanitizeValue(property, value) {
        const rule = this.validationRules.get(property);
        if (!rule) return value;

        try {
            return this.performSanitization(value, rule);
        } catch (error) {
            this.logger.error(`Failed to sanitize value for ${property}:`, error);
            return value;
        }
    }

    /**
     * Perform sanitization based on rule type
     */
    performSanitization(value, rule) {
        switch (rule.type) {
            case 'string':
                return this.sanitizeString(value, rule);
            case 'number':
                return this.sanitizeNumber(value, rule);
            case 'array':
                return this.sanitizeArray(value, rule);
            default:
                return value;
        }
    }

    /**
     * Sanitize string value
     */
    sanitizeString(value, rule) {
        if (typeof value !== 'string') return value;

        let sanitized = value.trim();
        if (rule.maxLength && sanitized.length > rule.maxLength) {
            sanitized = sanitized.substring(0, rule.maxLength);
        }
        return sanitized;
    }

    /**
     * Sanitize number value
     */
    sanitizeNumber(value, rule) {
        if (typeof value !== 'number') return value;

        let sanitized = value;
        if (rule.min !== undefined) sanitized = Math.max(sanitized, rule.min);
        if (rule.max !== undefined) sanitized = Math.min(sanitized, rule.max);
        return sanitized;
    }

    /**
     * Sanitize array value
     */
    sanitizeArray(value, rule) {
        if (!Array.isArray(value)) return value;

        if (rule.maxLength && value.length > rule.maxLength) {
            return value.slice(0, rule.maxLength);
        }
        return value;
    }

    /**
     * Add custom validation rule
     */
    addValidationRule(property, rule) {
        this.validationRules.set(property, rule);
        this.logger.log(`Added custom validation rule for ${property}`);
    }

    /**
     * Remove validation rule
     */
    removeValidationRule(property) {
        this.validationRules.delete(property);
        this.logger.log(`Removed validation rule for ${property}`);
    }

    /**
     * Get validation rules
     */
    getValidationRules() {
        return Object.fromEntries(this.validationRules);
    }

    /**
     * Get validation statistics
     */
    getValidationStatistics() {
        return {
            ruleCount: this.validationRules.size,
            properties: Array.from(this.validationRules.keys()),
            types: [...new Set(Array.from(this.validationRules.values()).map(r => r.type))]
        };
    }

    /**
     * Cleanup validation module
     */
    cleanup() {
        try {
            this.validationRules.clear();
            this.logger.log('🧹 Chart state validation cleanup complete');
            return true;
        } catch (error) {
            this.logger.error('Failed to cleanup validation module:', error);
            return false;
        }
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create chart state validation module instance
 */
export function createChartStateValidationModule() {
    return new ChartStateValidationModule();
}

