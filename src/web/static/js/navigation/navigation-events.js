/**
 * Navigation Events Module - V2 Compliant
 * Handles navigation-related events and user interactions
 * STREAMLINED: 350 lines → ~180 lines (49% reduction)
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE STREAMLINING
 * @license MIT
 */

export class NavigationEvents {
    constructor(navigationState, options = {}) {
        this.navigationState = navigationState;
        this.options = {
            debounceDelay: 300,
            enableKeyboardNavigation: true,
            enableTouchGestures: false,
            ...options
        };
        this.eventHandlers = new Map();
        this.debounceTimers = new Map();
        this.isInitialized = false;
    }

    initialize() {
        if (this.isInitialized) return;
        console.log('🎯 Initializing navigation events...');
        this.setupClickHandlers();
        this.setupKeyboardHandlers();
        this.setupTouchHandlers();
        this.setupCustomEventHandlers();
        this.isInitialized = true;
        console.log('✅ Navigation events initialized');
    }

    setupClickHandlers() {
        this.addEventHandler(document, 'click', this.handleNavigationClick.bind(this), {
            selector: '.nav-link, [data-nav-view]',
            debounce: true
        });
        this.addEventHandler(document, 'click', this.handleBackClick.bind(this), {
            selector: '.nav-back, .back-button',
            debounce: true
        });
        console.log('Click handlers configured');
    }

    setupKeyboardHandlers() {
        if (!this.options.enableKeyboardNavigation) return;
        this.addEventHandler(document, 'keydown', this.handleKeyboardNavigation.bind(this));
        this.addEventHandler(document, 'keydown', this.handleArrowNavigation.bind(this), {
            keys: ['ArrowLeft', 'ArrowRight']
        });
        console.log('Keyboard handlers configured');
    }

    setupTouchHandlers() {
        if (!this.options.enableTouchGestures) return;
        let startX = 0, startY = 0;
        this.addEventHandler(document, 'touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });
        this.addEventHandler(document, 'touchend', (e) => {
            if (!startX || !startY) return;
            const endX = e.changedTouches[0].clientX;
            const diffX = startX - endX;
            const diffY = startY - endY;
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                diffX > 0 ? this.handleSwipeLeft() : this.handleSwipeRight();
            }
        });
        console.log('Touch handlers configured');
    }

    setupCustomEventHandlers() {
        this.navigationState.addStateListener(this.handleStateChange.bind(this));
        this.addEventHandler(window, 'navigation:navigate', this.handleProgrammaticNavigation.bind(this));
        console.log('Custom event handlers configured');
    }

    addEventHandler(element, event, handler, options = {}) {
        const wrappedHandler = (e) => {
            if (options.selector) {
                const target = e.target.closest(options.selector);
                if (!target) return;
                e.navTarget = target;
            }
            if (options.keys && !options.keys.includes(e.key)) return;
            if (options.debounce) {
                this.debouncedExecute(event, () => handler(e));
                return;
            }
            handler(e);
        };
        element.addEventListener(event, wrappedHandler);
        this.eventHandlers.set(`${event}_${options.selector || 'global'}`, {
            element, event, handler: wrappedHandler, options
        });
    }

    handleNavigationClick(e) {
        e.preventDefault();
        const target = e.navTarget;
        const view = target.dataset.navView || target.dataset.view || target.getAttribute('href')?.substring(1);
        if (view && view !== this.navigationState.getCurrentView()) {
            this.navigateToView(view, { source: 'click', element: target });
        }
    }

    handleBackClick(e) {
        e.preventDefault();
        this.navigationState.goBack();
    }

    handleKeyboardNavigation(e) {
        if (e.key === 'Escape') {
            this.navigationState.goBack();
        }
    }

    handleArrowNavigation(e) {
        e.preventDefault();
        if (e.key === 'ArrowLeft') {
            this.navigateToPreviousView();
        } else if (e.key === 'ArrowRight') {
            this.navigateToNextView();
        }
    }

    handleSwipeLeft() {
        this.navigateToNextView();
    }

    handleSwipeRight() {
        this.navigateToPreviousView();
    }

    handleProgrammaticNavigation(e) {
        const { view, options = {} } = e.detail;
        this.navigateToView(view, { ...options, source: 'programmatic' });
    }

    handleStateChange(event) {
        window.dispatchEvent(new CustomEvent('navigation:stateChanged', { detail: event }));
        console.log(`Navigation state changed: ${event.currentView}`);
    }

    navigateToView(view, options = {}) {
        const success = this.navigationState.setCurrentView(view, options);
        if (success) {
            window.dispatchEvent(new CustomEvent('navigation:navigated', {
                detail: { view, options, timestamp: Date.now() }
            }));
        }
        return success;
    }

    navigateToPreviousView() {
        return this.navigationState.goBack();
    }

    navigateToNextView() {
        console.log('Next view navigation not implemented');
        return false;
    }

    debouncedExecute(key, fn) {
        if (this.debounceTimers.has(key)) {
            clearTimeout(this.debounceTimers.get(key));
        }
        this.debounceTimers.set(key, setTimeout(() => {
            this.debounceTimers.delete(key);
            fn();
        }, this.options.debounceDelay));
    }

    cleanup() {
        this.debounceTimers.forEach(timer => clearTimeout(timer));
        this.debounceTimers.clear();
        this.eventHandlers.forEach(({ element, event, handler }) => {
            element.removeEventListener(event, handler);
        });
        this.eventHandlers.clear();
        console.log('Navigation events cleaned up');
    }
}

export function createNavigationEvents(navigationState, options = {}) {
    return new NavigationEvents(navigationState, options);
}