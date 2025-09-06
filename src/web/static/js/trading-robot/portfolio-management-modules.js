/**
 * Portfolio Management Modules - V2 Compliant Portfolio Management Utilities
 * Handles all portfolio calculations and management operations
 *
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - Trading Robot Frontend V2 Compliance
 * @license MIT
 */

/**
 * Portfolio management utilities for trading portfolio
 */
export class PortfolioManagementModules {
    /**
     * Calculate portfolio metrics
     */
    static calculatePortfolioMetrics(portfolio) {
        let totalMarketValue = 0;
        let totalPnl = 0;

        portfolio.positions.forEach(position => {
            totalMarketValue += position.marketValue;
            totalPnl += position.pnl;
        });

        portfolio.totalValue = portfolio.cash + totalMarketValue;
        portfolio.pnl = totalPnl;
        portfolio.pnlPercent = portfolio.totalValue > 0 ? (totalPnl / portfolio.totalValue) * 100 : 0;
        portfolio.lastUpdated = new Date();
    }

    /**
     * Update position from order
     */
    static updatePositionFromOrder(portfolio, order) {
        if (order.status !== 'filled') return;

        const existingPosition = portfolio.positions.find(p => p.symbol === order.symbol);

        if (existingPosition) {
            if (order.side === 'buy') {
                const totalQuantity = existingPosition.quantity + order.filledQuantity;
                const totalCost = (existingPosition.quantity * existingPosition.avgPrice) +
                                 (order.filledQuantity * order.filledPrice);
                existingPosition.quantity = totalQuantity;
                existingPosition.avgPrice = totalCost / totalQuantity;
            } else {
                existingPosition.quantity -= order.filledQuantity;
                if (existingPosition.quantity <= 0) {
                    portfolio.positions = portfolio.positions.filter(p => p.symbol !== order.symbol);
                }
            }
        } else if (order.side === 'buy') {
            portfolio.positions.push({
                symbol: order.symbol,
                quantity: order.filledQuantity,
                avgPrice: order.filledPrice,
                currentPrice: order.filledPrice,
                marketValue: order.filledQuantity * order.filledPrice,
                pnl: 0,
                pnlPercent: 0
            });
        }

        // Update cash
        if (order.side === 'buy') {
            portfolio.cash -= order.filledQuantity * order.filledPrice;
        } else {
            portfolio.cash += order.filledQuantity * order.filledPrice;
        }

        this.calculatePortfolioMetrics(portfolio);
    }

    /**
     * Update position prices
     */
    static updatePositionPrices(portfolio, priceData) {
        portfolio.positions.forEach(position => {
            if (priceData[position.symbol]) {
                position.currentPrice = priceData[position.symbol];
                position.marketValue = position.quantity * position.currentPrice;
                position.pnl = (position.currentPrice - position.avgPrice) * position.quantity;
                position.pnlPercent = ((position.currentPrice - position.avgPrice) / position.avgPrice) * 100;
            }
        });

        this.calculatePortfolioMetrics(portfolio);
    }

    /**
     * Check risk limits
     */
    static checkRiskLimits(portfolio, riskLimits) {
        const violations = [];

        // Check position size limits
        portfolio.positions.forEach(position => {
            const positionPercent = position.marketValue / portfolio.totalValue;
            if (positionPercent > riskLimits.maxPositionSize) {
                violations.push({
                    type: 'position_size',
                    symbol: position.symbol,
                    current: positionPercent,
                    limit: riskLimits.maxPositionSize
                });
            }
        });

        // Check drawdown limits
        if (portfolio.pnlPercent < -riskLimits.maxDrawdown * 100) {
            violations.push({
                type: 'drawdown',
                current: portfolio.pnlPercent,
                limit: -riskLimits.maxDrawdown * 100
            });
        }

        return violations;
    }

    /**
     * Generate portfolio report
     */
    static generatePortfolioReport(portfolio) {
        return {
            summary: {
                totalValue: portfolio.totalValue,
                cash: portfolio.cash,
                investedValue: portfolio.totalValue - portfolio.cash,
                pnl: portfolio.pnl,
                pnlPercent: portfolio.pnlPercent,
                positionCount: portfolio.positions.length,
                lastUpdated: portfolio.lastUpdated
            },
            positions: portfolio.positions.map(position => ({
                symbol: position.symbol,
                quantity: position.quantity,
                avgPrice: position.avgPrice,
                currentPrice: position.currentPrice,
                marketValue: position.marketValue,
                pnl: position.pnl,
                pnlPercent: position.pnlPercent
            })),
            topPerformers: portfolio.positions
                .filter(p => p.pnl > 0)
                .sort((a, b) => b.pnl - a.pnl)
                .slice(0, 3),
            worstPerformers: portfolio.positions
                .filter(p => p.pnl < 0)
                .sort((a, b) => a.pnl - b.pnl)
                .slice(0, 3)
        };
    }

    /**
     * Load sample portfolio data
     */
    static loadSamplePortfolio() {
        return {
            totalValue: 100000,
            cash: 50000,
            positions: [
                {
                    symbol: 'AAPL',
                    quantity: 100,
                    avgPrice: 150.00,
                    currentPrice: 155.00,
                    marketValue: 15500,
                    pnl: 500,
                    pnlPercent: 3.33
                },
                {
                    symbol: 'GOOGL',
                    quantity: 50,
                    avgPrice: 2800.00,
                    currentPrice: 2750.00,
                    marketValue: 137500,
                    pnl: -2500,
                    pnlPercent: -1.79
                }
            ],
            pnl: -2000,
            pnlPercent: -2.0,
            lastUpdated: new Date()
        };
    }

    /**
     * Start portfolio updates
     */
    static startPortfolioUpdates(portfolio, updateCallback) {
        // Simulate real-time portfolio updates
        setInterval(() => {
            // Simulate price changes
            const priceChanges = {
                'AAPL': (Math.random() - 0.5) * 10,
                'GOOGL': (Math.random() - 0.5) * 100
            };

            const priceData = {};
            portfolio.positions.forEach(position => {
                priceData[position.symbol] = position.currentPrice + (priceChanges[position.symbol] || 0);
            });

            this.updatePositionPrices(portfolio, priceData);
            updateCallback(portfolio);
        }, 5000); // Update every 5 seconds
    }

    /**
     * Export portfolio data
     */
    static exportPortfolioData(portfolio) {
        const dataStr = JSON.stringify(portfolio, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);

        const link = document.createElement('a');
        link.href = url;
        link.download = 'portfolio-data.json';
        link.click();

        URL.revokeObjectURL(url);
    }

    /**
     * Import portfolio data
     */
    static async importPortfolioData(file) {
        try {
            const text = await file.text();
            const importedPortfolio = JSON.parse(text);

            if (importedPortfolio && importedPortfolio.positions) {
                this.calculatePortfolioMetrics(importedPortfolio);
                return importedPortfolio;
            } else {
                throw new Error('Invalid portfolio file format');
            }
        } catch (error) {
            console.error('❌ Error importing portfolio data:', error);
            throw error;
        }
    }
}
