/**
 * Trading Chart Simplified - V2 Compliant
 * Simplified orchestrator for trading chart management
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE SIMPLIFICATION
 * @license MIT
 */

import { createUnifiedLoggingSystem } from './unified-logging-module.js';
import { createChartDataModule } from './chart-data-module.js';
import { createChartControlsModule } from './chart-controls-module.js';
import { createChartNavigationModule } from './chart-navigation-module.js';
import { createChartStateModule } from './chart-state-module.js';

// ================================
// TRADING CHART SIMPLIFIED ORCHESTRATOR
// ================================

/**
 * Simplified orchestrator for trading chart management
 */
export class TradingChartSimplified {
    constructor() {
        // Initialize unified logging
        this.logger = createUnifiedLoggingSystem("TradingChartSimplified");

        // Log unified systems deployment
        this.logger.logUnifiedSystemsDeployment('trading_chart_simplified', 'active', {
            version: '2.0.0',
            agentId: 'Agent-7',
            integrationStatus: 'ACTIVE'
        });

        // Initialize modules
        this.dataModule = createChartDataModule();
        this.controlsModule = createChartControlsModule();
        this.navigationModule = createChartNavigationModule();
        this.stateModule = createChartStateModule();
    }

    /**
     * Initialize simplified trading chart orchestrator
     */
    async initialize() {
        this.logger.logOperationStart('tradingChartSimplifiedInitialization');

        // Initialize state module
        this.stateModule.initialize();

        // Load chart library (placeholder)
        await this.loadChartLibrary();

        // Create chart UI
        this.controlsModule.createChartControls();

        // Setup controls and navigation
        this.setupChartControls();
        this.setupNavigation();

        // Load initial data
        await this.dataModule.loadInitialData();

        // Render initial chart
        this.renderChart();

        this.logger.logOperationComplete('tradingChartSimplifiedInitialization', {
            modules: ['data', 'controls', 'navigation', 'state'],
            unifiedLogging: true
        });
    }

    /**
     * Load chart library
     */
    async loadChartLibrary() {
        return new Promise((resolve) => {
            setTimeout(() => {
                this.logger.log('📚 Chart library loaded');
                resolve();
            }, 100);
        });
    }

    /**
     * Setup chart controls
     */
    setupChartControls() {
        this.controlsModule.setupEventHandlers({
            onSymbolChange: (symbol) => this.handleSymbolChange(symbol),
            onTimeframeChange: (timeframe) => this.handleTimeframeChange(timeframe),
            onChartTypeChange: (chartType) => this.handleChartTypeChange(chartType),
            onIndicatorToggle: (indicator) => this.handleIndicatorToggle(indicator)
        });
    }

    /**
     * Setup navigation
     */
    setupNavigation() {
        const canvas = document.getElementById('price-chart');
        if (canvas) {
            this.navigationModule.initialize(canvas, {
                onZoom: (zoomLevel) => this.handleZoom(zoomLevel),
                onPan: (panOffset) => this.handlePan(panOffset),
                onReset: () => this.handleReset(),
                onResize: (width, height) => this.handleResize(width, height),
                onFullscreenToggle: (isFullscreen) => this.handleFullscreenToggle(isFullscreen),
                onCrosshairMove: (x, y) => this.handleCrosshairMove(x, y)
            });
        }
    }

    /**
     * Render chart
     */
    renderChart() {
        const canvas = document.getElementById('price-chart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Render chart data (simplified placeholder)
        const data = this.dataModule.getChartData();
        this.renderChartData(ctx, canvas.width, canvas.height, data);
    }

    /**
     * Render chart data (simplified)
     */
    renderChartData(ctx, width, height, data) {
        if (!data || data.length === 0) return;

        ctx.strokeStyle = '#2563eb';
        ctx.lineWidth = 2;
        ctx.beginPath();

        const maxPrice = Math.max(...data.map(d => d.high));
        const minPrice = Math.min(...data.map(d => d.low));
        const priceRange = maxPrice - minPrice;
        const barWidth = width / data.length;

        data.forEach((point, index) => {
            const x = index * barWidth;
            const y = ((maxPrice - point.close) / priceRange) * height;

            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });

        ctx.stroke();
    }

    // ================================
    // EVENT HANDLERS
    // ================================

    async handleSymbolChange(symbol) {
        this.dataModule.setCurrentSymbol(symbol);
        this.stateModule.updateState('currentSymbol', symbol);
        await this.dataModule.loadChartData();
        this.renderChart();
    }

    async handleTimeframeChange(timeframe) {
        this.dataModule.setTimeframe(timeframe);
        this.stateModule.updateState('timeframe', timeframe);
        await this.dataModule.loadChartData();
        this.renderChart();
    }

    handleChartTypeChange(chartType) {
        this.controlsModule.setChartType(chartType);
        this.stateModule.updateState('chartType', chartType);
        this.renderChart();
    }

    handleIndicatorToggle(indicator) {
        this.controlsModule.toggleIndicator(indicator);
        this.stateModule.updateState('indicators', this.controlsModule.getActiveIndicators());
        this.renderChart();
    }

    handleZoom(zoomLevel) {
        this.stateModule.updateState('zoomLevel', zoomLevel);
        this.renderChart();
    }

    handlePan(panOffset) {
        this.stateModule.updateState('panOffset', panOffset);
        this.renderChart();
    }

    handleReset() {
        this.navigationModule.resetChart();
        this.controlsModule.resetControls();
        this.stateModule.resetState();
        this.renderChart();
    }

    handleResize(width, height) {
        this.renderChart();
    }

    handleFullscreenToggle(isFullscreen) {
        this.logger.log(`🔳 Fullscreen ${isFullscreen ? 'enabled' : 'disabled'}`);
    }

    handleCrosshairMove(x, y) {
        this.logger.log(`Crosshair at (${x}, ${y})`);
    }

    // ================================
    // PUBLIC API METHODS
    // ================================

    getChartData() {
        return this.dataModule.getChartData();
    }

    setChartData(data) {
        this.dataModule.chartData = data;
        this.stateModule.updateState('chartData', data);
        this.renderChart();
    }

    getCurrentSymbol() {
        return this.dataModule.getCurrentSymbol();
    }

    async setCurrentSymbol(symbol) {
        await this.handleSymbolChange(symbol);
    }

    getCurrentTimeframe() {
        return this.dataModule.getTimeframe();
    }

    async setCurrentTimeframe(timeframe) {
        await this.handleTimeframeChange(timeframe);
    }

    getActiveIndicators() {
        return this.controlsModule.getActiveIndicators();
    }

    setActiveIndicators(indicators) {
        this.controlsModule.setActiveIndicators(indicators);
        this.stateModule.updateState('indicators', indicators);
    }

    // ================================
    // STATUS METHODS
    // ================================

    getStatus() {
        return {
            initialized: true,
            symbol: this.dataModule.getCurrentSymbol(),
            timeframe: this.dataModule.getTimeframe(),
            chartType: this.controlsModule.getChartType(),
            activeIndicators: this.controlsModule.getActiveIndicators().length,
            dataPoints: this.dataModule.getChartData().length,
            zoomLevel: this.navigationModule.getZoomLevel(),
            callbacks: this.stateModule.getAllCallbacks().length
        };
    }

    getComprehensiveStatistics() {
        return {
            status: this.getStatus(),
            dataStats: this.dataModule.getDataStatistics(),
            navigationState: this.navigationModule.getNavigationState(),
            stateSummary: this.stateModule.getStateSummary(),
            loggerStats: this.logger.getStatistics(),
            timestamp: new Date().toISOString()
        };
    }

    // ================================
    // CLEANUP
    // ================================

    cleanup() {
        this.navigationModule.cleanup();
        this.stateModule.cleanup();
        this.dataModule.clearChartData();
        this.logger.cleanup();
        this.logger.log('💥 Trading Chart Simplified cleanup complete');
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Legacy TradingChartOrchestrator class for backward compatibility
 * @deprecated Use TradingChartSimplified instead
 */
export class TradingChartOrchestrator extends TradingChartSimplified {
    constructor() {
        super();
        console.warn('[DEPRECATED] TradingChartOrchestrator is deprecated. Use TradingChartSimplified instead.');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create simplified trading chart instance
 */
export function createTradingChartSimplified() {
    return new TradingChartSimplified();
}

/**
 * Create legacy orchestrator (backward compatibility)
 */
export function createTradingChartOrchestrator() {
    return new TradingChartOrchestrator();
}

