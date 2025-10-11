/**
 * Unified Configuration System - Web Layer Integration
 * Centralized configuration management for web layer components
 * V2 COMPLIANCE: Under 300-line limit
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - Unified Configuration System
 * @license MIT
 */

export class UnifiedConfiguration {
    constructor() {
        this.config = {
            environment: this.detectEnvironment(),
            featureFlags: {},
            integrations: {},
            overrides: {}
        };
        this.listeners = [];
    }

    async configureWebLayerSettings() {
        console.log('⚙️ Configuring Unified Configuration System...');

        this.config.featureFlags = {
            newDashboard: true,
            realTimeUpdates: true,
            betaFeatures: false
        };

        this.config.integrations = {
            websocket: { enabled: true, url: 'ws://localhost:8080' },
            api: { baseUrl: 'http://localhost:3000/api', timeout: 10000 },
            analytics: { 
                enabled: this.config.environment === 'production',
                trackingId: this.config.environment === 'production' ? 'AGENT-CELLPHONE-V2' : 'dev-disabled',
                anonymizeIp: true,
                respectDoNotTrack: true
            }
        };

        this.setupConfigSync();
        console.log('✅ Unified Configuration System configured');
    }

    detectEnvironment() {
        if (window.location.hostname === 'localhost') return 'development';
        if (window.location.hostname.includes('staging')) return 'staging';
        return 'production';
    }

    get(key, defaultValue = null) {
        if (this.config.overrides[key] !== undefined) {
            return this.config.overrides[key];
        }

        const keys = key.split('.');
        let value = this.config;

        for (const k of keys) {
            if (value && typeof value === 'object' && k in value) {
                value = value[k];
            } else {
                return defaultValue;
            }
        }
        return value;
    }

    set(key, value) {
        this.config.overrides[key] = value;
        this.notifyListeners(key, value);
        this.persistConfig();
    }

    setupConfigSync() {
        this.loadPersistedConfig();
        window.addEventListener('storage', (e) => {
            if (e.key?.startsWith('config_')) {
                const key = e.key.replace('config_', '');
                this.config.overrides[key] = JSON.parse(e.newValue);
                this.notifyListeners(key, this.config.overrides[key]);
            }
        });
    }

    loadPersistedConfig() {
        try {
            const persisted = localStorage.getItem('unifiedConfig');
            if (persisted) this.config.overrides = JSON.parse(persisted);
        } catch (e) { console.warn('Config load failed:', e); }
    }

    persistConfig() {
        try {
            localStorage.setItem('unifiedConfig', JSON.stringify(this.config.overrides));
        } catch (e) { console.warn('Config save failed:', e); }
    }

    addListener(callback) { this.listeners.push(callback); }
    removeListener(callback) {
        const index = this.listeners.indexOf(callback);
        if (index > -1) this.listeners.splice(index, 1);
    }

    notifyListeners(key, value) {
        this.listeners.forEach(cb => {
            try { cb(key, value); } catch (e) {
                console.error('Listener error:', e);
            }
        });
    }

    getSnapshot() {
        return { ...this.config, timestamp: new Date().toISOString() };
    }

    validate() {
        const errors = [];
        if (!this.config.integrations.api) errors.push('API not configured');
        return { valid: errors.length === 0, errors };
    }
}

export function createUnifiedConfiguration() {
    return new UnifiedConfiguration();
}

export default UnifiedConfiguration;
