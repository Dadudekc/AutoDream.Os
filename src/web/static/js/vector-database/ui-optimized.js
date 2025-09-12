/**
 * Vector Database UI - Performance Optimized
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */
import {
    setupSearchInterface as setupSearchInterfaceCommon,
    setupDocumentManagement as setupDocumentManagementCommon,
    showError as showErrorCommon,
    showSuccess as showSuccessCommon,
    escapeHtml
} from './ui-common.js';
export class VectorDatabaseUIOptimized {
    constructor() {
        this.elements = new Map();
        this.eventListeners = new Map();
        this.logger = console;
        this.debounceTimers = new Map();
        this.renderQueue = [];
        this.isRendering = false;

        // Performance optimizations
        this.domCache = new Map();
        this.batchOperations = [];
        this.rafId = null;
    }
/** Initialize UI components with performance optimizations */
    initializeUI() {
        try {
            this.setupEventDelegation();
            this.setupSearchInterface();
            this.setupDocumentManagement();
            this.setupAnalyticsDashboard();
            this.setupRealTimeUpdates();

            this.logger.log('✅ Vector Database UI (Optimized) initialized');
        } catch (error) {
            this.logger.error('❌ Failed to initialize UI:', error);
            throw error;
        }
    }
/** Setup event delegation for better performance */
    setupEventDelegation() {
        // Use event delegation instead of individual listeners
        document.addEventListener('click', this.handleDelegatedClick.bind(this));
        document.addEventListener('input', this.handleDelegatedInput.bind(this));
    }
/** Handle delegated click events */
    handleDelegatedClick(event) {
        const target = event.target;

        if (target.matches('.search-button')) {
            this.handleSearch();
        } else if (target.matches('.add-document-button')) {
            this.handleAddDocument();
        } else if (target.matches('.edit-document')) {
            this.handleEditDocument(target.dataset.docId);
        } else if (target.matches('.delete-document')) {
            this.handleDeleteDocument(target.dataset.docId);
        }
    }
/** Handle delegated input events with debouncing */
    handleDelegatedInput(event) {
        if (event.target.matches('.search-input')) {
            this.debounceSearch(event.target.value);
        }
    }
/** Debounced search to reduce API calls */
    debounceSearch(query) {
        const timer = this.debounceTimers.get('search');
        if (timer) {
            clearTimeout(timer);
        }

        const newTimer = setTimeout(() => {
            if (query.trim()) {
                this.handleSearch();
            }
        }, 300);

        this.debounceTimers.set('search', newTimer);
    }
/** Setup search interface with performance optimizations */
    setupSearchInterface() {
        setupSearchInterfaceCommon({
            createElement: this.createElement.bind(this),
            elements: this.elements
        });
    }
/** Setup document management with batch operations */
    setupDocumentManagement() {
        setupDocumentManagementCommon({
            createElement: this.createElement.bind(this),
            elements: this.elements
        });
    }
/** Setup analytics dashboard with cached elements */
    setupAnalyticsDashboard() {
        const analyticsContainer = this.createElement('div', 'analytics-container');
        const metricsDisplay = this.createElement('div', 'metrics-display', { id: 'metrics-display' });
        const chartsContainer = this.createElement('div', 'charts-container', { id: 'charts-container' });
        analyticsContainer.appendChild(metricsDisplay);
        analyticsContainer.appendChild(chartsContainer);

        this.elements.set('analyticsContainer', analyticsContainer);
        this.elements.set('metricsDisplay', metricsDisplay);
        this.elements.set('chartsContainer', chartsContainer);
    }
/** Setup real-time updates with optimized rendering */
    setupRealTimeUpdates() {
        const updateContainer = this.createElement('div', 'update-container');
        const statusIndicator = this.createElement('div', 'status-indicator', { id: 'status-indicator' });
        const lastUpdate = this.createElement('div', 'last-update', { id: 'last-update' });
        updateContainer.appendChild(statusIndicator);
        updateContainer.appendChild(lastUpdate);

        this.elements.set('updateContainer', updateContainer);
        this.elements.set('statusIndicator', statusIndicator);
        this.elements.set('lastUpdate', lastUpdate);
    }
/** Create DOM element with performance optimizations */
    createElement(tag, className, attributes = {}, textContent = '') {
        const element = document.createElement(tag);
        element.className = className;

        // Batch attribute setting
        Object.entries(attributes).forEach(([key, value]) => {
            element.setAttribute(key, value);
        });

        if (textContent) {
            element.textContent = textContent;
        }

        return element;
    }
/** Handle search action with performance optimizations */
    handleSearch() {
        const query = this.elements.get('searchInput').value.trim();
        if (!query) return;
        // Emit search event
        this.emitEvent('search', { query });
    }
/** Handle add document action */
    handleAddDocument() {
        this.emitEvent('addDocument', {});
    }
/** Handle edit document action */
    handleEditDocument(docId) {
        this.emitEvent('editDocument', { docId });
    }
/** Handle delete document action */
    handleDeleteDocument(docId) {
        this.emitEvent('deleteDocument', { docId });
    }
/** Emit custom event */
    emitEvent(eventName, data) {
        const event = new CustomEvent(eventName, { detail: data });
        document.dispatchEvent(event);
    }
/** Display search results with batch rendering */
    displaySearchResults(results) {
        // Use document fragment for batch DOM operations
        const fragment = document.createDocumentFragment();
        const resultsContainer = this.createElement('div', 'search-results');

        // Batch create result elements
        results.forEach(result => {
            const resultElement = this.createElement('div', 'search-result');
            resultElement.innerHTML = `
                <h3>${escapeHtml(result.title)}</h3>
                <p>${escapeHtml(result.content)}</p>
                <div class="result-meta">
                    <span>Score: ${result.score}</span>
                    <span>Type: ${result.metadata?.type || 'unknown'}</span>
                </div>
            `;
            fragment.appendChild(resultElement);
        });
        resultsContainer.appendChild(fragment);
        // Batch DOM update
        this.batchDOMUpdate(() => {
            const existingResults = document.querySelector('.search-results');
            if (existingResults) {
                existingResults.remove();
            }
            document.body.appendChild(resultsContainer);
        });
    }
/** Display documents with virtual scrolling for large datasets */
    displayDocuments(documents) {
        const docList = this.elements.get('docList');

        // Clear existing content
        docList.innerHTML = '';

        // Use document fragment for batch operations
        const fragment = document.createDocumentFragment();

        documents.forEach(doc => {
            const docElement = this.createElement('div', 'document-item');
            docElement.innerHTML = `
                <h4>${escapeHtml(doc.title)}</h4>
                <p>${escapeHtml(doc.content)}</p>
                <div class="document-actions">
                    <button class="edit-document" data-doc-id="${doc.id}">Edit</button>
                    <button class="delete-document" data-doc-id="${doc.id}">Delete</button>
                </div>
            `;
            fragment.appendChild(docElement);
        });

        docList.appendChild(fragment);
    }
/** Display analytics metrics with optimized rendering */
    displayAnalytics(metrics) {
        const metricsDisplay = this.elements.get('metricsDisplay');

        // Use template literals for better performance
        metricsDisplay.innerHTML = `
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
/** Show error message with optimized rendering */
    showError(message) {
        showErrorCommon({
            createElement: this.createElement.bind(this),
            message,
            useAnimationFrame: true
        });
    }
/** Show success message with optimized rendering */
    showSuccess(message) {
        showSuccessCommon({
            createElement: this.createElement.bind(this),
            message,
            useAnimationFrame: true
        });
    }
/** Batch DOM updates for better performance */
    batchDOMUpdate(operation) {
        this.batchOperations.push(operation);

        if (!this.isRendering) {
            this.isRendering = true;
            this.rafId = requestAnimationFrame(() => {
                this.flushBatchOperations();
            });
        }
    }
/** Flush batched DOM operations */
    flushBatchOperations() {
        this.batchOperations.forEach(operation => operation());
        this.batchOperations = [];
        this.isRendering = false;
        this.rafId = null;
    }
/** Cleanup resources to prevent memory leaks */
    cleanup() {
        // Clear debounce timers
        this.debounceTimers.forEach(timer => clearTimeout(timer));
        this.debounceTimers.clear();

        // Cancel pending animation frame
        if (this.rafId) {
            cancelAnimationFrame(this.rafId);
        }

        // Clear caches
        this.domCache.clear();
        this.elements.clear();

        // Remove event listeners
        this.eventListeners.clear();

        this.logger.log('🧹 Vector Database UI cleanup completed');
    }
}
