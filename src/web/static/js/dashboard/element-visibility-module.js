/**
 * Element Visibility Module - V2 Compliant
 * Element visibility and positioning utilities
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// ELEMENT VISIBILITY MODULE
// ================================

/**
 * Element visibility and positioning utilities
 */
export class ElementVisibilityModule {
    constructor() {
        this.logger = console;
    }

    /**
     * Toggle element visibility
     */
    toggleVisibility(element, show = null) {
        if (!element) return false;

        try {
            const shouldShow = show !== null ? show : element.style.display === 'none';
            element.style.display = shouldShow ? '' : 'none';
            return shouldShow;
        } catch (error) {
            this.logger.error('Failed to toggle visibility', error);
            return false;
        }
    }

    /**
     * Show element
     */
    showElement(element) {
        return this.toggleVisibility(element, true);
    }

    /**
     * Hide element
     */
    hideElement(element) {
        return this.toggleVisibility(element, false);
    }

    /**
     * Check if element is visible
     */
    isVisible(element) {
        if (!element) return false;

        try {
            return element.style.display !== 'none' &&
                   element.style.visibility !== 'hidden' &&
                   element.style.opacity !== '0';
        } catch (error) {
            this.logger.error('Failed to check visibility', error);
            return false;
        }
    }

    /**
     * Check if element is visible in viewport
     */
    isElementVisible(element) {
        if (!element) return false;

        try {
            const rect = element.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        } catch (error) {
            this.logger.error('Failed to check element visibility', error);
            return false;
        }
    }

    /**
     * Get element dimensions
     */
    getDimensions(element) {
        if (!element) return null;

        try {
            const rect = element.getBoundingClientRect();
            return {
                width: rect.width,
                height: rect.height,
                top: rect.top,
                left: rect.left,
                right: rect.right,
                bottom: rect.bottom
            };
        } catch (error) {
            this.logger.error('Failed to get element dimensions', error);
            return null;
        }
    }

    /**
     * Smooth scroll to element
     */
    scrollToElement(element, options = {}) {
        if (!element) return false;

        try {
            const defaultOptions = {
                behavior: 'smooth',
                block: 'start',
                inline: 'nearest',
                ...options
            };

            element.scrollIntoView(defaultOptions);
            return true;
        } catch (error) {
            this.logger.error('Failed to scroll to element', error);
            return false;
        }
    }

    /**
     * Scroll element into center of viewport
     */
    scrollToCenter(element) {
        return this.scrollToElement(element, { block: 'center', inline: 'center' });
    }

    /**
     * Fade in element
     */
    fadeIn(element, duration = 300) {
        if (!element) return false;

        try {
            element.style.opacity = '0';
            element.style.display = '';
            element.style.transition = `opacity ${duration}ms ease-in-out`;

            setTimeout(() => {
                element.style.opacity = '1';
            }, 10);

            return true;
        } catch (error) {
            this.logger.error('Failed to fade in element', error);
            return false;
        }
    }

    /**
     * Fade out element
     */
    fadeOut(element, duration = 300) {
        if (!element) return false;

        try {
            element.style.opacity = '1';
            element.style.transition = `opacity ${duration}ms ease-in-out`;

            setTimeout(() => {
                element.style.opacity = '0';
                setTimeout(() => {
                    element.style.display = 'none';
                }, duration);
            }, 10);

            return true;
        } catch (error) {
            this.logger.error('Failed to fade out element', error);
            return false;
        }
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create element visibility module instance
 */
export function createElementVisibilityModule() {
    return new ElementVisibilityModule();
}
