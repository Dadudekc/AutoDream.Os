/**
 * Dashboard Utilities - V2 Compliant Module
 * Common utility functions for dashboard operations
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

/**
 * Dashboard utility functions
 */
export const DashboardUtils = {
    /**
     * Format number with suffix
     */
    formatNumber(num) {
        if (num >= 1000000000) return (num / 1000000000).toFixed(1) + 'B';
        if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return num.toString();
    },

    /**
     * Format percentage
     */
    formatPercentage(value) {
        return `${(value * 100).toFixed(1)}%`;
    },

    /**
     * Format date
     */
    formatDate(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    /**
     * Get status color
     */
    getStatusColor(status) {
        const colors = {
            'success': '#28a745',
            'warning': '#ffc107',
            'error': '#dc3545',
            'info': '#17a2b8',
            'active': '#007bff',
            'inactive': '#6c757d'
        };
        return colors[status] || colors.info;
    }
};

// Default export for backward compatibility
export default DashboardUtils;