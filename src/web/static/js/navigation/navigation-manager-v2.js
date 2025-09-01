/**
 * Navigation Manager V2 - V2 Compliant Main Orchestrator
 * Main orchestrator for navigation modules with clean architecture
 * REFACTORED: 339 lines → ~220 lines (35% reduction)
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist
 * @version 3.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

// ================================
// IMPORT MODULAR COMPONENTS
// ================================

import { NavigationState, createNavigationState } from './navigation-state.js';
import { NavigationEvents, createNavigationEvents } from './navigation-events.js';
import { NavigationUI, createNavigationUI } from './navigation-ui.js';

// ================================
// NAVIGATION MANAGER V2
// ================================

/**
 * Main orchestrator for all navigation modules
 * Provides unified interface with dependency injection
 */
export class NavigationManager {
    constructor(options = {}) {
        this.navigationState = options.navigationState || createNavigationState(options.initialView);
        this.navigationEvents = options.navigationEvents || createNavigationEvents(this.navigationState, options.eventOptions);
        this.navigationUI = options.navigationUI || createNavigationUI(this.navigationState, options.uiOptions);
        this.isInitialized = false;
    }

    initialize() {
        if (this.isInitialized) return;
        console.log('🧭 Initializing navigation manager V2...');

        this.navigationEvents.initialize();
        this.navigationUI.initialize();
        this.setupStateChangeHandling();
        this.isInitialized = true;
        console.log('✅ Navigation manager V2 initialized');
    }

    setupStateChangeHandling() {
        this.navigationState.addStateListener((event) => this.handleStateChange(event));
        window.addEventListener('navigation:navigated', (e) => this.handleNavigationEvent(e.detail));
    }

    navigateTo(view, options = {}) {
        return this.navigationEvents.navigateToView(view, options);
    }

    goBack() {
        return this.navigationEvents.navigateToPreviousView();
    }

    getCurrentView() {
        return this.navigationState.getCurrentView();
    }

    getHistory() {
        return this.navigationState.getViewHistory();
    }

    hasViewInHistory(view) {
        return this.navigationState.hasViewInHistory(view);
    }

    addNavigationItem(view, label, options = {}) {
        return this.navigationUI.addNavigationItem(view, label, options);
    }

    removeNavigationItem(view) {
        return this.navigationUI.removeNavigationItem(view);
    }

    updateUI() {
        this.navigationUI.updateNavigationUI();
    }

    addEventListener(event, listener) {
        this.navigationEvents.addEventHandler(window, event, listener);
    }

    removeEventListener(event, listener) {
        this.navigationEvents.removeEventListener(event, listener);
    }

    getState() {
        return {
            currentView: this.navigationState.getCurrentView(),
            previousView: this.navigationState.getPreviousView(),
            history: this.navigationState.getViewHistory(),
            ui: this.navigationUI.getStats(),
            events: { initialized: this.navigationEvents.isInitialized }
        };
    }

    exportState() {
        return this.navigationState.exportState();
    }

    importState(state) {
        return this.navigationState.importState(state);
    }

    handleStateChange(event) {
        this.navigationUI.updateNavigationUI();
        window.dispatchEvent(new CustomEvent('navigation:stateChanged', { detail: event }));
        console.log(`Navigation state changed: ${event.currentView}`);
    }

    handleNavigationEvent(detail) {
        console.log(`Navigation event: ${detail.view}`, detail);
        this.loadViewData(detail.view, detail.options);
    }

    async loadViewData(view, options = {}) {
        window.dispatchEvent(new CustomEvent('navigation:loadViewData', {
            detail: { view, options, timestamp: Date.now() }
        }));
        console.log(`Loading data for view: ${view}`);
    }

    isReady() {
        return this.isInitialized && this.navigationEvents.isInitialized && this.navigationUI.isInitialized;
    }

    getStats() {
        return {
            initialized: this.isInitialized,
            state: this.navigationState.getStats(),
            ui: this.navigationUI.getStats(),
            ready: this.isReady()
        };
    }

    cleanup() {
        this.navigationEvents.cleanup();
        this.navigationUI.cleanup();
        this.navigationState.clearHistory();
        this.isInitialized = false;
        console.log('Navigation manager cleaned up');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

export function createNavigationManager(options = {}) {
    return new NavigationManager(options);
}

export function createDefaultNavigationManager() {
    return new NavigationManager();
}

export default NavigationManager;