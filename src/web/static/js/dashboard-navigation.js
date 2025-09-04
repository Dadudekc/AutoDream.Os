/**
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
