/**
 * Trading Robot Main - V2 Compliant Trading Robot Frontend Entry Point
 * Main entry point for Trading Robot frontend application
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - Trading Robot Frontend V2 Compliance
 * @license MIT
 */

// V2 Compliance: Only import factory functions that are actually used
import { createTradingChartManager } from './trading-chart-manager.js';
import { createTradingDashboard } from './trading-dashboard.js';
import { createTradingOrderManager } from './trading-order-manager.js';
import { createTradingPortfolioManager } from './trading-portfolio-manager.js';
import { createTradingWebSocketManager } from './trading-websocket-manager.js';

import { AppManagementModules } from './app-management-modules.js';

// ================================
// TRADING ROBOT MAIN APPLICATION
// ================================

/**
 * Main Trading Robot Application
 * Orchestrates all trading components and manages application lifecycle
 */
export class TradingRobotApp {
    constructor() {
        this.dashboard = null;
        this.websocketManager = null;
        this.portfolioManager = null;
        this.orderManager = null;
        this.chartManager = null;
        this.isInitialized = false;
        this.appConfig = {
            version: '1.0.0',
            environment: 'development',
            debug: true
        };

        // V2 Compliance: Structured logging without console
        this.logger = {
            log: (message) => {
                const timestamp = new Date().toISOString();
                const logEntry = `[${timestamp}] TRADING-ROBOT: ${message}`;
                if (!this._logs) this._logs = [];
                this._logs.push(logEntry);
                // In development, still log to console for debugging
                if (this.appConfig.debug) console.log(logEntry);
            },
            error: (message, error) => {
                const timestamp = new Date().toISOString();
                const errorEntry = `[${timestamp}] TRADING-ROBOT ERROR: ${message}`;
                if (!this._logs) this._logs = [];
                this._logs.push(errorEntry);
                this._logs.push(`Error details: ${error}`);
                if (this.appConfig.debug) console.error(errorEntry, error);
            }
        };
    }

    /**
     * Initialize Trading Robot application
     */
    async initialize() {
        if (this.isInitialized) {
            this.logger.log('⚠️ Trading Robot already initialized');
            return;
        }

        try {
            this.logger.log('🚀 Initializing Trading Robot Application...');

            // Initialize all components
            await this.initializeComponents();

            // Set up cross-component communication
            this.setupComponentCommunication();

            // Initialize dashboard
            await this.dashboard.initialize();

            // Start application services
            this.startApplicationServices();

            this.isInitialized = true;
            this.logger.log('✅ Trading Robot Application initialized successfully');

            // Dispatch initialization complete event
            AppManagementModules.dispatchEvent('tradingRobot:initialized', {
                version: this.appConfig.version,
                timestamp: new Date()
            });

        } catch (error) {
            this.logger.error('❌ Trading Robot Application initialization failed:', error);
            AppManagementModules.handleInitializationError(error);
            throw error;
        }
    }

    /**
     * Initialize all trading components
     */
    async initializeComponents() {
        // Create component instances
        this.websocketManager = createTradingWebSocketManager();
        this.portfolioManager = createTradingPortfolioManager();
        this.orderManager = createTradingOrderManager();
        this.chartManager = createTradingChartManager();
        this.dashboard = createTradingDashboard();

        // Initialize components using AppManagementModules
        await AppManagementModules.initializeComponents(
            this.websocketManager,
            this.portfolioManager,
            this.orderManager,
            this.chartManager,
            this.dashboard
        );
    }

    /**
     * Setup cross-component communication
     */
    setupComponentCommunication() {
        AppManagementModules.setupComponentCommunication(
            this.websocketManager,
            this.portfolioManager,
            this.orderManager,
            this.chartManager
        );
    }

    /**
     * Start application services
     */
    startApplicationServices() {
        AppManagementModules.startApplicationServices(
            this.websocketManager,
            this.portfolioManager,
            this.orderManager,
            this.chartManager
        );
    }

    /**
     * Handle application errors
     */
    handleError(type, error) {
        AppManagementModules.handleError(type, error);
    }

    /**
     * Get application status
     */
    getApplicationStatus() {
        return AppManagementModules.getApplicationStatus(
            this.websocketManager,
            this.portfolioManager,
            this.orderManager,
            this.chartManager,
            this.dashboard,
            this.isInitialized,
            this.appConfig
        );
    }

    /**
     * Shutdown application
     */
    shutdown() {
        AppManagementModules.shutdown(this.websocketManager);
        this.isInitialized = false;
    }

    // Getters for component access
    getDashboard() { return this.dashboard; }
    getWebSocketManager() { return this.websocketManager; }
    getPortfolioManager() { return this.portfolioManager; }
    getOrderManager() { return this.orderManager; }
    getChartManager() { return this.chartManager; }
    getIsInitialized() { return this.isInitialized; }
    getAppConfig() { return this.appConfig; }

    // Setters for configuration
    setAppConfig(config) { this.appConfig = { ...this.appConfig, ...config }; }
    setEnvironment(env) { this.appConfig.environment = env; }
    setDebugMode(debug) { this.appConfig.debug = debug; }
}

// ================================
// APPLICATION FACTORY FUNCTIONS
// ================================

/**
 * Create Trading Robot Application instance
 */
export function createTradingRobotApp() {
    return new TradingRobotApp();
}

/**
 * Initialize Trading Robot Application
 */
export async function initializeTradingRobot() {
    const app = createTradingRobotApp();
    await app.initialize();
    return app;
}

// ================================
// GLOBAL APPLICATION INSTANCE
// ================================

// Create global application instance
window.tradingRobotApp = null;

/**
 * Initialize global Trading Robot Application
 */
export async function initializeGlobalTradingRobot() {
    if (window.tradingRobotApp) {
        // V2 Compliance: Use console only in development mode
        if (window.tradingRobotApp.appConfig?.debug) {
            console.log('⚠️ Trading Robot already initialized globally');
        }
        return window.tradingRobotApp;
    }

    window.tradingRobotApp = await initializeTradingRobot();
    return window.tradingRobotApp;
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeGlobalTradingRobot);
} else {
    initializeGlobalTradingRobot();
}
