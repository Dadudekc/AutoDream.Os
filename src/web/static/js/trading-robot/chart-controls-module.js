/**
 * Chart Controls Module - V2 Compliant
 * Chart controls and UI setup functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// CHART CONTROLS MODULE
// ================================

/**
 * Chart controls and UI setup functionality
 */
export class ChartControlsModule {
    constructor() {
        this.logger = console;
        this.chartType = 'candlestick';
        this.indicators = [];
        this.controls = {};
    }

    /**
     * Create chart controls UI
     */
    createChartControls() {
        const chartContainer = document.getElementById('trading-chart');
        if (!chartContainer) {
            this.logger.warn('Chart container not found');
            return false;
        }

        chartContainer.innerHTML = `
            <div class="chart-container">
                <div class="chart-controls">
                    <select id="chart-symbol" class="chart-control">
                        <option value="AAPL">AAPL</option>
                        <option value="GOOGL">GOOGL</option>
                        <option value="MSFT">MSFT</option>
                        <option value="TSLA">TSLA</option>
                    </select>
                    <select id="chart-timeframe" class="chart-control">
                        <option value="1m">1 Minute</option>
                        <option value="5m">5 Minutes</option>
                        <option value="15m">15 Minutes</option>
                        <option value="1h">1 Hour</option>
                        <option value="1d">1 Day</option>
                    </select>
                    <select id="chart-type" class="chart-control">
                        <option value="candlestick">Candlestick</option>
                        <option value="line">Line</option>
                        <option value="bar">Bar</option>
                    </select>
                </div>
                <div class="chart-canvas-container">
                    <canvas id="price-chart" width="800" height="400"></canvas>
                </div>
                <div class="chart-indicators">
                    <button class="indicator-btn" data-indicator="sma">SMA</button>
                    <button class="indicator-btn" data-indicator="ema">EMA</button>
                    <button class="indicator-btn" data-indicator="rsi">RSI</button>
                    <button class="indicator-btn" data-indicator="macd">MACD</button>
                </div>
            </div>
        `;

        this.initializeControls();
        return true;
    }

    /**
     * Initialize controls
     */
    initializeControls() {
        // Store control references
        this.controls.symbol = document.getElementById('chart-symbol');
        this.controls.timeframe = document.getElementById('chart-timeframe');
        this.controls.type = document.getElementById('chart-type');

        // Set initial values
        if (this.controls.symbol) this.controls.symbol.value = 'AAPL';
        if (this.controls.timeframe) this.controls.timeframe.value = '1m';
        if (this.controls.type) this.controls.type.value = this.chartType;
    }

    /**
     * Setup chart controls event handlers
     */
    setupEventHandlers(callbacks) {
        try {
            // Symbol change handler
            if (this.controls.symbol) {
                this.controls.symbol.addEventListener('change', (e) => {
                    if (callbacks.onSymbolChange) {
                        callbacks.onSymbolChange(e.target.value);
                    }
                });
            }

            // Timeframe change handler
            if (this.controls.timeframe) {
                this.controls.timeframe.addEventListener('change', (e) => {
                    if (callbacks.onTimeframeChange) {
                        callbacks.onTimeframeChange(e.target.value);
                    }
                });
            }

            // Chart type change handler
            if (this.controls.type) {
                this.controls.type.addEventListener('change', (e) => {
                    this.chartType = e.target.value;
                    if (callbacks.onChartTypeChange) {
                        callbacks.onChartTypeChange(e.target.value);
                    }
                });
            }

            // Indicator buttons
            const indicatorButtons = document.querySelectorAll('.indicator-btn');
            indicatorButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    const indicator = e.target.dataset.indicator;
                    this.toggleIndicator(indicator);
                    if (callbacks.onIndicatorToggle) {
                        callbacks.onIndicatorToggle(indicator);
                    }
                });
            });

            this.logger.log('🎛️ Chart controls event handlers setup complete');
        } catch (error) {
            this.logger.error('Failed to setup chart controls event handlers:', error);
        }
    }

    /**
     * Toggle indicator
     */
    toggleIndicator(indicator) {
        const index = this.indicators.indexOf(indicator);
        if (index > -1) {
            this.indicators.splice(index, 1);
        } else {
            this.indicators.push(indicator);
        }

        // Update button visual state
        const button = document.querySelector(`[data-indicator="${indicator}"]`);
        if (button) {
            button.classList.toggle('active', this.indicators.includes(indicator));
        }

        return this.indicators;
    }

    /**
     * Get current control values
     */
    getControlValues() {
        return {
            symbol: this.controls.symbol?.value || 'AAPL',
            timeframe: this.controls.timeframe?.value || '1m',
            chartType: this.controls.type?.value || 'candlestick',
            indicators: [...this.indicators]
        };
    }

    /**
     * Set control values
     */
    setControlValues(values) {
        try {
            if (values.symbol && this.controls.symbol) {
                this.controls.symbol.value = values.symbol;
            }
            if (values.timeframe && this.controls.timeframe) {
                this.controls.timeframe.value = values.timeframe;
            }
            if (values.chartType && this.controls.type) {
                this.controls.type.value = values.chartType;
                this.chartType = values.chartType;
            }
            if (values.indicators) {
                this.indicators = [...values.indicators];
                // Update button states
                this.updateIndicatorButtons();
            }
        } catch (error) {
            this.logger.error('Failed to set control values:', error);
        }
    }

    /**
     * Update indicator button states
     */
    updateIndicatorButtons() {
        this.indicators.forEach(indicator => {
            const button = document.querySelector(`[data-indicator="${indicator}"]`);
            if (button) {
                button.classList.add('active');
            }
        });
    }

    /**
     * Enable/disable controls
     */
    setControlsEnabled(enabled) {
        try {
            const controls = document.querySelectorAll('.chart-control, .indicator-btn');
            controls.forEach(control => {
                control.disabled = !enabled;
                control.style.opacity = enabled ? '1' : '0.5';
            });
        } catch (error) {
            this.logger.error('Failed to set controls enabled state:', error);
        }
    }

    /**
     * Reset controls to default values
     */
    resetControls() {
        try {
            if (this.controls.symbol) this.controls.symbol.value = 'AAPL';
            if (this.controls.timeframe) this.controls.timeframe.value = '1m';
            if (this.controls.type) this.controls.type.value = 'candlestick';
            this.chartType = 'candlestick';
            this.indicators = [];
            this.updateIndicatorButtons();
        } catch (error) {
            this.logger.error('Failed to reset controls:', error);
        }
    }

    /**
     * Get active indicators
     */
    getActiveIndicators() {
        return [...this.indicators];
    }

    /**
     * Set active indicators
     */
    setActiveIndicators(indicators) {
        this.indicators = [...indicators];
        this.updateIndicatorButtons();
    }

    /**
     * Get chart type
     */
    getChartType() {
        return this.chartType;
    }

    /**
     * Set chart type
     */
    setChartType(chartType) {
        this.chartType = chartType;
        if (this.controls.type) {
            this.controls.type.value = chartType;
        }
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create chart controls module instance
 */
export function createChartControlsModule() {
    return new ChartControlsModule();
}
