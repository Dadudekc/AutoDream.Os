/**
 * DOM Utilities Module - V2 Compliant
 * DOM utility functions extracted from utilities-consolidated.js
 * V2 Compliance: ≤400 lines for compliance
 *
 * @author Agent-7 - Web Development Specialist
 * @version 3.0.0 - V2 COMPLIANCE REFACTORED
 * @license MIT
 */

/**
 * DOM Utilities Class
 * V2 Compliance: Extracted from monolithic 1263-line file
 */
export class DOMUtils {
    constructor() {
        this.name = 'DOMUtils';
        this.cache = new Map();
        this.eventListeners = new Map();
    }

    /**
     * Find element by selector
     */
    find(selector) {
        const cacheKey = `find_${selector}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        const element = document.querySelector(selector);
        this.cache.set(cacheKey, element);
        return element;
    }

    /**
     * Find all elements by selector
     */
    findAll(selector) {
        const cacheKey = `findAll_${selector}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        const elements = document.querySelectorAll(selector);
        this.cache.set(cacheKey, elements);
        return elements;
    }

    /**
     * Create element with attributes
     */
    createElement(tag, attributes = {}, textContent = '') {
        const element = document.createElement(tag);

        Object.entries(attributes).forEach(([key, value]) => {
            if (key === 'className') {
                element.className = value;
            } else if (key === 'innerHTML') {
                element.innerHTML = value;
            } else {
                element.setAttribute(key, value);
            }
        });

        if (textContent) {
            element.textContent = textContent;
        }

        return element;
    }

    /**
     * Add event listener with cleanup
     */
    addEventListener(element, event, handler, options = {}) {
        const key = `${element}_${event}`;
        const cleanup = () => element.removeEventListener(event, handler, options);

        element.addEventListener(event, handler, options);
        this.eventListeners.set(key, cleanup);

        return cleanup;
    }

    /**
     * Remove event listener
     */
    removeEventListener(element, event) {
        const key = `${element}_${event}`;
        const cleanup = this.eventListeners.get(key);

        if (cleanup) {
            cleanup();
            this.eventListeners.delete(key);
        }
    }

    /**
     * Toggle class on element
     */
    toggleClass(element, className) {
        element.classList.toggle(className);
        return element.classList.contains(className);
    }

    /**
     * Add class to element
     */
    addClass(element, className) {
        element.classList.add(className);
        return element;
    }

    /**
     * Remove class from element
     */
    removeClass(element, className) {
        element.classList.remove(className);
        return element;
    }

    /**
     * Check if element has class
     */
    hasClass(element, className) {
        return element.classList.contains(className);
    }

    /**
     * Show/hide element
     */
    toggleVisibility(element, show = null) {
        if (show === null) {
            show = element.style.display === 'none';
        }
        element.style.display = show ? '' : 'none';
        return show;
    }

    /**
     * Show element
     */
    show(element) {
        element.style.display = '';
        return element;
    }

    /**
     * Hide element
     */
    hide(element) {
        element.style.display = 'none';
        return element;
    }

    /**
     * Set element text content
     */
    setText(element, text) {
        element.textContent = text;
        return element;
    }

    /**
     * Set element HTML content
     */
    setHTML(element, html) {
        element.innerHTML = html;
        return element;
    }

    /**
     * Get element text content
     */
    getText(element) {
        return element.textContent;
    }

    /**
     * Get element HTML content
     */
    getHTML(element) {
        return element.innerHTML;
    }

    /**
     * Set element attribute
     */
    setAttribute(element, name, value) {
        element.setAttribute(name, value);
        return element;
    }

    /**
     * Get element attribute
     */
    getAttribute(element, name) {
        return element.getAttribute(name);
    }

    /**
     * Remove element attribute
     */
    removeAttribute(element, name) {
        element.removeAttribute(name);
        return element;
    }

    /**
     * Set element style
     */
    setStyle(element, styles) {
        Object.entries(styles).forEach(([property, value]) => {
            element.style[property] = value;
        });
        return element;
    }

    /**
     * Get element style
     */
    getStyle(element, property) {
        return element.style[property];
    }

    /**
     * Append child to element
     */
    appendChild(parent, child) {
        parent.appendChild(child);
        return parent;
    }

    /**
     * Remove child from element
     */
    removeChild(parent, child) {
        parent.removeChild(child);
        return parent;
    }

    /**
     * Insert element before reference
     */
    insertBefore(parent, newElement, referenceElement) {
        parent.insertBefore(newElement, referenceElement);
        return parent;
    }

    /**
     * Replace element
     */
    replaceElement(oldElement, newElement) {
        oldElement.parentNode.replaceChild(newElement, oldElement);
        return newElement;
    }

    /**
     * Clone element
     */
    cloneElement(element, deep = true) {
        return element.cloneNode(deep);
    }

    /**
     * Get element position
     */
    getPosition(element) {
        const rect = element.getBoundingClientRect();
        return {
            top: rect.top,
            left: rect.left,
            bottom: rect.bottom,
            right: rect.right,
            width: rect.width,
            height: rect.height
        };
    }

    /**
     * Scroll element into view
     */
    scrollIntoView(element, options = {}) {
        element.scrollIntoView(options);
        return element;
    }

    /**
     * Get element dimensions
     */
    getDimensions(element) {
        return {
            width: element.offsetWidth,
            height: element.offsetHeight,
            scrollWidth: element.scrollWidth,
            scrollHeight: element.scrollHeight,
            clientWidth: element.clientWidth,
            clientHeight: element.clientHeight
        };
    }

    /**
     * Check if element is visible
     */
    isVisible(element) {
        const style = window.getComputedStyle(element);
        return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
    }

    /**
     * Check if element is in viewport
     */
    isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    /**
     * Get parent element
     */
    getParent(element) {
        return element.parentElement;
    }

    /**
     * Get child elements
     */
    getChildren(element) {
        return Array.from(element.children);
    }

    /**
     * Get siblings
     */
    getSiblings(element) {
        return Array.from(element.parentElement.children).filter(child => child !== element);
    }

    /**
     * Find closest parent matching selector
     */
    closest(element, selector) {
        return element.closest(selector);
    }

    /**
     * Clear all event listeners
     */
    clearEventListeners() {
        this.eventListeners.forEach(cleanup => cleanup());
        this.eventListeners.clear();
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
    }

    /**
     * Get cache size
     */
    getCacheSize() {
        return this.cache.size;
    }
}

// Export default instance
export default new DOMUtils();
