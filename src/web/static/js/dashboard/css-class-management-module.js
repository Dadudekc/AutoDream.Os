/**
 * CSS Class Management Module - V2 Compliant
 * CSS class manipulation utilities
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// CSS CLASS MANAGEMENT MODULE
// ================================

/**
 * CSS class management utilities for DOM elements
 */
export class CSSClassManagementModule {
    constructor() {
        this.logger = console;
    }

    /**
     * Add CSS class
     */
    addClass(element, className) {
        if (!element || !className) return false;

        try {
            element.classList.add(className);
            return true;
        } catch (error) {
            this.logger.error('Failed to add class', error);
            return false;
        }
    }

    /**
     * Remove CSS class
     */
    removeClass(element, className) {
        if (!element || !className) return false;

        try {
            element.classList.remove(className);
            return true;
        } catch (error) {
            this.logger.error('Failed to remove class', error);
            return false;
        }
    }

    /**
     * Toggle CSS class
     */
    toggleClass(element, className) {
        if (!element || !className) return false;

        try {
            return element.classList.toggle(className);
        } catch (error) {
            this.logger.error('Failed to toggle class', error);
            return false;
        }
    }

    /**
     * Check if element has class
     */
    hasClass(element, className) {
        if (!element || !className) return false;

        try {
            return element.classList.contains(className);
        } catch (error) {
            this.logger.error('Failed to check class', error);
            return false;
        }
    }

    /**
     * Replace CSS class
     */
    replaceClass(element, oldClass, newClass) {
        if (!element || !oldClass || !newClass) return false;

        try {
            return element.classList.replace(oldClass, newClass);
        } catch (error) {
            this.logger.error('Failed to replace class', error);
            return false;
        }
    }

    /**
     * Add multiple classes
     */
    addClasses(element, classNames) {
        if (!element || !classNames) return false;

        try {
            const classes = Array.isArray(classNames) ? classNames : classNames.split(' ');
            element.classList.add(...classes);
            return true;
        } catch (error) {
            this.logger.error('Failed to add classes', error);
            return false;
        }
    }

    /**
     * Remove multiple classes
     */
    removeClasses(element, classNames) {
        if (!element || !classNames) return false;

        try {
            const classes = Array.isArray(classNames) ? classNames : classNames.split(' ');
            element.classList.remove(...classes);
            return true;
        } catch (error) {
            this.logger.error('Failed to remove classes', error);
            return false;
        }
    }

    /**
     * Toggle multiple classes
     */
    toggleClasses(element, classNames) {
        if (!element || !classNames) return false;

        try {
            const classes = Array.isArray(classNames) ? classNames : classNames.split(' ');
            const results = classes.map(className => element.classList.toggle(className));
            return results;
        } catch (error) {
            this.logger.error('Failed to toggle classes', error);
            return false;
        }
    }

    /**
     * Get all classes as array
     */
    getClasses(element) {
        if (!element) return [];

        try {
            return Array.from(element.classList);
        } catch (error) {
            this.logger.error('Failed to get classes', error);
            return [];
        }
    }

    /**
     * Set class name directly
     */
    setClassName(element, className) {
        if (!element) return false;

        try {
            element.className = className || '';
            return true;
        } catch (error) {
            this.logger.error('Failed to set class name', error);
            return false;
        }
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create CSS class management module instance
 */
export function createCSSClassManagementModule() {
    return new CSSClassManagementModule();
}

