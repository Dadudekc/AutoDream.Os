/**
 * Deployment Phase Service - V2 Compliant
 * Phase management functionality extracted from deployment-service.js
 *
 * @author Agent-3 - Infrastructure & DevOps Specialist
 * @version 2.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

import { createPhaseActionMethods } from './phase-action-methods.js';

// ================================
// DEPLOYMENT PHASE SERVICE
// ================================

/**
 * Deployment phase management functionality
 */
class DeploymentPhaseService {
    constructor() {
        this.deploymentPhases = new Map();
        this.phaseHistory = new Map();
        this.phaseActionMethods = createPhaseActionMethods();
    }

    /**
     * Manage deployment phase
     */
    async manageDeploymentPhase(phase, action, data = {}) {
        try {
            if (!this.validatePhaseManagementRequest(phase, action)) {
                throw new Error('Invalid phase management request');
            }

            // Get current phase status
            const currentStatus = this.deploymentPhases.get(phase) || {
                phase: phase,
                status: 'not_started',
                lastUpdated: null
            };

            // Execute phase action
            const actionResult = await this.phaseActionMethods.executePhaseAction(phase, action, currentStatus, data);

            // Update phase status
            const updatedStatus = {
                ...currentStatus,
                status: actionResult.newStatus,
                lastUpdated: new Date().toISOString(),
                lastAction: action,
                actionData: data
            };

            this.deploymentPhases.set(phase, updatedStatus);

            // Store in history
            this.storePhaseHistory(phase, action, actionResult);

            return actionResult;

        } catch (error) {
            console.error(`Phase management failed for ${phase}:${action}:`, error);
            throw error;
        }
    }

    /**
     * Validate phase management request
     */
    validatePhaseManagementRequest(phase, action) {
        if (!phase || !action) {
            return false;
        }

        const validPhases = ['development', 'staging', 'production', 'rollback', 'maintenance'];
        const validActions = ['start', 'stop', 'pause', 'resume', 'rollback', 'validate', 'promote'];

        return validPhases.includes(phase) && validActions.includes(action);
    }



    /**
     * Get phase status
     */
    getPhaseStatus(phase) {
        return this.deploymentPhases.get(phase) || {
            phase: phase,
            status: 'not_started',
            lastUpdated: null
        };
    }

    /**
     * Get all phase statuses
     */
    getAllPhaseStatuses() {
        const statuses = {};
        for (const [phase, status] of this.deploymentPhases) {
            statuses[phase] = status;
        }
        return statuses;
    }

    /**
     * Store phase history
     */
    storePhaseHistory(phase, action, actionResult) {
        if (!this.phaseHistory.has(phase)) {
            this.phaseHistory.set(phase, []);
        }

        const history = this.phaseHistory.get(phase);
        history.push({
            action: action,
            result: actionResult,
            timestamp: new Date().toISOString()
        });

        // Keep only last 50 entries per phase
        if (history.length > 50) {
            history.shift();
        }
    }

    /**
     * Get phase history
     */
    getPhaseHistory(phase, limit = 10) {
        const history = this.phaseHistory.get(phase) || [];
        return history.slice(-limit);
    }

    /**
     * Reset phase
     */
    resetPhase(phase) {
        this.deploymentPhases.set(phase, {
            phase: phase,
            status: 'not_started',
            lastUpdated: new Date().toISOString(),
            resetReason: 'manual_reset'
        });

        console.log(`Phase ${phase} reset to initial state`);
    }
}

// ================================
// GLOBAL PHASE SERVICE INSTANCE
// ================================

/**
 * Global deployment phase service instance
 */
const deploymentPhaseService = new DeploymentPhaseService();

// ================================
// PHASE SERVICE API FUNCTIONS
// ================================

/**
 * Manage deployment phase
 */
export function manageDeploymentPhase(phase, action, data = {}) {
    return deploymentPhaseService.manageDeploymentPhase(phase, action, data);
}

/**
 * Get phase status
 */
export function getPhaseStatus(phase) {
    return deploymentPhaseService.getPhaseStatus(phase);
}

/**
 * Get phase history
 */
export function getPhaseHistory(phase, limit = 10) {
    return deploymentPhaseService.getPhaseHistory(phase, limit);
}

// ================================
// EXPORTS
// ================================

export { DeploymentPhaseService, deploymentPhaseService };
export default deploymentPhaseService;
