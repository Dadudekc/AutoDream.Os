/**
 * Dashboard Formatters Module - V2 Compliant
 * Number and data formatting utilities for dashboard components
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export const DashboardFormatters = {
    /**
     * Format number with appropriate suffix
     */
    formatNumber(num) {
        if (typeof num !== 'number' || isNaN(num)) {
            return '0';
        }

        if (num >= 1000000000) {
            return (num / 1000000000).toFixed(1) + 'B';
        }
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    },

    /**
     * Format percentage with validation
     */
    formatPercentage(value) {
        if (typeof value !== 'number' || isNaN(value)) {
            return '0%';
        }
        return `${(value * 100).toFixed(1)}%`;
    },

    /**
     * Format currency value
     */
    formatCurrency(amount, currency = 'USD') {
        if (typeof amount !== 'number' || isNaN(amount)) {
            return '$0.00';
        }

        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    },

    /**
     * Format file size
     */
    formatFileSize(bytes) {
        if (typeof bytes !== 'number' || isNaN(bytes)) {
            return '0 B';
        }

        const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
        if (bytes === 0) return '0 B';

        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    },

    /**
     * Format duration in milliseconds
     */
    formatDuration(ms) {
        if (typeof ms !== 'number' || isNaN(ms)) {
            return '0ms';
        }

        if (ms < 1000) {
            return `${Math.round(ms)}ms`;
        }

        const seconds = Math.floor(ms / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);

        if (hours > 0) {
            return `${hours}h ${minutes % 60}m`;
        } else if (minutes > 0) {
            return `${minutes}m ${seconds % 60}s`;
        } else {
            return `${seconds}s`;
        }
    }
};

// Factory function for creating formatters instance
export function createDashboardFormatters() {
    return { ...DashboardFormatters };
}
