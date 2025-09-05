/**
 * Vector Database Web Interface V2 - V2 Compliant
 * ===============================================
 * 
 * Modular vector database web interface using V2 compliant architecture.
 * Coordinates specialized modules for clean separation of concerns.
 * 
 * V2 Compliance: < 300 lines, modular design, single responsibility.
 * 
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

import { VectorDatabaseManager } from './vector-database/manager.js';

export class VectorDatabaseWebInterface {
    constructor() {
        this.manager = new VectorDatabaseManager();
        this.logger = console;
    }

    /**
     * Initialize the vector database web interface
     */
    async initializeInterface() {
        try {
            await this.manager.initialize();
            this.logger.log('✅ Vector Database Web Interface V2 initialized successfully');
        } catch (error) {
            this.logger.error('❌ Failed to initialize Vector Database Web Interface V2:', error);
            throw error;
        }
    }

    /**
     * Get system status
     */
    getSystemStatus() {
        return this.manager.getSystemStatus();
    }

    /**
     * Get performance metrics
     */
    getPerformanceMetrics() {
        return this.manager.getPerformanceMetrics();
    }

    /**
     * Generate system report
     */
    generateReport() {
        return this.manager.generateReport();
    }

    /**
     * Export all data
     */
    async exportData() {
        return await this.manager.exportData();
    }

    /**
     * Restart system
     */
    async restart() {
        return await this.manager.restart();
    }

    /**
     * Cleanup resources
     */
    cleanup() {
        this.manager.cleanup();
    }
}

// Backward compatibility
export default VectorDatabaseWebInterface;
