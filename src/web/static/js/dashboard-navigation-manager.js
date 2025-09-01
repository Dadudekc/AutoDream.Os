/**
 * Dashboard Navigation Manager - V2 Compliant Module
 * Handles all navigation functionality for the dashboard
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class DashboardNavigationManager {
    constructor(stateManager) {
        this.stateManager = stateManager;
    }

    /**
     * Setup navigation functionality
     */
    initialize() {
        console.log('🧭 Initializing dashboard navigation manager...');

        const navElement = document.getElementById('dashboardNav');
        if (!navElement) {
            console.warn('⚠️ Dashboard navigation element not found');
            return;
        }

        navElement.addEventListener('click', (e) => {
            this.handleNavigationClick(e);
        });

        // Initialize default view
        this.setActiveView(this.stateManager.currentView);
    }

    handleNavigationClick(event) {
        const target = event.target.closest('.nav-link');
        if (!target) return;

        event.preventDefault();

        const view = target.dataset.view;
        if (!view) return;

        // Update active states
        this.clearActiveStates();
        target.classList.add('active');

        // Update state and load data
        this.stateManager.updateView(view);
        if (window.loadDashboardData) {
            window.loadDashboardData(view);
        }

        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('dashboard:viewChanged', {
            detail: { view, previousView: this.stateManager.currentView }
        }));
    }

    clearActiveStates() {
        document.querySelectorAll('#dashboardNav .nav-link').forEach(link => {
            link.classList.remove('active');
        });
    }

    setActiveView(view) {
        this.clearActiveStates();

        const targetLink = document.querySelector(`#dashboardNav .nav-link[data-view="${view}"]`);
        if (targetLink) {
            targetLink.classList.add('active');
        }

        this.stateManager.updateView(view);
    }

    navigateTo(view) {
        this.setActiveView(view);
        if (window.loadDashboardData) {
            window.loadDashboardData(view);
        }
    }
}

// Factory function for creating navigation manager instances
export function createNavigationManager(stateManager) {
    return new DashboardNavigationManager(stateManager);
}
