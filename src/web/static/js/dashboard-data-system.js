/**
 * DASHBOARD DATA SYSTEM - V2 COMPLIANT MODULE
 * ===========================================
 * 
 * Dashboard data management functionality.
 * Extracted from dashboard-components-consolidated.js for V2 compliance.
 * 
 * @author Agent-2 (Architecture & Design Specialist)
 * @mission Phase 4 Consolidation - JS-02 Dashboard Components
 * @version 2.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @license MIT
 */

/**
 * Dashboard Data System
 * Handles all data management operations
 */
class DashboardDataSystem {
    constructor() {
        this.data = new Map();
        this.socketManager = null;
        this.communication = null;
        this.loadingManager = null;
        this.dataOperations = null;
        this.timeManager = null;
        
        this._initializeDataSubsystems();
    }

    /**
     * Initialize data management subsystems
     */
    _initializeDataSubsystems() {
        // Data Management
        this.dataManager = {
            data: new Map(),
            setData: (key, value) => {
                this.dataManager.data.set(key, value);
                this._notifyDataChange(key, value);
            },
            getData: (key) => this.dataManager.data.get(key),
            clearData: () => {
                this.dataManager.data.clear();
                this._notifyDataClear();
            },
            loadData: async (source) => {
                try {
                    this._startLoading('data-loading');
                    const response = await fetch(source);
                    const data = await response.json();
                    this.dataManager.setData(source, data);
                    return data;
                } catch (error) {
                    this._handleDataError(error, 'Data Loading');
                    throw error;
                } finally {
                    this._stopLoading('data-loading');
                }
            }
        };

        // WebSocket Management
        this.socketManager = {
            socket: null,
            connect: (url) => {
                this.socketManager.socket = new WebSocket(url);
                this.socketManager.socket.onmessage = (event) => {
                    this._handleWebSocketMessage(event);
                };
                this.socketManager.socket.onerror = (error) => {
                    this._handleDataError(error, 'WebSocket');
                };
            },
            disconnect: () => {
                if (this.socketManager.socket) {
                    this.socketManager.socket.close();
                    this.socketManager.socket = null;
                }
            },
            send: (message) => {
                if (this.socketManager.socket && this.socketManager.socket.readyState === WebSocket.OPEN) {
                    this.socketManager.socket.send(JSON.stringify(message));
                }
            }
        };

        // Communication
        this.communication = {
            sendMessage: (type, data) => {
                if (this.socketManager.socket) {
                    this.socketManager.send({ type, data });
                }
            },
            handleMessage: (message) => {
                switch (message.type) {
                    case 'data_update':
                        this.dataManager.setData(message.key, message.data);
                        break;
                    case 'view_change':
                        this._notifyViewChange(message.view);
                        break;
                    case 'error':
                        this._handleDataError(message.error, message.context);
                        break;
                    default:
                        console.log('Unknown message type:', message.type);
                }
            }
        };

        // Loading Management
        this.loadingManager = {
            activeLoaders: new Set(),
            startLoading: (id) => {
                this.loadingManager.activeLoaders.add(id);
                this._updateLoadingState();
            },
            stopLoading: (id) => {
                this.loadingManager.activeLoaders.delete(id);
                this._updateLoadingState();
            },
            isLoading: () => this.loadingManager.activeLoaders.size > 0
        };

        // Data Operations
        this.dataOperations = {
            processData: (data, operation) => {
                switch (operation) {
                    case 'filter':
                        return data.filter(item => item.active);
                    case 'sort':
                        return data.sort((a, b) => a.name.localeCompare(b.name));
                    case 'aggregate':
                        return data.reduce((acc, item) => acc + item.value, 0);
                    default:
                        return data;
                }
            },
            transformData: (data, transformer) => {
                return data.map(transformer);
            }
        };

        // Time Management
        this.timeManager = {
            getCurrentTime: () => new Date(),
            formatTime: (date) => date.toLocaleTimeString(),
            formatDate: (date) => date.toLocaleDateString(),
            getTimeAgo: (date) => {
                const now = new Date();
                const diff = now - date;
                const minutes = Math.floor(diff / 60000);
                if (minutes < 1) return 'just now';
                if (minutes < 60) return `${minutes}m ago`;
                const hours = Math.floor(minutes / 60);
                if (hours < 24) return `${hours}h ago`;
                const days = Math.floor(hours / 24);
                return `${days}d ago`;
            }
        };
    }

    /**
     * Initialize data system
     */
    async initialize() {
        console.log('🚀 Initializing Dashboard Data System...');
        
        try {
            // Set up WebSocket connection
            this._setupWebSocket();
            
            // Set up data operations
            this._setupDataOperations();
            
            // Set up loading management
            this._setupLoadingManagement();
            
            // Set up time management
            this._setupTimeManagement();
            
            // Load initial data
            await this._loadInitialData();
            
            console.log('✅ Dashboard Data System initialized successfully');
            
        } catch (error) {
            this._handleDataError(error, 'Data System Initialization');
            throw error;
        }
    }

    /**
     * Set up WebSocket connection
     */
    _setupWebSocket() {
        // Set up WebSocket connection
        this.socketManager.connect('ws://localhost:8080/dashboard');
    }

    /**
     * Set up data operations
     */
    _setupDataOperations() {
        // Set up data processing pipelines
        this.dataOperations.processData = this.dataOperations.processData.bind(this);
        this.dataOperations.transformData = this.dataOperations.transformData.bind(this);
    }

    /**
     * Set up loading management
     */
    _setupLoadingManagement() {
        // Set up loading state management
        this.loadingManager.startLoading('system');
    }

    /**
     * Set up time management
     */
    _setupTimeManagement() {
        // Set up time-based updates
        setInterval(() => {
            this._notifyTimeUpdate();
        }, 1000);
    }

    /**
     * Load initial data
     */
    async _loadInitialData() {
        // Initialize default data sources
        const defaultDataSources = [
            '/api/dashboard/overview',
            '/api/dashboard/performance',
            '/api/dashboard/alerts'
        ];

        for (const source of defaultDataSources) {
            try {
                await this.dataManager.loadData(source);
            } catch (error) {
                console.warn(`Failed to load data from ${source}:`, error);
            }
        }
    }

    /**
     * Handle WebSocket message
     */
    _handleWebSocketMessage(event) {
        try {
            const message = JSON.parse(event.data);
            this.communication.handleMessage(message);
        } catch (error) {
            this._handleDataError(error, 'WebSocket Message Handling');
        }
    }

    /**
     * Handle data error
     */
    _handleDataError(error, context) {
        console.error(`Data Error [${context}]:`, error);
        this._notifyDataError(error, context);
    }

    /**
     * Start loading
     */
    _startLoading(id) {
        this.loadingManager.startLoading(id);
    }

    /**
     * Stop loading
     */
    _stopLoading(id) {
        this.loadingManager.stopLoading(id);
    }

    /**
     * Update loading state
     */
    _updateLoadingState() {
        if (this.loadingManager.isLoading()) {
            this._showLoadingState();
        } else {
            this._hideLoadingState();
        }
    }

    /**
     * Show loading state
     */
    _showLoadingState() {
        const loadingContainer = document.getElementById('loading-container');
        if (loadingContainer) {
            loadingContainer.style.display = 'block';
        }
    }

    /**
     * Hide loading state
     */
    _hideLoadingState() {
        const loadingContainer = document.getElementById('loading-container');
        if (loadingContainer) {
            loadingContainer.style.display = 'none';
        }
    }

    /**
     * Notify data change
     */
    _notifyDataChange(key, value) {
        this._dispatchEvent('dataChange', { key, value });
    }

    /**
     * Notify data clear
     */
    _notifyDataClear() {
        this._dispatchEvent('dataClear', {});
    }

    /**
     * Notify view change
     */
    _notifyViewChange(view) {
        this._dispatchEvent('viewChange', { view });
    }

    /**
     * Notify data error
     */
    _notifyDataError(error, context) {
        this._dispatchEvent('dataError', { error, context });
    }

    /**
     * Notify time update
     */
    _notifyTimeUpdate() {
        this._dispatchEvent('timeUpdate', { timestamp: new Date() });
    }

    /**
     * Dispatch event
     */
    _dispatchEvent(type, detail) {
        const event = new CustomEvent(`dashboard:data:${type}`, { detail });
        document.dispatchEvent(event);
    }

    /**
     * Get data system status
     */
    getStatus() {
        return {
            dataCount: this.dataManager.data.size,
            socketConnected: this.socketManager.socket?.readyState === WebSocket.OPEN,
            loading: this.loadingManager.isLoading(),
            activeLoaders: Array.from(this.loadingManager.activeLoaders)
        };
    }

    /**
     * Shutdown data system
     */
    shutdown() {
        console.log('🔄 Shutting down Dashboard Data System...');
        
        // Disconnect WebSocket
        this.socketManager.disconnect();
        
        // Clear data
        this.dataManager.clearData();
        
        // Clear loading states
        this.loadingManager.activeLoaders.clear();
        
        console.log('✅ Dashboard Data System shutdown complete');
    }
}

// Export the main class
export default DashboardDataSystem;