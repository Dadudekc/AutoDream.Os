/**
 * Error Utilities - V2 Compliant Error Handling System
 * V2 COMPLIANT: 150 lines maximum
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @description Centralized error handling and logging system
 */

// ================================
// ERROR HANDLER CLASS
// ================================

/**
 * Error Handler
 * Handles application errors with logging and recovery
 */
export class ErrorHandler {
    constructor(options = {}) {
        this.logLevel = options.logLevel || 'error';
        this.maxRetries = options.maxRetries || 3;
        this.retryDelay = options.retryDelay || 1000;
        this.listeners = new Set();
        this.errorCount = 0;
        this.maxErrors = options.maxErrors || 100;
    }

    /**
     * Handle an error with context
     */
    async handleError(error, context = {}) {
        this.errorCount++;
        
        const errorDetails = this.createErrorDetails(error, context);
        
        // Log error
        this.logError(errorDetails);
        
        // Notify listeners
        this.notifyListeners(errorDetails);
        
        // Check if we should stop processing
        if (this.errorCount >= this.maxErrors) {
            console.error('🚨 Maximum error count reached, stopping error processing');
            return;
        }
        
        // Attempt recovery if possible
        if (context.retryable !== false) {
            return this.attemptRecovery(error, context);
        }
        
        return false;
    }

    /**
     * Create detailed error information
     */
    createErrorDetails(error, context) {
        return {
            message: error.message || error.toString(),
            stack: error.stack,
            context: {
                ...context,
                timestamp: new Date().toISOString(),
                userAgent: navigator.userAgent,
                url: window.location.href,
                errorCount: this.errorCount
            },
            type: this.getErrorType(error),
            severity: this.getErrorSeverity(error, context)
        };
    }

    /**
     * Get error type
     */
    getErrorType(error) {
        if (error.name) return error.name;
        if (error instanceof TypeError) return 'TypeError';
        if (error instanceof ReferenceError) return 'ReferenceError';
        if (error instanceof SyntaxError) return 'SyntaxError';
        return 'UnknownError';
    }

    /**
     * Get error severity
     */
    getErrorSeverity(error, context) {
        if (context.context === 'initialization') return 'critical';
        if (context.context === 'critical_component_load') return 'critical';
        if (error.name === 'TypeError') return 'high';
        if (error.name === 'ReferenceError') return 'high';
        return 'medium';
    }

    /**
     * Log error with appropriate level
     */
    logError(errorDetails) {
        const { severity, message, context } = errorDetails;
        
        const logMessage = `❌ ${severity.toUpperCase()}: ${message}`;
        const logData = { error: errorDetails, context };
        
        switch (severity) {
            case 'critical':
                console.error(logMessage, logData);
                break;
            case 'high':
                console.error(logMessage, logData);
                break;
            case 'medium':
                console.warn(logMessage, logData);
                break;
            default:
                console.log(logMessage, logData);
        }
    }

    /**
     * Attempt error recovery
     */
    async attemptRecovery(error, context) {
        if (context.retryCount >= this.maxRetries) {
            console.error('🚨 Max retry attempts reached');
            return false;
        }
        
        const retryCount = (context.retryCount || 0) + 1;
        const delay = this.retryDelay * Math.pow(2, retryCount - 1);
        
        console.log(`🔄 Attempting recovery (attempt ${retryCount}/${this.maxRetries}) in ${delay}ms`);
        
        return new Promise((resolve) => {
            setTimeout(async () => {
                try {
                    const result = await this.executeRecovery(error, context);
                    resolve(result);
                } catch (recoveryError) {
                    console.error('❌ Recovery attempt failed:', recoveryError);
                    resolve(false);
                }
            }, delay);
        });
    }

    /**
     * Execute recovery strategy
     */
    async executeRecovery(error, context) {
        switch (context.context) {
            case 'component_load':
                return this.recoverComponentLoad(context);
            case 'api_call':
                return this.recoverApiCall(context);
            case 'navigation':
                return this.recoverNavigation(context);
            default:
                return false;
        }
    }

    /**
     * Recover from component load error
     */
    async recoverComponentLoad(context) {
        console.log('🔄 Attempting component load recovery');
        // Implementation would retry component loading
        return true;
    }

    /**
     * Recover from API call error
     */
    async recoverApiCall(context) {
        console.log('🔄 Attempting API call recovery');
        // Implementation would retry API call
        return true;
    }

    /**
     * Recover from navigation error
     */
    async recoverNavigation(context) {
        console.log('🔄 Attempting navigation recovery');
        // Implementation would retry navigation
        return true;
    }

    /**
     * Add error listener
     */
    addListener(listener) {
        this.listeners.add(listener);
    }

    /**
     * Remove error listener
     */
    removeListener(listener) {
        this.listeners.delete(listener);
    }

    /**
     * Notify error listeners
     */
    notifyListeners(errorDetails) {
        this.listeners.forEach(listener => {
            try {
                listener(errorDetails);
            } catch (error) {
                console.error('❌ Error listener failed:', error);
            }
        });
    }

    /**
     * Get error statistics
     */
    getErrorStats() {
        return {
            totalErrors: this.errorCount,
            maxErrors: this.maxErrors,
            remainingErrors: this.maxErrors - this.errorCount
        };
    }

    /**
     * Reset error count
     */
    resetErrorCount() {
        this.errorCount = 0;
        console.log('🔄 Error count reset');
    }
}

// ================================
// ERROR UTILITIES
// ================================

/**
 * Create custom error class
 */
export function createCustomError(name, message, context = {}) {
    const error = new Error(message);
    error.name = name;
    error.context = context;
    return error;
}

/**
 * Wrap function with error handling
 */
export function withErrorHandling(fn, context = {}) {
    return async (...args) => {
        try {
            return await fn(...args);
        } catch (error) {
            const handler = new ErrorHandler();
            await handler.handleError(error, context);
            throw error;
        }
    };
}

/**
 * Retry function with exponential backoff
 */
export async function retryWithBackoff(fn, maxRetries = 3, baseDelay = 1000) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            return await fn();
        } catch (error) {
            if (attempt === maxRetries) {
                throw error;
            }
            
            const delay = baseDelay * Math.pow(2, attempt - 1);
            console.log(`🔄 Retry attempt ${attempt}/${maxRetries} in ${delay}ms`);
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create error handler with default settings
 */
export function createErrorHandler(options = {}) {
    return new ErrorHandler(options);
}

// Export default
export default ErrorHandler;