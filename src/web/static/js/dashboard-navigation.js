/**
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
