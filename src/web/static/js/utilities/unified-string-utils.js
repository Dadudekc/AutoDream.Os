/**
 * @fileoverview Unified String Utilities - JavaScript Adapter for Shared Core
 * @version 3.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 * 
 * JavaScript adapter that uses the shared StringCore implementation.
 * Provides a simplified API for JavaScript environments.
 */

import { StringCore } from '../../../../core/utilities/shared/string-core.js';

/**
 * Unified String Utilities Class
 * JavaScript adapter around the shared StringCore
 */
export class UnifiedStringUtils {
  constructor(config = {}) {
    this.core = new StringCore(config);
  }

  /**
   * Initialize the string utility with configuration
   */
  async initialize(config = {}) {
    return this.core.initialize(config);
  }

  /**
   * Clean up resources and reset state
   */
  async cleanup() {
    return this.core.cleanup();
  }

  /**
   * Get utility metadata and capabilities
   */
  getMetadata() {
    return this.core.getMetadata();
  }

  // === BASIC STRING OPERATIONS ===

  /**
   * Convert string to different cases
   */
  toCase(str, caseType) {
    return this.core.toCase(str, caseType);
  }

  /**
   * Trim whitespace with advanced options
   */
  trim(str, options = {}) {
    return this.core.trim(str, options);
  }

  /**
   * Pad string to specified length
   */
  pad(str, length, options = {}) {
    return this.core.pad(str, length, options);
  }

  /**
   * Reverse string with encoding support
   */
  reverse(str, options = {}) {
    return this.core.reverse(str, options);
  }

  // === STRING VALIDATION ===

  /**
   * Validate email format
   */
  validateEmail(email) {
    return this.core.validateEmail(email);
  }

  /**
   * Validate URL format
   */
  validateUrl(url) {
    return this.core.validateUrl(url);
  }

  /**
   * Validate phone number format
   */
  validatePhone(phone, format = 'US') {
    return this.core.validatePhone(phone, format);
  }

  /**
   * Validate password strength
   */
  validatePassword(password, options = {}) {
    return this.core.validatePassword(password, options);
  }

  /**
   * Validate JSON string
   */
  validateJson(jsonStr) {
    return this.core.validateJson(jsonStr);
  }

  /**
   * Validate UUID format
   */
  validateUuid(uuid) {
    return this.core.validateUuid(uuid);
  }

  // === STRING SEARCH & REPLACE ===

  /**
   * Advanced string search with multiple options
   */
  search(str, searchTerm, options = {}) {
    return this.core.search(str, searchTerm, options);
  }

  /**
   * Replace text with advanced options
   */
  replace(str, searchTerm, replacement, options = {}) {
    return this.core.replace(str, searchTerm, replacement, options);
  }

  /**
   * Replace multiple patterns at once
   */
  replaceMultiple(str, replacements) {
    return this.core.replaceMultiple(str, replacements);
  }

  // === STRING FORMATTING ===

  /**
   * Format string with placeholders
   */
  format(template, values, options = {}) {
    return this.core.format(template, values, options);
  }

  /**
   * Format currency
   */
  formatCurrency(amount, options = {}) {
    return this.core.formatCurrency(amount, options);
  }

  /**
   * Format date string
   */
  formatDate(date, options = {}) {
    return this.core.formatDate(date, options);
  }

  /**
   * Format number with locale support
   */
  formatNumber(number, options = {}) {
    return this.core.formatNumber(number, options);
  }

  // === STRING ENCODING & DECODING ===

  /**
   * Encode string to different formats
   */
  encode(str, encoding) {
    return this.core.encode(str, encoding);
  }

  /**
   * Decode string from different formats
   */
  decode(str, encoding) {
    return this.core.decode(str, encoding);
  }

  /**
   * Hash string using various algorithms
   */
  async hash(str, algorithm) {
    return this.core.hash(str, algorithm);
  }

  // === STRING ANALYSIS ===

  /**
   * Analyze string statistics
   */
  analyze(str) {
    return this.core.analyze(str);
  }

  /**
   * Extract patterns from string
   */
  extractPatterns(str, pattern) {
    return this.core.extractPatterns(str, pattern);
  }

  /**
   * Calculate string similarity
   */
  similarity(str1, str2, algorithm = 'levenshtein') {
    return this.core.similarity(str1, str2, algorithm);
  }

  // === STRING MANIPULATION ===

  /**
   * Slice string with advanced options
   */
  slice(str, start, end, options = {}) {
    return this.core.slice(str, start, end, options);
  }

  /**
   * Split string with advanced options
   */
  split(str, delimiter, options = {}) {
    return this.core.split(str, delimiter, options);
  }

  /**
   * Join array of strings
   */
  join(strings, separator, options = {}) {
    return this.core.join(strings, separator, options);
  }

  // === STRING GENERATION ===

  /**
   * Generate random string
   */
  generateRandom(length, options = {}) {
    return this.core.generateRandom(length, options);
  }

  /**
   * Generate UUID
   */
  generateUuid(version = 4) {
    return this.core.generateUuid(version);
  }

  /**
   * Generate slug from string
   */
  generateSlug(str, options = {}) {
    return this.core.generateSlug(str, options);
  }

  // === PERFORMANCE & MONITORING ===

  /**
   * Get performance metrics
   */
  getMetrics() {
    return this.core.getMetrics();
  }

  /**
   * Clear performance cache
   */
  clearCache() {
    this.core.clearCache();
  }

  /**
   * Reset performance metrics
   */
  resetMetrics() {
    this.core.resetMetrics();
  }

  // === CONVENIENCE METHODS ===

  /**
   * Simple string formatting (backward compatibility)
   */
  formatString(template, data) {
    const result = this.format(template, data);
    return result.success ? result.data : template;
  }

  /**
   * Simple input sanitization (backward compatibility)
   */
  sanitizeInput(input, options = {}) {
    const { maxLength = 1000, allowHtml = false, allowScripts = false } = options;
    
    if (typeof input !== 'string') {
      return '';
    }

    let sanitized = input.trim();

    if (sanitized.length > maxLength) {
      sanitized = sanitized.substring(0, maxLength);
    }

    if (!allowHtml) {
      sanitized = sanitized.replace(/<[^>]*>/g, '');
    }

    if (!allowScripts) {
      sanitized = sanitized.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
      sanitized = sanitized.replace(/javascript:/gi, '');
      sanitized = sanitized.replace(/on\w+\s*=/gi, '');
    }

    return sanitized;
  }

  /**
   * Simple slug generation (backward compatibility)
   */
  generateSlug(text) {
    const result = this.generateSlug(text);
    return result.success ? result.data : '';
  }

  /**
   * Simple capitalization (backward compatibility)
   */
  capitalize(text) {
    if (typeof text !== 'string' || text.length === 0) {
      return text;
    }
    return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
  }

  /**
   * Simple truncation (backward compatibility)
   */
  truncate(text, maxLength = 100, suffix = '...') {
    if (typeof text !== 'string' || text.length <= maxLength) {
      return text;
    }
    return text.substring(0, maxLength - suffix.length) + suffix;
  }
}

// Factory function for creating string utils instance
export function createUnifiedStringUtils(config = {}) {
  return new UnifiedStringUtils(config);
}

// Export default
export default UnifiedStringUtils;