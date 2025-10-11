/**
 * Vector Database Manager - V2 Compliant Module
 * ============================================
 *
 * Main manager that coordinates all vector database modules.
 * Provides unified API and manages module interactions.
 *
 * V2 Compliance: < 300 lines, single responsibility.
 *
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

import { VectorDatabaseCore } from './core.js';
import { VectorDatabaseUIOptimized as VectorDatabaseUI } from './ui-optimized.js';
import { VectorDatabaseSearch } from './search.js';
import { VectorDatabaseAnalytics } from './analytics.js';

export class VectorDatabaseManager {
    constructor() {
        this.core = new VectorDatabaseCore();
        this.ui = new VectorDatabaseUI();
        this.search = new VectorDatabaseSearch(this.core);
        this.analytics = new VectorDatabaseAnalytics();

        this.initialized = false;
        this.logger = console;

        this.setupEventListeners();
    }

    /**
     * Initialize the vector database interface
     */
    async initialize() {
        try {
            this.logger.log('🚀 Initializing Vector Database Manager...');

            // Initialize core
            await this.core.initializeVectorDatabase();

            // Initialize UI
            this.ui.initializeUI();

            // Initialize analytics
            this.analytics.initialize();

            // Load initial data
            await this.loadInitialData();

            this.initialized = true;
            this.logger.log('✅ Vector Database Manager initialized successfully');

            return true;
        } catch (error) {
            this.logger.error('❌ Failed to initialize Vector Database Manager:', error);
            this.ui.showError('Failed to initialize interface. Please refresh the page.');
            throw error;
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Search events
        document.addEventListener('search', (event) => {
            this.handleSearch(event.detail.query);
        });

        // Document events
        document.addEventListener('addDocument', () => {
            this.handleAddDocument();
        });

        // Analytics events
        document.addEventListener('analyticsUpdate', () => {
            this.updateAnalytics();
        });
    }

    /**
     * Handle search request
     */
    async handleSearch(query) {
        try {
            const startTime = Date.now();

            // Perform search
            const results = await this.search.search(query);

            // Record analytics
            const responseTime = Date.now() - startTime;
            this.analytics.recordSearchQuery(query, results.length, responseTime);

            // Display results
            this.ui.displaySearchResults(results);

            // Update analytics display
            this.updateAnalytics();

            this.logger.log(`🔍 Search completed: "${query}" (${results.length} results)`);
        } catch (error) {
            this.logger.error('❌ Search failed:', error);
            this.ui.showError('Search failed. Please try again.');
            this.analytics.recordError(error, 'search');
        }
    }

    /**
     * Handle add document request
     */
    async handleAddDocument() {
        try {
            // Create sample document
            const document = {
                title: `Document ${Date.now()}`,
                content: 'This is a sample document created by the interface.',
                metadata: {
                    type: 'sample',
                    created: Date.now()
                }
            };

            // Add document
            const addedDoc = await this.core.addDocument(document);

            // Record analytics
            this.analytics.recordDocumentOperation('add', addedDoc.id, true);

            // Update UI
            await this.loadInitialData();
            this.ui.showSuccess('Document added successfully');

            this.logger.log(`📄 Document added: ${addedDoc.id}`);
        } catch (error) {
            this.logger.error('❌ Failed to add document:', error);
            this.ui.showError('Failed to add document. Please try again.');
            this.analytics.recordError(error, 'addDocument');
        }
    }

    /**
     * Load initial data
     */
    async loadInitialData() {
        try {
            // Load documents
            const documents = await this.core.getAllDocuments();
            this.ui.displayDocuments(documents);

            // Update analytics
            this.updateAnalytics();

            this.logger.log(`📊 Loaded ${documents.length} documents`);
        } catch (error) {
            this.logger.error('❌ Failed to load initial data:', error);
            this.analytics.recordError(error, 'loadInitialData');
        }
    }

    /**
     * Update analytics display
     */
    updateAnalytics() {
        const metrics = this.analytics.getMetrics();
        this.ui.displayAnalytics(metrics);
    }

    /**
     * Get system status
     */
    getSystemStatus() {
        return {
            initialized: this.initialized,
            core: this.core.getStatus(),
            analytics: this.analytics.getMetrics(),
            search: this.search.getSearchStats()
        };
    }

    /**
     * Get performance metrics
     */
    getPerformanceMetrics() {
        return {
            analytics: this.analytics.getPerformanceSummary(),
            search: this.search.getSearchStats(),
            core: this.core.getCacheStats()
        };
    }

    /**
     * Export all data
     */
    async exportData() {
        try {
            const documents = await this.core.getAllDocuments();
            const analytics = this.analytics.exportAnalytics();
            const search = this.search.exportSearchData();

            return {
                documents,
                analytics,
                search,
                exportedAt: new Date().toISOString()
            };
        } catch (error) {
            this.logger.error('❌ Failed to export data:', error);
            throw error;
        }
    }

    /**
     * Generate system report
     */
    generateReport() {
        return {
            status: this.getSystemStatus(),
            performance: this.getPerformanceMetrics(),
            analytics: this.analytics.generateReport(),
            recommendations: this.getRecommendations()
        };
    }

    /**
     * Get system recommendations
     */
    getRecommendations() {
        const recommendations = [];
        const status = this.getSystemStatus();
        const performance = this.getPerformanceMetrics();

        // Check system health
        if (!status.initialized) {
            recommendations.push('System not properly initialized - restart required');
        }

        // Check performance
        if (performance.analytics.averageResponseTime > 1000) {
            recommendations.push('Consider optimizing search performance');
        }

        // Check error rate
        const errorRate = status.analytics.errorCount / Math.max(status.analytics.searchQueries, 1);
        if (errorRate > 0.1) {
            recommendations.push('High error rate detected - investigate issues');
        }

        return recommendations;
    }

    /**
     * Cleanup resources
     */
    cleanup() {
        try {
            this.ui.cleanup();
            this.search.clearSearchCache();
            this.analytics.resetAnalytics();

            this.logger.log('🧹 Vector Database Manager cleaned up');
        } catch (error) {
            this.logger.error('❌ Error during cleanup:', error);
        }
    }

    /**
     * Restart system
     */
    async restart() {
        try {
            this.logger.log('🔄 Restarting Vector Database Manager...');

            this.cleanup();
            await this.initialize();

            this.logger.log('✅ Vector Database Manager restarted successfully');
        } catch (error) {
            this.logger.error('❌ Failed to restart Vector Database Manager:', error);
            throw error;
        }
    }
}
