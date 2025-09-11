/**
 * Vector Database UI Module - Consolidated
 * =======================================
 *
 * Consolidated vector database user interface functionality.
 * Combines UI components, search interface, and analytics display.
 *
 * V2 Compliance: Single consolidated module, clean architecture.
 * Consolidation: 5→1 files (80% reduction)
 *
 * Author: Agent-8 - Operations & Support Specialist
 * Mission: Phase 2 Consolidation - Chunk JS-08
 * License: MIT
 */

/**
 * Vector Database UI - Consolidated Module
 * ========================================
 *
 * UI components and interactions for vector database.
 * Provides search interface, document management, and analytics display.
 */
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
        const searchContainer = this.createElement('div', 'search-container');
        const searchInput = this.createElement('input', 'search-input', {
            type: 'text',
            placeholder: 'Search documents...',
            id: 'vector-search-input'
        });
        const searchButton = this.createElement(
            'button',
            'search-button',
            { id: 'vector-search-button' },
            'Search'
        );

        searchContainer.appendChild(searchInput);
        searchContainer.appendChild(searchButton);

        this.elements.searchContainer = searchContainer;
        this.elements.searchInput = searchInput;
        this.elements.searchButton = searchButton;

        this.addEventListener(searchButton, 'click', () => this.handleSearch());
        this.addEventListener(searchInput, 'keypress', (e) => {
            if (e.key === 'Enter') this.handleSearch();
        });
    }

    /**
     * Setup document management interface
     */
    setupDocumentManagement() {
        const docContainer = this.createElement('div', 'document-container');
        const docList = this.createElement('div', 'document-list', { id: 'document-list' });
        const addButton = this.createElement(
            'button',
            'add-document-button',
            { id: 'add-document-button' },
            'Add Document'
        );

        docContainer.appendChild(docList);
        docContainer.appendChild(addButton);

        this.elements.docContainer = docContainer;
        this.elements.docList = docList;
        this.elements.addButton = addButton;

        this.addEventListener(addButton, 'click', () => this.handleAddDocument());
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
                <h3>${this.escapeHtml(result.title)}</h3>
                <p>${this.escapeHtml(result.content)}</p>
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
                <h4>${this.escapeHtml(doc.title)}</h4>
                <p>${this.escapeHtml(doc.content)}</p>
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
        this.showMessage(message, 'error-message', '#ff4444', 5000);
    }

    /**
     * Show success message
     */
    showSuccess(message) {
        this.showMessage(message, 'success-message', '#44ff44', 3000);
    }

    /**
     * Generic message display helper
     */
    showMessage(message, className, backgroundColor, duration) {
        const element = this.createElement('div', className);
        element.textContent = message;
        element.style.cssText =
            `position:fixed;top:20px;right:20px;background:${backgroundColor};` +
            'color:white;padding:10px;border-radius:5px;z-index:1000;';
        document.body.appendChild(element);

        setTimeout(() => {
            if (element.parentNode) element.parentNode.removeChild(element);
        }, duration);
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
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

/**
 * Shared UI helpers for vector database modules - Consolidated
 * ============================================================
 *
 * Provides reusable setup functions to maintain SSOT across UI variants.
 */
export function setupSearchInterface(options) {
    const { createElement, elements, addEventListener, handleSearch } = options;

    const searchContainer = createElement('div', 'search-container');
    const searchInput = createElement('input', 'search-input', {
        type: 'text',
        placeholder: 'Search documents...',
        id: 'vector-search-input'
    });
    const searchButton = createElement(
        'button',
        'search-button',
        { id: 'vector-search-button' },
        'Search'
    );

    searchContainer.appendChild(searchInput);
    searchContainer.appendChild(searchButton);

    elements.searchContainer = searchContainer;
    elements.searchInput = searchInput;
    elements.searchButton = searchButton;

    if (addEventListener && handleSearch) {
        addEventListener(searchButton, 'click', () => handleSearch());
        addEventListener(searchInput, 'keypress', (e) => {
            if (e.key === 'Enter') handleSearch();
        });
    }
}

export function setupDocumentManagement(options) {
    const { createElement, elements, addEventListener, handleAddDocument } = options;

    const docContainer = createElement('div', 'document-container');
    const docList = createElement('div', 'document-list', { id: 'document-list' });
    const addButton = createElement(
        'button',
        'add-document-button',
        { id: 'add-document-button' },
        'Add Document'
    );

    docContainer.appendChild(docList);
    docContainer.appendChild(addButton);

    elements.docContainer = docContainer;
    elements.docList = docList;
    elements.addButton = addButton;

    if (addEventListener && handleAddDocument) {
        addEventListener(addButton, 'click', () => handleAddDocument());
    }
}

export function showError(options) {
    const { createElement, message, useAnimationFrame = false } = options;

    const element = createElement('div', 'error-message');
    element.textContent = message;
    element.style.cssText =
        'position:fixed;top:20px;right:20px;background:#ff4444;' +
        'color:white;padding:10px;border-radius:5px;z-index:1000;';
    document.body.appendChild(element);

    const remove = () => {
        if (element.parentNode) element.parentNode.removeChild(element);
    };

    const schedule = () => setTimeout(remove, 5000);
    if (useAnimationFrame) requestAnimationFrame(schedule); else schedule();
}

export function showSuccess(options) {
    const { createElement, message, useAnimationFrame = false } = options;

    const element = createElement('div', 'success-message');
    element.textContent = message;
    element.style.cssText =
        'position:fixed;top:20px;right:20px;background:#44ff44;' +
        'color:white;padding:10px;border-radius:5px;z-index:1000;';
    document.body.appendChild(element);

    const remove = () => {
        if (element.parentNode) element.parentNode.removeChild(element);
    };

    const schedule = () => setTimeout(remove, 3000);
    if (useAnimationFrame) requestAnimationFrame(schedule); else schedule();
}

export function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Vector Database UI - Performance Optimized - Consolidated
 * ========================================================
 *
 * Performance optimized UI components with event delegation and batching.
 */
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

    /**
     * Initialize UI components with performance optimizations
     */
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

    /**
     * Setup event delegation for better performance
     */
    setupEventDelegation() {
        // Use event delegation instead of individual listeners
        document.addEventListener('click', this.handleDelegatedClick.bind(this));
        document.addEventListener('input', this.handleDelegatedInput.bind(this));
    }

    /**
     * Handle delegated click events
     */
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

    /**
     * Handle delegated input events with debouncing
     */
    handleDelegatedInput(event) {
        if (event.target.matches('.search-input')) {
            this.debounceSearch(event.target.value);
        }
    }

    /**
     * Debounced search to reduce API calls
     */
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

    /**
     * Setup search interface with performance optimizations
     */
    setupSearchInterface() {
        const searchContainer = document.createElement('div');
        searchContainer.className = 'search-container';

        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Search documents...';
        searchInput.id = 'vector-search-input';
        searchInput.className = 'search-input';

        const searchButton = document.createElement('button');
        searchButton.id = 'vector-search-button';
        searchButton.className = 'search-button';
        searchButton.textContent = 'Search';

        searchContainer.appendChild(searchInput);
        searchContainer.appendChild(searchButton);

        this.elements.set('searchContainer', searchContainer);
        this.elements.set('searchInput', searchInput);
        this.elements.set('searchButton', searchButton);
    }

    /**
     * Setup document management with batch operations
     */
    setupDocumentManagement() {
        const docContainer = document.createElement('div');
        docContainer.className = 'document-container';

        const docList = document.createElement('div');
        docList.id = 'document-list';
        docList.className = 'document-list';

        const addButton = document.createElement('button');
        addButton.id = 'add-document-button';
        addButton.className = 'add-document-button';
        addButton.textContent = 'Add Document';

        docContainer.appendChild(docList);
        docContainer.appendChild(addButton);

        this.elements.set('docContainer', docContainer);
        this.elements.set('docList', docList);
        this.elements.set('addButton', addButton);
    }

    /**
     * Setup analytics dashboard with cached elements
     */
    setupAnalyticsDashboard() {
        const analyticsContainer = document.createElement('div');
        analyticsContainer.className = 'analytics-container';

        const metricsDisplay = document.createElement('div');
        metricsDisplay.id = 'metrics-display';
        metricsDisplay.className = 'metrics-display';

        const chartsContainer = document.createElement('div');
        chartsContainer.id = 'charts-container';
        chartsContainer.className = 'charts-container';

        analyticsContainer.appendChild(metricsDisplay);
        analyticsContainer.appendChild(chartsContainer);

        this.elements.set('analyticsContainer', analyticsContainer);
        this.elements.set('metricsDisplay', metricsDisplay);
        this.elements.set('chartsContainer', chartsContainer);
    }

    /**
     * Setup real-time updates with optimized rendering
     */
    setupRealTimeUpdates() {
        const updateContainer = document.createElement('div');
        updateContainer.className = 'update-container';

        const statusIndicator = document.createElement('div');
        statusIndicator.id = 'status-indicator';
        statusIndicator.className = 'status-indicator';

        const lastUpdate = document.createElement('div');
        lastUpdate.id = 'last-update';
        lastUpdate.className = 'last-update';

        updateContainer.appendChild(statusIndicator);
        updateContainer.appendChild(lastUpdate);

        this.elements.set('updateContainer', updateContainer);
        this.elements.set('statusIndicator', statusIndicator);
        this.elements.set('lastUpdate', lastUpdate);
    }

    /**
     * Handle search action with performance optimizations
     */
    handleSearch() {
        const searchInput = this.elements.get('searchInput');
        const query = searchInput.value.trim();
        if (!query) return;

        // Emit search event
        this.emitEvent('search', { query });
    }

    /**
     * Handle add document action
     */
    handleAddDocument() {
        this.emitEvent('addDocument', {});
    }

    /**
     * Handle edit document action
     */
    handleEditDocument(docId) {
        this.emitEvent('editDocument', { docId });
    }

    /**
     * Handle delete document action
     */
    handleDeleteDocument(docId) {
        this.emitEvent('deleteDocument', { docId });
    }

    /**
     * Emit custom event
     */
    emitEvent(eventName, data) {
        const event = new CustomEvent(eventName, { detail: data });
        document.dispatchEvent(event);
    }

    /**
     * Display search results with batch rendering
     */
    displaySearchResults(results) {
        // Use document fragment for batch DOM operations
        const fragment = document.createDocumentFragment();
        const resultsContainer = document.createElement('div');
        resultsContainer.className = 'search-results';

        // Batch create result elements
        results.forEach(result => {
            const resultElement = document.createElement('div');
            resultElement.className = 'search-result';
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

    /**
     * Display documents with virtual scrolling for large datasets
     */
    displayDocuments(documents) {
        const docList = this.elements.get('docList');

        // Clear existing content
        docList.innerHTML = '';

        // Use document fragment for batch operations
        const fragment = document.createDocumentFragment();

        documents.forEach(doc => {
            const docElement = document.createElement('div');
            docElement.className = 'document-item';
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

    /**
     * Display analytics metrics with optimized rendering
     */
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

    /**
     * Show error message with optimized rendering
     */
    showError(message) {
        showError({
            createElement: (tag, className, attrs, text) => {
                const el = document.createElement(tag);
                el.className = className;
                if (attrs) Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
                if (text) el.textContent = text;
                return el;
            },
            message,
            useAnimationFrame: true
        });
    }

    /**
     * Show success message with optimized rendering
     */
    showSuccess(message) {
        showSuccess({
            createElement: (tag, className, attrs, text) => {
                const el = document.createElement(tag);
                el.className = className;
                if (attrs) Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
                if (text) el.textContent = text;
                return el;
            },
            message,
            useAnimationFrame: true
        });
    }

    /**
     * Batch DOM updates for better performance
     */
    batchDOMUpdate(operation) {
        this.batchOperations.push(operation);

        if (!this.isRendering) {
            this.isRendering = true;
            this.rafId = requestAnimationFrame(() => {
                this.flushBatchOperations();
            });
        }
    }

    /**
     * Flush batched DOM operations
     */
    flushBatchOperations() {
        this.batchOperations.forEach(operation => operation());
        this.batchOperations = [];
        this.isRendering = false;
        this.rafId = null;
    }

    /**
     * Cleanup resources to prevent memory leaks
     */
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

// Export all UI classes for backward compatibility
export {
    VectorDatabaseUI,
    VectorDatabaseUIOptimized,
    setupSearchInterface,
    setupDocumentManagement,
    showError,
    showSuccess,
    escapeHtml
};
