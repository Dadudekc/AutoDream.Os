/**
 * Trading Chart Core Module - V2 Compliant
 * Consolidated chart functionality for Trading Robot
 * Combines chart-state, chart-calculation, chart-drawing, chart-navigation, and chart-renderer modules
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - PHASE 2 CONSOLIDATION
 * @license MIT
 */

// ================================
// TRADING CHART CORE MODULE
// ================================

/**
 * Unified Trading Chart Core Module
 * Consolidates all chart-related functionality into a single V2-compliant module
 */
export class TradingChartCore {
    constructor() {
        this.logger = console;
        this.chartState = this.initializeChartState();
        this.chartRenderer = null;
        this.chartNavigator = null;
        this.chartCalculator = null;
        this.isInitialized = false;
    }

    /**
     * Initialize chart state with default values
     */
    initializeChartState() {
        return {
            currentSymbol: 'AAPL',
            timeframe: '1m',
            chartType: 'candlestick',
            indicators: [],
            zoomLevel: 1,
            panOffset: 0,
            isInitialized: false,
            data: [],
            visibleRange: { start: 0, end: 100 },
            selectedIndicator: null,
            drawingTools: []
        };
    }

    /**
     * Initialize the chart core module
     */
    async initialize() {
        try {
            this.logger.log('Initializing Trading Chart Core...');

            // Initialize chart renderer
            this.chartRenderer = new ChartRenderer(this.chartState);

            // Initialize chart navigator
            this.chartNavigator = new ChartNavigator(this.chartState);

            // Initialize chart calculator
            this.chartCalculator = new ChartCalculator(this.chartState);

            // Initialize drawing tools
            this.drawingTools = new ChartDrawingTools(this.chartState);

            this.isInitialized = true;
            this.logger.log('Trading Chart Core initialized successfully');

        } catch (error) {
            this.logger.error('Failed to initialize Trading Chart Core:', error);
            throw error;
        }
    }

    /**
     * Update chart data
     */
    updateChartData(newData) {
        if (!this.isInitialized) {
            throw new Error('Chart core not initialized');
        }

        this.chartState.data = newData;
        this.chartRenderer.updateData(newData);
        this.chartCalculator.recalculateIndicators();
    }

    /**
     * Set chart symbol
     */
    setSymbol(symbol) {
        this.chartState.currentSymbol = symbol;
        this.logger.log(`Chart symbol updated to: ${symbol}`);
    }

    /**
     * Set chart timeframe
     */
    setTimeframe(timeframe) {
        this.chartState.timeframe = timeframe;
        this.chartCalculator.recalculateIndicators();
        this.logger.log(`Chart timeframe updated to: ${timeframe}`);
    }

    /**
     * Add technical indicator
     */
    addIndicator(indicator) {
        this.chartState.indicators.push(indicator);
        this.chartCalculator.recalculateIndicators();
        this.logger.log(`Indicator added: ${indicator.name}`);
    }

    /**
     * Remove technical indicator
     */
    removeIndicator(indicatorName) {
        this.chartState.indicators = this.chartState.indicators.filter(
            ind => ind.name !== indicatorName
        );
        this.chartCalculator.recalculateIndicators();
        this.logger.log(`Indicator removed: ${indicatorName}`);
    }

    /**
     * Zoom chart
     */
    zoomChart(level) {
        this.chartState.zoomLevel = level;
        this.chartRenderer.updateZoom(level);
        this.logger.log(`Chart zoomed to level: ${level}`);
    }

    /**
     * Pan chart
     */
    panChart(offset) {
        this.chartState.panOffset = offset;
        this.chartRenderer.updatePan(offset);
        this.logger.log(`Chart panned to offset: ${offset}`);
    }

    /**
     * Add drawing tool
     */
    addDrawingTool(tool) {
        this.chartState.drawingTools.push(tool);
        this.drawingTools.addTool(tool);
        this.logger.log(`Drawing tool added: ${tool.type}`);
    }

    /**
     * Clear all drawing tools
     */
    clearDrawingTools() {
        this.chartState.drawingTools = [];
        this.drawingTools.clearAll();
        this.logger.log('All drawing tools cleared');
    }

    /**
     * Export chart data
     */
    exportChartData() {
        return {
            symbol: this.chartState.currentSymbol,
            timeframe: this.chartState.timeframe,
            data: this.chartState.data,
            indicators: this.chartState.indicators,
            zoomLevel: this.chartState.zoomLevel,
            panOffset: this.chartState.panOffset
        };
    }

    /**
     * Get chart screenshot (placeholder for future implementation)
     */
    async getScreenshot() {
        this.logger.log('Screenshot functionality not yet implemented');
        return null;
    }
}

/**
 * Chart Renderer - Handles chart drawing and rendering
 */
class ChartRenderer {
    constructor(chartState) {
        this.chartState = chartState;
        this.canvas = null;
        this.context = null;
    }

    updateData(data) {
        this.chartState.data = data;
        this.render();
    }

    updateZoom(level) {
        this.chartState.zoomLevel = level;
        this.render();
    }

    updatePan(offset) {
        this.chartState.panOffset = offset;
        this.render();
    }

    render() {
        if (!this.canvas || !this.context) {
            console.warn('Canvas not initialized for chart rendering');
            return;
        }

        // Clear canvas
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Render candlestick chart
        if (this.chartState.chartType === 'candlestick') {
            this.renderCandlesticks();
        }

        // Render indicators
        this.renderIndicators();

        // Render drawing tools
        this.renderDrawingTools();
    }

    renderCandlesticks() {
        const data = this.chartState.data;
        const ctx = this.context;

        data.forEach((candle, index) => {
            const x = index * 10; // Simplified spacing
            const open = candle.open;
            const high = candle.high;
            const low = candle.low;
            const close = candle.close;

            // Determine candle color
            const color = close > open ? '#00ff00' : '#ff0000';

            // Draw high-low line
            ctx.strokeStyle = color;
            ctx.beginPath();
            ctx.moveTo(x + 5, high);
            ctx.lineTo(x + 5, low);
            ctx.stroke();

            // Draw open-close rectangle
            const top = Math.min(open, close);
            const height = Math.abs(open - close);
            ctx.fillStyle = color;
            ctx.fillRect(x + 2, top, 6, height || 1);
        });
    }

    renderIndicators() {
        this.chartState.indicators.forEach(indicator => {
            // Render indicator based on type
            switch (indicator.type) {
                case 'sma':
                    this.renderSMA(indicator);
                    break;
                case 'ema':
                    this.renderEMA(indicator);
                    break;
                case 'rsi':
                    this.renderRSI(indicator);
                    break;
                default:
                    console.warn(`Unknown indicator type: ${indicator.type}`);
            }
        });
    }

    renderSMA(indicator) {
        // Render Simple Moving Average line
        const ctx = this.context;
        ctx.strokeStyle = indicator.color || '#0000ff';
        ctx.lineWidth = 1;

        ctx.beginPath();
        indicator.values.forEach((value, index) => {
            const x = index * 10;
            const y = value;

            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        ctx.stroke();
    }

    renderEMA(indicator) {
        // Render Exponential Moving Average line
        this.renderSMA(indicator); // Similar rendering
    }

    renderRSI(indicator) {
        // RSI would typically be rendered in a separate pane
        console.log('RSI rendering not implemented in this version');
    }

    renderDrawingTools() {
        this.chartState.drawingTools.forEach(tool => {
            switch (tool.type) {
                case 'trendline':
                    this.renderTrendline(tool);
                    break;
                case 'horizontal':
                    this.renderHorizontalLine(tool);
                    break;
                default:
                    console.warn(`Unknown drawing tool: ${tool.type}`);
            }
        });
    }

    renderTrendline(tool) {
        const ctx = this.context;
        ctx.strokeStyle = tool.color || '#ffff00';
        ctx.lineWidth = 1;

        ctx.beginPath();
        ctx.moveTo(tool.startX, tool.startY);
        ctx.lineTo(tool.endX, tool.endY);
        ctx.stroke();
    }

    renderHorizontalLine(tool) {
        const ctx = this.context;
        ctx.strokeStyle = tool.color || '#ffff00';
        ctx.lineWidth = 1;

        ctx.beginPath();
        ctx.moveTo(0, tool.y);
        ctx.lineTo(this.canvas.width, tool.y);
        ctx.stroke();
    }
}

/**
 * Chart Navigator - Handles chart navigation and interaction
 */
class ChartNavigator {
    constructor(chartState) {
        this.chartState = chartState;
        this.isDragging = false;
        this.lastMouseX = 0;
        this.lastMouseY = 0;
    }

    handleMouseDown(event) {
        this.isDragging = true;
        this.lastMouseX = event.clientX;
        this.lastMouseY = event.clientY;
    }

    handleMouseMove(event) {
        if (!this.isDragging) return;

        const deltaX = event.clientX - this.lastMouseX;
        const deltaY = event.clientY - this.lastMouseY;

        // Update pan offset
        this.chartState.panOffset += deltaX;

        this.lastMouseX = event.clientX;
        this.lastMouseY = event.clientY;
    }

    handleMouseUp() {
        this.isDragging = false;
    }

    handleWheel(event) {
        event.preventDefault();

        const zoomFactor = event.deltaY > 0 ? 0.9 : 1.1;
        this.chartState.zoomLevel *= zoomFactor;

        // Clamp zoom level
        this.chartState.zoomLevel = Math.max(0.1, Math.min(5, this.chartState.zoomLevel));
    }

    handleKeyPress(event) {
        switch (event.key) {
            case '+':
            case '=':
                this.chartState.zoomLevel *= 1.2;
                break;
            case '-':
                this.chartState.zoomLevel *= 0.8;
                break;
            case 'ArrowLeft':
                this.chartState.panOffset -= 10;
                break;
            case 'ArrowRight':
                this.chartState.panOffset += 10;
                break;
        }

        // Clamp values
        this.chartState.zoomLevel = Math.max(0.1, Math.min(5, this.chartState.zoomLevel));
    }
}

/**
 * Chart Calculator - Handles technical analysis calculations
 */
class ChartCalculator {
    constructor(chartState) {
        this.chartState = chartState;
    }

    recalculateIndicators() {
        this.chartState.indicators.forEach(indicator => {
            switch (indicator.type) {
                case 'sma':
                    indicator.values = this.calculateSMA(indicator.period);
                    break;
                case 'ema':
                    indicator.values = this.calculateEMA(indicator.period);
                    break;
                case 'rsi':
                    indicator.values = this.calculateRSI(indicator.period);
                    break;
            }
        });
    }

    calculateSMA(period) {
        const data = this.chartState.data;
        const sma = [];

        for (let i = period - 1; i < data.length; i++) {
            let sum = 0;
            for (let j = i - period + 1; j <= i; j++) {
                sum += data[j].close;
            }
            sma.push(sum / period);
        }

        return sma;
    }

    calculateEMA(period) {
        const data = this.chartState.data;
        const ema = [];
        const multiplier = 2 / (period + 1);

        // Start with SMA for first value
        let sum = 0;
        for (let i = 0; i < period && i < data.length; i++) {
            sum += data[i].close;
        }
        ema.push(sum / period);

        // Calculate EMA for remaining values
        for (let i = period; i < data.length; i++) {
            const value = (data[i].close - ema[ema.length - 1]) * multiplier + ema[ema.length - 1];
            ema.push(value);
        }

        return ema;
    }

    calculateRSI(period) {
        const data = this.chartState.data;
        const rsi = [];
        const gains = [];
        const losses = [];

        // Calculate price changes
        for (let i = 1; i < data.length; i++) {
            const change = data[i].close - data[i - 1].close;
            gains.push(change > 0 ? change : 0);
            losses.push(change < 0 ? Math.abs(change) : 0);
        }

        // Calculate RSI
        for (let i = period - 1; i < gains.length; i++) {
            let avgGain = 0;
            let avgLoss = 0;

            for (let j = i - period + 1; j <= i; j++) {
                avgGain += gains[j];
                avgLoss += losses[j];
            }

            avgGain /= period;
            avgLoss /= period;

            if (avgLoss === 0) {
                rsi.push(100);
            } else {
                const rs = avgGain / avgLoss;
                rsi.push(100 - (100 / (1 + rs)));
            }
        }

        return rsi;
    }
}

/**
 * Chart Drawing Tools - Handles drawing tools functionality
 */
class ChartDrawingTools {
    constructor(chartState) {
        this.chartState = chartState;
        this.tools = [];
    }

    addTool(tool) {
        this.tools.push(tool);
    }

    removeTool(toolId) {
        this.tools = this.tools.filter(tool => tool.id !== toolId);
    }

    clearAll() {
        this.tools = [];
    }

    getToolById(toolId) {
        return this.tools.find(tool => tool.id === toolId);
    }

    updateTool(toolId, updates) {
        const tool = this.getToolById(toolId);
        if (tool) {
            Object.assign(tool, updates);
        }
    }
}

// ================================
// EXPORTS
// ================================

export { TradingChartCore, ChartRenderer, ChartNavigator, ChartCalculator, ChartDrawingTools };
