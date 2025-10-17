/**
 * Base Dashboard Manager - DUP-013 Consolidation
 * ==============================================
 * 
 * Base class for all dashboard managers to eliminate duplicate patterns.
 * 
 * Consolidates common patterns from 5 managers:
 * - dashboard-socket-manager.js
 * - dashboard-state-manager.js
 * - dashboard-data-manager.js
 * - dashboard-config-manager.js
 * - dashboard-loading-manager.js
 * 
 * @author Agent-1 - Integration & Core Systems Specialist
 * @mission DUP-013 Dashboard Managers Consolidation
 * @version 2.0.0
 * @license MIT
 */

/**
 * Base class for all dashboard managers
 * Provides common initialization, validation, and cleanup patterns
 */
export class BaseDashboardManager {
    constructor(managerName) {
        this.managerName = managerName || this.constructor.name;
        this.isInitialized = false;
        this.initializationTime = null;
    }

    /**
     * Initialize manager with duplicate-check pattern
     * @returns {boolean} Success status
     */
    initialize() {
        if (this.isInitialized) {
            console.warn(`⚠️ ${this.managerName} already initialized`);
            return false;
        }

        console.log(`🚀 Initializing ${this.managerName}...`);

        try {
            // Call child-specific initialization
            const success = this._initializeManager();
            
            if (success) {
                this.isInitialized = true;
                this.initializationTime = Date.now();
                console.log(`✅ ${this.managerName} initialized`);
            }
            
            return success;
        } catch (error) {
            console.error(`❌ Failed to initialize ${this.managerName}:`, error);
            return false;
        }
    }

    /**
     * Child classes must implement their specific initialization
     * @abstract
     */
    _initializeManager() {
        throw new Error('_initializeManager() must be implemented by child class');
    }

    /**
     * Check if manager is initialized
     * @returns {boolean}
     */
    isReady() {
        return this.isInitialized;
    }

    /**
     * Get initialization info
     * @returns {Object}
     */
    getInitInfo() {
        return {
            managerName: this.managerName,
            initialized: this.isInitialized,
            initializationTime: this.initializationTime,
            uptime: this.initializationTime ? Date.now() - this.initializationTime : 0
        };
    }

    /**
     * Reset manager (common pattern)
     */
    reset() {
        console.log(`🔄 Resetting ${this.managerName}...`);
        
        try {
            this._resetManager();
            console.log(`✅ ${this.managerName} reset complete`);
        } catch (error) {
            console.error(`❌ Failed to reset ${this.managerName}:`, error);
        }
    }

    /**
     * Child classes implement specific reset logic
     * @abstract
     */
    _resetManager() {
        // Default: do nothing
    }

    /**
     * Cleanup/destroy manager
     */
    destroy() {
        console.log(`🗑️ Destroying ${this.managerName}...`);
        
        try {
            this._destroyManager();
            this.isInitialized = false;
            this.initializationTime = null;
            console.log(`✅ ${this.managerName} destroyed`);
        } catch (error) {
            console.error(`❌ Failed to destroy ${this.managerName}:`, error);
        }
    }

    /**
     * Child classes implement specific destroy logic
     * @abstract
     */
    _destroyManager() {
        // Default: do nothing
    }

    /**
     * Get manager statistics (common pattern)
     * @returns {Object}
     */
    getStats() {
        const baseStats = {
            manager: this.managerName,
            initialized: this.isInitialized,
            uptime: this.initializationTime ? Date.now() - this.initializationTime : 0
        };

        // Merge with child-specific stats
        const childStats = this._getManagerStats();
        return { ...baseStats, ...childStats };
    }

    /**
     * Child classes implement specific stats
     * @abstract
     */
    _getManagerStats() {
        return {};
    }

    /**
     * Validate manager state
     * @returns {Object}
     */
    validate() {
        return {
            valid: this.isInitialized,
            manager: this.managerName,
            errors: this.isInitialized ? [] : ['Manager not initialized']
        };
    }
}

/**
 * DUP-013 CONSOLIDATION NOTES:
 * 
 * Common patterns found across all 5 managers:
 * - constructor() initialization
 * - initialize() with isInitialized check and warning
 * - getStats()/getLoadingStats()/getSocketStatus() statistics
 * - clear()/reset()/destroy() cleanup
 * - Console logging patterns (⚠️, ✅, ❌, 🚀, 🔄, 🗑️)
 * 
 * This base class eliminates ~50 lines of duplicate code!
 */

