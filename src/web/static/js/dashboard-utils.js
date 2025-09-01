/**
 * Dashboard Utils Module - V2 Compliant
 * Contains utility functions and helpers for the dashboard
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0
 * @license MIT
 */

/**
 * Get status CSS class based on status
 * @param {string} status - Status value
 * @returns {string} CSS class name
 */
function getStatusClass(status) {
    switch (status) {
        case 'critical': return 'critical';
        case 'warning': return 'warning';
        case 'normal': return 'healthy';
        default: return 'healthy';
    }
}

/**
 * Get status badge color
 * @param {string} status - Agent status
 * @returns {string} Bootstrap color class
 */
function getStatusBadgeColor(status) {
    switch (status) {
        case 'active': return 'success';
        case 'busy': return 'warning';
        case 'idle': return 'secondary';
        case 'offline': return 'danger';
        default: return 'secondary';
    }
}

/**
 * Get score CSS class
 * @param {number} score - Performance score
 * @returns {string} CSS class name
 */
function getScoreClass(score) {
    if (score >= 80) return 'high';
    if (score >= 60) return 'medium';
    return 'low';
}

/**
 * Format timestamp for display
 * @param {string} timestamp - ISO timestamp
 * @returns {string} Formatted timestamp
 */
function formatTimestamp(timestamp) {
    if (!timestamp) return 'Unknown';
    const date = new Date(timestamp);
    return date.toLocaleString();
}

/**
 * Update current time display
 */
function updateCurrentTime() {
    const timeElement = document.getElementById('current-time');
    if (timeElement) {
        const now = new Date();
        timeElement.textContent = now.toLocaleTimeString();
    }
}

/**
 * Format number with appropriate suffix (K, M, B)
 * @param {number} num - Number to format
 * @returns {string} Formatted number
 */
function formatNumber(num) {
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
}

/**
 * Format percentage with proper decimal places
 * @param {number} value - Value to format as percentage
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted percentage
 */
function formatPercentage(value, decimals = 1) {
    return (value * 100).toFixed(decimals) + '%';
}

/**
 * Format date in a readable format
 * @param {Date|string} date - Date to format
 * @returns {string} Formatted date
 */
function formatDate(date) {
    const d = new Date(date);
    return d.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Get status color class based on value and thresholds
 * @param {number} value - Value to evaluate
 * @param {number} warningThreshold - Warning threshold
 * @param {number} criticalThreshold - Critical threshold
 * @returns {string} CSS class name
 */
function getStatusColor(value, warningThreshold = 70, criticalThreshold = 90) {
    if (value >= criticalThreshold) return 'text-danger';
    if (value >= warningThreshold) return 'text-warning';
    return 'text-success';
}

/**
 * Debounce function to limit function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function to limit function calls
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {Function} Throttled function
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Deep clone an object
 * @param {Object} obj - Object to clone
 * @returns {Object} Cloned object
 */
function deepClone(obj) {
    if (obj === null || typeof obj !== 'object') return obj;
    if (obj instanceof Date) return new Date(obj.getTime());
    if (obj instanceof Array) return obj.map(item => deepClone(item));
    if (typeof obj === 'object') {
        const clonedObj = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                clonedObj[key] = deepClone(obj[key]);
            }
        }
        return clonedObj;
    }
}

/**
 * Generate a unique ID
 * @returns {string} Unique ID
 */
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} True if valid email
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}



// Export utility functions
export {
    formatNumber,
    formatPercentage,
    formatDate,
    getStatusColor,
    debounce,
    throttle,
    deepClone,
    generateId,
    isValidEmail,
    sanitizeHtml,
    getElementDimensions,
    isInViewport,
    addClassWithAnimation,
    smoothScrollTo,
    copyToClipboard,
    downloadFile
};
