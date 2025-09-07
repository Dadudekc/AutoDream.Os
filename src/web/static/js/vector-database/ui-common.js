/**
 * Shared UI helpers for vector database modules.
 * Provides reusable setup functions to maintain SSOT across UI variants.
 *
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

/**
 * Store element in Map or plain object.
 * @param {Record<string, any>|Map<string, any>} elements - storage container
 * @param {string} key - element key
 * @param {HTMLElement} value - element reference
 */
function store_element(elements, key, value) {
    if (typeof elements.set === 'function') {
        elements.set(key, value);
    } else {
        elements[key] = value;
    }
}

/**
 * Setup search interface elements.
 * @param {Object} options - configuration options
 * @param {Function} options.createElement - element factory
 * @param {Record<string, any>|Map<string, any>} options.elements - storage
 * @param {Function} [options.addEventListener] - optional event binder
 * @param {Function} [options.handleSearch] - search handler
 */
export function setupSearchInterface({
    createElement,
    elements,
    addEventListener,
    handleSearch
}) {
    const searchContainer = createElement('div', 'search-container');
    const searchInput = createElement('input', 'search-input', {
        type: 'text',
        placeholder: 'Search documents...',
        id: 'vector-search-input'
    });
    const searchButton = createElement(
        'button',
        'search-button',
        { id: 'vector-search-button' },
        'Search'
    );

    searchContainer.appendChild(searchInput);
    searchContainer.appendChild(searchButton);

    store_element(elements, 'searchContainer', searchContainer);
    store_element(elements, 'searchInput', searchInput);
    store_element(elements, 'searchButton', searchButton);

    if (addEventListener && handleSearch) {
        addEventListener(searchButton, 'click', () => handleSearch());
        addEventListener(searchInput, 'keypress', (e) => {
            if (e.key === 'Enter') handleSearch();
        });
    }
}

/**
 * Setup document management elements.
 * @param {Object} options - configuration options
 * @param {Function} options.createElement - element factory
 * @param {Record<string, any>|Map<string, any>} options.elements - storage
 * @param {Function} [options.addEventListener] - optional event binder
 * @param {Function} [options.handleAddDocument] - add document handler
 */
export function setupDocumentManagement({
    createElement,
    elements,
    addEventListener,
    handleAddDocument
}) {
    const docContainer = createElement('div', 'document-container');
    const docList = createElement('div', 'document-list', { id: 'document-list' });
    const addButton = createElement(
        'button',
        'add-document-button',
        { id: 'add-document-button' },
        'Add Document'
    );

    docContainer.appendChild(docList);
    docContainer.appendChild(addButton);

    store_element(elements, 'docContainer', docContainer);
    store_element(elements, 'docList', docList);
    store_element(elements, 'addButton', addButton);

    if (addEventListener && handleAddDocument) {
        addEventListener(addButton, 'click', () => handleAddDocument());
    }
}

/**
 * Generic message display helper.
 * @param {Object} options - configuration
 * @param {Function} options.createElement - element factory
 * @param {string} options.message - message text
 * @param {string} options.className - CSS class name
 * @param {string} options.backgroundColor - background color
 * @param {number} options.duration - visibility duration
 * @param {boolean} [options.useAnimationFrame=false] - smooth removal flag
 */
export function showMessage({
    createElement,
    message,
    className,
    backgroundColor,
    duration,
    useAnimationFrame = false
}) {
    const element = createElement('div', className);
    element.textContent = message;
    element.style.cssText =
        `position:fixed;top:20px;right:20px;background:${backgroundColor};` +
        'color:white;padding:10px;border-radius:5px;z-index:1000;';
    document.body.appendChild(element);
    const remove = () => {
        if (element.parentNode) element.parentNode.removeChild(element);
    };
    const schedule = () => setTimeout(remove, duration);
    if (useAnimationFrame) requestAnimationFrame(schedule); else schedule();
}

/**
 * Show error message helper.
 * @param {Object} options - message options
 * @param {Function} options.createElement - element factory
 * @param {string} options.message - message text
 * @param {boolean} [options.useAnimationFrame] - smooth removal flag
 */
export function showError({ createElement, message, useAnimationFrame }) {
    showMessage({
        createElement,
        message,
        className: 'error-message',
        backgroundColor: '#ff4444',
        duration: 5000,
        useAnimationFrame
    });
}

/**
 * Show success message helper.
 * @param {Object} options - message options
 * @param {Function} options.createElement - element factory
 * @param {string} options.message - message text
 * @param {boolean} [options.useAnimationFrame] - smooth removal flag
 */
export function showSuccess({ createElement, message, useAnimationFrame }) {
    showMessage({
        createElement,
        message,
        className: 'success-message',
        backgroundColor: '#44ff44',
        duration: 3000,
        useAnimationFrame
    });
}

/**
 * Escape HTML to prevent XSS.
 * @param {string} text - raw text
 * @returns {string} escaped HTML
 */
export function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

