/**
 * System Integration Test Reporter - V2 Compliant Test Reporting Engine
 * Specialized test reporting and analytics methods
 * V2 COMPLIANCE: Under 100-line limit
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

export class SystemIntegrationTestReporter {
    constructor(systemHealth, testResults, performanceMetrics) {
        this.systemHealth = systemHealth;
        this.testResults = testResults;
        this.performanceMetrics = performanceMetrics;
    }

    async generateReport() {
        console.log('\n📊 SYSTEM INTEGRATION TEST REPORT');
        console.log('=====================================');

        this.generateSystemHealthReport();
        this.generateTestResultsReport();
        this.generatePerformanceReport();
        this.generateRecommendationsReport();

        console.log('=====================================');
        console.log('✅ System Integration Test Report Complete');
    }

    generateSystemHealthReport() {
        console.log('\n🏥 SYSTEM HEALTH STATUS:');
        Object.entries(this.systemHealth).forEach(([component, status]) => {
            const icon = status ? '✅' : '❌';
            const displayName = component.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
            console.log(`   ${icon} ${displayName}: ${status ? 'HEALTHY' : 'ISSUES DETECTED'}`);
        });
    }

    generateTestResultsReport() {
        console.log('\n🧪 TEST EXECUTION RESULTS:');
        console.log(`   📊 Total Tests: ${this.testResults.total}`);
        console.log(`   ✅ Passed: ${this.testResults.passed}`);
        console.log(`   ❌ Failed: ${this.testResults.failed}`);
        console.log(`   📈 Success Rate: ${this.testResults.total > 0 ? ((this.testResults.passed / this.testResults.total) * 100).toFixed(1) : 0}%`);

        if (this.testResults.details && this.testResults.details.length > 0) {
            console.log('\n   📋 Test Details:');
            this.testResults.details.slice(-5).forEach((detail, index) => {
                const icon = detail.success ? '✅' : '❌';
                console.log(`      ${icon} ${detail.name}: ${detail.details || 'Completed'}`);
            });
        }
    }

    generatePerformanceReport() {
        console.log('\n⚡ PERFORMANCE METRICS:');
        console.log(`   🕐 Total System Time: ${this.performanceMetrics.totalSystemTime.toFixed(2)}ms`);
        console.log(`   🏗️  Initialization Time: ${this.performanceMetrics.initializationTime.toFixed(2)}ms`);
        console.log(`   🔗 Integration Time: ${this.performanceMetrics.integrationTime.toFixed(2)}ms`);
        console.log(`   📦 Component Load Time: ${this.performanceMetrics.componentLoadTime.toFixed(2)}ms`);
    }

    generateRecommendationsReport() {
        const overallHealth = Object.values(this.systemHealth).every(status => status);
        const testSuccessRate = this.testResults.total > 0 ? (this.testResults.passed / this.testResults.total) : 0;

        console.log('\n💡 RECOMMENDATIONS:');

        if (overallHealth && testSuccessRate >= 0.95) {
            console.log('   🎉 EXCELLENT: System is healthy and performing optimally');
            console.log('   ✅ All components operational, high test success rate');
        } else if (overallHealth && testSuccessRate >= 0.80) {
            console.log('   👍 GOOD: System is healthy with minor test issues');
            console.log('   🔍 Review failed tests for optimization opportunities');
        } else {
            console.log('   ⚠️  ATTENTION: System health or test issues detected');
            console.log('   🛠️  Address failing components and tests immediately');
        }

        if (this.performanceMetrics.totalSystemTime > 5000) {
            console.log('   🚀 PERFORMANCE: Consider optimization for faster execution');
        }
    }

    exportReport() {
        return {
            timestamp: new Date().toISOString(),
            systemHealth: { ...this.systemHealth },
            testResults: { ...this.testResults },
            performanceMetrics: { ...this.performanceMetrics },
            overallStatus: this.calculateOverallStatus()
        };
    }

    calculateOverallStatus() {
        const healthScore = Object.values(this.systemHealth).filter(Boolean).length / Object.keys(this.systemHealth).length;
        const testScore = this.testResults.total > 0 ? this.testResults.passed / this.testResults.total : 0;
        const overallScore = (healthScore + testScore) / 2;

        if (overallScore >= 0.95) return 'EXCELLENT';
        if (overallScore >= 0.80) return 'GOOD';
        if (overallScore >= 0.60) return 'FAIR';
        return 'NEEDS_ATTENTION';
    }
}

// Factory function
export function createTestReporter(systemHealth, testResults, performanceMetrics) {
    return new SystemIntegrationTestReporter(systemHealth, testResults, performanceMetrics);
}
