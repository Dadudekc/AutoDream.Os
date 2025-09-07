/**
 * Vector Database UI - V2 Compliant Module
 * UI components and interactions for vector database.
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

import {
    setupSearchInterface as setupSearchInterfaceCommon,
    setupDocumentManagement as setupDocumentManagementCommon,
    showError as showErrorCommon,
    showSuccess as showSuccessCommon
} from './ui-common.js';

export class VectorDatabaseUI {
    constructor() {
        this.elements = {};
        this.eventListeners = new Map();
        this.logger = console;
    }

    /**
     * Initialize UI components
     */
    initializeUI() {
        try {
            this.setupSearchInterface();
            this.setupDocumentManagement();
            this.setupAnalyticsDashboard();
            this.setupRealTimeUpdates();
            
            this.logger.log('✅ Vector Database UI initialized');
        } catch (error) {
            this.logger.error('❌ Failed to initialize UI:', error);
            throw error;
        }
    }

    /**
     * Setup search interface
     */
    setupSearchInterface() {
        setupSearchInterfaceCommon({
            createElement: this.createElement.bind(this),
            elements: this.elements,
            addEventListener: this.addEventListener.bind(this),
            handleSearch: this.handleSearch.bind(this)
        });
    }

    /**
     * Setup document management interface
     */
    setupDocumentManagement() {
        setupDocumentManagementCommon({
            createElement: this.createElement.bind(this),
            elements: this.elements,
            addEventListener: this.addEventListener.bind(this),
            handleAddDocument: this.handleAddDocument.bind(this)
        });
    }

    /**
     * Setup analytics dashboard
     */
    setupAnalyticsDashboard() {
        const analyticsContainer = this.createElement('div', 'analytics-container');
        const metricsDisplay = this.createElement('div', 'metrics-display', { id: 'metrics-display' });
        const chartsContainer = this.createElement('div', 'charts-container', { id: 'charts-container' });

        analyticsContainer.appendChild(metricsDisplay);
        analyticsContainer.appendChild(chartsContainer);
        
        this.elements.analyticsContainer = analyticsContainer;
        this.elements.metricsDisplay = metricsDisplay;
        this.elements.chartsContainer = chartsContainer;
    }

    /**
     * Setup real-time updates
     */
    setupRealTimeUpdates() {
        const updateContainer = this.createElement('div', 'update-container');
        const statusIndicator = this.createElement('div', 'status-indicator', { id: 'status-indicator' });
        const lastUpdate = this.createElement('div', 'last-update', { id: 'last-update' });

        updateContainer.appendChild(statusIndicator);
        updateContainer.appendChild(lastUpdate);
        
        this.elements.updateContainer = updateContainer;
        this.elements.statusIndicator = statusIndicator;
        this.elements.lastUpdate = lastUpdate;
    }

    /**
     * Create DOM element
     */
    createElement(tag, className, attributes = {}, textContent = '') {
        const element = document.createElement(tag);
        element.className = className;
        
        Object.entries(attributes).forEach(([key, value]) => {
            element.setAttribute(key, value);
        });
        
        if (textContent) {
            element.textContent = textContent;
        }
        
        return element;
    }

    /**
     * Add event listener
     */
    addEventListener(element, event, handler) {
        const key = `${element.id || element.className}-${event}`;
        this.eventListeners.set(key, { element, event, handler });
        element.addEventListener(event, handler);
    }

    /**
     * Remove event listener
     */
    removeEventListener(element, event) {
        const key = `${element.id || element.className}-${event}`;
        const listener = this.eventListeners.get(key);
        if (listener) {
            listener.element.removeEventListener(event, listener.handler);
            this.eventListeners.delete(key);
        }
    }

    /**
     * Handle search action
     */
    handleSearch() {
        const query = this.elements.searchInput.value.trim();
        if (!query) return;

        // Emit search event
        this.emitEvent('search', { query });
    }

    /**
     * Handle add document action
     */
    handleAddDocument() {
        // Emit add document event
        this.emitEvent('addDocument', {});
    }

    /**
     * Emit custom event
     */
    emitEvent(eventName, data) {
        const event = new CustomEvent(eventName, { detail: data });
        document.dispatchEvent(event);
    }

    /**
     * Display search results
     */
    displaySearchResults(results) {
        const resultsContainer = this.createElement('div', 'search-results');
        
        results.forEach(result => {
            const resultElement = this.createElement('div', 'search-result');
            resultElement.innerHTML = `
                <h3>${result.title}</h3>
                <p>${result.content}</p>
                <div class="result-meta">
                    <span>Score: ${result.score}</span>
                    <span>Type: ${result.metadata?.type || 'unknown'}</span>
                </div>
            `;
            resultsContainer.appendChild(resultElement);
        });

        // Clear previous results and add new ones
        const existingResults = document.querySelector('.search-results');
        if (existingResults) {
            existingResults.remove();
        }
        
        document.body.appendChild(resultsContainer);
    }

    /**
     * Display documents
     */
    displayDocuments(documents) {
        this.elements.docList.innerHTML = '';
        
        documents.forEach(doc => {
            const docElement = this.createElement('div', 'document-item');
            docElement.innerHTML = `
                <h4>${doc.title}</h4>
                <p>${doc.content}</p>
                <div class="document-actions">
                    <button onclick="this.editDocument('${doc.id}')">Edit</button>
                    <button onclick="this.deleteDocument('${doc.id}')">Delete</button>
                </div>
            `;
            this.elements.docList.appendChild(docElement);
        });
    }

    /**
     * Display analytics metrics
     */
    displayAnalytics(metrics) {
        this.elements.metricsDisplay.innerHTML = `
            <div class="metric">
                <span class="metric-label">Total Documents:</span>
                <span class="metric-value">${metrics.totalDocuments || 0}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Search Queries:</span>
                <span class="metric-value">${metrics.searchQueries || 0}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Average Response Time:</span>
                <span class="metric-value">${metrics.averageResponseTime || 0}ms</span>
            </div>
        `;
    }

    /**
     * Show error message
     */
    showError(message) {
        showErrorCommon({
            createElement: this.createElement.bind(this),
            message
        });
    }

    /**
     * Show success message
     */
    showSuccess(message) {
        showSuccessCommon({
            createElement: this.createElement.bind(this),
            message
        });
    }

    /**
     * Update status indicator
     */
    updateStatus(status) {
        this.elements.statusIndicator.textContent = status;
        this.elements.statusIndicator.className = `status-indicator ${status.toLowerCase()}`;
    }

    /**
     * Cleanup UI
     */
    cleanup() {
        this.eventListeners.forEach(({ element, event, handler }) => {
            element.removeEventListener(event, handler);
        });
        this.eventListeners.clear();
    }
}
