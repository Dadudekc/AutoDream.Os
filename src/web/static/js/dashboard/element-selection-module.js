/**
 * Element Selection Module - V2 Compliant
 * DOM element selection utilities
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// ELEMENT SELECTION MODULE
// ================================

/**
 * Element selection utilities for safe DOM queries
 */
export class ElementSelectionModule {
    constructor() {
        this.logger = console;
    }

    /**
     * Safely get element by ID
     */
    getElementById(id) {
        try {
            return document.getElementById(id);
        } catch (error) {
            this.logger.warn(`Failed to get element with ID: ${id}`, error);
            return null;
        }
    }

    /**
     * Safely query selector
     */
    querySelector(selector) {
        try {
            return document.querySelector(selector);
        } catch (error) {
            this.logger.warn(`Failed to query selector: ${selector}`, error);
            return null;
        }
    }

    /**
     * Safely query selector all
     */
    querySelectorAll(selector) {
        try {
            return Array.from(document.querySelectorAll(selector));
        } catch (error) {
            this.logger.warn(`Failed to query selector all: ${selector}`, error);
            return [];
        }
    }

    /**
     * Get elements by class name
     */
    getElementsByClassName(className) {
        try {
            return Array.from(document.getElementsByClassName(className));
        } catch (error) {
            this.logger.warn(`Failed to get elements by class name: ${className}`, error);
            return [];
        }
    }

    /**
     * Get elements by tag name
     */
    getElementsByTagName(tagName) {
        try {
            return Array.from(document.getElementsByTagName(tagName));
        } catch (error) {
            this.logger.warn(`Failed to get elements by tag name: ${tagName}`, error);
            return [];
        }
    }

    /**
     * Find closest ancestor matching selector
     */
    closest(element, selector) {
        if (!element) return null;

        try {
            return element.closest(selector);
        } catch (error) {
            this.logger.warn(`Failed to find closest element: ${selector}`, error);
            return null;
        }
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create element selection module instance
 */
export function createElementSelectionModule() {
    return new ElementSelectionModule();
}

