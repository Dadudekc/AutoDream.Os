/**
 * Unified Frontend Utilities - V2 Compliant Module
 * ===============================================
 * 
 * Main utility coordinator that combines all utility modules.
 * Provides unified API for frontend utilities.
 * 
 * V2 Compliance: < 300 lines, single responsibility.
 * 
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

import { DOMUtils } from './dom-utils.js';
import { CacheUtils } from './cache-utils.js';
import { ValidationUtils } from './validation-utils.js';
import { EventUtils } from './event-utils.js';

export class UnifiedFrontendUtilities {
    constructor() {
        this.dom = new DOMUtils();
        this.cache = new CacheUtils();
        this.validation = new ValidationUtils();
        this.events = new EventUtils();
        this.logger = console;
    }

    /**
     * Initialize utilities
     */
    initialize() {
        this.logger.log('✅ Unified Frontend Utilities initialized');
    }

    /**
     * Get DOM utilities
     */
    getDOM() {
        return this.dom;
    }

    /**
     * Get cache utilities
     */
    getCache() {
        return this.cache;
    }

    /**
     * Get validation utilities
     */
    getValidation() {
        return this.validation;
    }

    /**
     * Get event utilities
     */
    getEvents() {
        return this.events;
    }

    /**
     * Quick element selection
     */
    $(selector, context = document) {
        return this.dom.selectElement(selector, context);
    }

    /**
     * Quick element selection (multiple)
     */
    $$(selector, context = document) {
        return this.dom.selectElements(selector, context);
    }

    /**
     * Quick element creation
     */
    create(tag, className = '', attributes = {}, content = '') {
        return this.dom.createElement(tag, className, attributes, content);
    }

    /**
     * Quick event listener
     */
    on(element, event, handler, options = {}) {
        this.events.addEventListener(element, event, handler, options);
    }

    /**
     * Quick event listener removal
     */
    off(element, event) {
        this.events.removeEventListener(element, event);
    }

    /**
     * Quick one-time event listener
     */
    once(element, event, handler, options = {}) {
        this.events.addOnceEventListener(element, event, handler, options);
    }

    /**
     * Quick event delegation
     */
    delegate(parent, selector, event, handler) {
        this.events.delegate(parent, selector, event, handler);
    }

    /**
     * Quick custom event emission
     */
    emit(element, eventName, detail = {}) {
        this.events.emitEvent(element, eventName, detail);
    }

    /**
     * Quick global event emission
     */
    emitGlobal(eventName, detail = {}) {
        this.events.emitGlobalEvent(eventName, detail);
    }

    /**
     * Quick global event listener
     */
    onGlobal(eventName, handler) {
        this.events.onGlobalEvent(eventName, handler);
    }

    /**
     * Quick cache operations
     */
    setCache(key, value, ttl = null) {
        this.cache.set(key, value, ttl);
    }

    getCache(key) {
        return this.cache.get(key);
    }

    hasCache(key) {
        return this.cache.has(key);
    }

    deleteCache(key) {
        this.cache.delete(key);
    }

    /**
     * Quick validation
     */
    validateEmail(email) {
        return this.validation.isValidEmail(email);
    }

    validateURL(url) {
        return this.validation.isValidURL(url);
    }

    validatePhone(phone) {
        return this.validation.isValidPhone(phone);
    }

    validatePassword(password) {
        return this.validation.validatePassword(password);
    }

    validateForm(formData, rules) {
        return this.validation.validateForm(formData, rules);
    }

    /**
     * Utility functions
     */
    throttle(func, delay) {
        return this.events.throttle(func, delay);
    }

    debounce(func, delay) {
        return this.events.debounce(func, delay);
    }

    sanitizeHTML(html) {
        return this.validation.sanitizeHTML(html);
    }

    sanitizeString(str) {
        return this.validation.sanitizeString(str);
    }

    /**
     * Get utility statistics
     */
    getStats() {
        return {
            dom: this.dom.getCacheStats(),
            cache: this.cache.getStats(),
            events: this.events.getStats()
        };
    }

    /**
     * Cleanup all utilities
     */
    cleanup() {
        this.dom.clearCache();
        this.cache.clear();
        this.events.cleanup();
        this.logger.log('🧹 Unified Frontend Utilities cleaned up');
    }

    /**
     * Export utility data
     */
    export() {
        return {
            cache: this.cache.export(),
            stats: this.getStats(),
            exportedAt: new Date().toISOString()
        };
    }

    /**
     * Import utility data
     */
    import(data) {
        if (data.cache) {
            this.cache.import(data.cache);
        }
        this.logger.log('📥 Utility data imported');
    }
}
