/**
 * Business Validation Module - V2 Compliant
 * Business validation and scoring functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// BUSINESS VALIDATION MODULE
// ================================

/**
 * Business validation and scoring functionality
 */
export class BusinessValidationModule {
    constructor() {
        this.logger = console;
        this.businessRules = new Map();
        this.scoringWeights = {
            v2Compliance: 0.3,
            performance: 0.25,
            quality: 0.2,
            security: 0.15,
            maintainability: 0.1
        };
    }

    /**
     * Perform business validation
     */
    performBusinessValidation(validationData) {
        const issues = [];
        let score = 100;

        try {
            // V2 Compliance validation
            if (validationData.v2Compliant === false) {
                issues.push('Component is not V2 compliant');
                score -= 30;
            }

            // Performance validation
            if (validationData.validationScore < 80) {
                issues.push(`Validation score too low: ${validationData.validationScore}/100`);
                score -= 20;
            }

            // Code quality validation
            if (validationData.complexity > 10) {
                issues.push(`Code complexity too high: ${validationData.complexity}`);
                score -= 15;
            }

            // Security validation
            if (validationData.securityIssues && validationData.securityIssues.length > 0) {
                issues.push(`Security issues detected: ${validationData.securityIssues.length}`);
                score -= 25;
            }

            // Maintainability validation
            if (validationData.maintainabilityIndex < 50) {
                issues.push(`Low maintainability index: ${validationData.maintainabilityIndex}`);
                score -= 10;
            }

            return {
                valid: issues.length === 0,
                issues: issues,
                score: Math.max(0, score),
                breakdown: this.generateScoreBreakdown(validationData)
            };
        } catch (error) {
            this.logger.error('Business validation failed:', error);
            return {
                valid: false,
                issues: ['Business validation failed due to error'],
                score: 0,
                breakdown: {}
            };
        }
    }

    /**
     * Generate score breakdown
     */
    generateScoreBreakdown(validationData) {
        const breakdown = {
            v2Compliance: 0,
            performance: 0,
            quality: 0,
            security: 0,
            maintainability: 0
        };

        // V2 Compliance score
        breakdown.v2Compliance = validationData.v2Compliant === true ? 100 : 0;

        // Performance score
        breakdown.performance = Math.min(100, validationData.validationScore || 0);

        // Quality score based on complexity
        const complexity = validationData.complexity || 0;
        breakdown.quality = Math.max(0, 100 - (complexity * 5));

        // Security score
        const securityIssues = validationData.securityIssues?.length || 0;
        breakdown.security = Math.max(0, 100 - (securityIssues * 10));

        // Maintainability score
        breakdown.maintainability = validationData.maintainabilityIndex || 50;

        return breakdown;
    }

    /**
     * Calculate weighted business score
     */
    calculateWeightedScore(breakdown) {
        let totalScore = 0;

        Object.entries(breakdown).forEach(([category, score]) => {
            const weight = this.scoringWeights[category] || 0;
            totalScore += score * weight;
        });

        return Math.round(totalScore);
    }

    /**
     * Register custom business rule
     */
    registerBusinessRule(name, validator) {
        try {
            this.businessRules.set(name, validator);
            return true;
        } catch (error) {
            this.logger.error(`Failed to register business rule ${name}:`, error);
            return false;
        }
    }

    /**
     * Apply custom business rules
     */
    applyCustomBusinessRules(validationData, rules) {
        const results = [];
        let passed = true;

        for (const ruleName of rules) {
            const validator = this.businessRules.get(ruleName);
            if (!validator) {
                results.push({
                    rule: ruleName,
                    passed: false,
                    message: `Business rule '${ruleName}' not found`
                });
                passed = false;
                continue;
            }

            const result = validator(validationData);
            results.push(result);

            if (!result.passed) {
                passed = false;
            }
        }

        return { passed, results };
    }

    /**
     * Generate business validation report
     */
    generateBusinessValidationReport(validationData) {
        const validation = this.performBusinessValidation(validationData);

        return {
            componentName: validationData.componentName,
            timestamp: new Date().toISOString(),
            overallScore: this.calculateWeightedScore(validation.breakdown),
            validation: validation,
            recommendations: this.generateBusinessRecommendations(validation),
            riskAssessment: this.assessBusinessRisk(validation)
        };
    }

    /**
     * Generate business recommendations
     */
    generateBusinessRecommendations(validation) {
        const recommendations = [];

        if (!validation.valid) {
            recommendations.push('Address all business validation issues for production readiness');
        }

        if (validation.score < 70) {
            recommendations.push('Improve overall business validation score above 70%');
        }

        validation.issues.forEach(issue => {
            if (issue.includes('V2 compliant')) {
                recommendations.push('Achieve V2 compliance through refactoring and modernization');
            } else if (issue.includes('complexity')) {
                recommendations.push('Reduce code complexity through modularization and refactoring');
            } else if (issue.includes('security')) {
                recommendations.push('Address security vulnerabilities and implement best practices');
            }
        });

        return recommendations;
    }

    /**
     * Assess business risk
     */
    assessBusinessRisk(validation) {
        if (validation.score >= 90) return 'low';
        if (validation.score >= 70) return 'medium';
        if (validation.score >= 50) return 'high';
        return 'critical';
    }

    /**
     * Get business validation metrics
     */
    getBusinessValidationMetrics() {
        return {
            rulesRegistered: this.businessRules.size,
            scoringWeights: this.scoringWeights,
            categories: Object.keys(this.scoringWeights)
        };
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create business validation module instance
 */
export function createBusinessValidationModule() {
    return new BusinessValidationModule();
}

