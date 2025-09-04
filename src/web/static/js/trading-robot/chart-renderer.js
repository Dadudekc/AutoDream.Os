/**
 * Chart Renderer - V2 Compliant Chart Rendering Module
 * Handles all chart drawing and rendering operations
 * V2 COMPLIANCE: Under 300-line limit achieved
 * 
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - Trading Robot Frontend V2 Compliance
 * @license MIT
 */

import { ChartCalculationModules } from './chart-calculation-modules.js';
import { ChartDrawingModules } from './chart-drawing-modules.js';

/**
 * Chart rendering utilities for trading charts
 */
export class ChartRenderer {
    /**
     * Draw price chart
     */
    static drawPriceChart(ctx, width, height, chartData, chartType) {
        ChartDrawingModules.drawPriceChart(ctx, width, height, chartData, chartType);
    }

    /**
     * Draw indicators
     */
    static drawIndicators(ctx, width, height, indicators, chartData) {
        ChartDrawingModules.drawIndicators(ctx, width, height, indicators, chartData);
    }

    /**
     * Draw Simple Moving Average
     */
    static drawSMA(ctx, width, height, chartData) {
        ChartDrawingModules.drawSMA(ctx, width, height, chartData);
    }

    /**
     * Draw Exponential Moving Average
     */
    static drawEMA(ctx, width, height, chartData) {
        ChartDrawingModules.drawEMA(ctx, width, height, chartData);
    }

    /**
     * Draw RSI indicator
     */
    static drawRSI(ctx, width, height, chartData) {
        ChartDrawingModules.drawRSI(ctx, width, height, chartData);
    }

    /**
     * Draw MACD indicator
     */
    static drawMACD(ctx, width, height, chartData) {
        ChartDrawingModules.drawMACD(ctx, width, height, chartData);
    }

    /**
     * Draw candlesticks
     */
    static drawCandlesticks(ctx, width, height, chartData, minPrice, maxPrice) {
        ChartDrawingModules.drawCandlesticks(ctx, width, height, chartData, minPrice, maxPrice);
    }

    /**
     * Calculate Simple Moving Average
     */
    static calculateSMA(data, period) {
        return ChartCalculationModules.calculateSMA(data, period);
    }

    /**
     * Calculate Exponential Moving Average
     */
    static calculateEMA(data, period) {
        return ChartCalculationModules.calculateEMA(data, period);
    }

    /**
     * Calculate RSI
     */
    static calculateRSI(data, period) {
        return ChartCalculationModules.calculateRSI(data, period);
    }

    /**
     * Calculate MACD
     */
    static calculateMACD(data) {
        return ChartCalculationModules.calculateMACD(data);
    }

    /**
     * Calculate Bollinger Bands
     */
    static calculateBollingerBands(data, period, stdDev) {
        return ChartCalculationModules.calculateBollingerBands(data, period, stdDev);
    }

    /**
     * Calculate Stochastic Oscillator
     */
    static calculateStochastic(data, kPeriod, dPeriod) {
        return ChartCalculationModules.calculateStochastic(data, kPeriod, dPeriod);
    }

    /**
     * Calculate Williams %R
     */
    static calculateWilliamsR(data, period) {
        return ChartCalculationModules.calculateWilliamsR(data, period);
    }

    /**
     * Calculate Average True Range
     */
    static calculateATR(data, period) {
        return ChartCalculationModules.calculateATR(data, period);
    }

    /**
     * Calculate Commodity Channel Index
     */
    static calculateCCI(data, period) {
        return ChartCalculationModules.calculateCCI(data, period);
    }

    /**
     * Render complete chart
     */
    static renderChart(canvas, chartData, chartType, indicators) {
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        // Clear canvas
        ctx.clearRect(0, 0, width, height);

        // Draw background
        ctx.fillStyle = '#1a1a1a';
        ctx.fillRect(0, 0, width, height);

        // Draw grid
        this.drawGrid(ctx, width, height);

        // Draw price chart
        this.drawPriceChart(ctx, width, height, chartData, chartType);

        // Draw indicators
        if (indicators && indicators.length > 0) {
            this.drawIndicators(ctx, width, height, indicators, chartData);
        }

        // Draw axes
        this.drawAxes(ctx, width, height, chartData);
    }

    /**
     * Draw grid
     */
    static drawGrid(ctx, width, height) {
        const padding = 40;
        const gridSize = 50;

        ctx.strokeStyle = '#333';
        ctx.lineWidth = 1;

        // Vertical grid lines
        for (let x = padding; x < width - padding; x += gridSize) {
            ctx.beginPath();
            ctx.moveTo(x, padding);
            ctx.lineTo(x, height - padding);
            ctx.stroke();
        }

        // Horizontal grid lines
        for (let y = padding; y < height - padding; y += gridSize) {
            ctx.beginPath();
            ctx.moveTo(padding, y);
            ctx.lineTo(width - padding, y);
            ctx.stroke();
        }
    }

    /**
     * Draw axes
     */
    static drawAxes(ctx, width, height, chartData) {
        const padding = 40;

        // Draw axes
        ctx.strokeStyle = '#666';
        ctx.lineWidth = 2;

        // X-axis
        ctx.beginPath();
        ctx.moveTo(padding, height - padding);
        ctx.lineTo(width - padding, height - padding);
        ctx.stroke();

        // Y-axis
        ctx.beginPath();
        ctx.moveTo(padding, padding);
        ctx.lineTo(padding, height - padding);
        ctx.stroke();

        // Draw labels
        ctx.fillStyle = '#fff';
        ctx.font = '12px Arial';

        // Price labels
        const prices = chartData.map(d => d.close);
        const minPrice = Math.min(...prices);
        const maxPrice = Math.max(...prices);
        const priceRange = maxPrice - minPrice;

        for (let i = 0; i <= 5; i++) {
            const price = minPrice + (priceRange * i / 5);
            const y = height - padding - (i * (height - 2 * padding) / 5);
            ctx.fillText(price.toFixed(2), 5, y + 4);
        }

        // Time labels
        const timeStep = Math.max(1, Math.floor(chartData.length / 10));
        for (let i = 0; i < chartData.length; i += timeStep) {
            const x = padding + (i / (chartData.length - 1)) * (width - 2 * padding);
            const time = new Date(chartData[i].timestamp).toLocaleTimeString();
            ctx.fillText(time, x - 20, height - 10);
        }
    }

    /**
     * Export chart as image
     */
    static exportChart(canvas, filename) {
        const link = document.createElement('a');
        link.download = filename || 'chart.png';
        link.href = canvas.toDataURL();
        link.click();
    }

    /**
     * Get chart dimensions
     */
    static getChartDimensions(canvas) {
        return {
            width: canvas.width,
            height: canvas.height,
            padding: 40
        };
    }

    /**
     * Clear chart
     */
    static clearChart(canvas) {
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
}