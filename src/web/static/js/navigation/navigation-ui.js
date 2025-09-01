/**
 * Navigation UI Module - V2 Compliant
 * Handles navigation user interface and visual management
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class NavigationUI {
    constructor(navigationState, options = {}) {
        this.navigationState = navigationState;
        this.options = {
            navContainerId: 'dashboardNav',
            mobileBreakpoint: 768,
            enableAnimations: true,
            enableBreadcrumbs: true,
            ...options
        };

        this.navContainer = null;
        this.breadcrumbContainer = null;
        this.mobileMenuOpen = false;
        this.isInitialized = false;
    }

    /**
     * Initialize navigation UI
     */
    initialize() {
        if (this.isInitialized) {
            console.warn('Navigation UI already initialized');
            return;
        }

        console.log('🎨 Initializing navigation UI...');
        this.setupNavigationContainer();
        this.setupMobileMenu();
        this.setupBreadcrumbs();
        this.setupAnimations();
        this.updateNavigationUI();
        this.isInitialized = true;
        console.log('✅ Navigation UI initialized');
    }

    /**
     * Setup navigation container
     */
    setupNavigationContainer() {
        try {
            this.navContainer = document.getElementById(this.options.navContainerId);
            if (!this.navContainer) {
                console.warn(`Navigation container with ID '${this.options.navContainerId}' not found`);
                return;
            }

            // Add navigation classes
            this.navContainer.classList.add('dashboard-navigation');
            if (this.isMobile()) {
                this.navContainer.classList.add('mobile-navigation');
            }

            console.log('Navigation container configured');
        } catch (error) {
            console.error('Failed to setup navigation container:', error);
        }
    }

    /**
     * Setup mobile menu functionality
     */
    setupMobileMenu() {
        if (!this.isMobile()) return;

        try {
            // Create mobile menu toggle
            const toggleButton = document.createElement('button');
            toggleButton.className = 'mobile-menu-toggle';
            toggleButton.innerHTML = '☰';
            toggleButton.setAttribute('aria-label', 'Toggle navigation menu');

            // Insert before navigation container
            if (this.navContainer) {
                this.navContainer.parentNode.insertBefore(toggleButton, this.navContainer);

                // Add toggle functionality
                toggleButton.addEventListener('click', () => this.toggleMobileMenu());
            }

            console.log('Mobile menu configured');
        } catch (error) {
            console.error('Failed to setup mobile menu:', error);
        }
    }

    /**
     * Setup breadcrumb navigation
     */
    setupBreadcrumbs() {
        if (!this.options.enableBreadcrumbs) return;

        try {
            // Create breadcrumb container
            this.breadcrumbContainer = document.createElement('nav');
            this.breadcrumbContainer.className = 'breadcrumb-navigation';
            this.breadcrumbContainer.setAttribute('aria-label', 'Breadcrumb navigation');

            // Insert breadcrumb navigation
            const mainContent = document.querySelector('main') || document.body;
            mainContent.insertBefore(this.breadcrumbContainer, mainContent.firstChild);

            console.log('Breadcrumb navigation configured');
        } catch (error) {
            console.error('Failed to setup breadcrumbs:', error);
        }
    }

    /**
     * Setup navigation animations
     */
    setupAnimations() {
        if (!this.options.enableAnimations) return;

        try {
            // Add CSS animations
            if (!document.getElementById('navigation-animations')) {
                const style = document.createElement('style');
                style.id = 'navigation-animations';
                style.textContent = `
                    .dashboard-navigation .nav-link {
                        transition: all 0.3s ease;
                    }

                    .dashboard-navigation .nav-link:hover {
                        transform: translateY(-2px);
                    }

                    .dashboard-navigation .nav-link.active {
                        background-color: #007bff;
                        color: white;
                    }

                    .mobile-navigation {
                        position: fixed;
                        top: 0;
                        left: -100%;
                        width: 280px;
                        height: 100vh;
                        background: white;
                        transition: left 0.3s ease;
                        z-index: 1000;
                    }

                    .mobile-navigation.open {
                        left: 0;
                    }

                    .breadcrumb-navigation {
                        margin-bottom: 1rem;
                        font-size: 0.875rem;
                    }

                    .breadcrumb-navigation ol {
                        list-style: none;
                        padding: 0;
                        margin: 0;
                    }

                    .breadcrumb-navigation li {
                        display: inline;
                    }

                    .breadcrumb-navigation li + li:before {
                        content: "/";
                        padding: 0 0.5rem;
                        color: #6c757d;
                    }
                `;
                document.head.appendChild(style);
            }

            console.log('Navigation animations configured');
        } catch (error) {
            console.error('Failed to setup animations:', error);
        }
    }

    /**
     * Update navigation UI to reflect current state
     */
    updateNavigationUI() {
        try {
            const currentView = this.navigationState.getCurrentView();
            this.updateActiveNavigation(currentView);
            this.updateBreadcrumbs();
            this.updateMobileMenu();
        } catch (error) {
            console.error('Failed to update navigation UI:', error);
        }
    }

    /**
     * Update active navigation item
     */
    updateActiveNavigation(currentView) {
        if (!this.navContainer) return;

        try {
            // Remove active class from all items
            this.navContainer.querySelectorAll('.nav-link, [data-nav-view]').forEach(item => {
                item.classList.remove('active');
            });

            // Add active class to current view
            const activeItem = this.navContainer.querySelector(
                `[data-nav-view="${currentView}"], [data-view="${currentView}"]`
            );

            if (activeItem) {
                activeItem.classList.add('active');

                // Scroll into view if needed
                if (this.isMobile() && this.mobileMenuOpen) {
                    activeItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        } catch (error) {
            console.error('Failed to update active navigation:', error);
        }
    }

    /**
     * Update breadcrumb navigation
     */
    updateBreadcrumbs() {
        if (!this.breadcrumbContainer || !this.options.enableBreadcrumbs) return;

        try {
            const history = this.navigationState.getViewHistory();
            const currentView = this.navigationState.getCurrentView();

            // Clear existing breadcrumbs
            this.breadcrumbContainer.innerHTML = '';

            // Create breadcrumb list
            const ol = document.createElement('ol');

            // Add home/dashboard link
            const homeLi = document.createElement('li');
            const homeLink = document.createElement('a');
            homeLink.href = '#overview';
            homeLink.textContent = 'Dashboard';
            homeLink.addEventListener('click', (e) => {
                e.preventDefault();
                this.navigationState.setCurrentView('overview');
            });
            homeLi.appendChild(homeLink);
            ol.appendChild(homeLi);

            // Add current view (if not overview)
            if (currentView !== 'overview') {
                const currentLi = document.createElement('li');
                currentLi.textContent = this.formatViewName(currentView);
                currentLi.classList.add('active');
                ol.appendChild(currentLi);
            }

            this.breadcrumbContainer.appendChild(ol);
        } catch (error) {
            console.error('Failed to update breadcrumbs:', error);
        }
    }

    /**
     * Update mobile menu state
     */
    updateMobileMenu() {
        if (!this.isMobile() || !this.navContainer) return;

        try {
            if (this.mobileMenuOpen) {
                this.navContainer.classList.add('open');
            } else {
                this.navContainer.classList.remove('open');
            }
        } catch (error) {
            console.error('Failed to update mobile menu:', error);
        }
    }

    /**
     * Toggle mobile menu
     */
    toggleMobileMenu() {
        try {
            this.mobileMenuOpen = !this.mobileMenuOpen;
            this.updateMobileMenu();

            // Update toggle button
            const toggleButton = document.querySelector('.mobile-menu-toggle');
            if (toggleButton) {
                toggleButton.innerHTML = this.mobileMenuOpen ? '✕' : '☰';
                toggleButton.setAttribute('aria-expanded', this.mobileMenuOpen.toString());
            }
        } catch (error) {
            console.error('Failed to toggle mobile menu:', error);
        }
    }

    /**
     * Format view name for display
     */
    formatViewName(view) {
        try {
            return view
                .split('-')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
        } catch (error) {
            return view;
        }
    }

    /**
     * Check if device is mobile
     */
    isMobile() {
        return window.innerWidth <= this.options.mobileBreakpoint;
    }

    /**
     * Handle window resize
     */
    handleResize() {
        try {
            const wasMobile = this.navContainer?.classList.contains('mobile-navigation');
            const isNowMobile = this.isMobile();

            if (wasMobile !== isNowMobile) {
                if (isNowMobile) {
                    this.navContainer.classList.add('mobile-navigation');
                    this.mobileMenuOpen = false;
                    this.updateMobileMenu();
                } else {
                    this.navContainer.classList.remove('mobile-navigation');
                    this.mobileMenuOpen = false;
                }
            }
        } catch (error) {
            console.error('Failed to handle resize:', error);
        }
    }

    /**
     * Add navigation item programmatically
     */
    addNavigationItem(view, label, options = {}) {
        if (!this.navContainer) return false;

        try {
            const item = document.createElement('a');
            item.className = 'nav-link';
            item.dataset.navView = view;
            item.href = `#${view}`;
            item.textContent = label;

            if (options.icon) {
                item.innerHTML = `${options.icon} ${label}`;
            }

            if (options.className) {
                item.classList.add(options.className);
            }

            this.navContainer.appendChild(item);

            // Add click handler
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.navigationState.setCurrentView(view);
            });

            console.log(`Navigation item added: ${view}`);
            return true;
        } catch (error) {
            console.error('Failed to add navigation item:', error);
            return false;
        }
    }

    /**
     * Remove navigation item
     */
    removeNavigationItem(view) {
        if (!this.navContainer) return false;

        try {
            const item = this.navContainer.querySelector(`[data-nav-view="${view}"]`);
            if (item) {
                item.remove();
                console.log(`Navigation item removed: ${view}`);
                return true;
            }
            return false;
        } catch (error) {
            console.error('Failed to remove navigation item:', error);
            return false;
        }
    }

    /**
     * Get navigation statistics
     */
    getStats() {
        if (!this.navContainer) return {};

        try {
            const navLinks = this.navContainer.querySelectorAll('.nav-link, [data-nav-view]');
            const activeLinks = this.navContainer.querySelectorAll('.nav-link.active, [data-nav-view].active');

            return {
                totalItems: navLinks.length,
                activeItems: activeLinks.length,
                isMobile: this.isMobile(),
                mobileMenuOpen: this.mobileMenuOpen,
                breadcrumbsEnabled: this.options.enableBreadcrumbs,
                animationsEnabled: this.options.enableAnimations
            };
        } catch (error) {
            console.error('Failed to get navigation stats:', error);
            return {};
        }
    }

    /**
     * Cleanup navigation UI
     */
    cleanup() {
        try {
            // Remove mobile menu toggle
            const toggleButton = document.querySelector('.mobile-menu-toggle');
            if (toggleButton) {
                toggleButton.remove();
            }

            // Remove breadcrumb container
            if (this.breadcrumbContainer) {
                this.breadcrumbContainer.remove();
            }

            // Remove navigation classes
            if (this.navContainer) {
                this.navContainer.classList.remove('dashboard-navigation', 'mobile-navigation');
            }

            console.log('Navigation UI cleaned up');
        } catch (error) {
            console.error('Navigation UI cleanup failed:', error);
        }
    }
}

// Factory function for creating navigation UI
export function createNavigationUI(navigationState, options = {}) {
    return new NavigationUI(navigationState, options);
}
