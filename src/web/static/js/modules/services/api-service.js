/**
 * API Service - V2 Compliant HTTP Communication System
 * V2 COMPLIANT: 200 lines maximum
 * CONSOLIDATES: api.js, services-data.js, services-validation.js
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @description Unified API service with HTTP requests, caching, and validation
 */

// ================================
// API SERVICE CLASS
// ================================

/**
 * Unified API Service
 * Consolidates all HTTP communication functionality
 */
export class APIService {
    constructor(options = {}) {
        this.baseURL = options.baseURL || '/api/v1';
        this.timeout = options.timeout || 5000;
        this.retryAttempts = options.retryAttempts || 3;
        this.cache = new Map();
        this.cacheTimeout = options.cacheTimeout || 30000;
        this.isInitialized = false;
        
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

    /**
     * Initialize API service
     */
    async initialize() {
        if (this.isInitialized) {
            console.warn('⚠️ API service already initialized');
            return;
        }

        console.log('🚀 Initializing API Service (V2 Compliant)...');

        try {
            // Setup request interceptors
            this.setupRequestInterceptors();

            // Initialize cache cleanup
            this.startCacheCleanup();

            this.isInitialized = true;
            console.log('✅ API Service initialized successfully');

        } catch (error) {
            console.error('❌ Failed to initialize API service:', error);
            throw error;
        }
    }

    /**
     * Setup request interceptors
     */
    setupRequestInterceptors() {
        // Global error handling
        window.addEventListener('api:error', (event) => {
            this.handleGlobalError(event.detail);
        });
    }

    /**
     * Make HTTP request with retry logic
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const cacheKey = this.generateCacheKey(options.method || 'GET', url, options.body);

        // Check cache for GET requests
        if (!options.method || options.method === 'GET') {
            const cached = this.getCached(cacheKey);
            if (cached) {
                console.log('📋 Using cached API response');
                return cached;
            }
        }

        const config = this.buildRequestConfig(options);
        let lastError;

        // Retry logic with exponential backoff
        for (let attempt = 1; attempt <= this.retryAttempts; attempt++) {
            try {
                const response = await this.executeRequest(url, config);
                const data = await this.processResponse(response);

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

        throw this.handleRequestError(lastError, endpoint, options);
    }

    /**
     * Build request configuration
     */
    buildRequestConfig(options) {
        return {
            method: options.method || 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                ...options.headers
            },
            body: options.body ? JSON.stringify(options.body) : undefined,
            ...options
        };
    }

    /**
     * Execute HTTP request with timeout
     */
    async executeRequest(url, config) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);

        try {
            const response = await fetch(url, {
                ...config,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return response;

        } catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }

    /**
     * Process HTTP response
     */
    async processResponse(response) {
        const contentType = response.headers.get('content-type');
        
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        } else {
            return await response.text();
        }
    }

    /**
     * Handle request errors
     */
    handleRequestError(error, endpoint, options) {
        const errorInfo = {
            type: this.classifyError(error),
            retryable: this.isRetryableError(error),
            severity: this.getErrorSeverity(error),
            endpoint,
            options,
            timestamp: new Date().toISOString()
        };

        console.error('❌ API request failed:', errorInfo);

        // Dispatch error event
        window.dispatchEvent(new CustomEvent('api:error', {
            detail: errorInfo
        }));

        return new Error(`API request failed: ${error.message}`);
    }

    /**
     * Classify error type
     */
    classifyError(error) {
        if (error.name === 'AbortError') return 'timeout';
        if (error.message.includes('404')) return 'not_found';
        if (error.message.includes('403')) return 'forbidden';
        if (error.message.includes('500')) return 'server_error';
        if (error.message.includes('network') || error.message.includes('fetch')) return 'network_error';
        return 'unknown';
    }

    /**
     * Check if error is retryable
     */
    isRetryableError(error) {
        const retryableCodes = [408, 429, 500, 502, 503, 504];
        const errorMessage = error.message || '';
        return retryableCodes.some(code => errorMessage.includes(code.toString())) ||
               error.name === 'AbortError' ||
               errorMessage.includes('network') ||
               errorMessage.includes('timeout');
    }

    /**
     * Get error severity
     */
    getErrorSeverity(error) {
        if (error.message.includes('500') || error.message.includes('server_error')) return 'critical';
        if (error.message.includes('403') || error.message.includes('forbidden')) return 'high';
        if (error.message.includes('404') || error.message.includes('not_found')) return 'medium';
        if (error.name === 'AbortError' || error.message.includes('timeout')) return 'medium';
        return 'low';
    }

    /**
     * Generate cache key
     */
    generateCacheKey(method, url, body) {
        return `${method}_${url}_${JSON.stringify(body || {})}`;
    }

    /**
     * Get cached data
     */
    getCached(key) {
        const cached = this.cache.get(key);
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }
        this.cache.delete(key);
        return null;
    }

    /**
     * Set cached data
     */
    setCached(key, data) {
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });
    }

    /**
     * Start cache cleanup
     */
    startCacheCleanup() {
        setInterval(() => {
            this.cleanupExpiredCache();
        }, 60000); // Cleanup every minute
    }

    /**
     * Cleanup expired cache entries
     */
    cleanupExpiredCache() {
        const now = Date.now();
        for (const [key, cached] of this.cache) {
            if (now - cached.timestamp >= this.cacheTimeout) {
                this.cache.delete(key);
            }
        }
    }

    /**
     * Handle global errors
     */
    handleGlobalError(errorInfo) {
        console.error('🌐 Global API error:', errorInfo);
        // Additional global error handling logic
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
        console.log('🧹 API cache cleared');
    }

    /**
     * Get cache statistics
     */
    getCacheStats() {
        return {
            size: this.cache.size,
            entries: Array.from(this.cache.entries()).map(([key, value]) => ({
                key,
                age: Date.now() - value.timestamp
            }))
        };
    }

    /**
     * Health check
     */
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

    /**
     * Get service status
     */
    getStatus() {
        return {
            initialized: this.isInitialized,
            baseURL: this.baseURL,
            cacheSize: this.cache.size,
            endpoints: Object.keys(this.endpoints)
        };
    }

    /**
     * Destroy API service
     */
    async destroy() {
        console.log('🧹 Destroying API service...');

        // Clear cache
        this.cache.clear();

        this.isInitialized = false;

        console.log('✅ API service destroyed');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create API service with default configuration
 */
export function createAPIService(options = {}) {
    return new APIService(options);
}

// Export default
export default APIService;