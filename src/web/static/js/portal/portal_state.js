/**
 * Portal State Management Module
 * Handles configuration, events, and data refreshing for the portal.
 */

(function() {
    'use strict';

    // Portal Framework Namespace
    window.PortalFramework = {
        version: '1.0.0',
        config: {},
        components: {},
        events: {},
        utils: PortalShared.utils
    };

    // Portal Configuration
    PortalFramework.config = {
        // Default settings
        sidebarWidth: 280,
        mobileBreakpoint: 992,
        refreshInterval: 30000, // 30 seconds
        animationDuration: 300,

        // API endpoints
        apiEndpoints: {
            agents: '/api/agents',
            status: '/api/portal/stats',
            activity: '/api/portal/activity'
        },

        // WebSocket settings
        websocket: {
            enabled: true,
            reconnectInterval: 5000,
            maxReconnectAttempts: 5
        }
    };

    // Portal Components
    PortalFramework.components = {
        sidebar: null,
        navigation: null,
        notifications: null,
        modals: null,
        charts: null
    };

    // Event System
    PortalFramework.events = {
        listeners: {},

        on: function(event, callback) {
            if (!this.listeners[event]) {
                this.listeners[event] = [];
            }
            this.listeners[event].push(callback);
        },

        emit: function(event, data) {
            if (this.listeners[event]) {
                this.listeners[event].forEach(function(callback) {
                    try {
                        callback(data);
                    } catch (error) {
                        console.error('Error in event listener:', error);
                    }
                });
            }
        },

        off: function(event, callback) {
            if (this.listeners[event]) {
                const index = this.listeners[event].indexOf(callback);
                if (index > -1) {
                    this.listeners[event].splice(index, 1);
                }
            }
        }
    };
    // Portal Initialization
    PortalFramework.init = function(config) {
        // Merge configuration
        if (config) {
            Object.assign(this.config, config);
        }

        // Initialize components
        this.initComponents();

        // Setup event listeners
        this.setupEventListeners();

        // Start real-time updates
        this.startRealTimeUpdates();

        // Emit ready event
        this.events.emit('portal:ready');

        console.log('Portal Framework initialized successfully');
    };

    // Initialize Portal Components
    PortalFramework.initComponents = function() {
        // Initialize sidebar
        this.components.sidebar = new PortalSidebar();

        // Initialize navigation
        this.components.navigation = new PortalNavigation();

        // Initialize notifications
        this.components.notifications = new PortalNotifications();

        // Initialize modals
        this.components.modals = new PortalModals();

        // Initialize charts (if available)
        if (typeof Chart !== 'undefined') {
            this.components.charts = new PortalCharts();
        }
    };

    // Setup Event Listeners
    PortalFramework.setupEventListeners = function() {
        // Window resize
        window.addEventListener('resize', this.utils.debounce(function() {
            PortalFramework.events.emit('portal:resize');
        }, 250));

        // Keyboard shortcuts
        document.addEventListener('keydown', function(event) {
            // Ctrl/Cmd + K for search
            if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
                event.preventDefault();
                PortalFramework.events.emit('portal:search');
            }

            // Escape key for closing modals
            if (event.key === 'Escape') {
                PortalFramework.events.emit('portal:escape');
            }
        });

        // Click outside to close modals
        document.addEventListener('click', function(event) {
            if (event.target.classList.contains('modal')) {
                PortalFramework.events.emit('portal:modalClose');
            }
        });
    };

    // Start Real-time Updates
    PortalFramework.startRealTimeUpdates = function() {
        if (this.config.refreshInterval > 0) {
            setInterval(function() {
                PortalFramework.refreshData();
            }, this.config.refreshInterval);
        }
    };

    // Refresh Portal Data
    PortalFramework.refreshData = function() {
        // Refresh agent status
        this.refreshAgentStatus();

        // Refresh system metrics
        this.refreshSystemMetrics();

        // Refresh recent activity
        this.refreshRecentActivity();

        // Emit refresh event
        this.events.emit('portal:refresh');
    };

    // Refresh Agent Status
    PortalFramework.refreshAgentStatus = function() {
        this.utils.http.get(this.config.apiEndpoints.agents)
            .then(function(data) {
                PortalFramework.events.emit('portal:agentsUpdated', data);
            })
            .catch(function(error) {
                console.error('Failed to refresh agent status:', error);
            });
    };

    // Refresh System Metrics
    PortalFramework.refreshSystemMetrics = function() {
        this.utils.http.get(this.config.apiEndpoints.status)
            .then(function(data) {
                PortalFramework.events.emit('portal:metricsUpdated', data);
            })
            .catch(function(error) {
                console.error('Failed to refresh system metrics:', error);
            });
    };

    // Refresh Recent Activity
    PortalFramework.refreshRecentActivity = function() {
        this.utils.http.get(this.config.apiEndpoints.activity)
            .then(function(data) {
                PortalFramework.events.emit('portal:activityUpdated', data);
            })
            .catch(function(error) {
                console.error('Failed to refresh recent activity:', error);
            });
    };


    // Initialize when DOM is ready
    PortalShared.utils.dom.ready(function() {
        if (window.PortalConfig) {
            PortalFramework.init(window.PortalConfig);
        }
    });

})();
