/**
 * DOM Utils Orchestrator - V2 Compliant
 * Main orchestrator for DOM utilities framework
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

import { createElementSelectionModule } from './element-selection-module.js';
import { createElementCreationModule } from './element-creation-module.js';
import { createEventManagementModule } from './event-management-module.js';
import { createCSSClassManagementModule } from './css-class-management-module.js';
import { createElementVisibilityModule } from './element-visibility-module.js';

// ================================
// DOM UTILS ORCHESTRATOR
// ================================

/**
 * Main orchestrator for DOM utilities
 * Coordinates all DOM utility modules for V2 compliance
 */
export class DOMUtilsOrchestrator {
    constructor() {
        this.logger = console;

        // Initialize all modules
        this.elementSelection = createElementSelectionModule();
        this.elementCreation = createElementCreationModule();
        this.eventManagement = createEventManagementModule();
        this.cssClassManagement = createCSSClassManagementModule();
        this.elementVisibility = createElementVisibilityModule();

        this.modules = {
            elementSelection: this.elementSelection,
            elementCreation: this.elementCreation,
            eventManagement: this.eventManagement,
            cssClassManagement: this.cssClassManagement,
            elementVisibility: this.elementVisibility
        };
    }

    // ================================
    // ELEMENT SELECTION METHODS
    // ================================

    getElementById(id) {
        return this.elementSelection.getElementById(id);
    }

    querySelector(selector) {
        return this.elementSelection.querySelector(selector);
    }

    querySelectorAll(selector) {
        return this.elementSelection.querySelectorAll(selector);
    }

    getElementsByClassName(className) {
        return this.elementSelection.getElementsByClassName(className);
    }

    getElementsByTagName(tagName) {
        return this.elementSelection.getElementsByTagName(tagName);
    }

    closest(element, selector) {
        return this.elementSelection.closest(element, selector);
    }

    // ================================
    // ELEMENT CREATION METHODS
    // ================================

    createElement(tagName, attributes = {}, content = '') {
        return this.elementCreation.createElement(tagName, attributes, content);
    }

    createTextNode(text) {
        return this.elementCreation.createTextNode(text);
    }

    createDocumentFragment() {
        return this.elementCreation.createDocumentFragment();
    }

    createLoadingSpinner(size = 'medium') {
        return this.elementCreation.createLoadingSpinner(size);
    }

    cloneElement(element, deep = true) {
        return this.elementCreation.cloneElement(element, deep);
    }

    // ================================
    // EVENT MANAGEMENT METHODS
    // ================================

    addEventListener(element, event, handler, options = {}) {
        return this.eventManagement.addEventListener(element, event, handler, options);
    }

    removeEventListener(element, event, handler, options = {}) {
        return this.eventManagement.removeEventListener(element, event, handler, options);
    }

    removeAllListeners(element) {
        return this.eventManagement.removeAllListeners(element);
    }

    addMultipleListeners(element, events) {
        return this.eventManagement.addMultipleListeners(element, events);
    }

    dispatchEvent(element, eventName, detail = {}) {
        return this.eventManagement.dispatchEvent(element, eventName, detail);
    }

    // ================================
    // CSS CLASS MANAGEMENT METHODS
    // ================================

    addClass(element, className) {
        return this.cssClassManagement.addClass(element, className);
    }

    removeClass(element, className) {
        return this.cssClassManagement.removeClass(element, className);
    }

    toggleClass(element, className) {
        return this.cssClassManagement.toggleClass(element, className);
    }

    hasClass(element, className) {
        return this.cssClassManagement.hasClass(element, className);
    }

    replaceClass(element, oldClass, newClass) {
        return this.cssClassManagement.replaceClass(element, oldClass, newClass);
    }

    addClasses(element, classNames) {
        return this.cssClassManagement.addClasses(element, classNames);
    }

    removeClasses(element, classNames) {
        return this.cssClassManagement.removeClasses(element, classNames);
    }

    toggleClasses(element, classNames) {
        return this.cssClassManagement.toggleClasses(element, classNames);
    }

    getClasses(element) {
        return this.cssClassManagement.getClasses(element);
    }

    setClassName(element, className) {
        return this.cssClassManagement.setClassName(element, className);
    }

    // ================================
    // ELEMENT VISIBILITY METHODS
    // ================================

    toggleVisibility(element, show = null) {
        return this.elementVisibility.toggleVisibility(element, show);
    }

    showElement(element) {
        return this.elementVisibility.showElement(element);
    }

    hideElement(element) {
        return this.elementVisibility.hideElement(element);
    }

    isVisible(element) {
        return this.elementVisibility.isVisible(element);
    }

    isElementVisible(element) {
        return this.elementVisibility.isElementVisible(element);
    }

    getDimensions(element) {
        return this.elementVisibility.getDimensions(element);
    }

    scrollToElement(element, options = {}) {
        return this.elementVisibility.scrollToElement(element, options);
    }

    scrollToCenter(element) {
        return this.elementVisibility.scrollToCenter(element);
    }

    fadeIn(element, duration = 300) {
        return this.elementVisibility.fadeIn(element, duration);
    }

    fadeOut(element, duration = 300) {
        return this.elementVisibility.fadeOut(element, duration);
    }

    // ================================
    // UTILITY METHODS
    // ================================

    /**
     * Set element text content safely
     */
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

    /**
     * Get orchestrator status
     */
    getStatus() {
        return {
            modules: Object.keys(this.modules),
            moduleCount: Object.keys(this.modules).length,
            v2Compliance: 'READY',
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Cleanup all event listeners
     */
    cleanup() {
        try {
            this.eventManagement.clearAllListeners();
            return true;
        } catch (error) {
            this.logger.error('Failed to cleanup DOM utils', error);
            return false;
        }
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Legacy DashboardDOMUtils class for backward compatibility
 * @deprecated Use DOMUtilsOrchestrator instead
 */
export class DashboardDOMUtils extends DOMUtilsOrchestrator {
    constructor() {
        super();
        console.warn('[DEPRECATED] DashboardDOMUtils is deprecated. Use DOMUtilsOrchestrator instead.');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create DOM utils orchestrator instance
 */
export function createDOMUtilsOrchestrator() {
    return new DOMUtilsOrchestrator();
}

/**
 * Create legacy dashboard DOM utils (backward compatibility)
 */
export function createDashboardDOMUtils() {
    return new DashboardDOMUtils();
}

// ================================
// EXPORTS
// ================================

export default DOMUtilsOrchestrator;
