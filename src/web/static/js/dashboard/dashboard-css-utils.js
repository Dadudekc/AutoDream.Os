/**
 * Dashboard CSS Utils Module - V2 Compliant
 * CSS class management utilities
 *
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

export class CSSClassManager {
    constructor() {
        this.logger = console;
    }

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

    toggleClass(element, className) {
        if (!element || !className) return false;
        try {
            return element.classList.toggle(className);
        } catch (error) {
            this.logger.error('Failed to toggle class', error);
            return false;
        }
    }

    hasClass(element, className) {
        if (!element || !className) return false;
        try {
            return element.classList.contains(className);
        } catch (error) {
            this.logger.error('Failed to check class', error);
            return false;
        }
    }

    replaceClass(element, oldClass, newClass) {
        if (!element || !oldClass || !newClass) return false;
        try {
            return element.classList.replace(oldClass, newClass);
        } catch (error) {
            this.logger.error('Failed to replace class', error);
            return false;
        }
    }

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

    getClasses(element) {
        if (!element) return [];
        try {
            return Array.from(element.classList);
        } catch (error) {
            this.logger.error('Failed to get classes', error);
            return [];
        }
    }

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
