/**
 * Portal Rendering Module
 * Contains UI component constructors for the portal.
 */
(function() {
    'use strict';

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
    
    // Expose constructors
    window.PortalRendering = {
        Sidebar: PortalSidebar,
        Navigation: PortalNavigation,
        Notifications: PortalNotifications,
        Modals: PortalModals,
        Charts: PortalCharts
    };
    
})();
