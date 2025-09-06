/**
 * Data Validation Module - V2 Compliant
 * Handles data structure and API response validation
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// DATA VALIDATION MODULE
// ================================

/**
 * Data validation module for complex data structures
 */
export class DataValidationModule {
    constructor() {
        this.logger = console;
    }

    /**
     * Validate dashboard configuration
     */
    validateDashboardConfig(config) {
        try {
            if (!config || typeof config !== 'object') {
                return { isValid: false, error: 'Dashboard configuration must be a valid object' };
            }

            const requiredFields = ['id', 'title'];
            const missingFields = requiredFields.filter(field => !config[field]);

            if (missingFields.length > 0) {
                return {
                    isValid: false,
                    error: `Dashboard configuration missing required fields: ${missingFields.join(', ')}`
                };
            }

            return { isValid: true, error: null };
        } catch (error) {
            this.logError('Dashboard config validation failed', error);
            return { isValid: false, error: 'Dashboard config validation error' };
        }
    }

    /**
     * Validate chart data structure
     */
    validateChartData(data) {
        try {
            if (!data || !Array.isArray(data)) {
                return { isValid: false, error: 'Chart data must be a valid array' };
            }

            if (data.length === 0) {
                return { isValid: false, error: 'Chart data cannot be empty' };
            }

            // Validate data structure
            const requiredFields = ['label', 'value'];
            for (let i = 0; i < data.length; i++) {
                const item = data[i];
                if (!item || typeof item !== 'object') {
                    return { isValid: false, error: `Chart data item ${i} must be an object` };
                }

                const missingFields = requiredFields.filter(field => !(field in item));
                if (missingFields.length > 0) {
                    return {
                        isValid: false,
                        error: `Chart data item ${i} missing required fields: ${missingFields.join(', ')}`
                    };
                }
            }

            return { isValid: true, error: null };
        } catch (error) {
            this.logError('Chart data validation failed', error);
            return { isValid: false, error: 'Chart data validation error' };
        }
    }

    /**
     * Validate API response structure
     */
    validateApiResponse(response, expectedStructure = {}) {
        try {
            if (!response || typeof response !== 'object') {
                return { isValid: false, error: 'API response must be a valid object' };
            }

            // Check expected structure if provided
            if (Object.keys(expectedStructure).length > 0) {
                for (const [key, expectedType] of Object.entries(expectedStructure)) {
                    if (!(key in response)) {
                        return { isValid: false, error: `API response missing required field: ${key}` };
                    }

                    if (typeof response[key] !== expectedType) {
                        return { isValid: false, error: `API response field ${key} must be of type ${expectedType}` };
                    }
                }
            }

            return { isValid: true, error: null };
        } catch (error) {
            this.logError('API response validation failed', error);
            return { isValid: false, error: 'API response validation error' };
        }
    }

    /**
     * Validate trading data structure
     */
    validateTradingData(data) {
        try {
            if (!data || typeof data !== 'object') {
                return { isValid: false, error: 'Trading data must be a valid object' };
            }

            const requiredFields = ['symbol', 'price', 'timestamp'];
            const missingFields = requiredFields.filter(field => !(field in data));

            if (missingFields.length > 0) {
                return {
                    isValid: false,
                    error: `Trading data missing required fields: ${missingFields.join(', ')}`
                };
            }

            // Validate price is numeric
            if (typeof data.price !== 'number' || isNaN(data.price) || data.price <= 0) {
                return { isValid: false, error: 'Price must be a valid positive number' };
            }

            // Validate timestamp
            if (typeof data.timestamp !== 'number' && typeof data.timestamp !== 'string') {
                return { isValid: false, error: 'Timestamp must be a valid number or string' };
            }

            return { isValid: true, error: null };
        } catch (error) {
            this.logError('Trading data validation failed', error);
            return { isValid: false, error: 'Trading data validation error' };
        }
    }

    /**
     * Validate portfolio data structure
     */
    validatePortfolioData(data) {
        try {
            if (!data || !Array.isArray(data)) {
                return { isValid: false, error: 'Portfolio data must be a valid array' };
            }

            for (let i = 0; i < data.length; i++) {
                const item = data[i];
                if (!item || typeof item !== 'object') {
                    return { isValid: false, error: `Portfolio item ${i} must be an object` };
                }

                const requiredFields = ['symbol', 'quantity', 'averagePrice'];
                const missingFields = requiredFields.filter(field => !(field in item));

                if (missingFields.length > 0) {
                    return {
                        isValid: false,
                        error: `Portfolio item ${i} missing required fields: ${missingFields.join(', ')}`
                    };
                }
            }

            return { isValid: true, error: null };
        } catch (error) {
            this.logError('Portfolio data validation failed', error);
            return { isValid: false, error: 'Portfolio data validation error' };
        }
    }

    /**
     * Log error with context
     */
    logError(message, error) {
        this.logger.error(`[DataValidationModule] ${message}:`, error);
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create data validation module instance
 */
export function createDataValidationModule() {
    return new DataValidationModule();
}
