/**
 * Dashboard Main - Modular Architecture Implementation
 * V2 Compliance: Modular ES6 architecture with component imports
 * Replaces dashboard.js (663 lines) with modular approach
 */

// Import modular components

import { DashboardCore } from './dashboard-core.js';
import { DashboardNavigation } from './dashboard-navigation.js';
import { DashboardUtils } from './dashboard-utils.js';
import { DashboardV2 } from './dashboard-v2.js';

// Dashboard state management
class DashboardMain {
    constructor() {
        this.currentView = 'overview';
        this.socket = null;
        this.charts = {};
        this.updateTimer = null;
        this.core = new DashboardCore();
        this.navigation = new DashboardNavigation();
        this.utils = new DashboardUtils();
        this.v2 = new DashboardV2();
    }

    // Initialize dashboard
    async initialize() {
        try {
            await this.core.initialize();
            this.navigation.setup();
            this.utils.updateCurrentTime();
            await this.loadDashboardData(this.currentView);
            
            // Update time every second
            setInterval(() => this.utils.updateCurrentTime(), 1000);
            
            console.log('Dashboard initialized successfully with modular architecture');
        } catch (error) {
            console.error('Dashboard initialization failed:', error);
            this.utils.showAlert('error', 'Dashboard initialization failed');
        }
    }

    // Load dashboard data
    async loadDashboardData(view) {
        this.utils.showLoading();
        
        try {
            // Use repository pattern for data access
            const { DashboardRepository } = await import('./repositories/dashboard-repository.js');
            const repository = new DashboardRepository();
            const data = await repository.getDashboardData(view);
            
            this.updateDashboard(data);
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
            this.utils.showAlert('error', 'Failed to load dashboard data');
        } finally {
            this.utils.hideLoading();
        }
    }

    // Update dashboard with new data
    updateDashboard(data) {
        const contentDiv = document.getElementById('dashboardContent');
        
        if (data.view === 'overview') {
            contentDiv.innerHTML = this.v2.renderOverviewView(data);
        } else if (data.view === 'agent_performance') {
            contentDiv.innerHTML = this.v2.renderAgentPerformanceView(data);
        } else if (data.view === 'contract_status') {
            contentDiv.innerHTML = this.v2.renderContractStatusView(data);
        } else if (data.view === 'system_health') {
            contentDiv.innerHTML = this.v2.renderSystemHealthView(data);
        } else if (data.view === 'performance_metrics') {
            contentDiv.innerHTML = this.v2.renderPerformanceMetricsView(data);
        } else if (data.view === 'workload_distribution') {
            contentDiv.innerHTML = this.v2.renderWorkloadDistributionView(data);
        }
    }

    // Handle navigation changes
    handleNavigationChange(view) {
        this.currentView = view;
        this.loadDashboardData(view);
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new DashboardMain();
    dashboard.initialize();
});

// Export for potential external use
export { DashboardMain };
