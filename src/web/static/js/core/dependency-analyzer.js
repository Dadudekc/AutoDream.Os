/**
 * Dependency Analyzer Module - V2 Compliant
 * Dependency graph analysis and validation utilities
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class DependencyAnalyzer {
    constructor(serviceRegistry, logger = console) {
        this.registry = serviceRegistry;
        this.logger = logger;
    }

    /**
     * Analyze dependency graph for issues
     */
    analyzeGraph() {
        const issues = [];
        const serviceNames = this.registry.getServiceNames();

        for (const serviceName of serviceNames) {
            const serviceIssues = this.analyzeService(serviceName);
            issues.push(...serviceIssues);
        }

        return {
            totalServices: serviceNames.length,
            issues: issues,
            hasCircularDependencies: issues.some(issue => issue.type === 'circular_dependency'),
            hasMissingDependencies: issues.some(issue => issue.type === 'missing_dependency'),
            isValid: issues.length === 0
        };
    }

    /**
     * Analyze individual service for dependency issues
     */
    analyzeService(serviceName) {
        const issues = [];
        const config = this.registry.getServiceConfig(serviceName);

        if (!config) {
            issues.push({
                type: 'service_not_found',
                service: serviceName,
                message: `Service '${serviceName}' not found in registry`
            });
            return issues;
        }

        // Check for missing dependencies
        for (const dep of config.dependencies) {
            const depName = typeof dep === 'string' ? dep : dep.service;
            const isOptional = typeof dep === 'object' && dep.optional === true;

            if (!this.registry.isRegistered(depName) && !isOptional) {
                issues.push({
                    type: 'missing_dependency',
                    service: serviceName,
                    dependency: depName,
                    message: `Missing required dependency '${depName}' for service '${serviceName}'`
                });
            }
        }

        // Check for circular dependencies
        const circularPath = this.detectCircularDependency(serviceName);
        if (circularPath.length > 1) {
            issues.push({
                type: 'circular_dependency',
                service: serviceName,
                path: circularPath,
                message: `Circular dependency detected: ${circularPath.join(' -> ')}`
            });
        }

        return issues;
    }

    /**
     * Detect circular dependencies using DFS
     */
    detectCircularDependency(serviceName, visited = new Set(), path = []) {
        if (visited.has(serviceName)) {
            // Found cycle
            const cycleStart = path.indexOf(serviceName);
            return path.slice(cycleStart);
        }

        visited.add(serviceName);
        path.push(serviceName);

        const config = this.registry.getServiceConfig(serviceName);
        if (config) {
            for (const dep of config.dependencies) {
                const depName = typeof dep === 'string' ? dep : dep.service;
                const cycle = this.detectCircularDependency(depName, visited, [...path]);
                if (cycle.length > 0) {
                    return cycle;
                }
            }
        }

        path.pop();
        return [];
    }

    /**
     * Get dependency tree for a service
     */
    getDependencyTree(serviceName, depth = 10, currentDepth = 0) {
        if (currentDepth >= depth) {
            return { name: serviceName, dependencies: [], truncated: true };
        }

        const config = this.registry.getServiceConfig(serviceName);
        if (!config) {
            return { name: serviceName, dependencies: [], error: 'Service not found' };
        }

        const dependencies = [];
        for (const dep of config.dependencies) {
            const depName = typeof dep === 'string' ? dep : dep.service;
            dependencies.push(this.getDependencyTree(depName, depth, currentDepth + 1));
        }

        return {
            name: serviceName,
            dependencies: dependencies,
            singleton: config.singleton,
            factory: !!config.factory
        };
    }

    /**
     * Find services that depend on a given service
     */
    findDependents(serviceName) {
        const dependents = [];
        const serviceNames = this.registry.getServiceNames();

        for (const name of serviceNames) {
            const config = this.registry.getServiceConfig(name);
            if (config) {
                const dependsOnService = config.dependencies.some(dep => {
                    const depName = typeof dep === 'string' ? dep : dep.service;
                    return depName === serviceName;
                });

                if (dependsOnService) {
                    dependents.push(name);
                }
            }
        }

        return dependents;
    }

    /**
     * Get dependency statistics
     */
    getDependencyStats() {
        const stats = {
            totalServices: 0,
            servicesWithDependencies: 0,
            totalDependencies: 0,
            averageDependencies: 0,
            mostDependencies: { service: null, count: 0 },
            leastDependencies: { service: null, count: Infinity },
            circularDependencies: 0,
            missingDependencies: 0
        };

        const serviceNames = this.registry.getServiceNames();
        stats.totalServices = serviceNames.length;

        for (const name of serviceNames) {
            const config = this.registry.getServiceConfig(name);
            if (config) {
                const depCount = config.dependencies.length;
                stats.totalDependencies += depCount;

                if (depCount > 0) {
                    stats.servicesWithDependencies++;
                }

                if (depCount > stats.mostDependencies.count) {
                    stats.mostDependencies = { service: name, count: depCount };
                }

                if (depCount < stats.leastDependencies.count) {
                    stats.leastDependencies = { service: name, count: depCount };
                }
            }
        }

        stats.averageDependencies = stats.totalServices > 0 ?
            (stats.totalDependencies / stats.totalServices).toFixed(2) : 0;

        if (stats.leastDependencies.count === Infinity) {
            stats.leastDependencies = { service: null, count: 0 };
        }

        // Analyze for issues
        const analysis = this.analyzeGraph();
        stats.circularDependencies = analysis.issues.filter(i => i.type === 'circular_dependency').length;
        stats.missingDependencies = analysis.issues.filter(i => i.type === 'missing_dependency').length;

        return stats;
    }

    /**
     * Validate dependency graph
     */
    validateGraph() {
        const analysis = this.analyzeGraph();

        return {
            isValid: analysis.isValid,
            summary: {
                totalServices: analysis.totalServices,
                totalIssues: analysis.issues.length,
                circularDependencies: analysis.hasCircularDependencies,
                missingDependencies: analysis.hasMissingDependencies
            },
            issues: analysis.issues,
            recommendations: this.generateRecommendations(analysis)
        };
    }

    /**
     * Generate recommendations based on analysis
     */
    generateRecommendations(analysis) {
        const recommendations = [];

        if (analysis.hasCircularDependencies) {
            recommendations.push({
                type: 'warning',
                message: 'Circular dependencies detected. Consider using dependency injection or service locator pattern.',
                priority: 'high'
            });
        }

        if (analysis.hasMissingDependencies) {
            recommendations.push({
                type: 'error',
                message: 'Missing dependencies found. Ensure all required services are registered.',
                priority: 'critical'
            });
        }

        const stats = this.getDependencyStats();
        if (stats.mostDependencies.count > 5) {
            recommendations.push({
                type: 'info',
                message: `Service '${stats.mostDependencies.service}' has many dependencies (${stats.mostDependencies.count}). Consider breaking it down.`,
                priority: 'medium'
            });
        }

        return recommendations;
    }
}

// Factory function for creating dependency analyzer instance
export function createDependencyAnalyzer(serviceRegistry, logger = console) {
    return new DependencyAnalyzer(serviceRegistry, logger);
}


