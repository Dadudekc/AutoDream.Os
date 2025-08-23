/**
 * Portal Components JavaScript
 * Agent_Cellphone_V2_Repository - Unified Portal Architecture
 */

(function() {
    'use strict';

    // Portal Components Namespace
    window.PortalComponents = {
        version: '1.0.0',
        components: {},
        widgets: {},
        utils: {}
    };

    // Dashboard Widgets
    PortalComponents.widgets = {
        // Agent Status Widget
        AgentStatusWidget: function(container, config) {
            this.container = container;
            this.config = config || {};
            this.agents = [];
            this.refreshInterval = null;

            this.init();
        },

        // System Health Widget
        SystemHealthWidget: function(container, config) {
            this.container = container;
            this.config = config || {};
            this.metrics = {};
            this.refreshInterval = null;

            this.init();
        },

        // Activity Timeline Widget
        ActivityTimelineWidget: function(container, config) {
            this.container = container;
            this.config = config || {};
            this.activities = [];
            this.refreshInterval = null;

            this.init();
        },

        // Quick Actions Widget
        QuickActionsWidget: function(container, config) {
            this.container = container;
            this.config = config || {};
            this.actions = [];

            this.init();
        }
    };

    // Agent Status Widget Implementation
    PortalComponents.widgets.AgentStatusWidget.prototype = {
        init: function() {
            this.render();
            this.setupEventListeners();
            this.startAutoRefresh();
        },

        render: function() {
            this.container.innerHTML = `
                <div class="widget-header">
                    <h3><i class="fas fa-robot"></i> Agent Status</h3>
                    <div class="widget-actions">
                        <button class="btn btn-sm btn-outline" onclick="this.refresh()">
                            <i class="fas fa-sync-alt"></i>
                        </button>
                    </div>
                </div>
                <div class="widget-content">
                    <div class="agent-status-list" id="agent-status-list-${this.container.id}">
                        <div class="loading">Loading agent status...</div>
                    </div>
                </div>
            `;
        },

        setupEventListeners: function() {
            // Listen for agent updates
            if (window.PortalFramework) {
                PortalFramework.events.on('portal:agentsUpdated', this.updateAgents.bind(this));
            }
        },

        startAutoRefresh: function() {
            if (this.config.autoRefresh !== false) {
                this.refreshInterval = setInterval(() => {
                    this.refresh();
                }, this.config.refreshInterval || 30000);
            }
        },

        refresh: function() {
            this.loadAgentStatus();
        },

        loadAgentStatus: function() {
            const url = this.config.apiEndpoint || '/api/agents';

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.updateAgents(data);
                })
                .catch(error => {
                    console.error('Failed to load agent status:', error);
                    this.showError('Failed to load agent status');
                });
        },

        updateAgents: function(agents) {
            this.agents = agents;
            this.renderAgentList();
        },

        renderAgentList: function() {
            const listContainer = this.container.querySelector('.agent-status-list');

            if (!this.agents || this.agents.length === 0) {
                listContainer.innerHTML = '<div class="no-data">No agents found</div>';
                return;
            }

            const agentHtml = this.agents.map(agent => `
                <div class="agent-status-item ${agent.status}">
                    <div class="agent-info">
                        <div class="agent-icon">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div class="agent-details">
                            <div class="agent-name">${agent.name}</div>
                            <div class="agent-id">${agent.agent_id}</div>
                        </div>
                        <div class="agent-status">
                            <span class="status-dot"></span>
                            ${agent.status}
                        </div>
                    </div>
                    <div class="agent-actions">
                        <button class="btn btn-sm btn-outline" onclick="this.showAgentDetails('${agent.agent_id}')">
                            Details
                        </button>
                    </div>
                </div>
            `).join('');

            listContainer.innerHTML = agentHtml;
        },

        showAgentDetails: function(agentId) {
            // Emit event for showing agent details
            if (window.PortalFramework) {
                PortalFramework.events.emit('portal:showAgentDetails', { agentId: agentId });
            }
        },

        showError: function(message) {
            const listContainer = this.container.querySelector('.agent-status-list');
            listContainer.innerHTML = `<div class="error">${message}</div>`;
        },

        destroy: function() {
            if (this.refreshInterval) {
                clearInterval(this.refreshInterval);
            }
        }
    };

    // System Health Widget Implementation
    PortalComponents.widgets.SystemHealthWidget.prototype = {
        init: function() {
            this.render();
            this.setupEventListeners();
            this.startAutoRefresh();
        },

        render: function() {
            this.container.innerHTML = `
                <div class="widget-header">
                    <h3><i class="fas fa-heartbeat"></i> System Health</h3>
                    <div class="widget-actions">
                        <button class="btn btn-sm btn-outline" onclick="this.refresh()">
                            <i class="fas fa-sync-alt"></i>
                        </button>
                    </div>
                </div>
                <div class="widget-content">
                    <div class="health-metrics" id="health-metrics-${this.container.id}">
                        <div class="loading">Loading system health...</div>
                    </div>
                </div>
            `;
        },

        setupEventListeners: function() {
            if (window.PortalFramework) {
                PortalFramework.events.on('portal:metricsUpdated', this.updateMetrics.bind(this));
            }
        },

        startAutoRefresh: function() {
            if (this.config.autoRefresh !== false) {
                this.refreshInterval = setInterval(() => {
                    this.refresh();
                }, this.config.refreshInterval || 30000);
            }
        },

        refresh: function() {
            this.loadSystemHealth();
        },

        loadSystemHealth: function() {
            const url = this.config.apiEndpoint || '/api/portal/stats';

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.updateMetrics(data);
                })
                .catch(error => {
                    console.error('Failed to load system health:', error);
                    this.showError('Failed to load system health');
                });
        },

        updateMetrics: function(metrics) {
            this.metrics = metrics;
            this.renderMetrics();
        },

        renderMetrics: function() {
            const metricsContainer = this.container.querySelector('.health-metrics');

            if (!this.metrics) {
                metricsContainer.innerHTML = '<div class="no-data">No metrics available</div>';
                return;
            }

            const metricsHtml = `
                <div class="health-overview">
                    <div class="health-status ${this.metrics.overall || 'unknown'}">
                        <i class="fas fa-circle"></i>
                        <span>${this.metrics.overall || 'Unknown'}</span>
                    </div>
                </div>
                <div class="health-details">
                    <div class="metric-item">
                        <span class="metric-label">CPU Usage:</span>
                        <span class="metric-value">${this.metrics.cpu_usage || 'N/A'}%</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Memory Usage:</span>
                        <span class="metric-value">${this.metrics.memory_usage || 'N/A'}%</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Active Connections:</span>
                        <span class="metric-value">${this.metrics.active_connections || 'N/A'}</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Uptime:</span>
                        <span class="metric-value">${this.metrics.uptime || 'N/A'}</span>
                    </div>
                </div>
            `;

            metricsContainer.innerHTML = metricsHtml;
        },

        showError: function(message) {
            const metricsContainer = this.container.querySelector('.health-metrics');
            metricsContainer.innerHTML = `<div class="error">${message}</div>`;
        },

        destroy: function() {
            if (this.refreshInterval) {
                clearInterval(this.refreshInterval);
            }
        }
    };

    // Activity Timeline Widget Implementation
    PortalComponents.widgets.ActivityTimelineWidget.prototype = {
        init: function() {
            this.render();
            this.setupEventListeners();
            this.startAutoRefresh();
        },

        render: function() {
            this.container.innerHTML = `
                <div class="widget-header">
                    <h3><i class="fas fa-clock"></i> Recent Activity</h3>
                    <div class="widget-actions">
                        <button class="btn btn-sm btn-outline" onclick="this.refresh()">
                            <i class="fas fa-sync-alt"></i>
                        </button>
                    </div>
                </div>
                <div class="widget-content">
                    <div class="activity-timeline" id="activity-timeline-${this.container.id}">
                        <div class="loading">Loading recent activity...</div>
                    </div>
                </div>
            `;
        },

        setupEventListeners: function() {
            if (window.PortalFramework) {
                PortalFramework.events.on('portal:activityUpdated', this.updateActivities.bind(this));
            }
        },

        startAutoRefresh: function() {
            if (this.config.autoRefresh !== false) {
                this.refreshInterval = setInterval(() => {
                    this.refresh();
                }, this.config.refreshInterval || 60000);
            }
        },

        refresh: function() {
            this.loadRecentActivity();
        },

        loadRecentActivity: function() {
            const url = this.config.apiEndpoint || '/api/portal/activity';

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.updateActivities(data);
                })
                .catch(error => {
                    console.error('Failed to load recent activity:', error);
                    this.showError('Failed to load recent activity');
                });
        },

        updateActivities: function(activities) {
            this.activities = activities;
            this.renderActivities();
        },

        renderActivities: function() {
            const timelineContainer = this.container.querySelector('.activity-timeline');

            if (!this.activities || this.activities.length === 0) {
                timelineContainer.innerHTML = '<div class="no-data">No recent activity</div>';
                return;
            }

            const activitiesHtml = this.activities.slice(0, this.config.maxItems || 10).map(activity => `
                <div class="activity-item ${activity.type || 'info'}">
                    <div class="activity-icon">
                        <i class="fas fa-${this.getActivityIcon(activity.type)}"></i>
                    </div>
                    <div class="activity-content">
                        <div class="activity-header">
                            <h4 class="activity-title">${activity.title}</h4>
                            <span class="activity-time">${this.formatTime(activity.timestamp)}</span>
                        </div>
                        <p class="activity-description">${activity.description}</p>
                        ${activity.agent_id ? `<span class="activity-agent">by ${activity.agent_id}</span>` : ''}
                    </div>
                </div>
            `).join('');

            timelineContainer.innerHTML = activitiesHtml;
        },

        getActivityIcon: function(type) {
            const iconMap = {
                'info': 'info-circle',
                'success': 'check-circle',
                'warning': 'exclamation-triangle',
                'error': 'times-circle',
                'default': 'info-circle'
            };
            return iconMap[type] || iconMap.default;
        },

        formatTime: function(timestamp) {
            if (!timestamp) return 'Unknown';

            try {
                const date = new Date(timestamp);
                const now = new Date();
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
            } catch (error) {
                return 'Unknown';
            }
        },

        showError: function(message) {
            const timelineContainer = this.container.querySelector('.activity-timeline');
            timelineContainer.innerHTML = `<div class="error">${message}</div>`;
        },

        destroy: function() {
            if (this.refreshInterval) {
                clearInterval(this.refreshInterval);
            }
        }
    };

    // Quick Actions Widget Implementation
    PortalComponents.widgets.QuickActionsWidget.prototype = {
        init: function() {
            this.actions = this.config.actions || this.getDefaultActions();
            this.render();
            this.setupEventListeners();
        },

        getDefaultActions: function() {
            return [
                {
                    id: 'add-agent',
                    title: 'Add Agent',
                    description: 'Register a new agent system',
                    icon: 'plus-circle',
                    action: 'showAddAgentModal'
                },
                {
                    id: 'start-workflow',
                    title: 'Start Workflow',
                    description: 'Launch automation workflow',
                    icon: 'play-circle',
                    action: 'showWorkflowModal'
                },
                {
                    id: 'view-reports',
                    title: 'View Reports',
                    description: 'Access system reports',
                    icon: 'chart-line',
                    action: 'showReportsModal'
                },
                {
                    id: 'portal-settings',
                    title: 'Portal Settings',
                    description: 'Configure portal options',
                    icon: 'cog',
                    action: 'showSettingsModal'
                }
            ];
        },

        render: function() {
            this.container.innerHTML = `
                <div class="widget-header">
                    <h3><i class="fas fa-bolt"></i> Quick Actions</h3>
                </div>
                <div class="widget-content">
                    <div class="quick-actions-grid" id="quick-actions-${this.container.id}">
                        ${this.renderActions()}
                    </div>
                </div>
            `;
        },

        renderActions: function() {
            return this.actions.map(action => `
                <div class="action-card" data-action="${action.action}">
                    <div class="action-icon">
                        <i class="fas fa-${action.icon}"></i>
                    </div>
                    <h3>${action.title}</h3>
                    <p>${action.description}</p>
                    <button class="btn btn-primary" onclick="this.executeAction('${action.action}')">
                        <i class="fas fa-${action.icon}"></i> ${action.title}
                    </button>
                </div>
            `).join('');
        },

        setupEventListeners: function() {
            // Action click events are handled inline for simplicity
        },

        executeAction: function(actionName) {
            switch (actionName) {
                case 'showAddAgentModal':
                    this.showAddAgentModal();
                    break;
                case 'showWorkflowModal':
                    this.showWorkflowModal();
                    break;
                case 'showReportsModal':
                    this.showReportsModal();
                    break;
                case 'showSettingsModal':
                    this.showSettingsModal();
                    break;
                default:
                    console.log('Unknown action:', actionName);
            }
        },

        showAddAgentModal: function() {
            if (window.PortalFramework) {
                PortalFramework.events.emit('portal:showModal', { modalId: 'addAgentModal' });
            }
        },

        showWorkflowModal: function() {
            if (window.PortalFramework) {
                PortalFramework.events.emit('portal:showModal', { modalId: 'workflowModal' });
            }
        },

        showReportsModal: function() {
            if (window.PortalFramework) {
                PortalFramework.events.emit('portal:showModal', { modalId: 'reportsModal' });
            }
        },

        showSettingsModal: function() {
            if (window.PortalFramework) {
                PortalFramework.events.emit('portal:showModal', { modalId: 'settingsModal' });
            }
        },

        destroy: function() {
            // No cleanup needed for this widget
        }
    };

    // Portal Components Factory
    PortalComponents.createWidget = function(type, container, config) {
        if (PortalComponents.widgets[type]) {
            return new PortalComponents.widgets[type](container, config);
        } else {
            console.error('Unknown widget type:', type);
            return null;
        }
    };

    // Portal Components Utilities
    PortalComponents.utils = {
        // Format numbers with appropriate units
        formatNumber: function(number, decimals = 2) {
            if (number >= 1000000) {
                return (number / 1000000).toFixed(decimals) + 'M';
            } else if (number >= 1000) {
                return (number / 1000).toFixed(decimals) + 'K';
            } else {
                return number.toString();
            }
        },

        // Format file sizes
        formatFileSize: function(bytes) {
            if (bytes === 0) return '0 Bytes';

            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));

            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },

        // Format duration
        formatDuration: function(seconds) {
            if (seconds < 60) {
                return seconds + 's';
            } else if (seconds < 3600) {
                const minutes = Math.floor(seconds / 60);
                const remainingSeconds = seconds % 60;
                return minutes + 'm ' + remainingSeconds + 's';
            } else {
                const hours = Math.floor(seconds / 3600);
                const remainingMinutes = Math.floor((seconds % 3600) / 60);
                return hours + 'h ' + remainingMinutes + 'm';
            }
        },

        // Debounce function
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = function() {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        // Throttle function
        throttle: function(func, limit) {
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
    };

    // Auto-initialize widgets when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        // Find all widget containers and initialize them
        const widgetContainers = document.querySelectorAll('[data-widget]');

        widgetContainers.forEach(function(container) {
            const widgetType = container.getAttribute('data-widget');
            const configData = container.getAttribute('data-widget-config');

            let config = {};
            if (configData) {
                try {
                    config = JSON.parse(configData);
                } catch (error) {
                    console.error('Invalid widget config:', configData);
                }
            }

            PortalComponents.createWidget(widgetType, container, config);
        });
    });

})();
