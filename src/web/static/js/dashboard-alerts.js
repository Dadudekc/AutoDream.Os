/**
 * Dashboard Alerts Module - V2 Compliant
 * Handles alert management functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0
 * @license MIT
 */

/**
 * Show alert message
 * @param {string} type - Alert type (success, error, warning, info)
 * @param {string} message - Alert message
 */
function showAlert(type, message) {
    // Simple alert display - could be enhanced with toast notifications
    console.log(`${type.toUpperCase()}: ${message}`);

    // Create visual alert if alert container exists
    const alertContainer = document.getElementById('alertsContainer');
    if (alertContainer) {
        const alertElement = createAlertElement(type, message);
        alertContainer.insertAdjacentHTML('afterbegin', alertElement);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            const firstAlert = alertContainer.querySelector('.alert-item');
            if (firstAlert) {
                firstAlert.remove();
            }
        }, 5000);
    }
}

/**
 * Create alert element HTML
 * @param {string} type - Alert type
 * @param {string} message - Alert message
 * @returns {string} HTML string
 */
function createAlertElement(type, message) {
    const alertClass = type === 'error' ? 'critical' : type;
    return `
        <div class="alert-item ${alertClass}">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <strong>${escapeHTML(message)}</strong>
                    <br><small class="text-muted">${new Date().toLocaleTimeString()}</small>
                </div>
                <button class="btn btn-sm btn-outline-secondary" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
    `;
}

/**
 * Show refresh indicator
 */
function showRefreshIndicator() {
    const indicator = document.getElementById('refreshIndicator');
    if (indicator) {
        indicator.classList.add('show');
        setTimeout(() => {
            indicator.classList.remove('show');
        }, 3000);
    }
}

/**
 * Request dashboard update
 */
function requestUpdate() {
    if (socket) {
        socket.emit('request_update');
        showRefreshIndicator();
    }
}

/**
 * Acknowledge alert
 * @param {string} alertId - Alert ID to acknowledge
 */
function acknowledgeAlert(alertId) {
    fetch(`/api/alerts/${alertId}/acknowledge`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showAlert('success', data.message);
            loadDashboardData(currentView);
        }
    })
    .catch(error => {
        console.error('Failed to acknowledge alert:', error);
        showAlert('error', 'Failed to acknowledge alert');
    });
}

/**
 * Resolve alert
 * @param {string} alertId - Alert ID to resolve
 */
function resolveAlert(alertId) {
    fetch(`/api/alerts/${alertId}/resolve`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showAlert('success', data.message);
            loadDashboardData(currentView);
        }
    })
    .catch(error => {
        console.error('Failed to resolve alert:', error);
        showAlert('error', 'Failed to resolve alert');
    });
}

/**
 * Load and display alerts
 * @param {Array} alerts - Array of alert objects
 */
function loadAlerts(alerts) {
    const alertsContainer = document.getElementById('alertsContainer');
    if (alertsContainer) {
        alertsContainer.innerHTML = renderAlerts(alerts);
    }
}

/**
 * Update alert display
 * @param {Object} data - Updated dashboard data
 */
function updateAlerts(data) {
    if (data.alerts) {
        loadAlerts(data.alerts);
    }
}
