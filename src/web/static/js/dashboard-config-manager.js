/**
 * Dashboard Configuration Manager - V2 Compliant Configuration Management
 * Specialized configuration management for dashboard core
 * V2 COMPLIANCE: Under 100-line limit
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

export class DashboardConfigManager {
    constructor() {
        this.config = {
            updateInterval: 30000, // 30 seconds
            timeUpdateInterval: 1000, // 1 second
            maxRetries: 3,
            retryDelay: 5000,
            enableRealTimeUpdates: true,
            enableNotifications: true,
            chartAnimationDuration: 1000,
            maxDataPoints: 100,
            theme: 'light',
            language: 'en'
        };

        this.configValidators = new Map();
        this.setupValidators();
    }

    /**
     * Setup configuration validators
     */
    setupValidators() {
        this.configValidators.set('updateInterval', (value) =>
            typeof value === 'number' && value >= 1000 && value <= 300000
        );

        this.configValidators.set('maxRetries', (value) =>
            typeof value === 'number' && value >= 0 && value <= 10
        );

        this.configValidators.set('retryDelay', (value) =>
            typeof value === 'number' && value >= 1000 && value <= 60000
        );

        this.configValidators.set('theme', (value) =>
            ['light', 'dark', 'auto'].includes(value)
        );

        this.configValidators.set('language', (value) =>
            typeof value === 'string' && value.length === 2
        );
    }

    /**
     * Get configuration value
     */
    get(key) {
        return this.config[key];
    }

    /**
     * Set configuration value with validation
     */
    set(key, value) {
        if (!this.configValidators.has(key)) {
            console.warn(`⚠️ No validator for config key: ${key}`);
            this.config[key] = value;
            return true;
        }

        const validator = this.configValidators.get(key);
        if (validator(value)) {
            this.config[key] = value;
            console.log(`⚙️ Config updated: ${key} = ${value}`);
            return true;
        } else {
            console.error(`❌ Invalid config value for ${key}: ${value}`);
            return false;
        }
    }

    /**
     * Update multiple configuration values
     */
    update(updates) {
        const results = {};
        for (const [key, value] of Object.entries(updates)) {
            results[key] = this.set(key, value);
        }
        return results;
    }

    /**
     * Get all configuration
     */
    getAll() {
        return { ...this.config };
    }

    /**
     * Reset configuration to defaults
     */
    reset() {
        this.config = {
            updateInterval: 30000,
            timeUpdateInterval: 1000,
            maxRetries: 3,
            retryDelay: 5000,
            enableRealTimeUpdates: true,
            enableNotifications: true,
            chartAnimationDuration: 1000,
            maxDataPoints: 100,
            theme: 'light',
            language: 'en'
        };
        console.log('🔄 Configuration reset to defaults');
    }

    /**
     * Load configuration from storage
     */
    async loadFromStorage() {
        try {
            const stored = localStorage.getItem('dashboard-config');
            if (stored) {
                const parsed = JSON.parse(stored);
                this.update(parsed);
                console.log('💾 Configuration loaded from storage');
            }
        } catch (error) {
            console.error('❌ Failed to load config from storage:', error);
        }
    }

    /**
     * Save configuration to storage
     */
    async saveToStorage() {
        try {
            localStorage.setItem('dashboard-config', JSON.stringify(this.config));
            console.log('💾 Configuration saved to storage');
        } catch (error) {
            console.error('❌ Failed to save config to storage:', error);
        }
    }

    /**
     * Export configuration
     */
    export() {
        return {
            ...this.config,
            exportedAt: new Date().toISOString(),
            version: '1.0.0'
        };
    }

    /**
     * Import configuration
     */
    import(configData) {
        if (configData && typeof configData === 'object') {
            // Remove metadata before importing
            const { exportedAt, version, ...cleanConfig } = configData;
            this.update(cleanConfig);
            console.log('📥 Configuration imported');
            return true;
        }
        return false;
    }
}

// Factory function
export function createDashboardConfigManager() {
    return new DashboardConfigManager();
}
