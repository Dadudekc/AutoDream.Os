/**
 * Chart Calculation Modules - V2 Compliant Chart Calculation Utilities
 * Handles all chart calculation operations
 * 
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - Trading Robot Frontend V2 Compliance
 * @license MIT
 */

/**
 * Chart calculation utilities for trading charts
 */
export class ChartCalculationModules {
    /**
     * Calculate Simple Moving Average
     */
    static calculateSMA(data, period) {
        const sma = [];
        for (let i = 0; i < data.length; i++) {
            if (i < period - 1) {
                sma.push(null);
            } else {
                const sum = data.slice(i - period + 1, i + 1).reduce((acc, d) => acc + d.close, 0);
                sma.push(sum / period);
            }
        }
        return sma;
    }

    /**
     * Calculate Exponential Moving Average
     */
    static calculateEMA(data, period) {
        const ema = [];
        const multiplier = 2 / (period + 1);
        
        for (let i = 0; i < data.length; i++) {
            if (i === 0) {
                ema.push(data[i].close);
            } else {
                ema.push((data[i].close * multiplier) + (ema[i - 1] * (1 - multiplier)));
            }
        }
        return ema;
    }

    /**
     * Calculate RSI
     */
    static calculateRSI(data, period) {
        const rsi = [];
        const gains = [];
        const losses = [];

        for (let i = 1; i < data.length; i++) {
            const change = data[i].close - data[i - 1].close;
            gains.push(change > 0 ? change : 0);
            losses.push(change < 0 ? Math.abs(change) : 0);
        }

        for (let i = 0; i < data.length; i++) {
            if (i < period) {
                rsi.push(null);
            } else {
                const avgGain = gains.slice(i - period, i).reduce((a, b) => a + b, 0) / period;
                const avgLoss = losses.slice(i - period, i).reduce((a, b) => a + b, 0) / period;
                const rs = avgGain / avgLoss;
                rsi.push(100 - (100 / (1 + rs)));
            }
        }

        return rsi;
    }

    /**
     * Calculate MACD
     */
    static calculateMACD(data) {
        const ema12 = this.calculateEMA(data, 12);
        const ema26 = this.calculateEMA(data, 26);
        const macd = [];

        for (let i = 0; i < data.length; i++) {
            if (i < 25) {
                macd.push({ macd: null, signal: null, histogram: null });
            } else {
                const macdValue = ema12[i] - ema26[i];
                macd.push({ macd: macdValue, signal: null, histogram: null });
            }
        }

        // Calculate signal line (9-period EMA of MACD)
        const macdValues = macd.map(m => m.macd).filter(v => v !== null);
        const signalLine = this.calculateEMA(macdValues.map(v => ({ close: v })), 9);

        for (let i = 0; i < macd.length; i++) {
            if (macd[i].macd !== null && signalLine[i - (macd.length - signalLine.length)] !== undefined) {
                macd[i].signal = signalLine[i - (macd.length - signalLine.length)];
                macd[i].histogram = macd[i].macd - macd[i].signal;
            }
        }

        return macd;
    }

    /**
     * Calculate Bollinger Bands
     */
    static calculateBollingerBands(data, period = 20, stdDev = 2) {
        const bb = [];
        
        for (let i = 0; i < data.length; i++) {
            if (i < period - 1) {
                bb.push({ upper: null, middle: null, lower: null });
            } else {
                const slice = data.slice(i - period + 1, i + 1);
                const sma = slice.reduce((sum, d) => sum + d.close, 0) / period;
                const variance = slice.reduce((sum, d) => sum + Math.pow(d.close - sma, 2), 0) / period;
                const stdDeviation = Math.sqrt(variance);
                
                bb.push({
                    upper: sma + (stdDev * stdDeviation),
                    middle: sma,
                    lower: sma - (stdDev * stdDeviation)
                });
            }
        }
        
        return bb;
    }

    /**
     * Calculate Stochastic Oscillator
     */
    static calculateStochastic(data, kPeriod = 14, dPeriod = 3) {
        const stoch = [];
        
        for (let i = 0; i < data.length; i++) {
            if (i < kPeriod - 1) {
                stoch.push({ k: null, d: null });
            } else {
                const slice = data.slice(i - kPeriod + 1, i + 1);
                const highest = Math.max(...slice.map(d => d.high));
                const lowest = Math.min(...slice.map(d => d.low));
                const k = ((data[i].close - lowest) / (highest - lowest)) * 100;
                stoch.push({ k: k, d: null });
            }
        }
        
        // Calculate %D (3-period SMA of %K)
        for (let i = 0; i < stoch.length; i++) {
            if (i >= dPeriod - 1) {
                const kValues = stoch.slice(i - dPeriod + 1, i + 1).map(s => s.k);
                stoch[i].d = kValues.reduce((sum, k) => sum + k, 0) / dPeriod;
            }
        }
        
        return stoch;
    }

    /**
     * Calculate Williams %R
     */
    static calculateWilliamsR(data, period = 14) {
        const williamsR = [];
        
        for (let i = 0; i < data.length; i++) {
            if (i < period - 1) {
                williamsR.push(null);
            } else {
                const slice = data.slice(i - period + 1, i + 1);
                const highest = Math.max(...slice.map(d => d.high));
                const lowest = Math.min(...slice.map(d => d.low));
                const wr = ((highest - data[i].close) / (highest - lowest)) * -100;
                williamsR.push(wr);
            }
        }
        
        return williamsR;
    }

    /**
     * Calculate Average True Range
     */
    static calculateATR(data, period = 14) {
        const atr = [];
        const trueRanges = [];
        
        for (let i = 1; i < data.length; i++) {
            const tr1 = data[i].high - data[i].low;
            const tr2 = Math.abs(data[i].high - data[i - 1].close);
            const tr3 = Math.abs(data[i].low - data[i - 1].close);
            trueRanges.push(Math.max(tr1, tr2, tr3));
        }
        
        for (let i = 0; i < data.length; i++) {
            if (i < period) {
                atr.push(null);
            } else {
                const atrValue = trueRanges.slice(i - period, i).reduce((sum, tr) => sum + tr, 0) / period;
                atr.push(atrValue);
            }
        }
        
        return atr;
    }

    /**
     * Calculate Commodity Channel Index
     */
    static calculateCCI(data, period = 20) {
        const cci = [];
        
        for (let i = 0; i < data.length; i++) {
            if (i < period - 1) {
                cci.push(null);
            } else {
                const slice = data.slice(i - period + 1, i + 1);
                const typicalPrices = slice.map(d => (d.high + d.low + d.close) / 3);
                const sma = typicalPrices.reduce((sum, tp) => sum + tp, 0) / period;
                const meanDeviation = typicalPrices.reduce((sum, tp) => sum + Math.abs(tp - sma), 0) / period;
                const cciValue = (typicalPrices[typicalPrices.length - 1] - sma) / (0.015 * meanDeviation);
                cci.push(cciValue);
            }
        }
        
        return cci;
    }
}
