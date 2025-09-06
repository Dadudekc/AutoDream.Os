/**
 * Dashboard Data Repository - V2 Compliance Implementation
 * Centralizes all dashboard data access operations
 * V2 Compliance: Repository pattern implementation for data access
 */

export class DashboardRepository {
    constructor() {
        this.baseUrl = '/api/dashboard';
        this.cache = new Map();
        this.cacheTimeout = 30000; // 30 seconds
    }

    // Dashboard data access methods
    async getDashboardData(view) {
        const cacheKey = `dashboard_${view}`;
        const cached = this.getFromCache(cacheKey);

        if (cached) {
            return cached;
        }

        try {
            const response = await fetch(`${this.baseUrl}/${view}`);
            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            this.setCache(cacheKey, data);
            return data;
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
            throw new Error('Failed to load dashboard data');
        }
    }

    // Agent performance data
    async getAgentPerformanceData() {
        return this.getDashboardData('agent_performance');
    }

    // Contract status data
    async getContractStatusData() {
        return this.getDashboardData('contract_status');
    }

    // System health data
    async getSystemHealthData() {
        return this.getDashboardData('system_health');
    }

    // Performance metrics data
    async getPerformanceMetricsData() {
        return this.getDashboardData('performance_metrics');
    }

    // Workload distribution data
    async getWorkloadDistributionData() {
        return this.getDashboardData('workload_distribution');
    }

    // Cache management
    getFromCache(key) {
        const cached = this.cache.get(key);
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }
        return null;
    }

    setCache(key, data) {
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });
    }

    clearCache() {
        this.cache.clear();
    }

    // Socket event handling
    handleDashboardUpdate(data) {
        // Clear cache for updated view
        const cacheKey = `dashboard_${data.view}`;
        this.cache.delete(cacheKey);

        return data;
    }
}
