/**
 * Utility Function Service - V2 Compliant
 * Function utilities and miscellaneous helpers extracted from utility-service.js
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// UTILITY FUNCTION SERVICE
// ================================

/**
 * Function utilities and miscellaneous helper functions
 */
class UtilityFunctionService {
    constructor() {
        this.logger = console;
    }

    /**
     * Debounce function calls
     */
    debounce(func, delay) {
        let timeoutId;
        return (...args) => {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }

    /**
     * Throttle function calls
     */
    throttle(func, limit) {
        let inThrottle;
        return (...args) => {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    /**
     * Retry function with exponential backoff
     */
    async retryFunction(func, maxRetries = 3, baseDelay = 1000) {
        let lastError;

        for (let attempt = 0; attempt <= maxRetries; attempt++) {
            try {
                return await func();
            } catch (error) {
                lastError = error;

                if (attempt < maxRetries) {
                    const delay = baseDelay * Math.pow(2, attempt);
                    if (this.logger) {
                        this.logger.warn(`Function failed, retrying in ${delay}ms (attempt ${attempt + 1}/${maxRetries + 1})`);
                    }
                    await this.delay(delay);
                }
            }
        }

        throw lastError;
    }

    /**
     * Delay execution
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Memoize function results
     */
    memoize(func, keyGenerator = null) {
        const cache = new Map();

        return (...args) => {
            const key = keyGenerator ? keyGenerator(...args) : JSON.stringify(args);

            if (cache.has(key)) {
                return cache.get(key);
            }

            const result = func.apply(this, args);
            cache.set(key, result);
            return result;
        };
    }

    /**
     * Create timeout wrapper
     */
    withTimeout(func, timeoutMs) {
        return (...args) => {
            return Promise.race([
                func.apply(this, args),
                new Promise((_, reject) =>
                    setTimeout(() => reject(new Error('Operation timed out')), timeoutMs)
                )
            ]);
        };
    }

    /**
     * Check if running on mobile device
     */
    isMobileDevice() {
        if (typeof window === 'undefined') return false;

        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
            window.navigator.userAgent
        );
    }

    /**
     * Get browser information
     */
    getBrowserInfo() {
        if (typeof window === 'undefined') {
            return { name: 'unknown', version: 'unknown' };
        }

        const userAgent = window.navigator.userAgent;
        let browser = { name: 'unknown', version: 'unknown' };

        // Chrome
        if (userAgent.includes('Chrome')) {
            const match = userAgent.match(/Chrome\/(\d+)/);
            browser = { name: 'Chrome', version: match ? match[1] : 'unknown' };
        }
        // Firefox
        else if (userAgent.includes('Firefox')) {
            const match = userAgent.match(/Firefox\/(\d+)/);
            browser = { name: 'Firefox', version: match ? match[1] : 'unknown' };
        }
        // Safari
        else if (userAgent.includes('Safari') && !userAgent.includes('Chrome')) {
            const match = userAgent.match(/Version\/(\d+)/);
            browser = { name: 'Safari', version: match ? match[1] : 'unknown' };
        }
        // Edge
        else if (userAgent.includes('Edg')) {
            const match = userAgent.match(/Edg\/(\d+)/);
            browser = { name: 'Edge', version: match ? match[1] : 'unknown' };
        }

        return browser;
    }

    /**
     * Get file extension
     */
    getFileExtension(filename) {
        try {
            if (!filename || typeof filename !== 'string') {
                return '';
            }

            const lastDotIndex = filename.lastIndexOf('.');
            if (lastDotIndex === -1 || lastDotIndex === filename.length - 1) {
                return '';
            }

            return filename.substring(lastDotIndex + 1).toLowerCase();
        } catch (error) {
            this.logError('File extension extraction failed', error);
            return '';
        }
    }

    /**
     * Format file size
     */
    formatFileSize(bytes) {
        try {
            if (typeof bytes !== 'number' || bytes < 0) {
                return 'Invalid size';
            }

            if (bytes === 0) return '0 Bytes';

            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));

            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        } catch (error) {
            this.logError('File size formatting failed', error);
            return 'Unknown size';
        }
    }

    /**
     * Round to decimal places
     */
    roundToDecimal(value, decimals = 2) {
        try {
            if (typeof value !== 'number') {
                return value;
            }

            return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
        } catch (error) {
            this.logError('Decimal rounding failed', error);
            return value;
        }
    }

    /**
     * Calculate percentage
     */
    calculatePercentage(part, total) {
        try {
            if (typeof part !== 'number' || typeof total !== 'number') {
                return 0;
            }

            if (total === 0) {
                return 0;
            }

            return (part / total) * 100;
        } catch (error) {
            this.logError('Percentage calculation failed', error);
            return 0;
        }
    }

    /**
     * Generate UUID (simple version)
     */
    generateUUID() {
        try {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                const r = Math.random() * 16 | 0;
                const v = c === 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
        } catch (error) {
            this.logError('UUID generation failed', error);
            return '00000000-0000-0000-0000-000000000000';
        }
    }

    /**
     * Log error
     */
    logError(message, error) {
        this.logger.error(`[UtilityFunctionService] ${message}:`, error);
    }
}

// ================================
// GLOBAL FUNCTION SERVICE INSTANCE
// ================================

/**
 * Global utility function service instance
 */
const utilityFunctionService = new UtilityFunctionService();

// ================================
// FUNCTION SERVICE API FUNCTIONS
// ================================

/**
 * Debounce function
 */
export function debounce(func, delay) {
    return utilityFunctionService.debounce(func, delay);
}

/**
 * Throttle function
 */
export function throttle(func, limit) {
    return utilityFunctionService.throttle(func, limit);
}

/**
 * Check if mobile device
 */
export function isMobileDevice() {
    return utilityFunctionService.isMobileDevice();
}

/**
 * Get browser info
 */
export function getBrowserInfo() {
    return utilityFunctionService.getBrowserInfo();
}

/**
 * Get file extension
 */
export function getFileExtension(filename) {
    return utilityFunctionService.getFileExtension(filename);
}

/**
 * Format file size
 */
export function formatFileSize(bytes) {
    return utilityFunctionService.formatFileSize(bytes);
}

/**
 * Round to decimal
 */
export function roundToDecimal(value, decimals = 2) {
    return utilityFunctionService.roundToDecimal(value, decimals);
}

/**
 * Calculate percentage
 */
export function calculatePercentage(part, total) {
    return utilityFunctionService.calculatePercentage(part, total);
}

// ================================
// EXPORTS
// ================================

export { UtilityFunctionService, utilityFunctionService };
export default utilityFunctionService;
