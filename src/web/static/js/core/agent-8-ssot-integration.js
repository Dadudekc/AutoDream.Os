/**
 * Agent-8 SSOT Integration - Web Layer Implementation
 * Single Source of Truth integration for web layer components
 * V2 COMPLIANCE: Under 300-line limit
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - SSOT Integration System
 * @license MIT
 */

export class SSOTIntegration {
    constructor() {
        this.stateStore = new Map();
        this.subscribers = new Map();
        this.syncQueue = [];
        this.isOnline = navigator.onLine;
    }

    async configureWebLayerSSOT() {
        console.log('🔗 Configuring SSOT Integration for Web Layer...');

        this.setupStateManagement();
        this.setupCrossComponentSync();
        this.setupDataConsistency();
        this.setupOfflineSupport();

        console.log('✅ SSOT Integration configured for Web Layer');
    }

    setupStateManagement() {
        this.stateStore.set('dashboard', {});
        this.stateStore.set('services', {});
        this.stateStore.set('utilities', {});
        this.stateStore.set('user', {});
    }

    setupCrossComponentSync() {
        window.addEventListener('ssot:stateUpdate', (event) => {
            this.handleStateUpdate(event.detail);
        });

        window.addEventListener('online', () => {
            this.isOnline = true;
            this.syncOfflineChanges();
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
        });
    }

    setupDataConsistency() {
        this.consistencyRules = {
            user: ['id', 'preferences', 'session'],
            dashboard: ['layout', 'widgets', 'settings'],
            services: ['connections', 'status', 'config']
        };
    }

    setupOfflineSupport() {
        this.offlineQueue = [];
        this.loadPersistedState();
    }

    handleStateUpdate(update) {
        const { component, key, value, source } = update;

        if (this.validateUpdate(component, key, value)) {
            this.applyStateUpdate(component, key, value);
            this.notifySubscribers(component, key, value, source);
            this.persistState();
        }
    }

    validateUpdate(component, key, value) {
        if (!this.stateStore.has(component)) return false;
        if (!this.consistencyRules[component]?.includes(key)) return false;
        return true;
    }

    applyStateUpdate(component, key, value) {
        const componentState = this.stateStore.get(component);
        componentState[key] = value;
        componentState.lastUpdated = new Date().toISOString();
    }

    notifySubscribers(component, key, value, source) {
        const componentSubs = this.subscribers.get(component) || [];
        componentSubs.forEach(callback => {
            try {
                callback({ key, value, source, timestamp: new Date() });
            } catch (error) {
                console.error('SSOT subscriber error:', error);
            }
        });
    }

    subscribe(component, callback) {
        if (!this.subscribers.has(component)) {
            this.subscribers.set(component, []);
        }
        this.subscribers.get(component).push(callback);
    }

    unsubscribe(component, callback) {
        const componentSubs = this.subscribers.get(component) || [];
        const index = componentSubs.indexOf(callback);
        if (index > -1) {
            componentSubs.splice(index, 1);
        }
    }

    getState(component, key = null) {
        const componentState = this.stateStore.get(component);
        if (!componentState) return null;

        if (key) {
            return componentState[key] || null;
        }

        return { ...componentState };
    }

    updateState(component, key, value, source = 'unknown') {
        const update = { component, key, value, source };
        window.dispatchEvent(new CustomEvent('ssot:stateUpdate', { detail: update }));
    }

    persistState() {
        try {
            const stateObj = {};
            for (const [component, state] of this.stateStore) {
                stateObj[component] = state;
            }
            localStorage.setItem('ssot_state', JSON.stringify(stateObj));
        } catch (error) {
            console.warn('Failed to persist SSOT state:', error);
        }
    }

    loadPersistedState() {
        try {
            const persisted = localStorage.getItem('ssot_state');
            if (persisted) {
                const stateObj = JSON.parse(persisted);
                for (const [component, state] of Object.entries(stateObj)) {
                    this.stateStore.set(component, state);
                }
            }
        } catch (error) {
            console.warn('Failed to load persisted SSOT state:', error);
        }
    }

    syncOfflineChanges() {
        if (this.offlineQueue.length > 0) {
            console.log(`🔄 Syncing ${this.offlineQueue.length} offline changes...`);
            this.offlineQueue.forEach(update => {
                this.handleStateUpdate(update);
            });
            this.offlineQueue = [];
        }
    }

    getStateSnapshot() {
        const snapshot = {};
        for (const [component, state] of this.stateStore) {
            snapshot[component] = { ...state };
        }
        return {
            snapshot,
            timestamp: new Date().toISOString(),
            online: this.isOnline
        };
    }

    validateConsistency() {
        const issues = [];

        for (const [component, rules] of Object.entries(this.consistencyRules)) {
            const state = this.stateStore.get(component);
            if (!state) {
                issues.push(`Missing state for component: ${component}`);
                continue;
            }

            for (const rule of rules) {
                if (!(rule in state)) {
                    issues.push(`Missing required field '${rule}' in ${component}`);
                }
            }
        }

        return {
            valid: issues.length === 0,
            issues: issues
        };
    }
}

export function createSSOTIntegration() {
    return new SSOTIntegration();
}

export default SSOTIntegration;
