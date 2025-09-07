/**
<<<<<<< HEAD
 * Dashboard Navigation - Refactored Main Orchestrator
 * Main entry point for navigation system using modular architecture
 * V2 Compliance: Under 300-line limit achieved
 *
 * @author Agent-3 - Infrastructure & DevOps Specialist
 * @version 2.0.0 - Refactored Architecture
 * @license MIT
 */

import { getDefaultView, getNavigationElementId } from './navigation-config-manager.js';
import { createNavigationStateManager } from './navigation-state-manager.js';
import { createNavigationViewRenderer } from './navigation-view-renderer.js';
import { createNavigationEventHandler } from './navigation-event-handler.js';

/**
 * Dashboard Navigation - Refactored Architecture
 * Main orchestrator for navigation system
 */
export class DashboardNavigation {
    constructor() {
        this.stateManager = null;
        this.viewRenderer = null;
        this.eventHandler = null;
        this.isInitialized = false;
    }

    /**
     * Initialize navigation system
     */
    async initialize() {
        if (this.isInitialized) {
            console.warn('⚠️ Navigation already initialized');
            return;
        }

        console.log('🧭 Initializing dashboard navigation (Refactored)...');

        try {
            // Initialize state manager
            this.stateManager = createNavigationStateManager();
            this.stateManager.initialize();

            // Initialize view renderer
            this.viewRenderer = createNavigationViewRenderer();
            this.viewRenderer.initialize();

            // Initialize event handler
            const navElement = document.getElementById(getNavigationElementId());
            this.eventHandler = createNavigationEventHandler();
            this.eventHandler.initialize(navElement);

            // Setup event listeners
            this.setupEventListeners();

            // Set initial view
            await this.setInitialView();

            this.isInitialized = true;
            console.log('✅ Dashboard navigation initialized successfully');

        } catch (error) {
            console.error('❌ Failed to initialize navigation:', error);
            throw error;
        }
    }

    /**
     * Setup event listeners between modules
     */
    setupEventListeners() {
        // Connect event handler to navigation actions
        this.eventHandler.addEventListener('navigationClick', (data) => {
            this.handleNavigationClick(data);
        });

        // Connect state manager to navigation changes
        this.stateManager.addEventListener('navigationChange', (data) => {
            console.log(`🧭 Navigation changed: ${data.previousView} → ${data.newView}`);
        });
    }

    /**
     * Handle navigation click
     */
    async handleNavigationClick(data) {
        const { view } = data;

        try {
            // Update navigation state
            const stateUpdated = this.stateManager.updateNavigationState(view);
            if (!stateUpdated) return;

            // Show loading state
            this.viewRenderer.showLoadingState();

            // Load and render view
            await this.loadAndRenderView(view);

            // Hide loading state
            this.viewRenderer.hideLoadingState();

            console.log(`🧭 Successfully navigated to: ${view}`);

        } catch (error) {
            console.error(`❌ Failed to navigate to ${view}:`, error);
            this.eventHandler.handleNavigationError(error, view);
            this.viewRenderer.hideLoadingState();
        }
    }

    /**
     * Load and render view
     */
    async loadAndRenderView(view) {
        try {
            // Load view data using repository pattern
            const { DashboardRepository } = await import('./repositories/dashboard-repository.js');
            const repository = new DashboardRepository();
            const data = await repository.getDashboardData(view);

            // Render view with data
            this.viewRenderer.renderView(view, data);

        } catch (error) {
            console.error(`❌ Failed to load view data for ${view}:`, error);
            // Render error view
            this.viewRenderer.renderView(view, { error: error.message });
        }
    }

    /**
     * Set initial view
     */
    async setInitialView() {
        const initialView = getDefaultView();
        await this.navigateToView(initialView);
    }

    /**
     * Navigate to view programmatically
     */
    async navigateToView(view) {
        const navigationData = {
            view,
            element: null,
            event: null,
            timestamp: new Date().toISOString()
        };

        await this.handleNavigationClick(navigationData);
    }

    /**
     * Get current navigation state
     */
    getNavigationState() {
        return {
            currentView: this.stateManager.getCurrentView(),
            isInitialized: this.isInitialized,
            modulesInitialized: {
                stateManager: this.stateManager.isNavigationInitialized(),
                viewRenderer: this.viewRenderer.isInitialized,
                eventHandler: this.eventHandler.isInitialized
            }
        };
    }

    /**
     * Cleanup navigation system
     */
    cleanup() {
        if (this.eventHandler) {
            this.eventHandler.cleanup();
        }

        this.stateManager = null;
        this.viewRenderer = null;
        this.eventHandler = null;
        this.isInitialized = false;

        console.log('🧹 Navigation system cleaned up');
    }
}

// ================================
// EXPORTS
// ================================

export { DashboardNavigation };
export default DashboardNavigation;

// ================================
// LEGACY COMPATIBILITY
// ================================

/**
 * Legacy setup navigation function
 * @deprecated Use new DashboardNavigation class instead
 */
export function setupNavigation() {
    console.warn('⚠️ setupNavigation() is deprecated. Use new DashboardNavigation class.');
    const navigation = new DashboardNavigation();
    navigation.initialize().catch(console.error);
}

/**
 * Legacy update navigation state function
 * @deprecated Use navigation.navigateToView() instead
 */
export function updateNavigationState(view) {
    console.warn('⚠️ updateNavigationState() is deprecated. Use navigation.navigateToView().');
    if (view) {
        const navigation = new DashboardNavigation();
        navigation.navigateToView(view).catch(console.error);
    }
}

/**
 * Legacy navigate to view function
 * @deprecated Use navigation.navigateToView() instead
 */
export function navigateToView(view) {
    console.warn('⚠️ navigateToView() is deprecated. Use navigation.navigateToView().');
    const navigation = new DashboardNavigation();
    navigation.navigateToView(view).catch(console.error);
}
=======
 * Dashboard Navigation Module - V2 Compliant
 * Handles navigation and view management functionality
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0
 * @license MIT
 */

import { loadDashboardData } from './dashboard-core.js';

/**
 * Setup navigation functionality
 */
function setupNavigation() {
    document.getElementById('dashboardNav').addEventListener('click', function(e) {
        if (e.target.classList.contains('nav-link')) {
            e.preventDefault();

            // Update active state
            document.querySelectorAll('#dashboardNav .nav-link').forEach(link => {
                link.classList.remove('active');
            });
            e.target.classList.add('active');

            // Load new view
            const view = e.target.dataset.view;
            loadDashboardData(view);
        }
    });
}

/**
 * Update navigation active state
 * @param {string} view - The active view
 */
function updateNavigationState(view) {
    document.querySelectorAll('#dashboardNav .nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.view === view) {
            link.classList.add('active');
        }
    });
}

/**
 * Setup breadcrumb navigation
 */
function setupBreadcrumbs() {
    const breadcrumbContainer = document.getElementById('breadcrumbContainer');
    if (!breadcrumbContainer) return;

    const breadcrumbs = {
        'overview': ['Dashboard', 'Overview'],
        'agent_performance': ['Dashboard', 'Agent Performance'],
        'contract_status': ['Dashboard', 'Contract Status'],
        'system_health': ['Dashboard', 'System Health'],
        'performance_metrics': ['Dashboard', 'Performance Metrics'],
        'workload_distribution': ['Dashboard', 'Workload Distribution']
    };

    function updateBreadcrumbs(view) {
        const items = breadcrumbs[view] || ['Dashboard', 'Unknown'];
        breadcrumbContainer.innerHTML = items.map((item, index) => {
            if (index === items.length - 1) {
                return `<li class="breadcrumb-item active" aria-current="page">${item}</li>`;
            }
            return `<li class="breadcrumb-item"><a href="#" data-view="${view}">${item}</a></li>`;
        }).join('');
    }

    // Handle breadcrumb clicks
    breadcrumbContainer.addEventListener('click', function(e) {
        if (e.target.tagName === 'A') {
            e.preventDefault();
            const view = e.target.dataset.view;
            if (view) {
                loadDashboardData(view);
            }
        }
    });

    return updateBreadcrumbs;
}

/**
 * Setup mobile navigation toggle
 */
function setupMobileNavigation() {
    const mobileToggle = document.getElementById('mobileNavToggle');
    const mobileNav = document.getElementById('mobileNav');

    if (mobileToggle && mobileNav) {
        mobileToggle.addEventListener('click', function() {
            mobileNav.classList.toggle('show');
        });

        // Close mobile nav when clicking outside
        document.addEventListener('click', function(e) {
            if (!mobileToggle.contains(e.target) && !mobileNav.contains(e.target)) {
                mobileNav.classList.remove('show');
            }
        });
    }
}

/**
 * Setup search functionality
 */
function setupSearch() {
    const searchInput = document.getElementById('dashboardSearch');
    if (!searchInput) return;

    let searchTimeout;

    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const query = this.value.trim();
            if (query.length > 2) {
                performSearch(query);
            } else {
                clearSearchResults();
            }
        }, 300);
    });

    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const query = this.value.trim();
            if (query) {
                performSearch(query);
            }
        }
    });
}

/**
 * Perform search across dashboard data
 * @param {string} query - Search query
 */
function performSearch(query) {
    // Implementation for dashboard search
    console.log('Searching for:', query);
    
    // Show search results container
    const resultsContainer = document.getElementById('searchResults');
    if (resultsContainer) {
        resultsContainer.style.display = 'block';
        resultsContainer.innerHTML = `<div class="search-loading">Searching for "${query}"...</div>`;
        
        // Simulate search results
        setTimeout(() => {
            resultsContainer.innerHTML = `
                <div class="search-results">
                    <h6>Search Results for "${query}"</h6>
                    <div class="search-item">Agent Performance: ${query}</div>
                    <div class="search-item">Contract Status: ${query}</div>
                    <div class="search-item">System Health: ${query}</div>
                </div>
            `;
        }, 500);
    }
}

/**
 * Clear search results
 */
function clearSearchResults() {
    const resultsContainer = document.getElementById('searchResults');
    if (resultsContainer) {
        resultsContainer.style.display = 'none';
        resultsContainer.innerHTML = '';
    }
}

/**
 * Setup keyboard shortcuts
 */
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('dashboardSearch');
            if (searchInput) {
                searchInput.focus();
            }
        }

        // Escape to close modals and mobile nav
        if (e.key === 'Escape') {
            const mobileNav = document.getElementById('mobileNav');
            if (mobileNav) {
                mobileNav.classList.remove('show');
            }
            
            const searchResults = document.getElementById('searchResults');
            if (searchResults) {
                searchResults.style.display = 'none';
            }
        }
    });
}

/**
 * Initialize all navigation functionality
 */
function initializeNavigation() {
    setupNavigation();
    setupMobileNavigation();
    setupSearch();
    setupKeyboardShortcuts();
    
    const updateBreadcrumbs = setupBreadcrumbs();
    
    return {
        updateNavigationState,
        updateBreadcrumbs
    };
}

// Export navigation functionality
export {
    setupNavigation,
    updateNavigationState,
    setupBreadcrumbs,
    setupMobileNavigation,
    setupSearch,
    performSearch,
    clearSearchResults,
    setupKeyboardShortcuts,
    initializeNavigation
};
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
