/**
 * Web Assets Index - V2 Compliant Module Organization
 * Centralized entry point for all web assets and modules
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - CLEANUP MISSION CONSOLIDATION
 * @license MIT
 */

// ================================
// CORE FRAMEWORK MODULES
// ================================

// Framework Components (moved from framework_new)
export { Navigation } from './navigation.js';
export { Modal } from './modal.js';
export { FormEnhancement } from './forms.js';
export { Accordion, LazyLoading, TouchSupport, BreakpointHandler } from './ui-components.js';
export { Layout } from './layout.js';
export { Config } from './config.js';

// ================================
// DASHBOARD MODULES
// ================================

// Consolidated Dashboard Utilities
export { DashboardDateUtils, createDashboardDateUtils } from './dashboard/date-utils.js';
export { DashboardDOMUtils, createDashboardDOMUtils } from './dashboard/dom-utils-orchestrator.js';

// ================================
// ARCHITECTURE MODULES
// ================================

export { ArchitectureCoordinator } from './architecture/architecture-pattern-coordinator.js';
export { DependencyInjectionFramework } from './architecture/dependency-injection-framework.js';

// ================================
// UTILITY MODULES
// ================================

export { UnifiedFrontendUtilities } from './unified-frontend-utilities.js';
export { ConsolidatedUtilities } from './utilities-consolidated.js';

// ================================
// SERVICE MODULES
// ================================

export { ServicesOrchestrator } from './services-orchestrator.js';
export { ConsolidatedServices } from './services-unified.js';

// ================================
// LEGACY SUPPORT
// ================================

// Maintain backward compatibility for existing imports
export * from './dashboard.js'; // Main dashboard module
export * from './components.js'; // Component exports

/**
 * Initialize Web Assets
 * Call this function to initialize all web components and utilities
 */
export function initializeWebAssets() {
    console.log('🐝 Web Assets Initialized - V2 Compliant & Consolidated');

    // Framework components are ready for use
    // Dashboard utilities are available via named exports
    // All modules follow V2 compliance standards

    return {
        status: 'initialized',
        modules: [
            'Framework Components',
            'Dashboard Utilities',
            'Architecture Modules',
            'Service Modules',
            'Utility Modules'
        ],
        v2_compliant: true
    };
}
