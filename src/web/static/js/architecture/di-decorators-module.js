/**
 * DI Decorators Module - V2 Compliant
 * Dependency injection decorators and utilities
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// DEPENDENCY INJECTION DECORATORS
// ================================

/**
 * Injectable decorator for service classes
 */
export function Injectable(token) {
    return function(target) {
        target.injectableToken = token;
        return target;
    };
}

/**
 * Inject decorator for constructor parameters
 */
export function Inject(token) {
    return function(target, propertyKey, parameterIndex) {
        if (!target.injections) {
            target.injections = [];
        }
        target.injections[parameterIndex] = token;
    };
}

/**
 * Service decorator for automatic registration
 */
export function Service(options = {}) {
    return function(target) {
        const token = options.token || target.name;
        Injectable(token)(target);

        // Add metadata for service configuration
        target.serviceOptions = {
            singleton: options.singleton !== false,
            scope: options.scope || 'global',
            dependencies: options.dependencies || []
        };

        return target;
    };
}

/**
 * Factory decorator for service factories
 */
export function Factory(token) {
    return function(target, propertyKey, descriptor) {
        const originalMethod = descriptor.value;
        descriptor.value = function(...args) {
            const result = originalMethod.apply(this, args);
            // Register the factory result if token is provided
            if (token && this.registerService) {
                this.registerService(token, () => result);
            }
            return result;
        };
        return descriptor;
    };
}

// ================================
// DECORATOR UTILITIES
// ================================

/**
 * Get injectable token from class
 */
export function getInjectableToken(target) {
    return target.injectableToken;
}

/**
 * Get injection metadata from class
 */
export function getInjectionMetadata(target) {
    return {
        token: target.injectableToken,
        injections: target.injections || [],
        serviceOptions: target.serviceOptions || {}
    };
}

/**
 * Check if class is injectable
 */
export function isInjectable(target) {
    return !!target.injectableToken;
}

/**
 * Get service configuration from class
 */
export function getServiceConfig(target) {
    return target.serviceOptions || {};
}

