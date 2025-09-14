/**
 * Configuration Manager - V2 Compliant Configuration System
 * V2 COMPLIANT: 100 lines maximum
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @description Centralized configuration management with validation
 */

// ================================
// CONFIGURATION MANAGER CLASS
// ================================

/**
 * Configuration Manager
 * Handles all application configuration with validation and persistence
 */
export class ConfigManager {
    constructor(options = {}) {
        this.storageKey = options.storageKey || 'v2swarm_config';
        this.config = { ...this.defaultConfig, ...options.initialConfig };
        this.validators = new Map();
        this.listeners = new Set();
        
        this.setupValidators();
    }

    /**
     * Default configuration values
     */
    get defaultConfig() {
        return {
            theme: 'dark',
            enableRealTimeUpdates: true,
            enableNotifications: true,
            refreshInterval: 30000,
            maxDataPoints: 100,
            aggressiveOptimization: true,
            tripleChecking: true,
            progressReporting: true,
            dominationMode: true,
            targetBenchmark: 99.5,
            api: {
                baseUrl: '/api',
                timeout: 5000,
                retryAttempts: 3
            },
            websocket: {
                url: 'ws://localhost:8080/ws',
                reconnectInterval: 5000,
                maxReconnectAttempts: 5
            },
            performance: {
                enableMonitoring: true,
                sampleRate: 0.1,
                maxMetrics: 1000
            }
        };
    }

    /**
     * Setup configuration validators
     */
    setupValidators() {
        this.validators.set('theme', (value) => ['dark', 'light'].includes(value));
        this.validators.set('refreshInterval', (value) => value >= 1000 && value <= 300000);
        this.validators.set('targetBenchmark', (value) => value >= 0 && value <= 100);
    }

    /**
     * Load configuration from storage
     */
    async load() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            if (stored) {
                const parsed = JSON.parse(stored);
                this.config = { ...this.defaultConfig, ...parsed };
            }
            console.log('✅ Configuration loaded');
        } catch (error) {
            console.warn('⚠️ Failed to load config, using defaults:', error);
        }
    }

    /**
     * Save configuration to storage
     */
    async save() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.config));
            console.log('✅ Configuration saved');
        } catch (error) {
            console.error('❌ Failed to save config:', error);
        }
    }

    /**
     * Update configuration with validation
     */
    async update(newConfig) {
        const validated = this.validateConfig(newConfig);
        this.config = { ...this.config, ...validated };
        await this.save();
        this.notifyListeners();
    }

    /**
     * Validate configuration values
     */
    validateConfig(config) {
        const validated = {};
        for (const [key, value] of Object.entries(config)) {
            const validator = this.validators.get(key);
            if (!validator || validator(value)) {
                validated[key] = value;
            } else {
                console.warn(`⚠️ Invalid config value for ${key}:`, value);
            }
        }
        return validated;
    }

    /**
     * Get configuration value
     */
    get(key, defaultValue = null) {
        return key ? this.config[key] || defaultValue : { ...this.config };
    }

    /**
     * Add configuration change listener
     */
    addListener(listener) {
        this.listeners.add(listener);
    }

    /**
     * Remove configuration change listener
     */
    removeListener(listener) {
        this.listeners.delete(listener);
    }

    /**
     * Notify listeners of configuration changes
     */
    notifyListeners() {
        this.listeners.forEach(listener => {
            try {
                listener(this.config);
            } catch (error) {
                console.error('❌ Config listener error:', error);
            }
        });
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create configuration manager with default settings
 */
export function createConfigManager(options = {}) {
    return new ConfigManager(options);
}

// Export default
export default ConfigManager;