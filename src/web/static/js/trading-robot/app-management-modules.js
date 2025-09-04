/**
 * App Management Modules - V2 Compliant Application Management Utilities
 * Handles all application lifecycle and management operations
 * 
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - Trading Robot Frontend V2 Compliance
 * @license MIT
 */

/**
 * Application management utilities for trading robot
 */
export class AppManagementModules {
    /**
     * Initialize all trading components
     */
    static async initializeComponents(websocketManager, portfolioManager, orderManager, chartManager, dashboard) {
        // Create component instances
        const components = {
            websocketManager,
            portfolioManager,
            orderManager,
            chartManager,
            dashboard
        };

        // Initialize components in parallel
        await Promise.all([
            websocketManager.initialize(),
            portfolioManager.initialize(),
            orderManager.initialize(),
            chartManager.initialize()
        ]);

        return components;
    }

    /**
     * Setup cross-component communication
     */
    static setupComponentCommunication(websocketManager, portfolioManager, orderManager, chartManager) {
        // WebSocket to Portfolio communication
        websocketManager.addCallback('portfolioUpdate', (data) => {
            portfolioManager.updatePortfolio(data);
        });

        // WebSocket to Chart communication
        websocketManager.addCallback('priceUpdate', (data) => {
            chartManager.updateChartData(data);
        });

        // Order Manager to Portfolio communication
        orderManager.addOrderCallback((order) => {
            if (order.status === 'filled') {
                portfolioManager.updatePortfolioFromOrder(order);
            }
        });

        // Portfolio to Dashboard communication
        portfolioManager.addCallback('portfolioUpdate', (data) => {
            // Dashboard will listen for this event
        });
    }

    /**
     * Start application services
     */
    static startApplicationServices(websocketManager, portfolioManager, orderManager, chartManager) {
        // Start WebSocket connection
        websocketManager.connect();

        // Start periodic updates
        setInterval(() => {
            this.updateApplicationMetrics(websocketManager, portfolioManager, orderManager, chartManager);
        }, 30000); // Update every 30 seconds

        // Start component health checks
        setInterval(() => {
            this.performHealthChecks(websocketManager, portfolioManager, orderManager, chartManager);
        }, 60000); // Check every minute
    }

    /**
     * Update application metrics
     */
    static updateApplicationMetrics(websocketManager, portfolioManager, orderManager, chartManager) {
        const metrics = {
            timestamp: new Date(),
            isConnected: websocketManager.isConnected(),
            portfolioValue: portfolioManager.getCurrentPortfolio().totalValue,
            activeOrders: orderManager.getOrderHistory().filter(o => 
                o.status === 'pending' || o.status === 'submitted'
            ).length,
            chartDataPoints: chartManager.getCurrentChartData().length
        };

        // Dispatch metrics event
        this.dispatchEvent('tradingRobot:metrics', metrics);
    }

    /**
     * Perform health checks
     */
    static performHealthChecks(websocketManager, portfolioManager, orderManager, chartManager) {
        const healthStatus = {
            websocket: websocketManager.isConnected(),
            portfolio: portfolioManager.isHealthy(),
            orders: orderManager.isHealthy(),
            charts: chartManager.isHealthy()
        };

        // Dispatch health check event
        this.dispatchEvent('tradingRobot:healthCheck', healthStatus);
    }

    /**
     * Handle initialization error
     */
    static handleInitializationError(error) {
        console.error('❌ Trading Robot initialization failed:', error);
        
        // Show user-friendly error message
        this.showErrorMessage('Failed to initialize Trading Robot. Please refresh the page.');
        
        // Dispatch error event
        this.dispatchEvent('tradingRobot:error', {
            type: 'initialization',
            error: error.message,
            timestamp: new Date()
        });
    }

    /**
     * Handle application errors
     */
    static handleError(type, error) {
        console.error(`❌ ${type}:`, error);
        
        // Dispatch error event
        this.dispatchEvent('tradingRobot:error', {
            type: type,
            error: error.message || error,
            timestamp: new Date()
        });
    }

    /**
     * Show error message to user
     */
    static showErrorMessage(message) {
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'trading-error-notification';
        errorDiv.innerHTML = `
            <div class="error-content">
                <span class="error-icon">⚠️</span>
                <span class="error-message">${message}</span>
                <button class="error-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;
        
        // Add to page
        document.body.appendChild(errorDiv);
        
        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (errorDiv.parentElement) {
                errorDiv.remove();
            }
        }, 10000);
    }

    /**
     * Dispatch custom event
     */
    static dispatchEvent(eventName, data) {
        const event = new CustomEvent(eventName, {
            detail: data
        });
        document.dispatchEvent(event);
    }

    /**
     * Get application status
     */
    static getApplicationStatus(websocketManager, portfolioManager, orderManager, chartManager, dashboard, isInitialized, appConfig) {
        return {
            isInitialized: isInitialized,
            version: appConfig.version,
            environment: appConfig.environment,
            components: {
                websocket: websocketManager ? websocketManager.getConnectionStatus() : 'not_initialized',
                portfolio: portfolioManager ? 'initialized' : 'not_initialized',
                orders: orderManager ? 'initialized' : 'not_initialized',
                charts: chartManager ? 'initialized' : 'not_initialized',
                dashboard: dashboard ? 'initialized' : 'not_initialized'
            }
        };
    }

    /**
     * Shutdown application
     */
    static shutdown(websocketManager) {
        console.log('🛑 Shutting down Trading Robot Application...');
        
        if (websocketManager) {
            websocketManager.disconnect();
        }
        
        console.log('✅ Trading Robot Application shutdown complete');
    }
}
