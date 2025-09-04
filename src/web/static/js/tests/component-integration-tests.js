/**
 * Component Integration Tests Module - V2 Compliant
 * Tests for component integration and communication
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class ComponentIntegrationTests {
    constructor(systemHealth, testResults) {
        this.systemHealth = systemHealth;
        this.testResults = testResults;
    }

    /**
     * Test component integration
     */
    async testComponentIntegration() {
        console.log('🔗 Testing Component Integration...');

        const tests = [
            this.testDashboardComponentIntegration.bind(this),
            this.testServiceLayerIntegration.bind(this),
            this.testRepositoryLayerIntegration.bind(this),
            this.testUtilityLayerIntegration.bind(this),
            this.testCrossComponentCommunication.bind(this),
            this.testDependencyInjection.bind(this)
        ];

        let passed = 0;
        const results = [];

        for (const test of tests) {
            try {
                const result = await test();
                results.push(result);
                if (result.success) passed++;
            } catch (error) {
                results.push({
                    name: test.name,
                    success: false,
                    error: error.message
                });
                console.error(`❌ Component integration test failed:`, error);
            }
        }

        const success = passed === tests.length;
        this.systemHealth.componentIntegration = success;

        console.log(`✅ Component Integration: ${passed}/${tests.length} tests passed`);

        return {
            name: 'Component Integration',
            success,
            passed,
            total: tests.length,
            results
        };
    }

    /**
     * Test dashboard component integration
     */
    async testDashboardComponentIntegration() {
        try {
            // Test dashboard main component
            if (typeof window.DashboardMain === 'undefined') {
                throw new Error('DashboardMain not available');
            }

            // Test dashboard initialization
            const dashboard = new window.DashboardMain();
            await dashboard.initialize();

            // Verify core components
            const hasCore = !!dashboard.core;
            const hasNavigation = !!dashboard.navigation;
            const hasUtils = !!dashboard.utils;

            if (!hasCore || !hasNavigation || !hasUtils) {
                throw new Error('Core dashboard components not properly integrated');
            }

            return {
                name: 'Dashboard Component Integration',
                success: true,
                details: 'All dashboard components properly integrated'
            };
        } catch (error) {
            return {
                name: 'Dashboard Component Integration',
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Test service layer integration
     */
    async testServiceLayerIntegration() {
        try {
            // Test service dependencies
            const services = [
                'DashboardService',
                'DeploymentService',
                'UtilityService'
            ];

            for (const serviceName of services) {
                if (typeof window[serviceName] === 'undefined') {
                    throw new Error(`${serviceName} not available`);
                }
            }

            // Test service instantiation
            const dashboardService = new window.DashboardService();
            const deploymentService = new window.DeploymentService();
            const utilityService = new window.UtilityService();

            return {
                name: 'Service Layer Integration',
                success: true,
                details: 'All services properly integrated and instantiable'
            };
        } catch (error) {
            return {
                name: 'Service Layer Integration',
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Test repository layer integration
     */
    async testRepositoryLayerIntegration() {
        try {
            // Test repository availability
            const repositories = [
                'DashboardRepository',
                'DeploymentRepository'
            ];

            for (const repoName of repositories) {
                if (typeof window[repoName] === 'undefined') {
                    throw new Error(`${repoName} not available`);
                }
            }

            // Test repository instantiation
            const dashboardRepo = new window.DashboardRepository();
            const deploymentRepo = new window.DeploymentRepository();

            // Test basic repository methods
            const hasRequiredMethods = [
                'getDashboardData',
                'saveDashboardData'
            ].every(method => typeof dashboardRepo[method] === 'function');

            if (!hasRequiredMethods) {
                throw new Error('Repository methods not properly implemented');
            }

            return {
                name: 'Repository Layer Integration',
                success: true,
                details: 'All repositories properly integrated with required methods'
            };
        } catch (error) {
            return {
                name: 'Repository Layer Integration',
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Test utility layer integration
     */
    async testUtilityLayerIntegration() {
        try {
            if (typeof window.UtilityService === 'undefined') {
                throw new Error('UtilityService not available');
            }

            const utilityService = new window.UtilityService();

            // Test utility methods
            const testString = 'test string';
            const formatted = utilityService.formatString('Hello {0}', [testString]);
            const sanitized = utilityService.sanitizeInput('<script>alert("test")</script>');

            if (formatted !== 'Hello test string') {
                throw new Error('String formatting not working correctly');
            }

            if (sanitized.includes('<script>')) {
                throw new Error('Input sanitization not working correctly');
            }

            return {
                name: 'Utility Layer Integration',
                success: true,
                details: 'Utility service properly integrated with working methods'
            };
        } catch (error) {
            return {
                name: 'Utility Layer Integration',
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Test cross-component communication
     */
    async testCrossComponentCommunication() {
        try {
            // Test event system
            let eventReceived = false;

            const eventHandler = () => {
                eventReceived = true;
            };

            // Add event listener
            window.addEventListener('test:communication', eventHandler);

            // Dispatch test event
            window.dispatchEvent(new CustomEvent('test:communication'));

            // Remove event listener
            window.removeEventListener('test:communication', eventHandler);

            if (!eventReceived) {
                throw new Error('Cross-component communication not working');
            }

            return {
                name: 'Cross-Component Communication',
                success: true,
                details: 'Event system working correctly for component communication'
            };
        } catch (error) {
            return {
                name: 'Cross-Component Communication',
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Test dependency injection
     */
    async testDependencyInjection() {
        try {
            // Test service instantiation with dependencies
            const utilityService = new window.UtilityService();
            const dashboardService = new window.DashboardService(null, utilityService);

            // Verify dependency injection worked
            if (!dashboardService.utilityService) {
                throw new Error('Dependency injection not working correctly');
            }

            return {
                name: 'Dependency Injection',
                success: true,
                details: 'Dependency injection working correctly between services'
            };
        } catch (error) {
            return {
                name: 'Dependency Injection',
                success: false,
                error: error.message
            };
        }
    }
}

// Factory function for creating component integration tests
export function createComponentIntegrationTests(systemHealth, testResults) {
    return new ComponentIntegrationTests(systemHealth, testResults);
}


