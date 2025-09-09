/**
 * Dashboard Main - Unified Consolidated System
 * V2 Compliance: Single consolidated dashboard replacing 20+ files
 * Uses UnifiedDashboard for complete dashboard functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 4.0.0 - CONSOLIDATED DASHBOARD SYSTEM
 * @license MIT
 */

// Import unified dashboard system
import UnifiedDashboard from './dashboard-unified.js';

// ================================
// MAIN DASHBOARD INITIALIZATION
// ================================

/**
 * Main dashboard entry point using unified system
 */
class DashboardMain {
    constructor() {
        this.dashboard = new UnifiedDashboard();
        this.isInitialized = false;
    }

    /**
     * Initialize the complete dashboard system
     */
    async initialize() {
        if (this.isInitialized) {
            console.warn('⚠️ Dashboard already initialized');
            return;
        }

        console.log('🚀 Starting Dashboard Main with Unified System...');

        try {
            // Initialize unified dashboard system
            await this.dashboard.initialize();

            this.isInitialized = true;
            console.log('✅ Dashboard Main initialized successfully');

        } catch (error) {
            console.error('❌ Dashboard Main initialization failed:', error);
            // Fallback error handling
            this.showFallbackError(error);
        }
    }

    /**
     * Show fallback error if unified system fails
     */
    showFallbackError(error) {
        const contentDiv = document.getElementById('dashboardContent');
        if (contentDiv) {
            contentDiv.innerHTML = `
                <div class="alert alert-danger">
                    <h4>Dashboard Initialization Failed</h4>
                    <p>There was an error starting the dashboard system: ${error.message}</p>
                    <p>Please refresh the page or contact support if the problem persists.</p>
                </div>
            `;
        }
    }

    /**
     * Get dashboard instance for external access
     */
    getDashboard() {
        return this.dashboard;
    }

    /**
     * Cleanup dashboard system
     */
    destroy() {
        if (this.dashboard) {
            this.dashboard.destroy();
        }
        this.isInitialized = false;
        console.log('🧹 Dashboard Main cleaned up');
    }
}

// ================================
// LEGACY COMPATIBILITY
// ================================

/**
 * Legacy factory function for existing code
 * @deprecated Use new DashboardMain class directly
 */
export function createDashboardMain() {
    return new DashboardMain();
}

/**
 * Legacy initialization function
 * @deprecated Use dashboard.initialize() instead
 */
export function initializeDashboardLegacy() {
    console.warn('⚠️ initializeDashboardLegacy() is deprecated. Use DashboardMain class.');
    const dashboard = new DashboardMain();
    dashboard.initialize().catch(console.error);
    return dashboard;
}

// ================================
// AUTO-INITIALIZATION
// ================================

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 DOM loaded, initializing dashboard...');
    const dashboard = new DashboardMain();
    dashboard.initialize();

    // Make dashboard globally available for debugging
    window.dashboard = dashboard;
});

// ================================
// EXPORTS
// ================================

export default DashboardMain;
export { DashboardMain, UnifiedDashboard };
