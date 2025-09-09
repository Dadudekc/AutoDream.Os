/**
 * Data Service Module - V2 Compliant
 * Handles data loading, caching, and processing operations
 * V2 COMPLIANCE: <200 lines, single responsibility
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - MODULAR COMPONENT
 * @license MIT
 */

class DataService {
    constructor(config = {}) {
        this.config = { cacheTimeout: 5 * 60 * 1000, enableCaching: true, maxCacheSize: 100, ...config };
        this.cache = new Map();
        this.eventListeners = new Map();
        this.isInitialized = false;
    }

    async initialize() {
        if (this.isInitialized) return;
        console.log('📊 Initializing Data Service...');
        this.isInitialized = true;
    }

    async loadData(request) {
        const { endpoint, params = {}, forceRefresh = false } = request;
        const cacheKey = this.generateCacheKey(endpoint, params);

        if (!forceRefresh && this.config.enableCaching) {
            const cached = this.getCachedData(cacheKey);
            if (cached) return cached;
        }

        try {
            const response = await this.makeRequest(endpoint, params);
            const data = await response.json();

            if (this.config.enableCaching) {
                this.setCachedData(cacheKey, data);
            }

            this.emit('dataLoaded', { endpoint, params, data });
            return data;
        } catch (error) {
            console.error(`❌ Failed to load data from ${endpoint}:`, error);
            throw error;
        }
    }

    async makeRequest(endpoint, params = {}) {
        const url = new URL(endpoint, window.location.origin);
        Object.entries(params).forEach(([key, value]) => {
            if (value !== null && value !== undefined) {
                url.searchParams.append(key, String(value));
            }
        });

        const response = await fetch(url.toString(), {
            method: 'GET',
            headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' }
        });

        if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        return response;
    }

    processData(data, transformations = []) {
        let processed = { ...data };
        transformations.forEach(transform => {
            try {
                switch (transform.type) {
                    case 'filter': processed = this.filterData(processed, transform.criteria); break;
                    case 'sort': processed = this.sortData(processed, transform.field, transform.direction); break;
                    case 'map': processed = this.mapData(processed, transform.mapper); break;
                    case 'group': processed = this.groupData(processed, transform.field); break;
                }
            } catch (error) {
                console.warn(`Data transformation failed:`, transform, error);
            }
        });
        return processed;
    }

    filterData(data, criteria) {
        if (!Array.isArray(data)) return data;
        return data.filter(item =>
            Object.entries(criteria).every(([key, value]) =>
                this.getNestedValue(item, key) === value
            )
        );
    }

    sortData(data, field, direction = 'asc') {
        if (!Array.isArray(data)) return data;
        return [...data].sort((a, b) => {
            const aVal = this.getNestedValue(a, field);
            const bVal = this.getNestedValue(b, field);
            if (direction === 'desc') return aVal < bVal ? 1 : aVal > bVal ? -1 : 0;
            return aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
        });
    }

    mapData(data, mapper) { return Array.isArray(data) ? data.map(mapper) : data; }

    groupData(data, field) {
        if (!Array.isArray(data)) return {};
        return data.reduce((groups, item) => {
            const key = this.getNestedValue(item, field);
            if (!groups[key]) groups[key] = [];
            groups[key].push(item);
            return groups;
        }, {});
    }

    getNestedValue(obj, path) {
        try { return path.split('.').reduce((current, key) => current?.[key], obj); }
        catch (error) { return undefined; }
    }

    generateCacheKey(endpoint, params = {}) {
        const sortedParams = Object.keys(params).sort().map(key => `${key}:${params[key]}`).join('|');
        return `${endpoint}?${sortedParams}`;
    }

    getCachedData(key) {
        try {
            const cached = this.cache.get(key);
            if (!cached || Date.now() - cached.timestamp > this.config.cacheTimeout) {
                if (cached) this.cache.delete(key);
                return null;
            }
            return cached.data;
        } catch (error) { return null; }
    }

    setCachedData(key, data) {
        try {
            if (this.cache.size >= this.config.maxCacheSize) {
                const firstKey = this.cache.keys().next().value;
                this.cache.delete(firstKey);
            }
            this.cache.set(key, { data, timestamp: Date.now() });
        } catch (error) { console.warn('Cache storage failed:', error); }
    }

    clearCache() { this.cache.clear(); console.log('🧹 Data service cache cleared'); }

    on(event, callback) {
        if (!this.eventListeners.has(event)) this.eventListeners.set(event, []);
        this.eventListeners.get(event).push(callback);
    }

    emit(event, data) {
        const listeners = this.eventListeners.get(event);
        if (listeners) listeners.forEach(callback => { try { callback(data); } catch (error) { console.error('Event callback error:', error); } });
    }

    getStats() {
        return {
            cacheSize: this.cache.size,
            maxCacheSize: this.config.maxCacheSize,
            initialized: this.isInitialized
        };
    }

    async destroy() {
        this.clearCache();
        this.eventListeners.clear();
        this.isInitialized = false;
        console.log('🧹 Data service cleaned up');
    }
}

export { DataService };
export default DataService;
