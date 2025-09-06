/**
 * Chart State Callbacks Module - V2 Compliant
 * Chart state callback management functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// CHART STATE CALLBACKS MODULE
// ================================

/**
 * Chart state callback management functionality
 */
export class ChartStateCallbacksModule {
    constructor() {
        this.logger = console;
        this.chartCallbacks = [];
    }

    /**
     * Add callback for chart events
     */
    addCallback(event, callback) {
        try {
            if (typeof callback !== 'function') {
                throw new Error('Callback must be a function');
            }

            this.chartCallbacks.push({ event, callback, id: this.generateCallbackId() });
            return true;
        } catch (error) {
            this.logger.error('Failed to add callback:', error);
            return false;
        }
    }

    /**
     * Remove callback
     */
    removeCallback(event, callback) {
        try {
            this.chartCallbacks = this.chartCallbacks.filter(
                cb => !(cb.event === event && cb.callback === callback)
            );
            return true;
        } catch (error) {
            this.logger.error('Failed to remove callback:', error);
            return false;
        }
    }

    /**
     * Remove callback by ID
     */
    removeCallbackById(id) {
        try {
            this.chartCallbacks = this.chartCallbacks.filter(cb => cb.id !== id);
            return true;
        } catch (error) {
            this.logger.error('Failed to remove callback by ID:', error);
            return false;
        }
    }

    /**
     * Trigger callbacks for specific event
     */
    triggerCallbacks(event, data) {
        try {
            const relevantCallbacks = this.chartCallbacks.filter(cb => cb.event === event);

            relevantCallbacks.forEach(cb => {
                try {
                    cb.callback(data);
                } catch (error) {
                    this.logger.error('❌ Error in chart callback:', error);
                }
            });

            return relevantCallbacks.length;
        } catch (error) {
            this.logger.error('Failed to trigger callbacks:', error);
            return 0;
        }
    }

    /**
     * Generate unique callback ID
     */
    generateCallbackId() {
        return `chart_cb_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Get callbacks for event
     */
    getCallbacksForEvent(event) {
        return this.chartCallbacks.filter(cb => cb.event === event);
    }

    /**
     * Get all callbacks
     */
    getAllCallbacks() {
        return [...this.chartCallbacks];
    }

    /**
     * Clear all callbacks
     */
    clearAllCallbacks() {
        try {
            this.chartCallbacks = [];
            return true;
        } catch (error) {
            this.logger.error('Failed to clear callbacks:', error);
            return false;
        }
    }

    /**
     * Get callback statistics
     */
    getCallbackStatistics() {
        const eventCounts = {};
        this.chartCallbacks.forEach(cb => {
            eventCounts[cb.event] = (eventCounts[cb.event] || 0) + 1;
        });

        return {
            totalCallbacks: this.chartCallbacks.length,
            eventCounts,
            events: Object.keys(eventCounts)
        };
    }

    /**
     * Validate callback function
     */
    validateCallback(callback) {
        if (typeof callback !== 'function') {
            return { valid: false, error: 'Callback must be a function' };
        }

        if (callback.length === 0) {
            return { valid: false, error: 'Callback should accept parameters' };
        }

        return { valid: true };
    }

    /**
     * Add callback with validation
     */
    addCallbackValidated(event, callback) {
        const validation = this.validateCallback(callback);
        if (!validation.valid) {
            this.logger.error(`❌ Invalid callback for ${event}:`, validation.error);
            return false;
        }

        return this.addCallback(event, callback);
    }

    /**
     * Batch add callbacks
     */
    batchAddCallbacks(callbacks) {
        if (!Array.isArray(callbacks)) {
            this.logger.error('❌ Callbacks must be an array');
            return false;
        }

        let successCount = 0;
        callbacks.forEach(cb => {
            if (cb.event && cb.callback) {
                if (this.addCallbackValidated(cb.event, cb.callback)) {
                    successCount++;
                }
            }
        });

        this.logger.log(`✅ Added ${successCount}/${callbacks.length} callbacks`);
        return successCount === callbacks.length;
    }

    /**
     * Batch remove callbacks
     */
    batchRemoveCallbacks(callbacks) {
        if (!Array.isArray(callbacks)) {
            this.logger.error('❌ Callbacks must be an array');
            return false;
        }

        callbacks.forEach(cb => {
            if (cb.event && cb.callback) {
                this.removeCallback(cb.event, cb.callback);
            }
        });

        this.logger.log(`✅ Removed ${callbacks.length} callbacks`);
        return true;
    }

    /**
     * Cleanup callbacks module
     */
    cleanup() {
        try {
            this.clearAllCallbacks();
            this.logger.log('🧹 Chart state callbacks cleanup complete');
            return true;
        } catch (error) {
            this.logger.error('Failed to cleanup callbacks module:', error);
            return false;
        }
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create chart state callbacks module instance
 */
export function createChartStateCallbacksModule() {
    return new ChartStateCallbacksModule();
}
