/**
 * Navigation Component - V2 SWARM Web Interface
 * Handles application navigation with performance optimization
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - COMPETITIVE_DOMINATION_MODE
 */

export class Navigation {
    constructor(app) {
        this.app = app;
        this.navElement = document.querySelector('.main-navigation');
        this.currentView = 'dashboard';
    }

    async init() {
        this.setupEventListeners();
        this.updateNavigationState();
        console.log('🧭 Navigation component initialized');
    }

    setupEventListeners() {
        if (this.navElement) {
            this.navElement.addEventListener('click', (event) => {
                if (event.target.matches('.nav-btn')) {
                    event.preventDefault();
                    const view = event.target.dataset.view;
                    this.navigateTo(view);
                }
            });
        }

        // Keyboard navigation support
        document.addEventListener('keydown', (event) => {
            if (event.altKey) {
                const keyMap = {
                    '1': 'dashboard',
                    '2': 'agents',
                    '3': 'analytics',
                    '4': 'settings'
                };

                const view = keyMap[event.key];
                if (view) {
                    event.preventDefault();
                    this.navigateTo(view);
                }
            }
        });
    }

    async navigateTo(view) {
        if (view === this.currentView) return;

        // Pre-navigation performance check
        const startTime = performance.now();

        try {
            // Update navigation UI
            this.updateActiveButton(view);

            // Navigate using app controller
            await this.app.switchView(view);

            this.currentView = view;

            // Performance tracking
            const endTime = performance.now();
            console.log(`🧭 Navigation to ${view}: ${(endTime - startTime).toFixed(2)}ms`);

        } catch (error) {
            console.error(`❌ Navigation error:`, error);
            this.app.handleError('navigation', error);
        }
    }

    updateActiveButton(view) {
        const buttons = this.navElement.querySelectorAll('.nav-btn');
        buttons.forEach(button => {
            button.classList.toggle('active', button.dataset.view === view);
        });
    }

    updateNavigationState() {
        // Update navigation based on application state
        const buttons = this.navElement.querySelectorAll('.nav-btn');

        buttons.forEach(button => {
            const view = button.dataset.view;
            const isAccessible = this.isViewAccessible(view);

            button.disabled = !isAccessible;
            button.setAttribute('aria-disabled', !isAccessible);
        });
    }

    isViewAccessible(view) {
        // Check if view is accessible based on permissions/state
        // In competitive domination mode, all views are accessible
        return this.app.mode === 'COMPETITIVE_DOMINATION_MODE' || ['dashboard'].includes(view);
    }

    getCurrentView() {
        return this.currentView;
    }

    getAvailableViews() {
        return ['dashboard', 'agents', 'analytics', 'settings'];
    }
}





