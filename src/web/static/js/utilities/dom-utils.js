/**
 * DOM Utilities - V2 Compliant Module
 * ==================================
 *
 * DOM manipulation utilities with caching and performance optimization.
 *
 * V2 Compliance: < 300 lines, single responsibility.
 *
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

export class DOMUtils {
    constructor() {
        this.cache = new Map();
        this.logger = console;
    }

    /**
     * Unified element selection with caching
     */
    selectElement(selector, context = document) {
        const cacheKey = `${selector}-${context === document ? 'doc' : 'ctx'}`;

        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        const element = context.querySelector(selector);
        if (element) {
            this.cache.set(cacheKey, element);
        }

        return element;
    }

    /**
     * Select multiple elements
     */
    selectElements(selector, context = document) {
        const cacheKey = `multi-${selector}-${context === document ? 'doc' : 'ctx'}`;

        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        const elements = context.querySelectorAll(selector);
        this.cache.set(cacheKey, elements);

        return elements;
    }

    /**
     * Create element with attributes and content
     */
    createElement(tag, className = '', attributes = {}, content = '') {
        const element = document.createElement(tag);

        if (className) {
            element.className = className;
        }

        Object.entries(attributes).forEach(([key, value]) => {
            element.setAttribute(key, value);
        });

        if (content) {
            element.innerHTML = content;
        }

        return element;
    }

    /**
     * Add class to element
     */
    addClass(element, className) {
        if (element && element.classList) {
            element.classList.add(className);
        }
    }

    /**
     * Remove class from element
     */
    removeClass(element, className) {
        if (element && element.classList) {
            element.classList.remove(className);
        }
    }

    /**
     * Toggle class on element
     */
    toggleClass(element, className) {
        if (element && element.classList) {
            element.classList.toggle(className);
        }
    }

    /**
     * Check if element has class
     */
    hasClass(element, className) {
        return element && element.classList && element.classList.contains(className);
    }

    /**
     * Set element text content
     */
    setText(element, text) {
        if (element) {
            element.textContent = text;
        }
    }

    /**
     * Set element HTML content
     */
    setHTML(element, html) {
        if (element) {
            element.innerHTML = html;
        }
    }

    /**
     * Get element text content
     */
    getText(element) {
        return element ? element.textContent : '';
    }

    /**
     * Get element HTML content
     */
    getHTML(element) {
        return element ? element.innerHTML : '';
    }

    /**
     * Set element attribute
     */
    setAttribute(element, name, value) {
        if (element) {
            element.setAttribute(name, value);
        }
    }

    /**
     * Get element attribute
     */
    getAttribute(element, name) {
        return element ? element.getAttribute(name) : null;
    }

    /**
     * Remove element attribute
     */
    removeAttribute(element, name) {
        if (element) {
            element.removeAttribute(name);
        }
    }

    /**
     * Show element
     */
    show(element) {
        if (element) {
            element.style.display = '';
            this.removeClass(element, 'hidden');
        }
    }

    /**
     * Hide element
     */
    hide(element) {
        if (element) {
            element.style.display = 'none';
            this.addClass(element, 'hidden');
        }
    }

    /**
     * Toggle element visibility
     */
    toggleVisibility(element) {
        if (element) {
            if (element.style.display === 'none' || this.hasClass(element, 'hidden')) {
                this.show(element);
            } else {
                this.hide(element);
            }
        }
    }

    /**
     * Append child to parent
     */
    appendChild(parent, child) {
        if (parent && child) {
            parent.appendChild(child);
        }
    }

    /**
     * Remove child from parent
     */
    removeChild(parent, child) {
        if (parent && child && parent.contains(child)) {
            parent.removeChild(child);
        }
    }

    /**
     * Clear element content
     */
    clear(element) {
        if (element) {
            element.innerHTML = '';
        }
    }

    /**
     * Get element position
     */
    getPosition(element) {
        if (!element) return null;

        const rect = element.getBoundingClientRect();
        return {
            top: rect.top,
            left: rect.left,
            width: rect.width,
            height: rect.height
        };
    }

    /**
     * Scroll element into view
     */
    scrollIntoView(element, options = {}) {
        if (element && element.scrollIntoView) {
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'center',
                ...options
            });
        }
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
        this.logger.log('🧹 DOM Utils cache cleared');
    }

    /**
     * Get cache statistics
     */
    getCacheStats() {
        return {
            size: this.cache.size,
            keys: Array.from(this.cache.keys())
        };
    }
}
