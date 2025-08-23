
// Dashboard Configuration
const DASHBOARD_CONFIG = {
    title: "Agent Cellphone V2 - Performance Dashboard",
    websocket_url: "ws://localhost:8080/ws",
    layout: {
        columns: 12,
        rows: 8,
        theme: "dark",
        auto_refresh: true,
        refresh_interval: 5
    },
    widgets: [{'id': 'cpu_usage', 'metric': 'cpu_percentage', 'chart_type': 'gauge', 'refresh_interval': 5, 'width': 4, 'height': 3, 'position_x': 0, 'position_y': 0}, {'id': 'memory_usage', 'metric': 'memory_percentage', 'chart_type': 'bar', 'refresh_interval': 5, 'width': 4, 'height': 3, 'position_x': 4, 'position_y': 0}, {'id': 'network_traffic', 'metric': 'network_bytes', 'chart_type': 'line', 'refresh_interval': 10, 'width': 4, 'height': 3, 'position_x': 8, 'position_y': 0}, {'id': 'disk_io', 'metric': 'disk_operations', 'chart_type': 'area', 'refresh_interval': 15, 'width': 6, 'height': 4, 'position_x': 0, 'position_y': 3}, {'id': 'system_health', 'metric': 'health_status', 'chart_type': 'table', 'refresh_interval': 30, 'width': 6, 'height': 4, 'position_x': 6, 'position_y': 3}]
};

// Global variables
let autoRefreshInterval = null;
let websocket = null;


// Utility Functions
function showNotification(title, message) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, { body: message });
    }
}

function log(message, level = 'info') {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [${level.toUpperCase()}] ${message}`);
}

function updateLastUpdate(widgetId) {
    const element = document.getElementById(`last-update-${widgetId}`);
    if (element) {
        element.textContent = new Date().toLocaleTimeString();
    }
}

function showError(message) {
    log(message, 'error');
    showNotification('Dashboard Error', message);
}


// Widget Functions
function refreshWidget(widgetId) {
    const widget = document.getElementById(`widget-${widgetId}`);
    if (widget) {
        widget.classList.add('refreshing');
        updateLastUpdate(widgetId);
        
        // Simulate refresh delay
        setTimeout(() => {
            widget.classList.remove('refreshing');
        }, 1000);
        
        log(`Widget ${widgetId} refreshed`);
    }
}

function toggleWidget(widgetId) {
    const widget = document.getElementById(`widget-${widgetId}`);
    if (widget) {
        widget.classList.toggle('collapsed');
        log(`Widget ${widgetId} toggled`);
    }
}

function initializeDashboard() {
    log('Initializing dashboard...');
    
    // Initialize all widgets
    DASHBOARD_CONFIG.widgets.forEach(widget => {
        const widgetElement = document.getElementById(`widget-${widget.id}`);
        if (widgetElement) {
            widgetElement.dataset.metric = widget.metric;
            widgetElement.dataset.refresh = widget.refresh_interval;
        }
    });
    
    log('Dashboard initialized successfully');
}


// Theme Functions
function changeTheme() {
    const themeSelect = document.getElementById('theme-select');
    const newTheme = themeSelect.value;
    setTheme(newTheme);
}

function setTheme(theme) {
    document.body.className = `theme-${theme}`;
    localStorage.setItem('dashboard-theme', theme);
    DASHBOARD_CONFIG.layout.theme = theme;
    log(`Theme changed to ${theme}`);
}

function toggleSettings() {
    const panel = document.getElementById('settings-panel');
    panel.classList.toggle('visible');
}


// Refresh Functions
function toggleAutoRefresh() {
    const checkbox = document.getElementById('auto-refresh');
    if (checkbox.checked) {
        startAutoRefresh();
    } else {
        stopAutoRefresh();
    }
}

function updateRefreshInterval() {
    const input = document.getElementById('refresh-interval');
    const newInterval = parseInt(input.value);
    
    if (newInterval > 0) {
        DASHBOARD_CONFIG.layout.refresh_interval = newInterval;
        
        if (autoRefreshInterval) {
            stopAutoRefresh();
            startAutoRefresh();
        }
        
        log(`Refresh interval updated to ${newInterval}s`);
    }
}

function startAutoRefresh() {
    stopAutoRefresh();
    autoRefreshInterval = setInterval(refreshDashboard, DASHBOARD_CONFIG.layout.refresh_interval * 1000);
    log('Auto-refresh started');
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
        log('Auto-refresh stopped');
    }
}

function refreshDashboard() {
    log('Refreshing dashboard...');
    DASHBOARD_CONFIG.widgets.forEach(widget => {
        refreshWidget(widget.id);
    });
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    if (DASHBOARD_CONFIG.layout.auto_refresh) {
        startAutoRefresh();
    }
    
    // Request notification permission
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
});