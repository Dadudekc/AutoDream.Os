/**
 * Dashboard V2 - Main Entry Point - V2 Compliant
 * Modular dashboard implementation using ES6 modules
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0
 * @license MIT
 */

// Import modular components

import { formatDate, formatNumber, formatPercentage, getStatusColor } from './dashboard-utils.js';
import { initializeDashboard, loadDashboardData, updateDashboard } from './dashboard-core.js';

import { initializeNavigation } from './dashboard-navigation.js';

// Dashboard configuration
const DASHBOARD_CONFIG = {
    refreshInterval: 30000, // 30 seconds
    chartAnimationDuration: 1000,
    maxDataPoints: 100,
    enableRealTimeUpdates: true,
    enableNotifications: true
};

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing Dashboard V2...');
    
    // Initialize core dashboard functionality
    initializeDashboard();
    
    // Initialize navigation system
    const navigation = initializeNavigation();
    
    // Setup real-time updates
    if (DASHBOARD_CONFIG.enableRealTimeUpdates) {
        setupRealTimeUpdates();
    }
    
    // Setup notifications
    if (DASHBOARD_CONFIG.enableNotifications) {
        setupNotifications();
    }
    
    // Setup performance monitoring
    setupPerformanceMonitoring();
    
    console.log('✅ Dashboard V2 initialized successfully');
});

/**
 * Setup real-time updates
 */
function setupRealTimeUpdates() {
    setInterval(() => {
        const currentView = getCurrentView();
        if (currentView) {
            loadDashboardData(currentView);
        }
    }, DASHBOARD_CONFIG.refreshInterval);
}

/**
 * Setup notifications
 */
function setupNotifications() {
    if ('Notification' in window && Notification.permission === 'granted') {
        // Notifications are enabled
        console.log('🔔 Notifications enabled');
    } else if ('Notification' in window && Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                console.log('🔔 Notifications enabled');
            }
        });
    }
}

/**
 * Setup performance monitoring
 */
function setupPerformanceMonitoring() {
    // Monitor dashboard performance
    const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
            if (entry.entryType === 'measure') {
                console.log(`📊 Performance: ${entry.name} - ${entry.duration}ms`);
            }
        }
    });
    
    observer.observe({ entryTypes: ['measure'] });
}

/**
 * Get current active view
 * @returns {string} Current view name
 */
function getCurrentView() {
    const activeLink = document.querySelector('#dashboardNav .nav-link.active');
    return activeLink ? activeLink.dataset.view : 'overview';
}

/**
 * Show notification
 * @param {string} title - Notification title
 * @param {string} body - Notification body
 */
function showNotification(title, body) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, { body });
    }
}

/**
 * Handle dashboard errors
 * @param {Error} error - Error object
 */
function handleDashboardError(error) {
    console.error('❌ Dashboard Error:', error);
    
    // Show error notification
    showNotification('Dashboard Error', error.message);
    
    // Log error for monitoring
    if (window.gtag) {
        window.gtag('event', 'dashboard_error', {
            error_message: error.message,
            error_stack: error.stack
        });
    }
}

/**
 * Export dashboard functions for external use
 */
window.DashboardV2 = {
    loadView: loadDashboardData,
    updateData: updateDashboard,
    showNotification,
    formatNumber,
    formatPercentage,
    formatDate,
    getStatusColor,
    getCurrentView
};

// Global error handler
window.addEventListener('error', (event) => {
    handleDashboardError(event.error);
});

// Unhandled promise rejection handler
window.addEventListener('unhandledrejection', (event) => {
    handleDashboardError(new Error(event.reason));
});

// Export for module usage
export {
    setupRealTimeUpdates,
    setupNotifications,
    setupPerformanceMonitoring,
    showNotification,
    handleDashboardError,
    getCurrentView
};
