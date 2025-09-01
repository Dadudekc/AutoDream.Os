/**
 * Navigation UI Module - V2 Compliant
 * Handles navigation user interface and visual management
 * STREAMLINED: 401 lines → ~180 lines (55% reduction)
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE STREAMLINING
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

    initialize() {
        if (this.isInitialized) return;
        console.log('🎨 Initializing navigation UI...');
        this.setupNavigationContainer();
        this.setupMobileMenu();
        this.setupBreadcrumbs();
        this.setupAnimations();
        this.updateNavigationUI();
        this.isInitialized = true;
        console.log('✅ Navigation UI initialized');
    }

    setupNavigationContainer() {
        this.navContainer = document.getElementById(this.options.navContainerId);
        if (!this.navContainer) {
            console.warn(`Navigation container with ID '${this.options.navContainerId}' not found`);
            return;
        }
        this.navContainer.classList.add('dashboard-navigation');
        if (this.isMobile()) {
            this.navContainer.classList.add('mobile-navigation');
        }
        console.log('Navigation container configured');
    }

    setupMobileMenu() {
        if (!this.isMobile()) return;
        const toggleButton = document.createElement('button');
        toggleButton.className = 'mobile-menu-toggle';
        toggleButton.innerHTML = '☰';
        toggleButton.setAttribute('aria-label', 'Toggle navigation menu');
        if (this.navContainer) {
            this.navContainer.parentNode.insertBefore(toggleButton, this.navContainer);
            toggleButton.addEventListener('click', () => this.toggleMobileMenu());
        }
        console.log('Mobile menu configured');
    }

    setupBreadcrumbs() {
        if (!this.options.enableBreadcrumbs) return;
        this.breadcrumbContainer = document.createElement('nav');
        this.breadcrumbContainer.className = 'breadcrumb-navigation';
        this.breadcrumbContainer.setAttribute('aria-label', 'Breadcrumb navigation');
        const mainContent = document.querySelector('main') || document.body;
        mainContent.insertBefore(this.breadcrumbContainer, mainContent.firstChild);
        console.log('Breadcrumb navigation configured');
    }

    setupAnimations() {
        if (!this.options.enableAnimations) return;
        if (!document.getElementById('navigation-animations')) {
            const style = document.createElement('style');
            style.id = 'navigation-animations';
            style.textContent = `
                .dashboard-navigation .nav-link { transition: all 0.3s ease; }
                .dashboard-navigation .nav-link:hover { transform: translateY(-2px); }
                .dashboard-navigation .nav-link.active { background-color: #007bff; color: white; }
                .mobile-navigation { position: fixed; top: 0; left: -100%; width: 280px; height: 100vh; background: white; transition: left 0.3s ease; z-index: 1000; }
                .mobile-navigation.open { left: 0; }
                .breadcrumb-navigation { margin-bottom: 1rem; font-size: 0.875rem; }
                .breadcrumb-navigation ol { list-style: none; padding: 0; margin: 0; }
                .breadcrumb-navigation li { display: inline; }
                .breadcrumb-navigation li + li:before { content: "/"; padding: 0 0.5rem; color: #6c757d; }
            `;
            document.head.appendChild(style);
        }
        console.log('Navigation animations configured');
    }

    updateNavigationUI() {
        this.updateActiveNavigation(this.navigationState.getCurrentView());
        this.updateBreadcrumbs();
        this.updateMobileMenu();
    }

    updateActiveNavigation(currentView) {
        if (!this.navContainer) return;
        this.navContainer.querySelectorAll('.nav-link, [data-nav-view]').forEach(item => {
            item.classList.remove('active');
        });
        const activeItem = this.navContainer.querySelector(`[data-nav-view="${currentView}"], [data-view="${currentView}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }
    }

    updateBreadcrumbs() {
        if (!this.breadcrumbContainer || !this.options.enableBreadcrumbs) return;
        this.breadcrumbContainer.innerHTML = '';
        const ol = document.createElement('ol');
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
        const currentView = this.navigationState.getCurrentView();
        if (currentView !== 'overview') {
            const currentLi = document.createElement('li');
            currentLi.textContent = this.formatViewName(currentView);
            currentLi.classList.add('active');
            ol.appendChild(currentLi);
        }
        this.breadcrumbContainer.appendChild(ol);
    }

    updateMobileMenu() {
        if (!this.isMobile() || !this.navContainer) return;
        if (this.mobileMenuOpen) {
            this.navContainer.classList.add('open');
        } else {
            this.navContainer.classList.remove('open');
        }
    }

    toggleMobileMenu() {
        this.mobileMenuOpen = !this.mobileMenuOpen;
        this.updateMobileMenu();
        const toggleButton = document.querySelector('.mobile-menu-toggle');
        if (toggleButton) {
            toggleButton.innerHTML = this.mobileMenuOpen ? '✕' : '☰';
            toggleButton.setAttribute('aria-expanded', this.mobileMenuOpen.toString());
        }
    }

    addNavigationItem(view, label, options = {}) {
        if (!this.navContainer) return false;
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
        item.addEventListener('click', (e) => {
            e.preventDefault();
            this.navigationState.setCurrentView(view);
        });
        console.log(`Navigation item added: ${view}`);
        return true;
    }

    removeNavigationItem(view) {
        if (!this.navContainer) return false;
        const item = this.navContainer.querySelector(`[data-nav-view="${view}"]`);
        if (item) {
            item.remove();
            console.log(`Navigation item removed: ${view}`);
            return true;
        }
        return false;
    }

    formatViewName(view) {
        return view.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    }

    isMobile() {
        return window.innerWidth <= this.options.mobileBreakpoint;
    }

    getStats() {
        if (!this.navContainer) return {};
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
    }

    cleanup() {
        const toggleButton = document.querySelector('.mobile-menu-toggle');
        if (toggleButton) toggleButton.remove();
        if (this.breadcrumbContainer) this.breadcrumbContainer.remove();
        if (this.navContainer) {
            this.navContainer.classList.remove('dashboard-navigation', 'mobile-navigation');
        }
        console.log('Navigation UI cleaned up');
    }
}

export function createNavigationUI(navigationState, options = {}) {
    return new NavigationUI(navigationState, options);
}