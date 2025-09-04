/**
 * Deployment Coordination Orchestrator - V2 Compliant
 * Main orchestrator for deployment coordination service
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

import { createCoordinationCoreModule } from './coordination-core-module.js';
import { createAgentCoordinationModule } from './agent-coordination-module.js';
import { createCoordinationReportingModule } from './coordination-reporting-module.js';

// ================================
// DEPLOYMENT COORDINATION ORCHESTRATOR
// ================================

/**
 * Main orchestrator for deployment coordination service
 */
export class DeploymentCoordinationOrchestrator {
    constructor(deploymentRepository = null) {
        this.deploymentRepository = deploymentRepository;
        this.modules = new Map();

        // Initialize modules
        this.modules.set('core', createCoordinationCoreModule());
        this.modules.set('agent', createAgentCoordinationModule());
        this.modules.set('reporting', createCoordinationReportingModule());
    }

    /**
     * Coordinate deployment across phases and agents
     */
    async coordinateDeployment(phase, agents, options = {}) {
        try {
            const result = await this.modules.get('core').coordinateDeployment(phase, agents, options);

            // Update deployment status if repository available
            if (this.deploymentRepository) {
                this.deploymentRepository.updateDeploymentPhase(phase, result.status);
            }

            return result;
        } catch (error) {
            console.error('Deployment coordination failed:', error);
            throw error;
        }
    }

    /**
     * Coordinate individual agent
     */
    async coordinateAgent(agentId, coordinationType, data = {}) {
        try {
            const result = await this.modules.get('agent').coordinateAgent(agentId, coordinationType, data);

            // Store coordination result if repository available
            if (this.deploymentRepository) {
                this.deploymentRepository.storeCoordinationResult(agentId, result);
            }

            return result;
        } catch (error) {
            console.error(`Agent coordination failed for ${agentId}:`, error);
            throw error;
        }
    }

    /**
     * Generate coordination report
     */
    generateCoordinationReport(agentId, coordinationResult) {
        return this.modules.get('reporting').generateCoordinationReport(agentId, coordinationResult);
    }

    /**
     * Generate deployment coordination summary
     */
    generateDeploymentSummary(deploymentResult) {
        return this.modules.get('reporting').generateDeploymentSummary(deploymentResult);
    }

    /**
     * Generate coordination metrics report
     */
    generateMetricsReport(coordinationHistory) {
        return this.modules.get('reporting').generateMetricsReport(coordinationHistory);
    }

    /**
     * Validate deployment phase
     */
    validateDeploymentPhase(phase) {
        return this.modules.get('core').validateDeploymentPhase(phase);
    }

    /**
     * Validate agent coordination configuration
     */
    validateAgentCoordination(agents) {
        return this.modules.get('core').validateAgentCoordination(agents);
    }

    /**
     * Validate agent coordination request
     */
    validateAgentCoordinationRequest(agentId, coordinationType) {
        return this.modules.get('agent').validateAgentCoordinationRequest(agentId, coordinationType);
    }

    /**
     * Get orchestrator status
     */
    getStatus() {
        return {
            modules: Array.from(this.modules.keys()),
            repositoryAvailable: !!this.deploymentRepository,
            timestamp: new Date().toISOString()
        };
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Legacy DeploymentCoordinationService class for backward compatibility
 * @deprecated Use DeploymentCoordinationOrchestrator instead
 */
export class DeploymentCoordinationService extends DeploymentCoordinationOrchestrator {
    constructor(deploymentRepository = null) {
        super(deploymentRepository);
        console.warn('[DEPRECATED] DeploymentCoordinationService is deprecated. Use DeploymentCoordinationOrchestrator instead.');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create deployment coordination orchestrator instance
 */
export function createDeploymentCoordinationOrchestrator(deploymentRepository = null) {
    return new DeploymentCoordinationOrchestrator(deploymentRepository);
}

/**
 * Create legacy deployment coordination service (backward compatibility)
 */
export function createDeploymentCoordinationService(deploymentRepository = null) {
    return new DeploymentCoordinationService(deploymentRepository);
}

