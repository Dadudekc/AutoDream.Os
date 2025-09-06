/**
 * Function Utilities - V2 Compliant Module
 * Function-related utilities: debounce, throttle, retry, etc.
 * MODULAR: ~120 lines (V2 compliant)
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE MODULAR EXTRACTION
 * @license MIT
 */

export class FunctionUtils {
    constructor() {
        this.logger = new UnifiedLoggingSystem("FunctionUtils");
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
    async retry(func, maxRetries = 3, baseDelay = 1000) {
        let lastError;

        for (let attempt = 0; attempt < maxRetries; attempt++) {
            try {
                return await func();
            } catch (error) {
                lastError = error;
                if (attempt < maxRetries - 1) {
                    const delay = baseDelay * Math.pow(2, attempt);
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
            }
        }

        throw lastError;
    }

    /**
     * Memoize function results
     */
    memoize(func, getKey = (...args) => JSON.stringify(args)) {
        const cache = new Map();

        return (...args) => {
            const key = getKey(...args);
            if (cache.has(key)) {
                return cache.get(key);
            }

            const result = func.apply(this, args);
            cache.set(key, result);
            return result;
        };
    }

    /**
     * Create a pipeline of functions
     */
    pipe(...fns) {
        return (initialValue) => {
            return fns.reduce((value, fn) => fn(value), initialValue);
        };
    }
}
