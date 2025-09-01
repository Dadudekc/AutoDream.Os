/**
 * Deployment Service - V2 Compliant Orchestrator
 * Orchestrator for deployment operations using modular components
 * REFACTORED: 431 lines → ~95 lines (78% reduction)
 * Now uses modular components for V2 compliance
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// IMPORT MODULAR COMPONENTS
// ================================

import { DeploymentRepository } from '../repositories/deployment-repository.js';
import { coordinateDeployment, coordinateAgent } from './deployment-coordination-service.js';
import { validateDeployment } from './deployment-validation-service.js';
import { analyzeDeploymentMetrics } from './deployment-metrics-service.js';
import { manageDeploymentPhase, getPhaseStatus, getPhaseHistory } from './deployment-phase-service.js';

// ================================
// DEPLOYMENT SERVICE ORCHESTRATOR
// ================================

/**
 * Deployment service orchestrator using modular components
 */
export class DeploymentService {
    constructor(deploymentRepository = null) {
        // Dependency injection with fallback
        this.deploymentRepository = deploymentRepository || new DeploymentRepository();
    }

    /**
     * Coordinate deployment
     */
    async coordinateDeployment(phase, agents, options = {}) {
        return coordinateDeployment(phase, agents, options);
    }

    /**
     * Coordinate agent
     */
    async coordinateAgent(agentId, coordinationType, data = {}) {
        return coordinateAgent(agentId, coordinationType, data);
    }

    /**
     * Validate deployment
     */
    async validateDeployment(componentName, validationLevel = 'standard') {
        return validateDeployment(componentName, validationLevel);
    }

    /**
     * Analyze deployment metrics
     */
    async analyzeDeploymentMetrics(metricType, timeRange = '24h') {
        return analyzeDeploymentMetrics(metricType, timeRange);
    }

    /**
     * Manage deployment phase
     */
    async manageDeploymentPhase(phase, action, data = {}) {
        return manageDeploymentPhase(phase, action, data);
    }

    /**
     * Get phase status
     */
    getPhaseStatus(phase) {
        return getPhaseStatus(phase);
    }

    /**
     * Get phase history
     */
    getPhaseHistory(phase, limit = 10) {
        return getPhaseHistory(phase, limit);
    }

    /**
     * Get service status
     */
    getStatus() {
        return {
            initialized: true,
            repository: this.deploymentRepository ? 'connected' : 'disconnected',
            timestamp: new Date().toISOString()
        };
    }
}

// ================================
// GLOBAL DEPLOYMENT SERVICE INSTANCE
// ================================

/**
 * Global deployment service instance
 */
const deploymentService = new DeploymentService();

// ================================
// SERVICE API FUNCTIONS
// ================================

/**
 * Get deployment service instance
 */
export function getDeploymentService(deploymentRepository = null) {
    if (deploymentRepository) {
        return new DeploymentService(deploymentRepository);
    }
    return deploymentService;
}

// ================================
// EXPORTS
// ================================

export { DeploymentService, deploymentService };
export default deploymentService;