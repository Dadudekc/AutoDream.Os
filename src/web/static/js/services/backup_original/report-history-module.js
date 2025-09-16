/**
 * Report History Module - V2 Compliant
 * Report storage and retrieval functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// REPORT HISTORY MODULE
// ================================

/**
 * Report storage and retrieval functionality
 */
export class ReportHistoryModule {
    constructor() {
        this.logger = console;
        this.reportHistory = new Map();
        this.maxHistorySize = 10;
    }

    /**
     * Store report in history
     */
    storeReport(suiteName, report) {
        try {
            if (!this.reportHistory.has(suiteName)) {
                this.reportHistory.set(suiteName, []);
            }

            const history = this.reportHistory.get(suiteName);
            history.push({
                ...report,
                storedAt: new Date().toISOString()
            });

            // Keep only last N reports
            if (history.length > this.maxHistorySize) {
                history.shift();
            }

            return true;
        } catch (error) {
            this.logger.error(`Failed to store report for ${suiteName}:`, error);
            return false;
        }
    }

    /**
     * Get report history
     */
    getReportHistory(suiteName, limit = 5) {
        try {
            const history = this.reportHistory.get(suiteName) || [];
            return history.slice(-limit);
        } catch (error) {
            this.logger.error(`Failed to get report history for ${suiteName}:`, error);
            return [];
        }
    }

    /**
     * Get all stored suites
     */
    getStoredSuites() {
        return Array.from(this.reportHistory.keys());
    }

    /**
     * Clear history for suite
     */
    clearSuiteHistory(suiteName) {
        try {
            this.reportHistory.delete(suiteName);
            return true;
        } catch (error) {
            this.logger.error(`Failed to clear history for ${suiteName}:`, error);
            return false;
        }
    }

    /**
     * Clear all history
     */
    clearAllHistory() {
        try {
            this.reportHistory.clear();
            return true;
        } catch (error) {
            this.logger.error('Failed to clear all history:', error);
            return false;
        }
    }

    /**
     * Get history statistics
     */
    getHistoryStatistics() {
        const stats = {
            totalSuites: this.reportHistory.size,
            totalReports: 0,
            averageReportsPerSuite: 0,
            oldestReport: null,
            newestReport: null
        };

        if (stats.totalSuites === 0) return stats;

        let oldestTimestamp = null;
        let newestTimestamp = null;

        this.reportHistory.forEach((reports) => {
            stats.totalReports += reports.length;

            reports.forEach(report => {
                const timestamp = new Date(report.storedAt);
                if (!oldestTimestamp || timestamp < oldestTimestamp) {
                    oldestTimestamp = timestamp;
                }
                if (!newestTimestamp || timestamp > newestTimestamp) {
                    newestTimestamp = timestamp;
                }
            });
        });

        stats.averageReportsPerSuite = stats.totalReports / stats.totalSuites;
        stats.oldestReport = oldestTimestamp ? oldestTimestamp.toISOString() : null;
        stats.newestReport = newestTimestamp ? newestTimestamp.toISOString() : null;

        return stats;
    }

    /**
     * Filter history by date range
     */
    filterHistoryByDateRange(suiteName, startDate, endDate) {
        try {
            const history = this.getReportHistory(suiteName, this.maxHistorySize);
            const start = new Date(startDate);
            const end = new Date(endDate);

            return history.filter(report => {
                const reportDate = new Date(report.storedAt);
                return reportDate >= start && reportDate <= end;
            });
        } catch (error) {
            this.logger.error(`Failed to filter history for ${suiteName}:`, error);
            return [];
        }
    }

    /**
     * Get latest report for suite
     */
    getLatestReport(suiteName) {
        try {
            const history = this.getReportHistory(suiteName, 1);
            return history.length > 0 ? history[0] : null;
        } catch (error) {
            this.logger.error(`Failed to get latest report for ${suiteName}:`, error);
            return null;
        }
    }

    /**
     * Export history to JSON
     */
    exportHistory() {
        try {
            const exportData = {
                exportedAt: new Date().toISOString(),
                statistics: this.getHistoryStatistics(),
                history: Object.fromEntries(this.reportHistory)
            };
            return JSON.stringify(exportData, null, 2);
        } catch (error) {
            this.logger.error('Failed to export history:', error);
            return null;
        }
    }

    /**
     * Import history from JSON
     */
    importHistory(jsonData) {
        try {
            const importData = JSON.parse(jsonData);
            this.reportHistory = new Map(Object.entries(importData.history || {}));
            return true;
        } catch (error) {
            this.logger.error('Failed to import history:', error);
            return false;
        }
    }

    /**
     * Set maximum history size
     */
    setMaxHistorySize(size) {
        if (typeof size === 'number' && size > 0) {
            this.maxHistorySize = size;

            // Trim existing histories if needed
            this.reportHistory.forEach((reports, suiteName) => {
                if (reports.length > this.maxHistorySize) {
                    const trimmed = reports.slice(-this.maxHistorySize);
                    this.reportHistory.set(suiteName, trimmed);
                }
            });

            return true;
        }
        return false;
    }

    /**
     * Get history summary for suite
     */
    getHistorySummary(suiteName) {
        try {
            const history = this.getReportHistory(suiteName, this.maxHistorySize);
            const latest = this.getLatestReport(suiteName);

            return {
                suiteName: suiteName,
                totalReports: history.length,
                latestReport: latest,
                dateRange: history.length > 0 ? {
                    oldest: history[0].storedAt,
                    newest: history[history.length - 1].storedAt
                } : null,
                maxHistorySize: this.maxHistorySize
            };
        } catch (error) {
            this.logger.error(`Failed to get history summary for ${suiteName}:`, error);
            return null;
        }
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create report history module instance
 */
export function createReportHistoryModule() {
    return new ReportHistoryModule();
}
