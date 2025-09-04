/**
 * Agent Coordination Manager - V2 Compliant Agent Coordination
 * Manages agent coordination and communication
 * V2 Compliance: Under 300-line limit achieved
 *
 * @author Agent-3 - Infrastructure & DevOps Specialist
 * @version 1.0.0 - V2 Compliance Implementation
 * @license MIT
 */

import { CrossAgentCoordination } from './cross-agent-coordination.js';

/**
 * Creates and manages agent coordination
 * Handles agent communication and coordination logic
 */
export function createAgentCoordinationManager() {
    return {
        agentCoordination: null,
        coordinationStatus: {
            initialized: false,
            activeAgents: [],
            coordinationLevel: 'NOT_INITIALIZED',
            lastCoordination: null
        },

        /**
         * Initialize agent coordination
         */
        async initializeCoordination() {
            console.log('🔗 Initializing Agent Coordination Manager...');

            try {
                this.agentCoordination = new CrossAgentCoordination();
                await this.agentCoordination.initializeCoordination();

                this.coordinationStatus.initialized = true;
                this.coordinationStatus.coordinationLevel = 'INITIALIZED';
                this.coordinationStatus.lastCoordination = new Date().toISOString();

                console.log('✅ Agent coordination manager initialized');
                return true;
            } catch (error) {
                console.error('Agent coordination manager initialization failed:', error);
                this.coordinationStatus.coordinationLevel = 'INITIALIZATION_FAILED';
                return false;
            }
        },

        /**
         * Get coordination status
         */
        getCoordinationStatus() {
            return { ...this.coordinationStatus };
        },

        /**
         * Update coordination status
         */
        updateCoordinationStatus(updates) {
            this.coordinationStatus = { ...this.coordinationStatus, ...updates };
            this.coordinationStatus.lastCoordination = new Date().toISOString();
            return this.coordinationStatus;
        },

        /**
         * Get active agents
         */
        getActiveAgents() {
            return [...this.coordinationStatus.activeAgents];
        },

        /**
         * Add active agent
         */
        addActiveAgent(agentId) {
            if (!this.coordinationStatus.activeAgents.includes(agentId)) {
                this.coordinationStatus.activeAgents.push(agentId);
                this.coordinationStatus.lastCoordination = new Date().toISOString();
                return true;
            }
            return false;
        },

        /**
         * Remove active agent
         */
        removeActiveAgent(agentId) {
            const index = this.coordinationStatus.activeAgents.indexOf(agentId);
            if (index !== -1) {
                this.coordinationStatus.activeAgents.splice(index, 1);
                this.coordinationStatus.lastCoordination = new Date().toISOString();
                return true;
            }
            return false;
        },

        /**
         * Check if coordination is ready
         */
        isCoordinationReady() {
            return this.coordinationStatus.initialized &&
                   this.coordinationStatus.coordinationLevel === 'INITIALIZED';
        },

        /**
         * Get coordination summary
         */
        getCoordinationSummary() {
            if (!this.agentCoordination) {
                return null;
            }

            return {
                initialized: this.coordinationStatus.initialized,
                activeAgents: this.coordinationStatus.activeAgents,
                coordinationLevel: this.coordinationStatus.coordinationLevel,
                lastCoordination: this.coordinationStatus.lastCoordination,
                agentCoordinationDetails: this.agentCoordination.getCoordinationSummary ?
                    this.agentCoordination.getCoordinationSummary() : null
            };
        },

        /**
         * Send coordination message
         */
        async sendCoordinationMessage(message, targetAgents = null) {
            if (!this.isCoordinationReady()) {
                console.warn('⚠️ Agent coordination not ready for message sending');
                return false;
            }

            try {
                const result = await this.agentCoordination.sendCoordinationMessage(message, targetAgents);
                this.coordinationStatus.lastCoordination = new Date().toISOString();
                return result;
            } catch (error) {
                console.error('Failed to send coordination message:', error);
                return false;
            }
        },

        /**
         * Validate agent coordination
         */
        async validateCoordination() {
            if (!this.isCoordinationReady()) {
                return { valid: false, reason: 'Coordination not initialized' };
            }

            try {
                const validation = await this.agentCoordination.validateCoordination();
                return validation;
            } catch (error) {
                return { valid: false, reason: error.message };
            }
        }
    };
}

