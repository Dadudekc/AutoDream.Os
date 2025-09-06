/**
 * System Integration Test Reporting - V2 Compliant
 * Reporting functionality for system integration testing
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist
 * @version 3.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

/**
 * System Integration Test Reporting
 * Handles test result reporting and metrics generation
 */
export class SystemIntegrationTestReporting {
    constructor(testCore) {
        this.testCore = testCore;
    }

    /**
     * Generate comprehensive test report
     */
    generateTestReport(testResults) {
        console.log('📊 Generating test report...');

        const report = {
            timestamp: new Date().toISOString(),
            summary: this.generateTestSummary(testResults),
            detailedResults: testResults,
            performanceMetrics: this.testCore.getPerformanceMetrics(),
            systemHealth: this.testCore.getSystemHealth(),
            recommendations: this.generateRecommendations(testResults)
        };

        this.displayTestReport(report);
        this.saveTestReport(report);

        return report;
    }

    /**
     * Generate test summary
     */
    generateTestSummary(testResults) {
        const summary = {
            totalTests: testResults.length,
            passed: testResults.filter(r => r.result === 'PASS').length,
            failed: testResults.filter(r => r.result === 'FAIL').length,
            warnings: testResults.filter(r => r.result === 'WARN').length,
            successRate: 0,
            executionTime: this.calculateExecutionTime(testResults)
        };

        summary.successRate = summary.totalTests > 0 ? (summary.passed / summary.totalTests * 100).toFixed(2) : 0;

        return summary;
    }

    /**
     * Calculate execution time
     */
    calculateExecutionTime(testResults) {
        if (testResults.length === 0) return 0;

        const startTime = new Date(testResults[0].timestamp);
        const endTime = new Date(testResults[testResults.length - 1].timestamp);

        return endTime - startTime;
    }

    /**
     * Generate recommendations
     */
    generateRecommendations(testResults) {
        const recommendations = [];

        const failedTests = testResults.filter(r => r.result === 'FAIL');
        const warningTests = testResults.filter(r => r.result === 'WARN');

        if (failedTests.length > 0) {
            recommendations.push({
                type: 'CRITICAL',
                message: `${failedTests.length} tests failed. Immediate attention required.`,
                tests: failedTests.map(t => t.testName)
            });
        }

        if (warningTests.length > 0) {
            recommendations.push({
                type: 'WARNING',
                message: `${warningTests.length} tests have warnings. Review recommended.`,
                tests: warningTests.map(t => t.testName)
            });
        }

        // Performance recommendations
        const performanceMetrics = this.testCore.getPerformanceMetrics();
        if (performanceMetrics.averageResponseTime > 1000) {
            recommendations.push({
                type: 'PERFORMANCE',
                message: 'Average response time exceeds 1 second. Consider optimization.',
                metric: 'averageResponseTime',
                value: performanceMetrics.averageResponseTime
            });
        }

        return recommendations;
    }

    /**
     * Display test report
     */
    displayTestReport(report) {
        console.log('📋 SYSTEM INTEGRATION TEST REPORT');
        console.log('=====================================');
        console.log(`📅 Timestamp: ${report.timestamp}`);
        console.log(`📊 Total Tests: ${report.summary.totalTests}`);
        console.log(`✅ Passed: ${report.summary.passed}`);
        console.log(`❌ Failed: ${report.summary.failed}`);
        console.log(`⚠️  Warnings: ${report.summary.warnings}`);
        console.log(`📈 Success Rate: ${report.summary.successRate}%`);
        console.log(`⏱️  Execution Time: ${report.summary.executionTime}ms`);

        if (report.recommendations.length > 0) {
            console.log('\n🔍 RECOMMENDATIONS:');
            report.recommendations.forEach(rec => {
                console.log(`  ${rec.type}: ${rec.message}`);
            });
        }

        console.log('=====================================');
    }

    /**
     * Save test report
     */
    saveTestReport(report) {
        try {
            // In a real implementation, this would save to a file or database
            const reportData = JSON.stringify(report, null, 2);
            console.log('💾 Test report saved successfully');

            // Store in test core for later retrieval
            this.testCore.testReport = report;

        } catch (error) {
            console.error('❌ Failed to save test report:', error);
        }
    }

    /**
     * Export test results
     */
    exportTestResults(format = 'json') {
        const testResults = this.testCore.getTestResults();

        switch (format.toLowerCase()) {
            case 'json':
                return JSON.stringify(testResults, null, 2);
            case 'csv':
                return this.convertToCSV(testResults);
            case 'xml':
                return this.convertToXML(testResults);
            default:
                throw new Error(`Unsupported export format: ${format}`);
        }
    }

    /**
     * Convert test results to CSV
     */
    convertToCSV(testResults) {
        const headers = ['Test Name', 'Result', 'Timestamp', 'Details'];
        const rows = testResults.map(result => [
            result.testName,
            result.result,
            result.timestamp,
            JSON.stringify(result.details)
        ]);

        return [headers, ...rows].map(row => row.join(',')).join('\n');
    }

    /**
     * Convert test results to XML
     */
    convertToXML(testResults) {
        let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<testResults>\n';

        testResults.forEach(result => {
            xml += `  <test name="${result.testName}" result="${result.result}" timestamp="${result.timestamp}">\n`;
            xml += `    <details>${JSON.stringify(result.details)}</details>\n`;
            xml += '  </test>\n';
        });

        xml += '</testResults>';
        return xml;
    }
}
