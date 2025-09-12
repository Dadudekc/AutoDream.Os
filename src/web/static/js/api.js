/**
 * API Integration Layer - V2 SWARM Web Interface
 * Aggressive API integration with competitive performance optimization
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - COMPETITIVE_DOMINATION_MODE
 */

class V2SwarmAPI {
    constructor() {
        this.baseURL = '/api/v1';
        this.timeout = 5000; // Aggressive 5-second timeout
        this.retryAttempts = 3;
        this.cache = new Map();
        this.cacheTimeout = 30000; // 30-second cache

        this.endpoints = {
            health: '/health',
            agents: '/agents',
            messages: '/messages',
            coordination: '/coordination',
            analytics: '/analytics',
            tasks: '/tasks',
            metrics: '/metrics',
            config: '/config'
        };
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const cacheKey = `${options.method || 'GET'}_${url}_${JSON.stringify(options.body || {})}`;

        // Check cache for GET requests
        if (!options.method || options.method === 'GET') {
            const cached = this.getCached(cacheKey);
            if (cached) return cached;
        }

        const config = {
            method: options.method || 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                ...options.headers
            },
            ...options
        };

        // Add body for non-GET requests
        if (options.body && typeof options.body === 'object') {
            config.body = JSON.stringify(options.body);
        }

        let lastError;
        for (let attempt = 1; attempt <= this.retryAttempts; attempt++) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), this.timeout);

                const response = await fetch(url, {
                    ...config,
                    signal: controller.signal
                });

                clearTimeout(timeoutId);

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();

                // Cache successful GET responses
                if (config.method === 'GET') {
                    this.setCached(cacheKey, data);
                }

                return data;

            } catch (error) {
                lastError = error;

                if (attempt === this.retryAttempts) {
                    break;
                }

                // Exponential backoff
                const delay = Math.min(1000 * Math.pow(2, attempt - 1), 5000);
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }

        throw lastError;
    }

    getCached(key) {
        const cached = this.cache.get(key);
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }
        this.cache.delete(key);
        return null;
    }

    setCached(key, data) {
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });
    }

    // Health check with competitive monitoring
    async health() {
        try {
            const start = performance.now();
            const result = await this.request(this.endpoints.health);
            const end = performance.now();

            return {
                ...result,
                responseTime: end - start,
                status: 'healthy'
            };
        } catch (error) {
            return {
                status: 'unhealthy',
                error: error.message,
                responseTime: this.timeout
            };
        }
    }

    // Agents API with aggressive caching
    async getAgents() {
        return this.request(this.endpoints.agents);
    }

    async getAgent(id) {
        return this.request(`${this.endpoints.agents}/${id}`);
    }

    async updateAgent(id, data) {
        return this.request(`${this.endpoints.agents}/${id}`, {
            method: 'PUT',
            body: data
        });
    }

    // Messages API with real-time optimization
    async getMessages(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = queryString ? `${this.endpoints.messages}?${queryString}` : this.endpoints.messages;
        return this.request(endpoint);
    }

    async sendMessage(message) {
        return this.request(this.endpoints.messages, {
            method: 'POST',
            body: message
        });
    }

    // Coordination API for swarm intelligence
    async getCoordinationStatus() {
        return this.request(`${this.endpoints.coordination}/status`);
    }

    async updateCoordination(data) {
        return this.request(this.endpoints.coordination, {
            method: 'PUT',
            body: data
        });
    }

    // Analytics API with performance optimization
    async getAnalytics(timeframe = '1h') {
        return this.request(`${this.endpoints.analytics}?timeframe=${timeframe}`);
    }

    async getMetrics() {
        return this.request(this.endpoints.metrics);
    }

    // Tasks API for competitive task management
    async getTasks(status = null) {
        const endpoint = status ? `${this.endpoints.tasks}?status=${status}` : this.endpoints.tasks;
        return this.request(endpoint);
    }

    async createTask(task) {
        return this.request(this.endpoints.tasks, {
            method: 'POST',
            body: task
        });
    }

    async updateTask(id, updates) {
        return this.request(`${this.endpoints.tasks}/${id}`, {
            method: 'PUT',
            body: updates
        });
    }

    // Configuration API for competitive settings
    async getConfig() {
        return this.request(this.endpoints.config);
    }

    async updateConfig(config) {
        return this.request(this.endpoints.config, {
            method: 'PUT',
            body: config
        });
    }

    // Bulk operations for competitive performance
    async bulkUpdateAgents(updates) {
        return this.request(`${this.endpoints.agents}/bulk`, {
            method: 'PUT',
            body: { updates }
        });
    }

    async bulkSendMessages(messages) {
        return this.request(`${this.endpoints.messages}/bulk`, {
            method: 'POST',
            body: { messages }
        });
    }

    // Competitive monitoring endpoints
    async getPerformanceMetrics() {
        return this.request('/api/performance/metrics');
    }

    async getDominationStatus() {
        return this.request('/api/competitive/domination');
    }

    async reportProgress(report) {
        return this.request('/api/competitive/progress', {
            method: 'POST',
            body: report
        });
    }

    // Error handling with competitive recovery
    handleError(error, endpoint, attempt = 1) {
        console.error(`API Error (attempt ${attempt}):`, error);

        // Competitive error reporting
        if (window.v2swarm) {
            window.v2swarm.handleError('api', {
                error: error.message,
                endpoint,
                attempt,
                timestamp: new Date().toISOString()
            });
        }

        // Return error classification for competitive analysis
        return {
            type: this.classifyError(error),
            retryable: this.isRetryableError(error),
            severity: this.getErrorSeverity(error),
            endpoint,
            attempt
        };
    }

    classifyError(error) {
        if (error.name === 'AbortError') return 'timeout';
        if (error.message.includes('404')) return 'not_found';
        if (error.message.includes('403')) return 'forbidden';
        if (error.message.includes('500')) return 'server_error';
        if (error.message.includes('network') || error.message.includes('fetch')) return 'network_error';
        return 'unknown';
    }

    isRetryableError(error) {
        const retryableCodes = [408, 429, 500, 502, 503, 504]; // Timeout, rate limit, server errors
        const errorMessage = error.message || '';
        return retryableCodes.some(code => errorMessage.includes(code.toString())) ||
               error.name === 'AbortError' ||
               errorMessage.includes('network') ||
               errorMessage.includes('timeout');
    }

    getErrorSeverity(error) {
        if (error.message.includes('500') || error.message.includes('server_error')) return 'critical';
        if (error.message.includes('403') || error.message.includes('forbidden')) return 'high';
        if (error.message.includes('404') || error.message.includes('not_found')) return 'medium';
        if (error.name === 'AbortError' || error.message.includes('timeout')) return 'medium';
        return 'low';
    }

    // Cache management for competitive performance
    clearCache() {
        this.cache.clear();
        console.log('🧹 API cache cleared for fresh competitive data');
    }

    getCacheStats() {
        return {
            size: this.cache.size,
            entries: Array.from(this.cache.entries()).map(([key, value]) => ({
                key,
                age: Date.now() - value.timestamp
            }))
        };
    }

    // WebSocket integration for real-time competitive updates
    connectWebSocket(onMessage) {
        try {
            const ws = new WebSocket(`ws://${window.location.host}/ws`);

            ws.onopen = () => {
                console.log('🔗 API WebSocket connected for competitive updates');
            };

            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    onMessage(data);
                } catch (error) {
                    console.error('WebSocket message parse error:', error);
                }
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            ws.onclose = () => {
                console.log('🔌 API WebSocket disconnected');
                // Auto-reconnect after delay
                setTimeout(() => this.connectWebSocket(onMessage), 5000);
            };

            return ws;
        } catch (error) {
            console.error('WebSocket connection failed:', error);
            return null;
        }
    }
}

// Export singleton instance for competitive performance
export const api = new V2SwarmAPI();

// Make available globally for debugging
window.v2swarmAPI = api;

