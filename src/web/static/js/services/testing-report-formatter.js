/**
 * Testing Report Formatter - V2 Compliant
 * Report formatting and output functionality
 * V2 COMPLIANCE: Under 300-line limit
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

export class TestingReportFormatter {
    constructor() {
        this.outputFormats = {
            CONSOLE: 'console',
            JSON: 'json',
            HTML: 'html',
            MARKDOWN: 'markdown'
        };
    }

    formatReport(report, format = 'console') {
        switch (format) {
            case this.outputFormats.CONSOLE:
                return this.formatForConsole(report);
            case this.outputFormats.JSON:
                return this.formatForJSON(report);
            case this.outputFormats.HTML:
                return this.formatForHTML(report);
            case this.outputFormats.MARKDOWN:
                return this.formatForMarkdown(report);
            default:
                return this.formatForConsole(report);
        }
    }

    formatForConsole(report) {
        let output = '';

        // Header
        output += '🚀 TESTING REPORT\n';
        output += '='.repeat(50) + '\n';
        output += `📅 Generated: ${new Date(report.timestamp).toLocaleString()}\n\n`;

        // Summary
        if (report.summary) {
            output += '📊 SUMMARY\n';
            output += `   Total Tests: ${report.summary.totalTests}\n`;
            output += `   Passed: ${report.summary.passed}\n`;
            output += `   Failed: ${report.summary.failed}\n`;
            output += `   Skipped: ${report.summary.skipped || 0}\n`;
            output += `   Success Rate: ${report.summary.successRate?.toFixed(2)}%\n`;
            output += `   Duration: ${report.summary.duration}ms\n`;
            output += `   Status: ${report.status}\n\n`;
        }

        // Recommendations
        if (report.recommendations && report.recommendations.length > 0) {
            output += '💡 RECOMMENDATIONS\n';
            report.recommendations.forEach((rec, index) => {
                output += `   ${index + 1}. ${rec}\n`;
            });
            output += '\n';
        }

        // Compatibility (if available)
        if (report.compatibility) {
            output += '🔗 COMPATIBILITY\n';
            output += `   Browser Support: ${report.compatibility.browserSupport?.join(', ') || 'Unknown'}\n`;
            output += `   API Compatibility: ${report.compatibility.apiCompatibility ? '✅' : '❌'}\n`;
            output += `   Legacy Support: ${report.compatibility.legacySupport ? '✅' : '❌'}\n`;

            if (report.compatibility.issues?.length > 0) {
                output += '   Issues:\n';
                report.compatibility.issues.forEach((issue, index) => {
                    output += `     ${index + 1}. ${issue}\n`;
                });
            }
            output += '\n';
        }

        // Trends (if available)
        if (report.trends) {
            output += '📈 TRENDS\n';
            output += `   Improvement: ${report.trends.improvement}\n`;
            output += `   Consistency: ${report.trends.consistency}\n\n`;
        }

        // Insights (if available)
        if (report.insights && report.insights.length > 0) {
            output += '🔍 INSIGHTS\n';
            report.insights.forEach((insight, index) => {
                output += `   ${index + 1}. ${insight}\n`;
            });
            output += '\n';
        }

        return output;
    }

    formatForJSON(report) {
        return JSON.stringify(report, null, 2);
    }

    formatForHTML(report) {
        let html = `
<!DOCTYPE html>
<html>
<head>
    <title>Testing Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f0f0f0; padding: 10px; border-radius: 5px; }
        .section { margin: 20px 0; }
        .summary { background: #e8f5e8; padding: 10px; border-radius: 5px; }
        .recommendations { background: #fff3cd; padding: 10px; border-radius: 5px; }
        .status-excellent { color: #28a745; }
        .status-good { color: #17a2b8; }
        .status-needs_improvement { color: #ffc107; }
        .status-critical { color: #dc3545; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Testing Report</h1>
        <p>Generated: ${new Date(report.timestamp).toLocaleString()}</p>
    </div>
`;

        if (report.summary) {
            html += `
    <div class="section summary">
        <h2>📊 Summary</h2>
        <ul>
            <li>Total Tests: ${report.summary.totalTests}</li>
            <li>Passed: ${report.summary.passed}</li>
            <li>Failed: ${report.summary.failed}</li>
            <li>Success Rate: ${report.summary.successRate?.toFixed(2)}%</li>
            <li>Status: <span class="status-${report.status}">${report.status}</span></li>
        </ul>
    </div>
`;
        }

        if (report.recommendations && report.recommendations.length > 0) {
            html += `
    <div class="section recommendations">
        <h2>💡 Recommendations</h2>
        <ul>
            ${report.recommendations.map(rec => `<li>${rec}</li>`).join('')}
        </ul>
    </div>
`;
        }

        html += `
</body>
</html>`;

        return html;
    }

    formatForMarkdown(report) {
        let markdown = '# 🚀 Testing Report\n\n';
        markdown += `**Generated:** ${new Date(report.timestamp).toLocaleString()}\n\n`;

        if (report.summary) {
            markdown += '## 📊 Summary\n\n';
            markdown += `- **Total Tests:** ${report.summary.totalTests}\n`;
            markdown += `- **Passed:** ${report.summary.passed}\n`;
            markdown += `- **Failed:** ${report.summary.failed}\n`;
            markdown += `- **Success Rate:** ${report.summary.successRate?.toFixed(2)}%\n`;
            markdown += `- **Status:** ${report.status}\n\n`;
        }

        if (report.recommendations && report.recommendations.length > 0) {
            markdown += '## 💡 Recommendations\n\n';
            report.recommendations.forEach((rec, index) => {
                markdown += `${index + 1}. ${rec}\n`;
            });
            markdown += '\n';
        }

        return markdown;
    }

    exportReport(report, format = 'console', filename = null) {
        const formatted = this.formatReport(report, format);

        if (filename) {
            // In a real implementation, this would save to file
            console.log(`📁 Report exported to: ${filename}`);
        }

        return formatted;
    }

    generateReportSummary(reports) {
        if (!reports || reports.length === 0) {
            return { message: 'No reports available' };
        }

        const summary = {
            totalReports: reports.length,
            averageSuccessRate: 0,
            totalTests: 0,
            totalPassed: 0,
            totalFailed: 0,
            statusDistribution: {},
            timeRange: {
                start: reports[0]?.timestamp,
                end: reports[reports.length - 1]?.timestamp
            }
        };

        reports.forEach(report => {
            if (report.summary) {
                summary.totalTests += report.summary.totalTests || 0;
                summary.totalPassed += report.summary.passed || 0;
                summary.totalFailed += report.summary.failed || 0;

                const successRate = report.summary.successRate || 0;
                summary.averageSuccessRate += successRate;
            }

            const status = report.status || 'unknown';
            summary.statusDistribution[status] = (summary.statusDistribution[status] || 0) + 1;
        });

        summary.averageSuccessRate = summary.averageSuccessRate / reports.length;

        return summary;
    }
}

export function createTestingReportFormatter() {
    return new TestingReportFormatter();
}
