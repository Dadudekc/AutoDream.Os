/**
 * Utility Validation Service - V2 Compliant with Modular Architecture
 * Main orchestrator using specialized validation modules
 * REFACTORED: 327 lines → ~127 lines (61% reduction)
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist, Agent-8 - Integration & Performance Specialist
 * @version 4.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

// ================================
// IMPORT MODULAR VALIDATION COMPONENTS
// ================================

import { UnifiedLoggingSystem } from './utilities/logging-utils.js';
import { ValidationUtils } from '../../utilities/validation-utils.js';

// ================================
// UTILITY VALIDATION SERVICE V4
// ================================

/**
 * Main orchestrator for validation utilities using modular architecture
 * V2 COMPLIANT: Delegates to specialized validation modules for specific functionality
 */
export class UtilityValidationService {
    constructor() {
        this.logger = new UnifiedLoggingSystem("UtilityValidationService");
        this.validationUtils = new ValidationUtils();
    }

    // ================================
    // DELEGATION METHODS - CORE VALIDATIONS
    // ================================

    /**
     * Validate email address
     */
    validateEmail(email) {
        const result = this.validationUtils.isValidEmail(email);
        return {
            valid: result,
            message: result ? 'Email is valid' : 'Invalid email format'
        };
    }

    /**
     * Validate URL
     */
    validateUrl(url) {
        const result = this.validationUtils.isValidUrl(url);
        return {
            valid: result,
            message: result ? 'URL is valid' : 'Invalid URL format'
        };
    }

    /**
     * Validate phone number
     */
    validatePhone(phone) {
        const result = this.validationUtils.isValidPhone(phone);
        return {
            valid: result,
            message: result ? 'Phone number is valid' : 'Invalid phone number format'
        };
    }

    /**
     * Validate required field
     */
    validateRequired(value, fieldName) {
        try {
            this.validationUtils.validateRequired(value, fieldName);
            return { valid: true, message: `${fieldName} is valid` };
        } catch (error) {
            return { valid: false, message: error.message };
        }
    }

    /**
     * Validate string length
     */
    validateLength(str, min = 0, max = Infinity, fieldName = 'string') {
        try {
            this.validationUtils.validateLength(str, min, max, fieldName);
            return { valid: true, message: `${fieldName} length is valid` };
        } catch (error) {
            return { valid: false, message: error.message };
        }
    }

    /**
     * Sanitize string input
     */
    sanitizeString(str) {
        return this.validationUtils.sanitizeString(str);
    }
}

// ================================
// LEGACY EXPORTS FOR BACKWARD COMPATIBILITY
// ================================

const utilityValidationService = new UtilityValidationService();

/**
 * Legacy validation functions export
 */
export function validateEmail(email) {
    return utilityValidationService.validateEmail(email);
}

export function validateUrl(url) {
    return utilityValidationService.validateUrl(url);
}

export function validatePhone(phone) {
    return utilityValidationService.validatePhone(phone);
}

// ================================
// EXPORTS
// ================================

export default UtilityValidationService;