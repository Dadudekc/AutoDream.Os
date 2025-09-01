/**
 * Dashboard Real-Time Manager - V2 Compliant Module
 * Handles real-time updates and live data synchronization
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class DashboardRealTimeManager {
    constructor(stateManager, socketManager) {
        this.stateManager = stateManager;
        this.socketManager = socketManager;
        this.updateInterval = null;
        this.isActive = false;
    }

    /**
     * Initialize real-time updates
     */
    initialize() {
        if (!this.stateManager.config.enableRealTimeUpdates) {
            console.log('🔄 Real-time updates disabled in configuration');
            return;
        }

        console.log('🔄 Initializing real-time updates...');
        this.setupRealTimeUpdates();
        this.isActive = true;
    }

    /**
     * Setup real-time update mechanisms
     */
    setupRealTimeUpdates() {
        console.log('🔄 Setting up real-time update mechanisms...');

        // Setup socket-based updates
        this.setupSocketUpdates();

        // Setup periodic data refresh
        this.setupPeriodicUpdates();

        // Setup visibility change handling
        this.setupVisibilityHandling();
    }

    /**
     * Setup socket-based real-time updates
     */
    setupSocketUpdates() {
        if (this.socketManager && this.socketManager.socket) {
            this.socketManager.socket.on('dataUpdate', (data) => {
                this.handleDataUpdate(data);
            });

            this.socketManager.socket.on('statusChange', (status) => {
                this.handleStatusChange(status);
            });
        }
    }

    /**
     * Setup periodic updates
     */
    setupPeriodicUpdates() {
        const interval = this.stateManager.config.updateInterval || 30000; // 30 seconds default

        this.updateInterval = setInterval(() => {
            if (document.visibilityState === 'visible') {
                this.performPeriodicUpdate();
            }
        }, interval);
    }

    /**
     * Setup visibility change handling
     */
    setupVisibilityHandling() {
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible' && this.isActive) {
                this.handleVisibilityReturn();
            }
        });
    }

    /**
     * Handle incoming data updates
     */
    handleDataUpdate(data) {
        console.log('📡 Received real-time data update:', data);

        // Update state manager
        this.stateManager.updateData(data);

        // Dispatch update event
        window.dispatchEvent(new CustomEvent('dashboard:dataUpdated', {
            detail: { data, timestamp: new Date() }
        }));
    }

    /**
     * Handle status changes
     */
    handleStatusChange(status) {
        console.log('📊 Status change received:', status);

        this.stateManager.updateStatus(status);

        window.dispatchEvent(new CustomEvent('dashboard:statusChanged', {
            detail: { status, timestamp: new Date() }
        }));
    }

    /**
     * Perform periodic data update
     */
    performPeriodicUpdate() {
        if (window.loadDashboardData) {
            const currentView = this.stateManager.currentView;
            window.loadDashboardData(currentView, { isPeriodicUpdate: true });
        }
    }

    /**
     * Handle page visibility return
     */
    handleVisibilityReturn() {
        console.log('👁️ Page became visible, refreshing data...');
        this.performPeriodicUpdate();
    }

    /**
     * Stop real-time updates
     */
    stop() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
        this.isActive = false;
        console.log('🔄 Real-time updates stopped');
    }

    /**
     * Check if real-time updates are active
     */
    isActive() {
        return this.isActive;
    }
}

// Factory function for creating real-time manager instances
export function createRealTimeManager(stateManager, socketManager) {
    return new DashboardRealTimeManager(stateManager, socketManager);
}
