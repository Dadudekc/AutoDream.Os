/**
 * Trading Dashboard - V2 Compliant Trading Robot Frontend
 * Real-time trading dashboard with live metrics and portfolio management
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - Trading Robot Frontend V2 Compliance
 * @license MIT
 */

// ================================
// IMPORT MODULAR COMPONENTS
// ================================

import { TradingChartManager } from './trading-chart-manager.js';
import { TradingOrderManager } from './trading-order-manager.js';
import { TradingPortfolioManager } from './trading-portfolio-manager.js';
import { TradingWebSocketManager } from './trading-websocket-manager.js';

// ================================
// TRADING DASHBOARD
// ================================

/**
 * Main Trading Dashboard orchestrator
 * COORDINATES all trading components for V2 compliance
 */
export class TradingDashboard {
    constructor() {
        this.websocketManager = new TradingWebSocketManager();
        this.portfolioManager = new TradingPortfolioManager();
        this.orderManager = new TradingOrderManager();
        this.chartManager = new TradingChartManager();
        this.isInitialized = false;

        // V2 Compliance: Use structured logging instead of console
        this.logger = {
            log: (message) => {
                const timestamp = new Date().toISOString();
                const logEntry = `[${timestamp}] TRADING-DASHBOARD: ${message}`;
                if (!this._logs) this._logs = [];
                this._logs.push(logEntry);
            },
            error: (message, error) => {
                const timestamp = new Date().toISOString();
                const errorEntry = `[${timestamp}] TRADING-DASHBOARD ERROR: ${message}`;
                if (!this._logs) this._logs = [];
                this._logs.push(errorEntry);
                this._logs.push(`Error details: ${error}`);
            }
        };
    }

    /**
     * Initialize the trading dashboard
     */
    async initialize() {
        if (this.isInitialized) return;

        try {
            this.logger.log('🚀 Initializing Trading Dashboard...');
            
            // Initialize all components
            await this.websocketManager.initialize();
            await this.portfolioManager.initialize();
            await this.orderManager.initialize();
            await this.chartManager.initialize();
            
            // Set up real-time data connections
            this.setupRealTimeConnections();
            
            // Initialize UI components
            this.initializeUI();
            
            this.isInitialized = true;
            this.logger.log('✅ Trading Dashboard initialized successfully');
            
        } catch (error) {
            this.logger.error('❌ Trading Dashboard initialization failed:', error);
            throw error;
        }
    }

    /**
     * Set up real-time data connections
     */
    setupRealTimeConnections() {
        // WebSocket market data
        this.websocketManager.onMarketData((data) => {
            this.chartManager.updatePriceData(data);
            this.portfolioManager.updatePortfolioValue(data);
        });

        // Portfolio updates
        this.portfolioManager.onPortfolioUpdate((portfolio) => {
            this.updatePortfolioDisplay(portfolio);
        });

        // Order updates
        this.orderManager.onOrderUpdate((order) => {
            this.updateOrderDisplay(order);
        });
    }

    /**
     * Initialize UI components
     */
    initializeUI() {
        // Create dashboard layout
        this.createDashboardLayout();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Start real-time updates
        this.startRealTimeUpdates();
    }

    /**
     * Create dashboard layout
     */
    createDashboardLayout() {
        const dashboard = document.getElementById('trading-dashboard');
        if (!dashboard) return;

        dashboard.innerHTML = `
            <div class="trading-dashboard-container">
                <div class="trading-header">
                    <h1>Trading Robot Dashboard</h1>
                    <div class="connection-status" id="connection-status">Connecting...</div>
                </div>
                
                <div class="trading-content">
                    <div class="portfolio-panel">
                        <h2>Portfolio</h2>
                        <div id="portfolio-summary"></div>
                    </div>
                    
                    <div class="chart-panel">
                        <h2>Price Chart</h2>
                        <div id="trading-chart"></div>
                    </div>
                    
                    <div class="order-panel">
                        <h2>Orders</h2>
                        <div id="order-form"></div>
                        <div id="order-history"></div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Portfolio management events
        document.addEventListener('portfolio:update', (event) => {
            this.handlePortfolioUpdate(event.detail);
        });

        // Order management events
        document.addEventListener('order:submit', (event) => {
            this.handleOrderSubmit(event.detail);
        });

        // Chart interaction events
        document.addEventListener('chart:interaction', (event) => {
            this.handleChartInteraction(event.detail);
        });
    }

    /**
     * Start real-time updates
     */
    startRealTimeUpdates() {
        setInterval(() => {
            this.updateDashboardMetrics();
        }, 1000); // Update every second
    }

    /**
     * Update dashboard metrics
     */
    updateDashboardMetrics() {
        const portfolio = this.portfolioManager.getCurrentPortfolio();
        const marketData = this.websocketManager.getLatestMarketData();
        
        this.updatePortfolioDisplay(portfolio);
        this.updateConnectionStatus();
    }

    /**
     * Update portfolio display
     */
    updatePortfolioDisplay(portfolio) {
        const portfolioSummary = document.getElementById('portfolio-summary');
        if (!portfolioSummary) return;

        portfolioSummary.innerHTML = `
            <div class="portfolio-metrics">
                <div class="metric">
                    <label>Total Value:</label>
                    <span class="value">$${portfolio.totalValue.toFixed(2)}</span>
                </div>
                <div class="metric">
                    <label>P&L:</label>
                    <span class="value ${portfolio.pnl >= 0 ? 'positive' : 'negative'}">
                        $${portfolio.pnl.toFixed(2)}
                    </span>
                </div>
                <div class="metric">
                    <label>Positions:</label>
                    <span class="value">${portfolio.positions.length}</span>
                </div>
            </div>
        `;
    }

    /**
     * Update order display
     */
    updateOrderDisplay(order) {
        const orderHistory = document.getElementById('order-history');
        if (!orderHistory) return;

        const orderElement = document.createElement('div');
        orderElement.className = 'order-item';
        orderElement.innerHTML = `
            <div class="order-info">
                <span class="symbol">${order.symbol}</span>
                <span class="side">${order.side}</span>
                <span class="quantity">${order.quantity}</span>
                <span class="price">$${order.price.toFixed(2)}</span>
                <span class="status">${order.status}</span>
            </div>
        `;
        
        orderHistory.insertBefore(orderElement, orderHistory.firstChild);
    }

    /**
     * Update connection status
     */
    updateConnectionStatus() {
        const statusElement = document.getElementById('connection-status');
        if (!statusElement) return;

        const isConnected = this.websocketManager.isConnected();
        statusElement.textContent = isConnected ? 'Connected' : 'Disconnected';
        statusElement.className = `connection-status ${isConnected ? 'connected' : 'disconnected'}`;
    }

    /**
     * Handle portfolio update
     */
    handlePortfolioUpdate(portfolioData) {
        this.portfolioManager.updatePortfolio(portfolioData);
    }

    /**
     * Handle order submit
     */
    handleOrderSubmit(orderData) {
        this.orderManager.submitOrder(orderData);
    }

    /**
     * Handle chart interaction
     */
    handleChartInteraction(interactionData) {
        this.chartManager.handleInteraction(interactionData);
    }

    /**
     * Get dashboard metrics
     */
    getDashboardMetrics() {
        return {
            portfolio: this.portfolioManager.getCurrentPortfolio(),
            marketData: this.websocketManager.getLatestMarketData(),
            orders: this.orderManager.getOrderHistory(),
            isConnected: this.websocketManager.isConnected()
        };
    }
}

/**
 * Factory function for TradingDashboard
 */
export function createTradingDashboard() {
    return new TradingDashboard();
}

/**
 * Default export for backward compatibility
 */
export default TradingDashboard;
