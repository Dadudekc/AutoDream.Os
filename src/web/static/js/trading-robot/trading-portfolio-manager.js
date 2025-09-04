/**
 * Trading Portfolio Manager - V2 Compliant Portfolio Management
 * Portfolio tracking, position management, and risk calculations
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - Trading Robot Frontend V2 Compliance
 * @license MIT
 */

import { PortfolioManagementModules } from './portfolio-management-modules.js';

// ================================
// TRADING PORTFOLIO MANAGER
// ================================

/**
 * Portfolio Manager for trading positions and risk management
 * Handles portfolio tracking, position management, and risk calculations
 */
export class TradingPortfolioManager {
    constructor() {
        this.portfolio = {
            totalValue: 0,
            cash: 0,
            positions: [],
            pnl: 0,
            pnlPercent: 0,
            lastUpdated: null
        };
        this.portfolioCallbacks = [];
        this.riskLimits = {
            maxPositionSize: 0.1, // 10% of portfolio
            maxDrawdown: 0.05,    // 5% max drawdown
            stopLoss: 0.02        // 2% stop loss
        };
    }

    /**
     * Initialize portfolio manager
     */
    async initialize() {
        try {
            console.log('💼 Initializing Trading Portfolio Manager...');
            await this.loadPortfolio();
            this.startPortfolioUpdates();
            console.log('✅ Trading Portfolio Manager initialized');
        } catch (error) {
            console.error('❌ Trading Portfolio Manager initialization failed:', error);
            throw error;
        }
    }

    /**
     * Load portfolio data
     */
    async loadPortfolio() {
        try {
            this.portfolio = PortfolioManagementModules.loadSamplePortfolio();
            PortfolioManagementModules.calculatePortfolioMetrics(this.portfolio);
        } catch (error) {
            console.error('❌ Error loading portfolio:', error);
            throw error;
        }
    }

    /**
     * Start portfolio updates
     */
    startPortfolioUpdates() {
        PortfolioManagementModules.startPortfolioUpdates(this.portfolio, (updatedPortfolio) => {
            this.notifyPortfolioCallbacks(updatedPortfolio);
        });
    }

    /**
     * Update portfolio from order
     */
    updatePortfolioFromOrder(order) {
        PortfolioManagementModules.updatePositionFromOrder(this.portfolio, order);
        this.notifyPortfolioCallbacks(this.portfolio);
    }

    /**
     * Update portfolio with price data
     */
    updatePortfolio(priceData) {
        PortfolioManagementModules.updatePositionPrices(this.portfolio, priceData);
        this.notifyPortfolioCallbacks(this.portfolio);
    }

    /**
     * Check risk limits
     */
    checkRiskLimits() {
        return PortfolioManagementModules.checkRiskLimits(this.portfolio, this.riskLimits);
    }

    /**
     * Get current portfolio
     */
    getCurrentPortfolio() {
        return { ...this.portfolio };
    }

    /**
     * Get portfolio positions
     */
    getPositions() {
        return [...this.portfolio.positions];
    }

    /**
     * Get position by symbol
     */
    getPosition(symbol) {
        return this.portfolio.positions.find(p => p.symbol === symbol);
    }

    /**
     * Get portfolio value
     */
    getPortfolioValue() {
        return this.portfolio.totalValue;
    }

    /**
     * Get cash balance
     */
    getCashBalance() {
        return this.portfolio.cash;
    }

    /**
     * Get portfolio P&L
     */
    getPortfolioPnL() {
        return {
            pnl: this.portfolio.pnl,
            pnlPercent: this.portfolio.pnlPercent
        };
    }

    /**
     * Generate portfolio report
     */
    generatePortfolioReport() {
        return PortfolioManagementModules.generatePortfolioReport(this.portfolio);
    }

    /**
     * Add portfolio callback
     */
    addCallback(callback) {
        this.portfolioCallbacks.push(callback);
    }

    /**
     * Remove portfolio callback
     */
    removeCallback(callback) {
        const index = this.portfolioCallbacks.indexOf(callback);
        if (index > -1) {
            this.portfolioCallbacks.splice(index, 1);
        }
    }

    /**
     * Notify portfolio callbacks
     */
    notifyPortfolioCallbacks(portfolio) {
        this.portfolioCallbacks.forEach(callback => {
            try {
                callback(portfolio);
            } catch (error) {
                console.error('❌ Error in portfolio callback:', error);
            }
        });
    }

    /**
     * Set risk limits
     */
    setRiskLimits(limits) {
        this.riskLimits = { ...this.riskLimits, ...limits };
    }

    /**
     * Get risk limits
     */
    getRiskLimits() {
        return { ...this.riskLimits };
    }

    /**
     * Export portfolio data
     */
    exportPortfolioData() {
        PortfolioManagementModules.exportPortfolioData(this.portfolio);
    }

    /**
     * Import portfolio data
     */
    async importPortfolioData(file) {
        try {
            this.portfolio = await PortfolioManagementModules.importPortfolioData(file);
            this.notifyPortfolioCallbacks(this.portfolio);
            console.log('✅ Portfolio data imported successfully');
        } catch (error) {
            console.error('❌ Error importing portfolio data:', error);
            throw error;
        }
    }

    /**
     * Clear portfolio
     */
    clearPortfolio() {
        this.portfolio = {
            totalValue: 0,
            cash: 0,
            positions: [],
            pnl: 0,
            pnlPercent: 0,
            lastUpdated: new Date()
        };
        this.notifyPortfolioCallbacks(this.portfolio);
    }

    /**
     * Check if portfolio is healthy
     */
    isHealthy() {
        const violations = this.checkRiskLimits();
        return violations.length === 0;
    }

    /**
     * Get portfolio statistics
     */
    getPortfolioStatistics() {
        const stats = {
            totalValue: this.portfolio.totalValue,
            cash: this.portfolio.cash,
            investedValue: this.portfolio.totalValue - this.portfolio.cash,
            positionCount: this.portfolio.positions.length,
            pnl: this.portfolio.pnl,
            pnlPercent: this.portfolio.pnlPercent,
            lastUpdated: this.portfolio.lastUpdated
        };

        return stats;
    }

    /**
     * Destroy portfolio manager
     */
    destroy() {
        this.portfolioCallbacks = [];
        this.portfolio = {
            totalValue: 0,
            cash: 0,
            positions: [],
            pnl: 0,
            pnlPercent: 0,
            lastUpdated: null
        };
    }
}

// ================================
// PORTFOLIO MANAGER FACTORY
// ================================

/**
 * Create Trading Portfolio Manager instance
 */
export function createTradingPortfolioManager() {
    return new TradingPortfolioManager();
}