/**
 * Dashboard Error Handler - V2 Compliance Module
 * Extracted from dashboard-consolidated-refactored.js
 * Handles all error display and management functionality
 *
 * @author Agent-2 - Architecture & Design Specialist
 * @version 1.0.0 - V2 COMPLIANCE
 * @license MIT
 */

// ================================
// ERROR HANDLER
// ================================

/**
 * Dashboard Error Handler
 * Manages error display and user notifications
 */
class DashboardErrorHandler {
    constructor(logger = null) {
        this.logger = logger;
        this.errorContainer = null;
    }

    /**
     * Show error message to user
     */
    showError(message, title = "🚨 Dashboard Error") {
        // Remove existing error if any
        this.clearError();

        // Create error container
        this.errorContainer = document.createElement('div');
        this.errorContainer.id = 'dashboardError';
        this.errorContainer.className = 'dashboard-error';
        this.errorContainer.innerHTML = `
            <div class="error-content">
                <h3>${title}</h3>
                <p>${message}</p>
                <button onclick="location.reload()">Refresh Page</button>
            </div>
        `;

        // Add styles
        this.errorContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ff4444;
            color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10000;
            max-width: 400px;
        `;

        this.errorContainer.querySelector('.error-content').style.cssText = `
            margin: 0;
        `;

        this.errorContainer.querySelector('button').style.cssText = `
            background: white;
            color: #ff4444;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        `;

        document.body.appendChild(this.errorContainer);

        // Log error if logger available
        if (this.logger) {
            this.logger.logErrorGeneric('DashboardErrorHandler', message, {
                title,
                userDisplayed: true
            });
        }

        // Auto-hide after 10 seconds
        setTimeout(() => this.clearError(), 10000);
    }

    /**
     * Show warning message
     */
    showWarning(message, title = "⚠️ Warning") {
        // Remove existing error if any
        this.clearError();

        // Create warning container
        this.errorContainer = document.createElement('div');
        this.errorContainer.id = 'dashboardWarning';
        this.errorContainer.className = 'dashboard-warning';
        this.errorContainer.innerHTML = `
            <div class="warning-content">
                <h3>${title}</h3>
                <p>${message}</p>
                <button onclick="this.parentElement.parentElement.remove()">Dismiss</button>
            </div>
        `;

        // Add styles
        this.errorContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ffaa00;
            color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10000;
            max-width: 400px;
        `;

        this.errorContainer.querySelector('.warning-content').style.cssText = `
            margin: 0;
        `;

        this.errorContainer.querySelector('button').style.cssText = `
            background: white;
            color: #ffaa00;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        `;

        document.body.appendChild(this.errorContainer);

        // Log warning if logger available
        if (this.logger) {
            this.logger.logOperationFailed('user_warning', message, {
                title,
                type: 'warning'
            });
        }
    }

    /**
     * Show success message
     */
    showSuccess(message, title = "✅ Success") {
        const successElement = document.createElement('div');
        successElement.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #44aa44;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10000;
            max-width: 400px;
            animation: fadeIn 0.3s ease-in;
        `;

        successElement.innerHTML = `
            <div style="margin: 0;">
                <h3 style="margin: 0 0 10px 0; font-size: 16px;">${title}</h3>
                <p style="margin: 0; font-size: 14px;">${message}</p>
            </div>
        `;

        document.body.appendChild(successElement);

        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (successElement.parentElement) {
                successElement.remove();
            }
        }, 3000);
    }

    /**
     * Clear current error/warning
     */
    clearError() {
        if (this.errorContainer && this.errorContainer.parentElement) {
            this.errorContainer.remove();
            this.errorContainer = null;
        }
    }

    /**
     * Handle uncaught errors
     */
    handleGlobalError(error, source, lineno, colno) {
        const errorMessage = `Uncaught error in ${source}:${lineno}:${colno} - ${error}`;

        this.showError(errorMessage, "🚨 JavaScript Error");

        // Log detailed error information
        if (this.logger) {
            this.logger.logErrorGeneric('GlobalErrorHandler', error, {
                source,
                lineno,
                colno,
                stack: error.stack
            });
        }

        // Prevent default error handling
        return true;
    }
}

// ================================
// EXPORTS
// ================================

export { DashboardErrorHandler };
export default DashboardErrorHandler;