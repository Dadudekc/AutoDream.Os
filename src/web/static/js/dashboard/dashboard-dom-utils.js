/**
 * Dashboard DOM Utils Module - V2 Compliant
 * DOM manipulation utilities
 *
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

export class DOMUtils {
    constructor() {
        this.logger = console;
        this._eventListeners = new WeakMap();
    }

    getElementById(id) {
        if (!id) return null;
        try {
            return document.getElementById(id);
        } catch (error) {
            this.logger.error('Failed to get element by ID', error);
            return null;
        }
    }

    querySelector(selector) {
        if (!selector) return null;
        try {
            return document.querySelector(selector);
        } catch (error) {
            this.logger.error('Failed to query selector', error);
            return null;
        }
    }

    querySelectorAll(selector) {
        if (!selector) return [];
        try {
            return Array.from(document.querySelectorAll(selector));
        } catch (error) {
            this.logger.error('Failed to query selector all', error);
            return [];
        }
    }

    getElementsByClassName(className) {
        if (!className) return [];
        try {
            return Array.from(document.getElementsByClassName(className));
        } catch (error) {
            this.logger.error('Failed to get elements by class name', error);
            return [];
        }
    }

    getElementsByTagName(tagName) {
        if (!tagName) return [];
        try {
            return Array.from(document.getElementsByTagName(tagName));
        } catch (error) {
            this.logger.error('Failed to get elements by tag name', error);
            return [];
        }
    }

    closest(element, selector) {
        if (!element || !selector) return null;
        try {
            return element.closest(selector);
        } catch (error) {
            this.logger.error('Failed to find closest element', error);
            return null;
        }
    }

    createElement(tagName, attributes = {}, content = '') {
        if (!tagName) return null;
        try {
            const element = document.createElement(tagName);

            Object.entries(attributes).forEach(([key, value]) => {
                if (key === 'className' && Array.isArray(value)) {
                    element.className = value.join(' ');
                } else if (key === 'style' && typeof value === 'object') {
                    Object.assign(element.style, value);
                } else {
                    element.setAttribute(key, value);
                }
            });

            if (content) {
                element.textContent = content;
            }

            return element;
        } catch (error) {
            this.logger.error('Failed to create element', error);
            return null;
        }
    }

    createTextNode(text) {
        try {
            return document.createTextNode(text || '');
        } catch (error) {
            this.logger.error('Failed to create text node', error);
            return null;
        }
    }

    cloneElement(element, deep = true) {
        if (!element) return null;
        try {
            return element.cloneNode(deep);
        } catch (error) {
            this.logger.error('Failed to clone element', error);
            return null;
        }
    }

    toggleVisibility(element, show = null) {
        if (!element) return false;
        try {
            const currentDisplay = window.getComputedStyle(element).display;
            const shouldShow = show !== null ? show : currentDisplay === 'none';

            element.style.display = shouldShow ? (element.dataset.originalDisplay || 'block') : 'none';

            if (shouldShow && !element.dataset.originalDisplay) {
                element.dataset.originalDisplay = currentDisplay;
            }

            return shouldShow;
        } catch (error) {
            this.logger.error('Failed to toggle visibility', error);
            return false;
        }
    }

    showElement(element) {
        return this.toggleVisibility(element, true);
    }

    hideElement(element) {
        return this.toggleVisibility(element, false);
    }

    isVisible(element) {
        if (!element) return false;
        try {
            const style = window.getComputedStyle(element);
            return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
        } catch (error) {
            this.logger.error('Failed to check visibility', error);
            return false;
        }
    }

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
            this.logger.error('Failed to get dimensions', error);
            return null;
        }
    }

    setTextContent(element, text) {
        if (!element) return false;
        try {
            element.textContent = text || '';
            return true;
        } catch (error) {
            this.logger.error('Failed to set text content', error);
            return false;
        }
    }

    addEventListener(element, event, handler, options = {}) {
        if (!element || !event || !handler) return false;
        try {
            element.addEventListener(event, handler, options);

            if (!this._eventListeners.has(element)) {
                this._eventListeners.set(element, new Map());
            }
            const elementListeners = this._eventListeners.get(element);
            if (!elementListeners.has(event)) {
                elementListeners.set(event, new Set());
            }
            elementListeners.get(event).add(handler);

            return true;
        } catch (error) {
            this.logger.error('Failed to add event listener', error);
            return false;
        }
    }

    removeEventListener(element, event, handler, options = {}) {
        if (!element || !event || !handler) return false;
        try {
            element.removeEventListener(event, handler, options);

            if (this._eventListeners.has(element)) {
                const elementListeners = this._eventListeners.get(element);
                if (elementListeners.has(event)) {
                    elementListeners.get(event).delete(handler);
                }
            }

            return true;
        } catch (error) {
            this.logger.error('Failed to remove event listener', error);
            return false;
        }
    }

    cleanup() {
        try {
            this._eventListeners = new WeakMap();
            return true;
        } catch (error) {
            this.logger.error('Failed to cleanup DOM utils', error);
            return false;
        }
    }
}
