/**
 * Dashboard Utils V2 - V2 Compliant Main Orchestrator
 * Main orchestrator for dashboard utility modules with lazy loading
 * REFACTORED: 522 lines → 175 lines (67% reduction)
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist
 * @version 4.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

// ================================
// IMPORT MODULAR COMPONENTS
// ================================

import { DashboardFormatters, createDashboardFormatters } from './dashboard/formatters.js';
import { DashboardDateUtils, createDashboardDateUtils } from './dashboard/date-utils.js';
import { DashboardStyleUtils, createDashboardStyleUtils } from './dashboard/style-utils.js';
import { DashboardDOMUtils, createDashboardDOMUtils } from './dashboard/dom-utils.js';

// ================================
// DASHBOARD UTILS V2 ORCHESTRATOR
// ================================

/**
 * Main orchestrator for all dashboard utility modules
 * Provides unified interface with lazy loading for optimal performance
 */
export class DashboardUtils {
    constructor(options = {}) {
        // Lazy-loaded components for memory efficiency
        this._formatters = null;
        this._dateUtils = null;
        this._styleUtils = null;
        this._domUtils = null;
        this.logger = options.logger || console;
    }

    // ================================
    // LAZY-LOADED COMPONENTS
    // ================================

    get formatters() {
        if (!this._formatters) {
            this._formatters = createDashboardFormatters();
        }
        return this._formatters;
    }

    get dateUtils() {
        if (!this._dateUtils) {
            this._dateUtils = createDashboardDateUtils();
        }
        return this._dateUtils;
    }

    get styleUtils() {
        if (!this._styleUtils) {
            this._styleUtils = createDashboardStyleUtils();
        }
        return this._styleUtils;
    }

    get domUtils() {
        if (!this._domUtils) {
            this._domUtils = createDashboardDOMUtils();
        }
        return this._domUtils;
    }

    // ================================
    // UNIFIED INTERFACE METHODS
    // ================================

    formatNumber(num) {
        return this.formatters.formatNumber(num);
    }

    formatPercentage(value) {
        return this.formatters.formatPercentage(value);
    }

    formatDate(date, format = 'short') {
        return this.dateUtils.formatDate(date, format);
    }

    addClass(element, className) {
        return this.domUtils.addClass(element, className);
    }

    removeClass(element, className) {
        return this.domUtils.removeClass(element, className);
    }

    toggleClass(element, className) {
        return this.domUtils.toggleClass(element, className);
    }

    setStyle(element, property, value) {
        return this.styleUtils.setStyle(element, property, value);
    }

    getElement(selector) {
        return this.domUtils.getElement(selector);
    }

    getElements(selector) {
        return this.domUtils.getElements(selector);
    }

    // ================================
    // UTILITY METHODS
    // ================================

    /**
     * Initialize all components
     */
    async initialize() {
        try {
            // Pre-load commonly used components
            await Promise.all([
                this.formatters,
                this.domUtils
            ]);
            console.log('✅ Dashboard Utils initialized');
        } catch (error) {
            console.error('❌ Failed to initialize Dashboard Utils:', error);
        }
    }

    /**
     * Get status of loaded components
     */
    getStatus() {
        return {
            formatters: !!this._formatters,
            dateUtils: !!this._dateUtils,
            styleUtils: !!this._styleUtils,
            domUtils: !!this._domUtils
        };
    }

    /**
     * Clear cached components
     */
    clearCache() {
        this._formatters = null;
        this._dateUtils = null;
        this._styleUtils = null;
        this._domUtils = null;
        console.log('🗑️ Dashboard Utils cache cleared');
    }
}

// ================================
// GLOBAL INSTANCE
// ================================

/**
 * Global dashboard utils instance
 */
export const dashboardUtils = new DashboardUtils();

/**
 * Convenience functions for direct access
 */
export const formatNumber = (num) => dashboardUtils.formatNumber(num);
export const formatPercentage = (value) => dashboardUtils.formatPercentage(value);
export const formatDate = (date, format) => dashboardUtils.formatDate(date, format);
export const addClass = (element, className) => dashboardUtils.addClass(element, className);
export const removeClass = (element, className) => dashboardUtils.removeClass(element, className);
export const toggleClass = (element, className) => dashboardUtils.toggleClass(element, className);
export const setStyle = (element, property, value) => dashboardUtils.setStyle(element, property, value);
export const getElement = (selector) => dashboardUtils.getElement(selector);
export const getElements = (selector) => dashboardUtils.getElements(selector);
