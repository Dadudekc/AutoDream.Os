/**
 * Dashboard Validation Utilities Module - V2 Compliant
 * Validation utilities specific to dashboard operations
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export const DashboardValidationUtils = {
    /**
     * Validate dashboard configuration
     */
    validateDashboardConfig(config) {
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
    },

    /**
     * Validate chart data
     */
    validateChartData(data) {
        if (!Array.isArray(data)) {
            return { isValid: false, error: 'Chart data must be an array' };
        }

        if (data.length === 0) {
            return { isValid: false, error: 'Chart data cannot be empty' };
        }

        // Validate first item structure
        const firstItem = data[0];
        if (!firstItem || typeof firstItem !== 'object') {
            return { isValid: false, error: 'Chart data items must be objects' };
        }

        return { isValid: true, error: null };
    },

    /**
     * Validate dashboard permissions
     */
    validatePermissions(user, requiredPermissions = []) {
        if (!user || !user.permissions) {
            return { isValid: false, error: 'User permissions not available' };
        }

        const missingPermissions = requiredPermissions.filter(
            permission => !user.permissions.includes(permission)
        );

        if (missingPermissions.length > 0) {
            return {
                isValid: false,
                error: `Missing required permissions: ${missingPermissions.join(', ')}`
            };
        }

        return { isValid: true, error: null };
    },

    /**
     * Validate date range
     */
    validateDateRange(startDate, endDate) {
        if (!startDate || !endDate) {
            return { isValid: false, error: 'Both start and end dates are required' };
        }

        const start = new Date(startDate);
        const end = new Date(endDate);

        if (isNaN(start.getTime()) || isNaN(end.getTime())) {
            return { isValid: false, error: 'Invalid date format' };
        }

        if (start > end) {
            return { isValid: false, error: 'Start date cannot be after end date' };
        }

        return { isValid: true, error: null };
    },

    /**
     * Validate numeric range for dashboard metrics
     */
    validateMetricRange(value, min = 0, max = Number.MAX_SAFE_INTEGER, fieldName = 'value') {
        if (typeof value !== 'number' || isNaN(value)) {
            return { isValid: false, error: `${fieldName} must be a valid number` };
        }

        if (value < min) {
            return { isValid: false, error: `${fieldName} must be at least ${min}` };
        }

        if (value > max) {
            return { isValid: false, error: `${fieldName} must be at most ${max}` };
        }

        return { isValid: true, error: null };
    },

    /**
     * Validate dashboard component props
     */
    validateComponentProps(props, requiredProps = []) {
        if (!props || typeof props !== 'object') {
            return { isValid: false, error: 'Component props must be a valid object' };
        }

        const missingProps = requiredProps.filter(prop => props[prop] === undefined);

        if (missingProps.length > 0) {
            return {
                isValid: false,
                error: `Missing required component props: ${missingProps.join(', ')}`
            };
        }

        return { isValid: true, error: null };
    },

    /**
     * Validate API response structure
     */
    validateApiResponse(response, expectedStructure = {}) {
        if (!response || typeof response !== 'object') {
            return { isValid: false, error: 'API response must be a valid object' };
        }

        // Check for common API response fields
        if (expectedStructure.hasOwnProperty('success') && typeof response.success !== 'boolean') {
            return { isValid: false, error: 'API response missing valid success field' };
        }

        if (expectedStructure.hasOwnProperty('data') && !response.data) {
            return { isValid: false, error: 'API response missing data field' };
        }

        return { isValid: true, error: null };
    },

    /**
     * Validate form input
     */
    validateFormInput(value, rules = {}) {
        const errors = [];

        // Required validation
        if (rules.required && (!value || (typeof value === 'string' && value.trim() === ''))) {
            errors.push('This field is required');
        }

        // Type validation
        if (rules.type && typeof value !== rules.type) {
            errors.push(`Must be of type ${rules.type}`);
        }

        // Length validation
        if (rules.minLength && typeof value === 'string' && value.length < rules.minLength) {
            errors.push(`Must be at least ${rules.minLength} characters`);
        }

        if (rules.maxLength && typeof value === 'string' && value.length > rules.maxLength) {
            errors.push(`Must be at most ${rules.maxLength} characters`);
        }

        // Pattern validation
        if (rules.pattern && typeof value === 'string' && !rules.pattern.test(value)) {
            errors.push('Invalid format');
        }

        return {
            isValid: errors.length === 0,
            error: errors.length > 0 ? errors[0] : null,
            allErrors: errors
        };
    }
};

// Factory function for creating validation utils instance
export function createDashboardValidationUtils() {
    return { ...DashboardValidationUtils };
}


