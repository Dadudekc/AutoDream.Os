import { dom as domUtils, createEventBus } from '../shared_utils.js';

/**
 * Portal Framework JavaScript
 * Agent_Cellphone_V2_Repository - Unified Portal Architecture
 */

import { debounce } from './utils.js';

(function() {
    'use strict';

    // Portal Framework Namespace
    window.PortalFramework = {
        version: '1.0.0',
        config: {},
        components: {},
        events: createEventBus(),
        utils: {}
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

    // Utility Functions
    PortalFramework.utils = {
        // DOM utilities
        dom: domUtils,

        // Storage utilities
        storage: {
            set: function(key, value) {
                try {
                    localStorage.setItem(key, JSON.stringify(value));
                } catch (error) {
                    console.warn('Could not save to localStorage:', error);
                }
            },

            get: function(key, defaultValue) {
                try {
                    const item = localStorage.getItem(key);
                    return item ? JSON.parse(item) : defaultValue;
                } catch (error) {
                    console.warn('Could not read from localStorage:', error);
                    return defaultValue;
                }
            },

            remove: function(key) {
                try {
                    localStorage.removeItem(key);
                } catch (error) {
                    console.warn('Could not remove from localStorage:', error);
                }
            }
        },

        // HTTP utilities
        http: {
            get: function(url, options) {
                return this.request('GET', url, options);
            },

            post: function(url, data, options) {
                return this.request('POST', url, { ...options, data });
            },

            put: function(url, data, options) {
                return this.request('PUT', url, { ...options, data });
            },

            delete: function(url, options) {
                return this.request('DELETE', url, options);
            },

            request: function(method, url, options = {}) {
                return new Promise(function(resolve, reject) {
                    const xhr = new XMLHttpRequest();

                    xhr.open(method, url);

                    // Set headers
                    if (options.headers) {
                        Object.keys(options.headers).forEach(function(key) {
                            xhr.setRequestHeader(key, options.headers[key]);
                        });
                    }

                    // Set response type
                    if (options.responseType) {
                        xhr.responseType = options.responseType;
                    }

                    // Handle response
                    xhr.onload = function() {
                        if (xhr.status >= 200 && xhr.status < 300) {
                            try {
                                const response = xhr.responseType === 'json' ? xhr.response : JSON.parse(xhr.response);
                                resolve(response);
                            } catch (error) {
                                resolve(xhr.response);
                            }
                        } else {
                            reject(new Error(`HTTP ${xhr.status}: ${xhr.statusText}`));
                        }
                    };

                    // Handle errors
                    xhr.onerror = function() {
                        reject(new Error('Network error'));
                    };

                    // Handle timeout
                    if (options.timeout) {
                        xhr.timeout = options.timeout;
                        xhr.ontimeout = function() {
                            reject(new Error('Request timeout'));
                        };
                    }

                    // Send request
                    if (options.data && method !== 'GET') {
                        xhr.send(JSON.stringify(options.data));
                    } else {
                        xhr.send();
                    }
                });
            }
        },

        // Time utilities
        time: {
            formatRelative: function(timestamp) {
                const now = new Date();
                const date = new Date(timestamp);
                const diff = now - date;

                const seconds = Math.floor(diff / 1000);
                const minutes = Math.floor(seconds / 60);
                const hours = Math.floor(minutes / 60);
                const days = Math.floor(hours / 24);

                if (days > 0) {
                    return days === 1 ? '1 day ago' : `${days} days ago`;
                } else if (hours > 0) {
                    return hours === 1 ? '1 hour ago' : `${hours} hours ago`;
                } else if (minutes > 0) {
                    return minutes === 1 ? '1 minute ago' : `${minutes} minutes ago`;
                } else {
                    return 'Just now';
                }
            },

            formatDate: function(timestamp, format = 'YYYY-MM-DD HH:mm:ss') {
                const date = new Date(timestamp);

                const year = date.getFullYear();
                const month = String(date.getMonth() + 1).padStart(2, '0');
                const day = String(date.getDate()).padStart(2, '0');
                const hours = String(date.getHours()).padStart(2, '0');
                const minutes = String(date.getMinutes()).padStart(2, '0');
                const seconds = String(date.getSeconds()).padStart(2, '0');

                return format
                    .replace('YYYY', year)
                    .replace('MM', month)
                    .replace('DD', day)
                    .replace('HH', hours)
                    .replace('mm', minutes)
                    .replace('ss', seconds);
            }
        },

        // Validation utilities
        validation: {
            isEmail: function(email) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                return emailRegex.test(email);
            },

            isUrl: function(url) {
                try {
                    new URL(url);
                    return true;
                } catch {
                    return false;
                }
            },

            isRequired: function(value) {
                return value !== null && value !== undefined && value !== '';
            },

            minLength: function(value, min) {
                return value && value.length >= min;
            },

            maxLength: function(value, max) {
                return value && value.length <= max;
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

    // Utility function for debouncing sourced from shared utils
    PortalFramework.utils.debounce = debounce;

    // Portal Sidebar Component
    function PortalSidebar() {
        this.element = document.querySelector('.portal-sidebar');
        this.toggleButton = document.querySelector('.portal-sidebar-toggle');
        this.isOpen = true;

        this.init();
    }

    PortalSidebar.prototype.init = function() {
        if (this.element) {
            this.setupEventListeners();
            this.checkResponsive();
        }
    };

    PortalSidebar.prototype.setupEventListeners = function() {
        if (this.toggleButton) {
            this.toggleButton.addEventListener('click', this.toggle.bind(this));
        }

        // Close sidebar on mobile when clicking outside
        document.addEventListener('click', function(event) {
            if (window.innerWidth <= PortalFramework.config.mobileBreakpoint) {
                if (!event.target.closest('.portal-sidebar') &&
                    !event.target.closest('.portal-sidebar-toggle')) {
                    PortalFramework.components.sidebar.close();
                }
            }
        });
    };

    PortalSidebar.prototype.toggle = function() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    };

    PortalSidebar.prototype.open = function() {
        if (this.element) {
            PortalFramework.utils.addClass(this.element, 'open');
            this.isOpen = true;
            PortalFramework.events.emit('portal:sidebarOpen');
        }
    };

    PortalSidebar.prototype.close = function() {
        if (this.element) {
            PortalFramework.utils.removeClass(this.element, 'open');
            this.isOpen = false;
            PortalFramework.events.emit('portal:sidebarClose');
        }
    };

    PortalSidebar.prototype.checkResponsive = function() {
        if (window.innerWidth <= PortalFramework.config.mobileBreakpoint) {
            this.close();
        } else {
            this.open();
        }
    };

    // Portal Navigation Component
    function PortalNavigation() {
        this.currentRoute = window.location.pathname;
        this.init();
    }

    PortalNavigation.prototype.init = function() {
        this.setupEventListeners();
        this.updateActiveNavigation();
    };

    PortalNavigation.prototype.setupEventListeners = function() {
        // Handle navigation clicks
        document.addEventListener('click', function(event) {
            if (event.target.closest('.nav-link')) {
                const link = event.target.closest('.nav-link');
                const href = link.getAttribute('href');

                if (href && href !== '#' && !href.startsWith('http')) {
                    PortalFramework.events.emit('portal:navigation', { href: href, link: link });
                }
            }
        });
    };

    PortalNavigation.prototype.updateActiveNavigation = function() {
        const navLinks = document.querySelectorAll('.nav-link');

        navLinks.forEach(function(link) {
            const href = link.getAttribute('href');
            if (href === PortalFramework.components.navigation.currentRoute) {
                PortalFramework.utils.addClass(link, 'active');
            } else {
                PortalFramework.utils.removeClass(link, 'active');
            }
        });
    };

    // Portal Notifications Component
    function PortalNotifications() {
        this.container = null;
        this.notifications = [];
        this.init();
    }

    PortalNotifications.prototype.init = function() {
        this.createContainer();
        this.setupEventListeners();
    };

    PortalNotifications.prototype.createContainer = function() {
        this.container = PortalFramework.utils.createElement('div', {
            id: 'portal-notifications',
            className: 'portal-notifications'
        });
        document.body.appendChild(this.container);
    };

    PortalNotifications.prototype.setupEventListeners = function() {
        PortalFramework.events.on('portal:notification', this.show.bind(this));
    };

    PortalNotifications.prototype.show = function(options) {
        const notification = this.createNotification(options);
        this.container.appendChild(notification);
        this.notifications.push(notification);

        // Auto-remove after delay
        setTimeout(function() {
            this.remove(notification);
        }.bind(this), options.duration || 5000);

        return notification;
    };

    PortalNotifications.prototype.createNotification = function(options) {
        const notification = PortalFramework.utils.createElement('div', {
            className: `portal-notification ${options.type || 'info'}`
        });

        const icon = PortalFramework.utils.createElement('i', {
            className: `fas fa-${options.icon || 'info-circle'}`
        });

        const message = PortalFramework.utils.createElement('span', {
            className: 'notification-message'
        }, options.message);

        const closeButton = PortalFramework.utils.createElement('button', {
            className: 'notification-close',
            type: 'button'
        }, '×');

        closeButton.addEventListener('click', function() {
            this.remove(notification);
        }.bind(this));

        notification.appendChild(icon);
        notification.appendChild(message);
        notification.appendChild(closeButton);

        return notification;
    };

    PortalNotifications.prototype.remove = function(notification) {
        const index = this.notifications.indexOf(notification);
        if (index > -1) {
            this.notifications.splice(index, 1);
        }

        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    };

    // Portal Modals Component
    function PortalModals() {
        this.activeModal = null;
        this.init();
    }

    PortalModals.prototype.init = function() {
        this.setupEventListeners();
    };

    PortalModals.prototype.setupEventListeners = function() {
        PortalFramework.events.on('portal:modalClose', this.closeActive.bind(this));
        PortalFramework.events.on('portal:escape', this.closeActive.bind(this));
    };

    PortalModals.prototype.show = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            this.activeModal = modal;
            PortalFramework.utils.addClass(modal, 'show');
            PortalFramework.events.emit('portal:modalOpen', { modalId: modalId });
        }
    };

    PortalModals.prototype.close = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            PortalFramework.utils.removeClass(modal, 'show');
            if (this.activeModal === modal) {
                this.activeModal = null;
            }
            PortalFramework.events.emit('portal:modalClose', { modalId: modalId });
        }
    };

    PortalModals.prototype.closeActive = function() {
        if (this.activeModal) {
            this.close(this.activeModal.id);
        }
    };

    // Portal Charts Component (if Chart.js is available)
    function PortalCharts() {
        this.charts = new Map();
        this.init();
    }

    PortalCharts.prototype.init = function() {
        // Initialize charts when DOM is ready
        PortalFramework.utils.dom.ready(function() {
            this.initializeCharts();
        }.bind(this));
    };

    PortalCharts.prototype.initializeCharts = function() {
        const chartElements = document.querySelectorAll('[data-chart]');

        chartElements.forEach(function(element) {
            const chartType = element.getAttribute('data-chart');
            const chartData = JSON.parse(element.getAttribute('data-chart-data') || '{}');
            const chartOptions = JSON.parse(element.getAttribute('data-chart-options') || '{}');

            this.createChart(element, chartType, chartData, chartOptions);
        }.bind(this));
    };

    PortalCharts.prototype.createChart = function(element, type, data, options) {
        try {
            const chart = new Chart(element, {
                type: type,
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    ...options
                }
            });

            this.charts.set(element, chart);
        } catch (error) {
            console.error('Failed to create chart:', error);
        }
    };

    PortalCharts.prototype.updateChart = function(element, newData) {
        const chart = this.charts.get(element);
        if (chart) {
            chart.data = newData;
            chart.update();
        }
    };

    PortalCharts.prototype.destroyChart = function(element) {
        const chart = this.charts.get(element);
        if (chart) {
            chart.destroy();
            this.charts.delete(element);
        }
    };

    // Initialize when DOM is ready
    PortalFramework.utils.dom.ready(function() {
        // Auto-initialize if config is available
        if (window.PortalConfig) {
            PortalFramework.init(window.PortalConfig);
        }
    });

})();

export default window.PortalFramework;
