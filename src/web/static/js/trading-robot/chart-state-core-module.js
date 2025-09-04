/**
 * Chart State Core Module - V2 Compliant
 * Core chart state management functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// CHART STATE CORE MODULE
// ================================

/**
 * Core chart state management functionality
 */
export class ChartStateCoreModule {
    constructor() {
        this.logger = console;
        this.state = {
            currentSymbol: 'AAPL',
            timeframe: '1m',
            chartType: 'candlestick',
            indicators: [],
            zoomLevel: 1,
            panOffset: 0,
            isInitialized: false
        };
    }

    /**
     * Initialize state module
     */
    initialize() {
        this.state.isInitialized = true;
        this.logger.log('📊 Chart state core module initialized');
    }

    /**
     * Update state property
     */
    updateState(property, value) {
        try {
            const oldValue = this.state[property];
            this.state[property] = value;
            return true;
        } catch (error) {
            this.logger.error(`Failed to update state property ${property}:`, error);
            return false;
        }
    }

    /**
     * Get state property
     */
    getState(property) {
        if (property) {
            return this.state[property];
        }
        return { ...this.state };
    }

    /**
     * Set multiple state properties
     */
    setState(newState) {
        try {
            Object.assign(this.state, newState);
            return true;
        } catch (error) {
            this.logger.error('Failed to set state:', error);
            return false;
        }
    }

    /**
     * Reset state to defaults
     */
    resetState() {
        try {
            this.state = {
                currentSymbol: 'AAPL',
                timeframe: '1m',
                chartType: 'candlestick',
                indicators: [],
                zoomLevel: 1,
                panOffset: 0,
                isInitialized: true
            };
            this.logger.log('🔄 Chart state reset to defaults');
            return true;
        } catch (error) {
            this.logger.error('Failed to reset state:', error);
            return false;
        }
    }

    /**
     * Get state summary
     */
    getStateSummary() {
        return {
            isInitialized: this.state.isInitialized,
            symbol: this.state.currentSymbol,
            timeframe: this.state.timeframe,
            chartType: this.state.chartType,
            activeIndicators: this.state.indicators.length,
            zoomLevel: this.state.zoomLevel
        };
    }

    /**
     * Validate state integrity
     */
    validateStateIntegrity() {
        try {
            const required = ['currentSymbol', 'timeframe', 'chartType', 'indicators'];
            for (const prop of required) {
                if (!(prop in this.state)) {
                    return { valid: false, error: `Missing required property: ${prop}` };
                }
            }

            if (!Array.isArray(this.state.indicators)) {
                return { valid: false, error: 'Indicators must be an array' };
            }

            if (typeof this.state.zoomLevel !== 'number' || this.state.zoomLevel <= 0) {
                return { valid: false, error: 'Zoom level must be a positive number' };
            }

            return { valid: true };
        } catch (error) {
            return { valid: false, error: error.message };
        }
    }

    // Convenience getters
    getChartData() { return this.state.chartData || []; }
    setChartData(data) { return this.updateState('chartData', data); }
    getCurrentSymbol() { return this.state.currentSymbol; }
    setCurrentSymbol(symbol) { return this.updateState('currentSymbol', symbol); }
    getCurrentTimeframe() { return this.state.timeframe; }
    setCurrentTimeframe(timeframe) { return this.updateState('timeframe', timeframe); }
    getActiveIndicators() { return [...this.state.indicators]; }
    setActiveIndicators(indicators) { return this.updateState('indicators', [...indicators]); }

    /**
     * Cleanup state module
     */
    cleanup() {
        try {
            this.resetState();
            this.state.isInitialized = false;
            this.logger.log('🧹 Chart state core cleanup complete');
            return true;
        } catch (error) {
            this.logger.error('Failed to cleanup state module:', error);
            return false;
        }
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create chart state core module instance
 */
export function createChartStateCoreModule() {
    return new ChartStateCoreModule();
}

