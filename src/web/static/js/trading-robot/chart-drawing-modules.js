/**
 * Chart Drawing Modules - V2 Compliant Chart Drawing Utilities
 * Handles all chart drawing and rendering operations
 * 
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - Trading Robot Frontend V2 Compliance
 * @license MIT
 */

import { ChartCalculationModules } from './chart-calculation-modules.js';

/**
 * Chart drawing utilities for trading charts
 */
export class ChartDrawingModules {
    /**
     * Draw Simple Moving Average
     */
    static drawSMA(ctx, width, height, chartData) {
        if (chartData.length < 20) return;

        const smaData = ChartCalculationModules.calculateSMA(chartData, 20);
        const padding = 40;
        const chartWidth = width - (padding * 2);
        const chartHeight = height - (padding * 2);

        const prices = chartData.map(d => d.close);
        const minPrice = Math.min(...prices);
        const maxPrice = Math.max(...prices);
        const priceRange = maxPrice - minPrice;

        ctx.strokeStyle = '#FF9800';
        ctx.lineWidth = 2;
        ctx.beginPath();

        smaData.forEach((value, index) => {
            if (value !== null) {
                const x = padding + (index / (chartData.length - 1)) * chartWidth;
                const y = padding + ((maxPrice - value) / priceRange) * chartHeight;
                
                if (index === 0 || smaData[index - 1] === null) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
        });

        ctx.stroke();
    }

    /**
     * Draw Exponential Moving Average
     */
    static drawEMA(ctx, width, height, chartData) {
        if (chartData.length < 12) return;

        const emaData = ChartCalculationModules.calculateEMA(chartData, 12);
        const padding = 40;
        const chartWidth = width - (padding * 2);
        const chartHeight = height - (padding * 2);

        const prices = chartData.map(d => d.close);
        const minPrice = Math.min(...prices);
        const maxPrice = Math.max(...prices);
        const priceRange = maxPrice - minPrice;

        ctx.strokeStyle = '#9C27B0';
        ctx.lineWidth = 2;
        ctx.beginPath();

        emaData.forEach((value, index) => {
            if (value !== null) {
                const x = padding + (index / (chartData.length - 1)) * chartWidth;
                const y = padding + ((maxPrice - value) / priceRange) * chartHeight;
                
                if (index === 0 || emaData[index - 1] === null) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
        });

        ctx.stroke();
    }

    /**
     * Draw RSI indicator
     */
    static drawRSI(ctx, width, height, chartData) {
        if (chartData.length < 14) return;

        const rsiData = ChartCalculationModules.calculateRSI(chartData, 14);
        const padding = 40;
        const chartWidth = width - (padding * 2);
        const chartHeight = height - (padding * 2);

        ctx.strokeStyle = '#E91E63';
        ctx.lineWidth = 2;
        ctx.beginPath();

        rsiData.forEach((value, index) => {
            if (value !== null) {
                const x = padding + (index / (chartData.length - 1)) * chartWidth;
                const y = padding + ((100 - value) / 100) * chartHeight;
                
                if (index === 0 || rsiData[index - 1] === null) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
        });

        ctx.stroke();

        // Draw RSI levels
        ctx.strokeStyle = '#666';
        ctx.lineWidth = 1;
        ctx.setLineDash([5, 5]);
        
        // 70 level
        const y70 = padding + ((100 - 70) / 100) * chartHeight;
        ctx.beginPath();
        ctx.moveTo(padding, y70);
        ctx.lineTo(padding + chartWidth, y70);
        ctx.stroke();

        // 30 level
        const y30 = padding + ((100 - 30) / 100) * chartHeight;
        ctx.beginPath();
        ctx.moveTo(padding, y30);
        ctx.lineTo(padding + chartWidth, y30);
        ctx.stroke();

        ctx.setLineDash([]);
    }

    /**
     * Draw MACD indicator
     */
    static drawMACD(ctx, width, height, chartData) {
        if (chartData.length < 26) return;

        const macdData = ChartCalculationModules.calculateMACD(chartData);
        const padding = 40;
        const chartWidth = width - (padding * 2);
        const chartHeight = height - (padding * 2);

        // Draw MACD line
        ctx.strokeStyle = '#2196F3';
        ctx.lineWidth = 2;
        ctx.beginPath();

        macdData.forEach((value, index) => {
            if (value.macd !== null) {
                const x = padding + (index / (chartData.length - 1)) * chartWidth;
                const y = padding + ((0 - value.macd) / 0.1) * chartHeight;
                
                if (index === 0 || macdData[index - 1].macd === null) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
        });

        ctx.stroke();

        // Draw signal line
        ctx.strokeStyle = '#FF5722';
        ctx.lineWidth = 2;
        ctx.beginPath();

        macdData.forEach((value, index) => {
            if (value.signal !== null) {
                const x = padding + (index / (chartData.length - 1)) * chartWidth;
                const y = padding + ((0 - value.signal) / 0.1) * chartHeight;
                
                if (index === 0 || macdData[index - 1].signal === null) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
        });

        ctx.stroke();

        // Draw histogram
        macdData.forEach((value, index) => {
            if (value.histogram !== null) {
                const x = padding + (index / (chartData.length - 1)) * chartWidth;
                const y = padding + ((0 - value.histogram) / 0.1) * chartHeight;
                
                ctx.fillStyle = value.histogram >= 0 ? '#4CAF50' : '#F44336';
                ctx.fillRect(x - 1, y, 2, chartHeight - (y - padding));
            }
        });
    }

    /**
     * Draw candlesticks
     */
    static drawCandlesticks(ctx, width, height, chartData, minPrice, maxPrice) {
        const padding = 40;
        const chartWidth = width - (padding * 2);
        const chartHeight = height - (padding * 2);
        const priceRange = maxPrice - minPrice;

        chartData.forEach((data, index) => {
            const x = padding + (index / (chartData.length - 1)) * chartWidth;
            const openY = padding + ((maxPrice - data.open) / priceRange) * chartHeight;
            const closeY = padding + ((maxPrice - data.close) / priceRange) * chartHeight;
            const highY = padding + ((maxPrice - data.high) / priceRange) * chartHeight;
            const lowY = padding + ((maxPrice - data.low) / priceRange) * chartHeight;

            // Draw wick
            ctx.strokeStyle = data.close >= data.open ? '#4CAF50' : '#F44336';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(x, highY);
            ctx.lineTo(x, lowY);
            ctx.stroke();

            // Draw body
            const bodyHeight = Math.abs(closeY - openY);
            const bodyY = Math.min(openY, closeY);
            
            ctx.fillStyle = data.close >= data.open ? '#4CAF50' : '#F44336';
            ctx.fillRect(x - 2, bodyY, 4, Math.max(bodyHeight, 1));
        });
    }

    /**
     * Draw price chart
     */
    static drawPriceChart(ctx, width, height, chartData, chartType) {
        if (chartData.length === 0) return;

        const padding = 40;
        const chartWidth = width - (padding * 2);
        const chartHeight = height - (padding * 2);

        // Find price range
        const prices = chartData.map(d => [d.high, d.low]).flat();
        const minPrice = Math.min(...prices);
        const maxPrice = Math.max(...prices);
        const priceRange = maxPrice - minPrice;

        // Draw price line
        ctx.strokeStyle = '#2196F3';
        ctx.lineWidth = 2;
        ctx.beginPath();

        chartData.forEach((data, index) => {
            const x = padding + (index / (chartData.length - 1)) * chartWidth;
            const y = padding + ((maxPrice - data.close) / priceRange) * chartHeight;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });

        ctx.stroke();

        // Draw candlesticks if chart type is candlestick
        if (chartType === 'candlestick') {
            this.drawCandlesticks(ctx, width, height, chartData, minPrice, maxPrice);
        }
    }

    /**
     * Draw indicators
     */
    static drawIndicators(ctx, width, height, indicators, chartData) {
        if (indicators.length === 0) return;

        indicators.forEach(indicator => {
            switch (indicator) {
                case 'sma':
                    this.drawSMA(ctx, width, height, chartData);
                    break;
                case 'ema':
                    this.drawEMA(ctx, width, height, chartData);
                    break;
                case 'rsi':
                    this.drawRSI(ctx, width, height, chartData);
                    break;
                case 'macd':
                    this.drawMACD(ctx, width, height, chartData);
                    break;
            }
        });
    }
}
