/**
 * Dashboard Style Utilities Module - V2 Compliant
 * Color and style utilities for dashboard components
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export const DashboardStyleUtils = {
    /**
     * Get status color based on status value
     */
    getStatusColor(status) {
        const statusColors = {
            'success': '#28a745',
            'error': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8',
            'active': '#007bff',
            'inactive': '#6c757d',
            'pending': '#fd7e14',
            'completed': '#20c997',
            'failed': '#e83e8c',
            'running': '#6f42c1',
            'stopped': '#adb5bd'
        };

        return statusColors[status] || statusColors.info;
    },

    /**
     * Get priority color
     */
    getPriorityColor(priority) {
        const priorityColors = {
            'low': '#17a2b8',
            'medium': '#ffc107',
            'high': '#fd7e14',
            'urgent': '#dc3545',
            'critical': '#e83e8c'
        };

        return priorityColors[priority] || priorityColors.medium;
    },

    /**
     * Get severity color
     */
    getSeverityColor(severity) {
        const severityColors = {
            'low': '#28a745',
            'medium': '#ffc107',
            'high': '#fd7e14',
            'critical': '#dc3545'
        };

        return severityColors[severity] || severityColors.medium;
    },

    /**
     * Generate gradient color
     */
    generateGradient(startColor, endColor, steps = 5) {
        // Simple gradient generation between two colors
        const start = this.hexToRgb(startColor);
        const end = this.hexToRgb(endColor);

        if (!start || !end) return [startColor];

        const gradient = [];
        for (let i = 0; i < steps; i++) {
            const r = Math.round(start.r + (end.r - start.r) * (i / (steps - 1)));
            const g = Math.round(start.g + (end.g - start.g) * (i / (steps - 1)));
            const b = Math.round(start.b + (end.b - start.b) * (i / (steps - 1)));
            gradient.push(this.rgbToHex(r, g, b));
        }

        return gradient;
    },

    /**
     * Lighten color
     */
    lightenColor(color, percent = 10) {
        const rgb = this.hexToRgb(color);
        if (!rgb) return color;

        const lighten = (value) => Math.min(255, Math.round(value + (255 - value) * (percent / 100)));

        return this.rgbToHex(lighten(rgb.r), lighten(rgb.g), lighten(rgb.b));
    },

    /**
     * Darken color
     */
    darkenColor(color, percent = 10) {
        const rgb = this.hexToRgb(color);
        if (!rgb) return color;

        const darken = (value) => Math.max(0, Math.round(value * (1 - percent / 100)));

        return this.rgbToHex(darken(rgb.r), darken(rgb.g), darken(rgb.b));
    },

    /**
     * Get contrast color (black or white) for background
     */
    getContrastColor(backgroundColor) {
        const rgb = this.hexToRgb(backgroundColor);
        if (!rgb) return '#000000';

        // Calculate relative luminance
        const luminance = (0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b) / 255;

        return luminance > 0.5 ? '#000000' : '#ffffff';
    },

    /**
     * Convert hex to RGB
     */
    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    },

    /**
     * Convert RGB to hex
     */
    rgbToHex(r, g, b) {
        return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    },

    /**
     * Generate random color
     */
    generateRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    },

    /**
     * Get CSS class for status
     */
    getStatusClass(status) {
        const statusClasses = {
            'success': 'status-success',
            'error': 'status-error',
            'warning': 'status-warning',
            'info': 'status-info',
            'active': 'status-active',
            'inactive': 'status-inactive',
            'pending': 'status-pending',
            'completed': 'status-completed',
            'failed': 'status-failed'
        };

        return statusClasses[status] || 'status-default';
    },

    /**
     * Get icon class for status
     */
    getStatusIcon(status) {
        const statusIcons = {
            'success': 'fas fa-check-circle',
            'error': 'fas fa-exclamation-triangle',
            'warning': 'fas fa-exclamation-circle',
            'info': 'fas fa-info-circle',
            'active': 'fas fa-play-circle',
            'inactive': 'fas fa-pause-circle',
            'pending': 'fas fa-clock',
            'completed': 'fas fa-check-double',
            'failed': 'fas fa-times-circle'
        };

        return statusIcons[status] || 'fas fa-question-circle';
    }
};

// Factory function for creating style utils instance
export function createDashboardStyleUtils() {
    return { ...DashboardStyleUtils };
}
