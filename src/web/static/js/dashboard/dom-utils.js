/**
 * Dashboard DOM Utilities Module - V2 Compliant
 * DOM manipulation utilities for dashboard components
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export const DashboardDOMUtils = {
    /**
     * Safely get element by ID
     */
    getElementById(id) {
        try {
            return document.getElementById(id);
        } catch (error) {
            console.warn(`Failed to get element with ID: ${id}`, error);
            return null;
        }
    },

    /**
     * Safely query selector
     */
    querySelector(selector) {
        try {
            return document.querySelector(selector);
        } catch (error) {
            console.warn(`Failed to query selector: ${selector}`, error);
            return null;
        }
    },

    /**
     * Safely query selector all
     */
    querySelectorAll(selector) {
        try {
            return Array.from(document.querySelectorAll(selector));
        } catch (error) {
            console.warn(`Failed to query selector all: ${selector}`, error);
            return [];
        }
    },

    /**
     * Create element with attributes and content
     */
    createElement(tagName, attributes = {}, content = '') {
        try {
            const element = document.createElement(tagName);

            // Set attributes
            Object.entries(attributes).forEach(([key, value]) => {
                if (key === 'className') {
                    element.className = value;
                } else if (key === 'style' && typeof value === 'object') {
                    Object.assign(element.style, value);
                } else {
                    element.setAttribute(key, value);
                }
            });

            // Set content
            if (content) {
                if (typeof content === 'string') {
                    element.textContent = content;
                } else if (content instanceof Node) {
                    element.appendChild(content);
                }
            }

            return element;
        } catch (error) {
            console.error(`Failed to create element: ${tagName}`, error);
            return null;
        }
    },

    /**
     * Add event listener with cleanup tracking
     */
    addEventListener(element, event, handler, options = {}) {
        if (!element || !event || !handler) {
            console.warn('Invalid parameters for addEventListener');
            return null;
        }

        try {
            element.addEventListener(event, handler, options);
            return { element, event, handler, options };
        } catch (error) {
            console.error('Failed to add event listener', error);
            return null;
        }
    },

    /**
     * Remove event listener
     */
    removeEventListener(element, event, handler, options = {}) {
        if (!element || !event || !handler) {
            console.warn('Invalid parameters for removeEventListener');
            return false;
        }

        try {
            element.removeEventListener(event, handler, options);
            return true;
        } catch (error) {
            console.error('Failed to remove event listener', error);
            return false;
        }
    },

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
            console.error('Failed to toggle visibility', error);
            return false;
        }
    },

    /**
     * Add CSS class
     */
    addClass(element, className) {
        if (!element || !className) return false;

        try {
            element.classList.add(className);
            return true;
        } catch (error) {
            console.error('Failed to add class', error);
            return false;
        }
    },

    /**
     * Remove CSS class
     */
    removeClass(element, className) {
        if (!element || !className) return false;

        try {
            element.classList.remove(className);
            return true;
        } catch (error) {
            console.error('Failed to remove class', error);
            return false;
        }
    },

    /**
     * Toggle CSS class
     */
    toggleClass(element, className) {
        if (!element || !className) return false;

        try {
            return element.classList.toggle(className);
        } catch (error) {
            console.error('Failed to toggle class', error);
            return false;
        }
    },

    /**
     * Set element text content safely
     */
    setTextContent(element, text) {
        if (!element) return false;

        try {
            element.textContent = text || '';
            return true;
        } catch (error) {
            console.error('Failed to set text content', error);
            return false;
        }
    },

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
            console.error('Failed to get element dimensions', error);
            return null;
        }
    },

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
            console.error('Failed to check element visibility', error);
            return false;
        }
    },

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
            console.error('Failed to scroll to element', error);
            return false;
        }
    },

    /**
     * Create loading spinner
     */
    createLoadingSpinner(size = 'medium') {
        try {
            const sizes = {
                small: '16px',
                medium: '24px',
                large: '32px'
            };

            const spinner = this.createElement('div', {
                className: 'loading-spinner',
                style: {
                    width: sizes[size] || sizes.medium,
                    height: sizes[size] || sizes.medium,
                    border: '2px solid #f3f3f3',
                    borderTop: '2px solid #3498db',
                    borderRadius: '50%',
                    animation: 'spin 1s linear infinite'
                }
            });

            // Add CSS animation if not already present
            if (!document.getElementById('loading-spinner-styles')) {
                const style = this.createElement('style', { id: 'loading-spinner-styles' });
                style.textContent = `
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                    .loading-spinner {
                        display: inline-block;
                    }
                `;
                document.head.appendChild(style);
            }

            return spinner;
        } catch (error) {
            console.error('Failed to create loading spinner', error);
            return null;
        }
    }
};

// Factory function for creating DOM utils instance
export function createDashboardDOMUtils() {
    return { ...DashboardDOMUtils };
}
