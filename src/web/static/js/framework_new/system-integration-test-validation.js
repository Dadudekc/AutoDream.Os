/**
 * System Integration Test Validation - V2 Compliant
 * Validation logic for system integration testing
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist
 * @version 3.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

/**
 * System Integration Test Validation
 * Handles validation of test results and system health
 */
export class SystemIntegrationTestValidation {
    constructor(testCore) {
        this.testCore = testCore;
    }

    /**
     * Validate test results
     */
    validateTestResults(testResults) {
        console.log('🔍 Validating test results...');

        const validationResults = {
            totalTests: testResults.length,
            passedTests: 0,
            failedTests: 0,
            warnings: 0,
            criticalIssues: []
        };

        testResults.forEach(result => {
            if (result.result === 'PASS') {
                validationResults.passedTests++;
            } else if (result.result === 'FAIL') {
                validationResults.failedTests++;
                if (result.details.severity === 'CRITICAL') {
                    validationResults.criticalIssues.push(result.testName);
                }
            } else if (result.result === 'WARN') {
                validationResults.warnings++;
            }
        });

        // Update system health based on validation
        this.testCore.updateSystemHealth('validation', {
            status: validationResults.failedTests === 0 ? 'HEALTHY' : 'ISSUES_DETECTED',
            details: validationResults
        });

        console.log('✅ Test validation completed:', validationResults);
        return validationResults;
    }

    /**
     * Validate component health
     */
    validateComponentHealth(componentName, healthData) {
        const healthChecks = {
            isResponsive: this.checkResponsiveness(healthData),
            hasErrors: this.checkForErrors(healthData),
            performanceAcceptable: this.checkPerformance(healthData),
            memoryUsage: this.checkMemoryUsage(healthData)
        };

        const overallHealth = Object.values(healthChecks).every(check => check === true) ? 'HEALTHY' : 'ISSUES_DETECTED';

        this.testCore.updateSystemHealth(componentName, {
            status: overallHealth,
            checks: healthChecks
        });

        return healthChecks;
    }

    /**
     * Check component responsiveness
     */
    checkResponsiveness(healthData) {
        return healthData.responseTime < 1000; // Under 1 second
    }

    /**
     * Check for errors
     */
    checkForErrors(healthData) {
        return !healthData.errors || healthData.errors.length === 0;
    }

    /**
     * Check performance
     */
    checkPerformance(healthData) {
        return healthData.performanceScore >= 80; // 80% or higher
    }

    /**
     * Check memory usage
     */
    checkMemoryUsage(healthData) {
        return healthData.memoryUsage < 100; // Under 100MB
    }

    /**
     * Validate system integration
     */
    validateSystemIntegration(integrationData) {
        const integrationChecks = {
            dataFlow: this.validateDataFlow(integrationData),
            apiConnections: this.validateApiConnections(integrationData),
            componentCommunication: this.validateComponentCommunication(integrationData),
            errorPropagation: this.validateErrorPropagation(integrationData)
        };

        const overallIntegration = Object.values(integrationChecks).every(check => check === true) ? 'INTEGRATED' : 'INTEGRATION_ISSUES';

        this.testCore.updateSystemHealth('system_integration', {
            status: overallIntegration,
            checks: integrationChecks
        });

        return integrationChecks;
    }

    /**
     * Validate data flow
     */
    validateDataFlow(integrationData) {
        return integrationData.dataFlow && integrationData.dataFlow.isValid;
    }

    /**
     * Validate API connections
     */
    validateApiConnections(integrationData) {
        return integrationData.apiConnections && integrationData.apiConnections.allConnected;
    }

    /**
     * Validate component communication
     */
    validateComponentCommunication(integrationData) {
        return integrationData.componentCommunication && integrationData.componentCommunication.isWorking;
    }

    /**
     * Validate error propagation
     */
    validateErrorPropagation(integrationData) {
        return integrationData.errorPropagation && integrationData.errorPropagation.isHandled;
    }
}
