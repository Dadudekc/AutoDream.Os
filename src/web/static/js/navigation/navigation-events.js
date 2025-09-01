/**
 * Navigation Events Module - V2 Compliant
 * Handles navigation-related events and user interactions
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
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

    /**
     * Initialize event handlers
     */
    initialize() {
        if (this.isInitialized) {
            console.warn('Navigation events already initialized');
            return;
        }

        console.log('🎯 Initializing navigation events...');
        this.setupClickHandlers();
        this.setupKeyboardHandlers();
        this.setupTouchHandlers();
        this.setupCustomEventHandlers();
        this.isInitialized = true;
        console.log('✅ Navigation events initialized');
    }

    /**
     * Setup click event handlers
     */
    setupClickHandlers() {
        try {
            // Navigation link clicks
            this.addEventHandler(document, 'click', this.handleNavigationClick.bind(this), {
                selector: '.nav-link, [data-nav-view]',
                debounce: true
            });

            // Back button clicks
            this.addEventHandler(document, 'click', this.handleBackClick.bind(this), {
                selector: '.nav-back, .back-button',
                debounce: true
            });

            console.log('Click handlers configured');
        } catch (error) {
            console.error('Failed to setup click handlers:', error);
        }
    }

    /**
     * Setup keyboard event handlers
     */
    setupKeyboardHandlers() {
        if (!this.options.enableKeyboardNavigation) return;

        try {
            this.addEventHandler(document, 'keydown', this.handleKeyboardNavigation.bind(this));

            // Arrow key navigation
            this.addEventHandler(document, 'keydown', this.handleArrowNavigation.bind(this), {
                keys: ['ArrowLeft', 'ArrowRight']
            });

            console.log('Keyboard handlers configured');
        } catch (error) {
            console.error('Failed to setup keyboard handlers:', error);
        }
    }

    /**
     * Setup touch gesture handlers
     */
    setupTouchHandlers() {
        if (!this.options.enableTouchGestures) return;

        try {
            let startX = 0;
            let startY = 0;

            this.addEventHandler(document, 'touchstart', (e) => {
                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
            });

            this.addEventHandler(document, 'touchend', (e) => {
                if (!startX || !startY) return;

                const endX = e.changedTouches[0].clientX;
                const endY = e.changedTouches[0].clientY;
                const diffX = startX - endX;
                const diffY = startY - endY;

                // Detect swipe gestures
                if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                    if (diffX > 0) {
                        this.handleSwipeLeft();
                    } else {
                        this.handleSwipeRight();
                    }
                }
            });

            console.log('Touch handlers configured');
        } catch (error) {
            console.error('Failed to setup touch handlers:', error);
        }
    }

    /**
     * Setup custom event handlers
     */
    setupCustomEventHandlers() {
        try {
            // Listen for navigation state changes
            this.navigationState.addStateListener(this.handleStateChange.bind(this));

            // Listen for programmatic navigation requests
            this.addEventHandler(window, 'navigation:navigate', this.handleProgrammaticNavigation.bind(this));

            console.log('Custom event handlers configured');
        } catch (error) {
            console.error('Failed to setup custom event handlers:', error);
        }
    }

    /**
     * Add event handler with options
     */
    addEventHandler(element, event, handler, options = {}) {
        try {
            const wrappedHandler = (e) => {
                // Check selector match
                if (options.selector) {
                    const target = e.target.closest(options.selector);
                    if (!target) return;
                    e.navTarget = target;
                }

                // Check key match
                if (options.keys && !options.keys.includes(e.key)) {
                    return;
                }

                // Debounce if requested
                if (options.debounce) {
                    this.debouncedExecute(event, () => handler(e));
                    return;
                }

                handler(e);
            };

            element.addEventListener(event, wrappedHandler);
            this.eventHandlers.set(`${event}_${options.selector || 'global'}`, {
                element,
                event,
                handler: wrappedHandler,
                options
            });

        } catch (error) {
            console.error(`Failed to add event handler for ${event}:`, error);
        }
    }

    /**
     * Handle navigation click
     */
    handleNavigationClick(e) {
        try {
            e.preventDefault();

            const target = e.navTarget;
            const view = target.dataset.navView || target.dataset.view || target.getAttribute('href')?.substring(1);

            if (view && view !== this.navigationState.getCurrentView()) {
                this.navigateToView(view, { source: 'click', element: target });
            }
        } catch (error) {
            console.error('Navigation click handler failed:', error);
        }
    }

    /**
     * Handle back button click
     */
    handleBackClick(e) {
        try {
            e.preventDefault();
            this.navigationState.goBack();
        } catch (error) {
            console.error('Back click handler failed:', error);
        }
    }

    /**
     * Handle keyboard navigation
     */
    handleKeyboardNavigation(e) {
        try {
            // Handle Escape key for back navigation
            if (e.key === 'Escape') {
                this.navigationState.goBack();
            }
        } catch (error) {
            console.error('Keyboard navigation handler failed:', error);
        }
    }

    /**
     * Handle arrow key navigation
     */
    handleArrowNavigation(e) {
        try {
            // Prevent default scrolling
            e.preventDefault();

            if (e.key === 'ArrowLeft') {
                this.navigateToPreviousView();
            } else if (e.key === 'ArrowRight') {
                this.navigateToNextView();
            }
        } catch (error) {
            console.error('Arrow navigation handler failed:', error);
        }
    }

    /**
     * Handle swipe left gesture
     */
    handleSwipeLeft() {
        try {
            this.navigateToNextView();
        } catch (error) {
            console.error('Swipe left handler failed:', error);
        }
    }

    /**
     * Handle swipe right gesture
     */
    handleSwipeRight() {
        try {
            this.navigateToPreviousView();
        } catch (error) {
            console.error('Swipe right handler failed:', error);
        }
    }

    /**
     * Handle programmatic navigation
     */
    handleProgrammaticNavigation(e) {
        try {
            const { view, options = {} } = e.detail;
            this.navigateToView(view, { ...options, source: 'programmatic' });
        } catch (error) {
            console.error('Programmatic navigation handler failed:', error);
        }
    }

    /**
     * Handle navigation state change
     */
    handleStateChange(event) {
        try {
            // Update UI to reflect current view
            this.updateActiveNavigation(event.currentView);

            // Dispatch custom event for other components
            window.dispatchEvent(new CustomEvent('navigation:stateChanged', {
                detail: event
            }));

            console.log(`Navigation state changed to: ${event.currentView}`);
        } catch (error) {
            console.error('State change handler failed:', error);
        }
    }

    /**
     * Navigate to specific view
     */
    navigateToView(view, options = {}) {
        try {
            const success = this.navigationState.setCurrentView(view, options);
            if (success) {
                // Dispatch navigation event
                window.dispatchEvent(new CustomEvent('navigation:navigated', {
                    detail: { view, options, timestamp: Date.now() }
                }));
            }
            return success;
        } catch (error) {
            console.error(`Failed to navigate to view '${view}':`, error);
            return false;
        }
    }

    /**
     * Navigate to previous view
     */
    navigateToPreviousView() {
        try {
            return this.navigationState.goBack();
        } catch (error) {
            console.error('Failed to navigate to previous view:', error);
            return false;
        }
    }

    /**
     * Navigate to next view (implementation depends on specific navigation structure)
     */
    navigateToNextView() {
        try {
            // This would need to be implemented based on specific navigation structure
            console.log('Next view navigation not implemented');
            return false;
        } catch (error) {
            console.error('Failed to navigate to next view:', error);
            return false;
        }
    }

    /**
     * Update active navigation UI
     */
    updateActiveNavigation(currentView) {
        try {
            // Remove active class from all navigation items
            document.querySelectorAll('.nav-link, [data-nav-view]').forEach(item => {
                item.classList.remove('active');
            });

            // Add active class to current view navigation item
            const activeItem = document.querySelector(`[data-nav-view="${currentView}"], [data-view="${currentView}"]`);
            if (activeItem) {
                activeItem.classList.add('active');
            }
        } catch (error) {
            console.error('Failed to update active navigation:', error);
        }
    }

    /**
     * Debounced execution
     */
    debouncedExecute(key, fn) {
        if (this.debounceTimers.has(key)) {
            clearTimeout(this.debounceTimers.get(key));
        }

        this.debounceTimers.set(key, setTimeout(() => {
            this.debounceTimers.delete(key);
            fn();
        }, this.options.debounceDelay));
    }

    /**
     * Remove all event handlers
     */
    cleanup() {
        try {
            // Clear debounce timers
            this.debounceTimers.forEach(timer => clearTimeout(timer));
            this.debounceTimers.clear();

            // Remove event handlers
            this.eventHandlers.forEach(({ element, event, handler }) => {
                element.removeEventListener(event, handler);
            });
            this.eventHandlers.clear();

            console.log('Navigation events cleaned up');
        } catch (error) {
            console.error('Navigation events cleanup failed:', error);
        }
    }
}

// Factory function for creating navigation events
export function createNavigationEvents(navigationState, options = {}) {
    return new NavigationEvents(navigationState, options);
}
