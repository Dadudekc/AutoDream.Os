/**
 * Element Creation Module - V2 Compliant
 * DOM element creation utilities
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// ELEMENT CREATION MODULE
// ================================

/**
 * Element creation utilities for dynamic DOM manipulation
 */
export class ElementCreationModule {
    constructor() {
        this.logger = console;
    }

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
            this.logger.error(`Failed to create element: ${tagName}`, error);
            return null;
        }
    }

    /**
     * Create text node
     */
    createTextNode(text) {
        try {
            return document.createTextNode(text || '');
        } catch (error) {
            this.logger.error('Failed to create text node', error);
            return null;
        }
    }

    /**
     * Create document fragment for batch operations
     */
    createDocumentFragment() {
        try {
            return document.createDocumentFragment();
        } catch (error) {
            this.logger.error('Failed to create document fragment', error);
            return null;
        }
    }

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
            this.ensureSpinnerStyles();

            return spinner;
        } catch (error) {
            this.logger.error('Failed to create loading spinner', error);
            return null;
        }
    }

    /**
     * Ensure spinner CSS styles are present
     */
    ensureSpinnerStyles() {
        try {
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
        } catch (error) {
            this.logger.error('Failed to ensure spinner styles', error);
        }
    }

    /**
     * Clone element
     */
    cloneElement(element, deep = true) {
        if (!element) return null;

        try {
            return element.cloneNode(deep);
        } catch (error) {
            this.logger.error('Failed to clone element', error);
            return null;
        }
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create element creation module instance
 */
export function createElementCreationModule() {
    return new ElementCreationModule();
}
