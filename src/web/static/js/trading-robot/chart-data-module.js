/**
 * Chart Data Module - V2 Compliant
 * Chart data management and sample data generation
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// CHART DATA MODULE
// ================================

/**
 * Chart data management and sample data generation
 */
export class ChartDataModule {
    constructor() {
        this.logger = console;
        this.chartData = [];
        this.currentSymbol = 'AAPL';
        this.timeframe = '1m';
    }

    /**
     * Load initial chart data
     */
    async loadInitialData() {
        try {
            this.logger.log('📈 Loading initial chart data...');
            this.chartData = await this.generateSampleData();
            this.logger.log('✅ Initial data loaded');
            return this.chartData;
        } catch (error) {
            this.logger.error('❌ Failed to load initial data:', error);
            throw error;
        }
    }

    /**
     * Load chart data for current symbol and timeframe
     */
    async loadChartData() {
        try {
            this.logger.log(`📊 Loading data for ${this.currentSymbol} (${this.timeframe})`);
            this.chartData = await this.generateSampleData();
            return this.chartData;
        } catch (error) {
            this.logger.error('❌ Failed to load chart data:', error);
            throw error;
        }
    }

    /**
     * Generate sample trading data
     */
    async generateSampleData() {
        const data = [];
        const basePrice = 150;
        let currentPrice = basePrice;
        const now = new Date();

        for (let i = 0; i < 100; i++) {
            const timestamp = new Date(now.getTime() - (99 - i) * 60000);
            const change = (Math.random() - 0.5) * 0.02 * currentPrice;
            currentPrice += change;

            data.push({
                timestamp: timestamp.toISOString(),
                open: i === 0 ? currentPrice : data[i - 1].close,
                high: currentPrice + Math.random() * 2,
                low: currentPrice - Math.random() * 2,
                close: currentPrice,
                volume: Math.floor(Math.random() * 1000000) + 100000
            });
        }

        return data;
    }

    /**
     * Update chart data with new price point
     */
    updateChartData(newPricePoint) {
        try {
            if (this.chartData.length >= 100) {
                this.chartData.shift(); // Remove oldest data point
            }
            this.chartData.push(newPricePoint);
            return this.chartData;
        } catch (error) {
            this.logger.error('Failed to update chart data:', error);
            return this.chartData;
        }
    }

    /**
     * Get chart data in specified format
     */
    getChartData(format = 'default') {
        switch (format) {
            case 'ohlc':
                return this.chartData.map(d => [d.timestamp, d.open, d.high, d.low, d.close]);
            case 'close':
                return this.chartData.map(d => [d.timestamp, d.close]);
            case 'volume':
                return this.chartData.map(d => [d.timestamp, d.volume]);
            default:
                return this.chartData;
        }
    }

    /**
     * Set current symbol
     */
    setCurrentSymbol(symbol) {
        this.currentSymbol = symbol;
    }

    /**
     * Get current symbol
     */
    getCurrentSymbol() {
        return this.currentSymbol;
    }

    /**
     * Set timeframe
     */
    setTimeframe(timeframe) {
        this.timeframe = timeframe;
    }

    /**
     * Get timeframe
     */
    getTimeframe() {
        return this.timeframe;
    }

    /**
     * Clear chart data
     */
    clearChartData() {
        this.chartData = [];
    }

    /**
     * Get data statistics
     */
    getDataStatistics() {
        if (this.chartData.length === 0) {
            return { count: 0, min: 0, max: 0, average: 0 };
        }

        const prices = this.chartData.map(d => d.close);
        const min = Math.min(...prices);
        const max = Math.max(...prices);
        const average = prices.reduce((sum, price) => sum + price, 0) / prices.length;

        return {
            count: this.chartData.length,
            min: min,
            max: max,
            average: average,
            range: max - min
        };
    }

    /**
     * Validate data integrity
     */
    validateDataIntegrity() {
        if (!Array.isArray(this.chartData)) {
            return { valid: false, error: 'Data is not an array' };
        }

        for (let i = 0; i < this.chartData.length; i++) {
            const point = this.chartData[i];

            if (!point.timestamp || !point.open || !point.high || !point.low || !point.close) {
                return { valid: false, error: `Invalid data point at index ${i}` };
            }

            if (point.low > point.high) {
                return { valid: false, error: `Invalid price range at index ${i}` };
            }
        }

        return { valid: true };
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create chart data module instance
 */
export function createChartDataModule() {
    return new ChartDataModule();
}

