/**
 * Chart State Rules - V2 Compliant Module
 * ======================================
 * 
 * Chart state validation rules and rule definitions.
 * 
 * V2 Compliance: < 300 lines, single responsibility.
 * 
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

export class ChartStateRules {
    constructor() {
        this.logger = console;
    }

    /**
     * Get all validation rules
     */
    getAllRules() {
        return {
            // Required field rules
            requiredFields: this.getRequiredFieldRules(),
            
            // Data type rules
            dataTypes: this.getDataTypeRules(),
            
            // Range validation rules
            ranges: this.getRangeRules(),
            
            // Business logic rules
            business: this.getBusinessRules(),
            
            // Performance rules
            performance: this.getPerformanceRules()
        };
    }

    /**
     * Get required field validation rules
     */
    getRequiredFieldRules() {
        return {
            chartId: (state) => ({
                isValid: !!state.chartId,
                message: 'Chart ID is required',
                field: 'chartId',
                severity: 'error'
            }),
            
            chartType: (state) => ({
                isValid: !!state.chartType,
                message: 'Chart type is required',
                field: 'chartType',
                severity: 'error'
            }),
            
            data: (state) => ({
                isValid: !!state.data && Array.isArray(state.data),
                message: 'Chart data is required and must be an array',
                field: 'data',
                severity: 'error'
            })
        };
    }

    /**
     * Get data type validation rules
     */
    getDataTypeRules() {
        return {
            chartIdString: (state) => ({
                isValid: typeof state.chartId === 'string',
                message: 'Chart ID must be a string',
                field: 'chartId',
                severity: 'error'
            }),
            
            chartTypeString: (state) => ({
                isValid: typeof state.chartType === 'string',
                message: 'Chart type must be a string',
                field: 'chartType',
                severity: 'error'
            }),
            
            dataArray: (state) => ({
                isValid: Array.isArray(state.data),
                message: 'Data must be an array',
                field: 'data',
                severity: 'error'
            }),
            
            optionsObject: (state) => ({
                isValid: !state.options || typeof state.options === 'object',
                message: 'Options must be an object',
                field: 'options',
                severity: 'error'
            })
        };
    }

    /**
     * Get range validation rules
     */
    getRangeRules() {
        return {
            dataLength: (state) => ({
                isValid: !state.data || state.data.length > 0,
                message: 'Data array cannot be empty',
                field: 'data',
                severity: 'error'
            }),
            
            dataLengthMax: (state) => ({
                isValid: !state.data || state.data.length <= 10000,
                message: 'Data array cannot exceed 10,000 items',
                field: 'data',
                severity: 'warning'
            }),
            
            chartIdLength: (state) => ({
                isValid: !state.chartId || state.chartId.length <= 100,
                message: 'Chart ID cannot exceed 100 characters',
                field: 'chartId',
                severity: 'warning'
            })
        };
    }

    /**
     * Get business logic validation rules
     */
    getBusinessRules() {
        return {
            validChartType: (state) => {
                const validTypes = ['line', 'bar', 'pie', 'scatter', 'area', 'candlestick'];
                return {
                    isValid: !state.chartType || validTypes.includes(state.chartType),
                    message: `Chart type must be one of: ${validTypes.join(', ')}`,
                    field: 'chartType',
                    severity: 'error'
                };
            },
            
            dataStructure: (state) => {
                if (!state.data || !Array.isArray(state.data)) {
                    return { isValid: true, message: '', field: 'data', severity: 'error' };
                }
                
                const hasValidStructure = state.data.every(item => 
                    item && typeof item === 'object' && 
                    (item.x !== undefined || item.label !== undefined) &&
                    (item.y !== undefined || item.value !== undefined)
                );
                
                return {
                    isValid: hasValidStructure,
                    message: 'Data items must have x/label and y/value properties',
                    field: 'data',
                    severity: 'error'
                };
            },
            
            optionsValidation: (state) => {
                if (!state.options) {
                    return { isValid: true, message: '', field: 'options', severity: 'error' };
                }
                
                const validOptions = ['title', 'xAxis', 'yAxis', 'legend', 'tooltip', 'colors'];
                const invalidKeys = Object.keys(state.options).filter(key => !validOptions.includes(key));
                
                return {
                    isValid: invalidKeys.length === 0,
                    message: `Invalid option keys: ${invalidKeys.join(', ')}`,
                    field: 'options',
                    severity: 'warning'
                };
            }
        };
    }

    /**
     * Get performance validation rules
     */
    getPerformanceRules() {
        return {
            dataSize: (state) => {
                if (!state.data) {
                    return { isValid: true, message: '', field: 'data', severity: 'error' };
                }
                
                const dataSize = JSON.stringify(state.data).length;
                const maxSize = 1024 * 1024; // 1MB
                
                return {
                    isValid: dataSize <= maxSize,
                    message: `Data size (${Math.round(dataSize / 1024)}KB) exceeds recommended limit`,
                    field: 'data',
                    severity: 'warning'
                };
            },
            
            updateFrequency: (state) => {
                if (!state.lastUpdate) {
                    return { isValid: true, message: '', field: 'lastUpdate', severity: 'error' };
                }
                
                const timeSinceUpdate = Date.now() - state.lastUpdate;
                const maxUpdateInterval = 60000; // 1 minute
                
                return {
                    isValid: timeSinceUpdate <= maxUpdateInterval,
                    message: 'Chart state has not been updated recently',
                    field: 'lastUpdate',
                    severity: 'warning'
                };
            }
        };
    }

    /**
     * Get rule by name
     */
    getRule(ruleName) {
        const allRules = this.getAllRules();
        
        for (const category of Object.values(allRules)) {
            if (category[ruleName]) {
                return category[ruleName];
            }
        }
        
        return null;
    }

    /**
     * Get rules by category
     */
    getRulesByCategory(category) {
        const allRules = this.getAllRules();
        return allRules[category] || {};
    }

    /**
     * Validate rule definition
     */
    validateRuleDefinition(rule) {
        if (typeof rule !== 'function') {
            return { isValid: false, message: 'Rule must be a function' };
        }
        
        try {
            const testResult = rule({});
            if (!testResult || typeof testResult.isValid !== 'boolean') {
                return { isValid: false, message: 'Rule must return an object with isValid property' };
            }
            
            return { isValid: true };
        } catch (error) {
            return { isValid: false, message: `Rule execution error: ${error.message}` };
        }
    }
}
