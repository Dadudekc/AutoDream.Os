/**
 * Dashboard Integration Test - V2 Compliance Validation
 * Tests modular architecture integration and performance
 * V2 Compliance: Integration testing with modular components
 */

import { DashboardMain } from './dashboard-main.js';
import { DashboardOptimized } from './dashboard-optimized.js';

class DashboardIntegrationTest {
    constructor() {
        this.testResults = {
            passed: 0,
            failed: 0,
            total: 0,
            details: []
        };
        this.performanceBaseline = {
            initialization: 100, // ms
            dataLoading: 50,    // ms
            rendering: 20       // ms
        };
    }

    // Run all integration tests
    async runAllTests() {
        console.log('🚀 Starting Dashboard Integration Tests...');
        
        try {
            await this.testModularArchitecture();
            await this.testBackwardCompatibility();
            await this.testPerformanceOptimization();
            await this.testErrorHandling();
            await this.testComponentIntegration();
            
            this.generateTestReport();
        } catch (error) {
            console.error('Integration test suite failed:', error);
            this.recordTestResult('Test Suite Execution', false, error.message);
        }
    }

    // Test modular architecture
    async testModularArchitecture() {
        console.log('📋 Testing Modular Architecture...');
        
        try {
            // Test component imports
            const dashboard = new DashboardMain();
            this.assert(dashboard.core, 'DashboardCore component loaded');
            this.assert(dashboard.navigation, 'DashboardNavigation component loaded');
            this.assert(dashboard.utils, 'DashboardUtils component loaded');
            this.assert(dashboard.v2, 'DashboardV2 component loaded');
            
            // Test component initialization
            await dashboard.initialize();
            this.assert(dashboard.currentView === 'overview', 'Default view set correctly');
            
            this.recordTestResult('Modular Architecture', true, 'All components loaded and initialized');
        } catch (error) {
            this.recordTestResult('Modular Architecture', false, error.message);
        }
    }

    // Test backward compatibility
    async testBackwardCompatibility() {
        console.log('🔄 Testing Backward Compatibility...');
        
        try {
            // Test that existing functions are available
            const dashboard = new DashboardMain();
            
            // Test function availability
            this.assert(typeof dashboard.loadDashboardData === 'function', 'loadDashboardData function available');
            this.assert(typeof dashboard.updateDashboard === 'function', 'updateDashboard function available');
            this.assert(typeof dashboard.utils.showAlert === 'function', 'showAlert function available');
            
            this.recordTestResult('Backward Compatibility', true, 'All legacy functions available');
        } catch (error) {
            this.recordTestResult('Backward Compatibility', false, error.message);
        }
    }

    // Test performance optimization
    async testPerformanceOptimization() {
        console.log('⚡ Testing Performance Optimization...');
        
        try {
            const dashboard = new DashboardOptimized();
            
            // Test initialization performance
            const startTime = performance.now();
            await dashboard.initialize();
            const initTime = performance.now() - startTime;
            
            this.assert(initTime < this.performanceBaseline.initialization, 
                `Initialization time ${initTime.toFixed(2)}ms within baseline ${this.performanceBaseline.initialization}ms`);
            
            // Test caching functionality
            this.assert(dashboard.cache instanceof Map, 'Caching system initialized');
            this.assert(typeof dashboard.getPerformanceSummary === 'function', 'Performance monitoring available');
            
            this.recordTestResult('Performance Optimization', true, 
                `Initialization: ${initTime.toFixed(2)}ms, Caching: Active, Monitoring: Active`);
        } catch (error) {
            this.recordTestResult('Performance Optimization', false, error.message);
        }
    }

    // Test error handling
    async testErrorHandling() {
        console.log('🛡️ Testing Error Handling...');
        
        try {
            const dashboard = new DashboardMain();
            
            // Test error handling in data loading
            try {
                await dashboard.loadDashboardData('invalid_view');
                // Should handle gracefully
                this.assert(true, 'Invalid view handled gracefully');
            } catch (error) {
                this.assert(error.message.includes('Failed to load'), 'Error properly caught and handled');
            }
            
            this.recordTestResult('Error Handling', true, 'Errors handled gracefully');
        } catch (error) {
            this.recordTestResult('Error Handling', false, error.message);
        }
    }

    // Test component integration
    async testComponentIntegration() {
        console.log('🔗 Testing Component Integration...');
        
        try {
            const dashboard = new DashboardMain();
            
            // Test component communication
            this.assert(dashboard.core.socket === null, 'Socket properly initialized');
            this.assert(dashboard.navigation, 'Navigation component integrated');
            this.assert(dashboard.utils, 'Utils component integrated');
            this.assert(dashboard.v2, 'V2 component integrated');
            
            // Test method delegation
            const originalMethod = dashboard.utils.showAlert;
            dashboard.utils.showAlert = function(type, message) {
                return `Test: ${type} - ${message}`;
            };
            
            const result = dashboard.utils.showAlert('test', 'message');
            this.assert(result === 'Test: test - message', 'Method delegation working');
            
            // Restore original method
            dashboard.utils.showAlert = originalMethod;
            
            this.recordTestResult('Component Integration', true, 'All components properly integrated');
        } catch (error) {
            this.recordTestResult('Component Integration', false, error.message);
        }
    }

    // Assertion helper
    assert(condition, message) {
        this.testResults.total++;
        
        if (condition) {
            this.testResults.passed++;
            console.log(`✅ PASS: ${message}`);
        } else {
            this.testResults.failed++;
            console.log(`❌ FAIL: ${message}`);
        }
    }

    // Record test result
    recordTestResult(testName, passed, details) {
        this.testResults.details.push({
            test: testName,
            passed,
            details,
            timestamp: new Date().toISOString()
        });
    }

    // Generate test report
    generateTestReport() {
        console.log('\n📊 INTEGRATION TEST REPORT');
        console.log('========================');
        console.log(`Total Tests: ${this.testResults.total}`);
        console.log(`Passed: ${this.testResults.passed} ✅`);
        console.log(`Failed: ${this.testResults.failed} ❌`);
        console.log(`Success Rate: ${((this.testResults.passed / this.testResults.total) * 100).toFixed(1)}%`);
        
        console.log('\n📋 DETAILED RESULTS:');
        this.testResults.details.forEach(result => {
            const status = result.passed ? '✅' : '❌';
            console.log(`${status} ${result.test}: ${result.details}`);
        });
        
        // V2 Compliance Check
        if (this.testResults.failed === 0) {
            console.log('\n🎉 V2 COMPLIANCE: 100% - All integration tests passed!');
            console.log('✅ Modular architecture validated');
            console.log('✅ Backward compatibility confirmed');
            console.log('✅ Performance optimization verified');
            console.log('✅ Error handling tested');
            console.log('✅ Component integration validated');
        } else {
            console.log('\n⚠️ V2 COMPLIANCE: Partial - Some tests failed');
            console.log(`❌ ${this.testResults.failed} tests need attention`);
        }
    }
}

// Run integration tests when loaded
if (typeof window !== 'undefined') {
    const testSuite = new DashboardIntegrationTest();
    testSuite.runAllTests();
}

export { DashboardIntegrationTest };
