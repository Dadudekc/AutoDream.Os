/**
 * Chart Events - V2 Compliant Event Management Module
 * Handles all chart event listeners and interactions
 *
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - Trading Robot Frontend V2 Compliance
 * @license MIT
 */

/**
 * Chart event management utilities
 */
export class ChartEvents {
    /**
     * Setup chart controls event listeners
     */
    static setupChartControls(chartManager) {
        // Symbol selector
        const symbolSelect = document.getElementById('chart-symbol');
        if (symbolSelect) {
            symbolSelect.addEventListener('change', (e) => {
                chartManager.currentSymbol = e.target.value;
                chartManager.loadChartData();
            });
        }

        // Timeframe selector
        const timeframeSelect = document.getElementById('chart-timeframe');
        if (timeframeSelect) {
            timeframeSelect.addEventListener('change', (e) => {
                chartManager.timeframe = e.target.value;
                chartManager.loadChartData();
            });
        }

        // Chart type selector
        const chartTypeSelect = document.getElementById('chart-type');
        if (chartTypeSelect) {
            chartTypeSelect.addEventListener('change', (e) => {
                chartManager.chartType = e.target.value;
                chartManager.renderChart();
            });
        }

        // Indicator buttons
        const indicatorButtons = document.querySelectorAll('.indicator-btn');
        indicatorButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const indicator = e.target.dataset.indicator;
                chartManager.toggleIndicator(indicator);
            });
        });
    }

    /**
     * Setup chart canvas interactions
     */
    static setupChartInteractions(chartManager) {
        const canvas = document.getElementById('price-chart');
        if (!canvas) return;

        // Mouse move for price display
        canvas.addEventListener('mousemove', (e) => {
            this.handleMouseMove(e, chartManager);
        });

        // Click for crosshair
        canvas.addEventListener('click', (e) => {
            this.handleChartClick(e, chartManager);
        });

        // Wheel for zoom
        canvas.addEventListener('wheel', (e) => {
            this.handleChartZoom(e, chartManager);
        });
    }

    /**
     * Handle mouse move events
     */
    static handleMouseMove(event, chartManager) {
        const canvas = event.target;
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        // Find closest data point
        const dataPoint = this.findClosestDataPoint(x, y, chartManager.chartData, canvas);

        if (dataPoint) {
            this.showPriceTooltip(x, y, dataPoint, canvas);
        }
    }

    /**
     * Handle chart click events
     */
    static handleChartClick(event, chartManager) {
        const canvas = event.target;
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        // Toggle crosshair
        chartManager.toggleCrosshair(x, y);
    }

    /**
     * Handle chart zoom events
     */
    static handleChartZoom(event, chartManager) {
        event.preventDefault();

        const delta = event.deltaY > 0 ? 0.9 : 1.1;
        chartManager.zoomChart(delta);
    }

    /**
     * Find closest data point to mouse position
     */
    static findClosestDataPoint(x, y, chartData, canvas) {
        if (!chartData || chartData.length === 0) return null;

        const padding = 40;
        const chartWidth = canvas.width - (padding * 2);
        const chartHeight = canvas.height - (padding * 2);

        const prices = chartData.map(d => [d.high, d.low]).flat();
        const minPrice = Math.min(...prices);
        const maxPrice = Math.max(...prices);
        const priceRange = maxPrice - minPrice;

        let closestIndex = 0;
        let minDistance = Infinity;

        chartData.forEach((data, index) => {
            const dataX = padding + (index / (chartData.length - 1)) * chartWidth;
            const dataY = padding + ((maxPrice - data.close) / priceRange) * chartHeight;

            const distance = Math.sqrt(Math.pow(x - dataX, 2) + Math.pow(y - dataY, 2));

            if (distance < minDistance) {
                minDistance = distance;
                closestIndex = index;
            }
        });

        return {
            index: closestIndex,
            data: chartData[closestIndex],
            x: padding + (closestIndex / (chartData.length - 1)) * chartWidth,
            y: padding + ((maxPrice - chartData[closestIndex].close) / priceRange) * chartHeight
        };
    }

    /**
     * Show price tooltip
     */
    static showPriceTooltip(x, y, dataPoint, canvas) {
        // Remove existing tooltip
        const existingTooltip = document.getElementById('price-tooltip');
        if (existingTooltip) {
            existingTooltip.remove();
        }

        // Create tooltip
        const tooltip = document.createElement('div');
        tooltip.id = 'price-tooltip';
        tooltip.className = 'price-tooltip';
        tooltip.style.cssText = `
            position: absolute;
            left: ${x + 10}px;
            top: ${y - 10}px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            pointer-events: none;
            z-index: 1000;
        `;

        tooltip.innerHTML = `
            <div>Time: ${dataPoint.data.timestamp}</div>
            <div>Open: $${dataPoint.data.open.toFixed(2)}</div>
            <div>High: $${dataPoint.data.high.toFixed(2)}</div>
            <div>Low: $${dataPoint.data.low.toFixed(2)}</div>
            <div>Close: $${dataPoint.data.close.toFixed(2)}</div>
            <div>Volume: ${dataPoint.data.volume}</div>
        `;

        document.body.appendChild(tooltip);

        // Remove tooltip after delay
        setTimeout(() => {
            if (tooltip.parentNode) {
                tooltip.remove();
            }
        }, 3000);
    }

    /**
     * Setup keyboard shortcuts
     */
    static setupKeyboardShortcuts(chartManager) {
        document.addEventListener('keydown', (e) => {
            switch (e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    chartManager.navigateChart(-1);
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    chartManager.navigateChart(1);
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    chartManager.zoomChart(1.1);
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    chartManager.zoomChart(0.9);
                    break;
                case 'r':
                case 'R':
                    e.preventDefault();
                    chartManager.resetChart();
                    break;
                case 'f':
                case 'F':
                    e.preventDefault();
                    chartManager.toggleFullscreen();
                    break;
            }
        });
    }

    /**
     * Setup window resize handler
     */
    static setupResizeHandler(chartManager) {
        window.addEventListener('resize', () => {
            chartManager.handleResize();
        });
    }

    /**
     * Setup all event listeners
     */
    static setupAllEvents(chartManager) {
        this.setupChartControls(chartManager);
        this.setupChartInteractions(chartManager);
        this.setupKeyboardShortcuts(chartManager);
        this.setupResizeHandler(chartManager);
    }
}
