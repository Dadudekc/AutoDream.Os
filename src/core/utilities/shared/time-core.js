/**
 * @fileoverview Shared Time Utilities Core - Universal JavaScript Implementation
 * @version 3.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 * 
 * Universal time utility functions that work in both Node.js and browser environments.
 * This is the core implementation that both TypeScript and JavaScript utilities will use.
 */

/**
 * Universal Time Utilities Core
 * Provides comprehensive time manipulation, formatting, and calculation capabilities
 * Works in both Node.js and browser environments
 */
export class TimeCore {
  constructor(config = {}) {
    this.config = {
      defaultTimezone: 'UTC',
      defaultLocale: 'en-US',
      maxCacheSize: 1000,
      enableMetrics: true,
      enableCaching: true,
      ...config
    };
    
    this.metrics = {
      totalOperations: 0,
      totalProcessingTime: 0,
      cacheHits: 0,
      cacheMisses: 0,
      errors: 0,
      memoryUsage: 0
    };
    
    this.cache = new Map();
    this.maxCacheSize = this.config.maxCacheSize;
  }

  /**
   * Initialize the time utility with configuration
   */
  async initialize(config = {}) {
    try {
      this.config = { ...this.config, ...config };
      this.maxCacheSize = this.config.maxCacheSize;
    } catch (error) {
      this.metrics.errors++;
      throw new Error(`TimeCore initialization failed: ${error}`);
    }
  }

  /**
   * Clean up resources and reset state
   */
  async cleanup() {
    try {
      this.cache.clear();
      this.resetMetrics();
    } catch (error) {
      throw new Error(`TimeCore cleanup failed: ${error}`);
    }
  }

  /**
   * Get utility metadata and capabilities
   */
  getMetadata() {
    return {
      name: 'TimeCore',
      version: '3.0.0',
      capabilities: [
        'creation', 'parsing', 'formatting', 'calculation', 'validation',
        'comparison', 'conversion', 'ranges', 'business', 'performance'
      ],
      dependencies: []
    };
  }

  // === TIME CREATION & PARSING ===

  /**
   * Create date from input
   */
  create(input, options = {}) {
    const startTime = performance.now();
    
    try {
      let result;
      
      if (!input) {
        result = new Date();
      } else if (input instanceof Date) {
        result = new Date(input);
      } else if (typeof input === 'string') {
        result = new Date(input);
      } else if (typeof input === 'number') {
        result = new Date(input);
      } else {
        return this.createErrorResult('Invalid input type');
      }

      if (isNaN(result.getTime())) {
        return this.createErrorResult('Invalid date');
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Date creation failed: ${error}`);
    }
  }

  /**
   * Parse date string with format
   */
  parse(dateString, options = {}) {
    const startTime = performance.now();
    
    try {
      if (!dateString || typeof dateString !== 'string') {
        return this.createErrorResult('Invalid date string');
      }

      const { strict = false } = options;
      let result;

      if (options.format) {
        result = this.parseWithFormat(dateString, options.format);
      } else {
        result = new Date(dateString);
      }

      if (isNaN(result.getTime())) {
        if (strict) {
          return this.createErrorResult('Invalid date format');
        }
        // Try alternative parsing methods
        result = this.tryAlternativeParsing(dateString);
        if (isNaN(result.getTime())) {
          return this.createErrorResult('Unable to parse date');
        }
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Date parsing failed: ${error}`);
    }
  }

  /**
   * Get current time
   */
  now(options = {}) {
    const startTime = performance.now();
    
    try {
      const { precision = 'milliseconds' } = options;
      const now = new Date();
      
      let result = now;
      if (precision === 'seconds') {
        result = new Date(Math.floor(now.getTime() / 1000) * 1000);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Now operation failed: ${error}`);
    }
  }

  /**
   * Get UTC time
   */
  utc(options = {}) {
    const startTime = performance.now();
    
    try {
      const { precision = 'milliseconds' } = options;
      const now = new Date();
      const utc = new Date(now.getTime() + (now.getTimezoneOffset() * 60000));
      
      let result = utc;
      if (precision === 'seconds') {
        result = new Date(Math.floor(utc.getTime() / 1000) * 1000);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`UTC operation failed: ${error}`);
    }
  }

  // === TIME FORMATTING ===

  /**
   * Format date with options
   */
  format(date, options = {}) {
    const startTime = performance.now();
    
    try {
      const dateObj = this.toDate(date);
      if (!dateObj) {
        return this.createErrorResult('Invalid date');
      }

      const {
        locale = 'en-US',
        timeZone = 'UTC',
        format = 'medium',
        customFormat,
        includeTime = true,
        includeDate = true,
        includeTimezone = false
      } = options;

      let result;

      if (customFormat) {
        result = this.formatWithCustomFormat(dateObj, customFormat);
      } else {
        const formatOptions = this.getFormatOptions(format, includeTime, includeDate);
        result = new Intl.DateTimeFormat(locale, {
          ...formatOptions,
          timeZone
        }).format(dateObj);
      }

      if (includeTimezone) {
        result += ` (${timeZone})`;
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Date formatting failed: ${error}`);
    }
  }

  /**
   * Format relative time
   */
  formatRelative(date, options = {}) {
    const startTime = performance.now();
    
    try {
      const dateObj = this.toDate(date);
      const baseDate = this.toDate(options.baseDate) || new Date();
      
      if (!dateObj) {
        return this.createErrorResult('Invalid date');
      }

      const diffMs = dateObj.getTime() - baseDate.getTime();
      const diffSeconds = Math.floor(diffMs / 1000);
      const diffMinutes = Math.floor(diffSeconds / 60);
      const diffHours = Math.floor(diffMinutes / 60);
      const diffDays = Math.floor(diffHours / 24);
      const diffWeeks = Math.floor(diffDays / 7);
      const diffMonths = Math.floor(diffDays / 30);
      const diffYears = Math.floor(diffDays / 365);

      const { precision = 'days', includeSuffix = true } = options;
      let result;

      if (Math.abs(diffYears) >= 1 && ['years', 'months', 'days', 'hours', 'minutes', 'seconds'].includes(precision)) {
        result = `${Math.abs(diffYears)} year${Math.abs(diffYears) !== 1 ? 's' : ''}`;
      } else if (Math.abs(diffMonths) >= 1 && ['months', 'days', 'hours', 'minutes', 'seconds'].includes(precision)) {
        result = `${Math.abs(diffMonths)} month${Math.abs(diffMonths) !== 1 ? 's' : ''}`;
      } else if (Math.abs(diffWeeks) >= 1 && ['days', 'hours', 'minutes', 'seconds'].includes(precision)) {
        result = `${Math.abs(diffWeeks)} week${Math.abs(diffWeeks) !== 1 ? 's' : ''}`;
      } else if (Math.abs(diffDays) >= 1 && ['days', 'hours', 'minutes', 'seconds'].includes(precision)) {
        result = `${Math.abs(diffDays)} day${Math.abs(diffDays) !== 1 ? 's' : ''}`;
      } else if (Math.abs(diffHours) >= 1 && ['hours', 'minutes', 'seconds'].includes(precision)) {
        result = `${Math.abs(diffHours)} hour${Math.abs(diffHours) !== 1 ? 's' : ''}`;
      } else if (Math.abs(diffMinutes) >= 1 && ['minutes', 'seconds'].includes(precision)) {
        result = `${Math.abs(diffMinutes)} minute${Math.abs(diffMinutes) !== 1 ? 's' : ''}`;
      } else {
        result = `${Math.abs(diffSeconds)} second${Math.abs(diffSeconds) !== 1 ? 's' : ''}`;
      }

      if (includeSuffix) {
        if (diffMs > 0) {
          result += ' from now';
        } else if (diffMs < 0) {
          result += ' ago';
        } else {
          result = 'now';
        }
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Relative formatting failed: ${error}`);
    }
  }

  // === TIME CALCULATIONS ===

  /**
   * Add time to date
   */
  add(date, amount, options = {}) {
    const startTime = performance.now();
    
    try {
      const dateObj = this.toDate(date);
      if (!dateObj) {
        return this.createErrorResult('Invalid date');
      }

      const { unit = 'days', businessDays = false } = options;
      let result = new Date(dateObj);

      if (businessDays && unit === 'days') {
        result = this.addBusinessDays(result, amount);
      } else {
        switch (unit) {
          case 'milliseconds':
            result.setTime(result.getTime() + amount);
            break;
          case 'seconds':
            result.setTime(result.getTime() + (amount * 1000));
            break;
          case 'minutes':
            result.setTime(result.getTime() + (amount * 60 * 1000));
            break;
          case 'hours':
            result.setTime(result.getTime() + (amount * 60 * 60 * 1000));
            break;
          case 'days':
            result.setDate(result.getDate() + amount);
            break;
          case 'weeks':
            result.setDate(result.getDate() + (amount * 7));
            break;
          case 'months':
            result.setMonth(result.getMonth() + amount);
            break;
          case 'years':
            result.setFullYear(result.getFullYear() + amount);
            break;
          default:
            return this.createErrorResult(`Unsupported unit: ${unit}`);
        }
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Date addition failed: ${error}`);
    }
  }

  /**
   * Subtract time from date
   */
  subtract(date, amount, options = {}) {
    return this.add(date, -amount, options);
  }

  /**
   * Calculate difference between dates
   */
  difference(date1, date2, options = {}) {
    const startTime = performance.now();
    
    try {
      const dateObj1 = this.toDate(date1);
      const dateObj2 = this.toDate(date2);
      
      if (!dateObj1 || !dateObj2) {
        return this.createErrorResult('Invalid dates');
      }

      const { unit = 'milliseconds', absolute = true } = options;
      let diffMs = dateObj2.getTime() - dateObj1.getTime();
      
      if (absolute) {
        diffMs = Math.abs(diffMs);
      }

      let result;
      switch (unit) {
        case 'milliseconds':
          result = diffMs;
          break;
        case 'seconds':
          result = Math.floor(diffMs / 1000);
          break;
        case 'minutes':
          result = Math.floor(diffMs / (1000 * 60));
          break;
        case 'hours':
          result = Math.floor(diffMs / (1000 * 60 * 60));
          break;
        case 'days':
          result = Math.floor(diffMs / (1000 * 60 * 60 * 24));
          break;
        case 'weeks':
          result = Math.floor(diffMs / (1000 * 60 * 60 * 24 * 7));
          break;
        case 'months':
          result = Math.floor(diffMs / (1000 * 60 * 60 * 24 * 30));
          break;
        case 'years':
          result = Math.floor(diffMs / (1000 * 60 * 60 * 24 * 365));
          break;
        default:
          return this.createErrorResult(`Unsupported unit: ${unit}`);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Date difference calculation failed: ${error}`);
    }
  }

  // === TIME VALIDATION ===

  /**
   * Validate date
   */
  validate(date, options = {}) {
    try {
      const errors = [];
      const warnings = [];
      
      const dateObj = this.toDate(date);
      if (!dateObj || isNaN(dateObj.getTime())) {
        errors.push('Invalid date');
        return { isValid: false, errors, warnings };
      }

      const { minDate, maxDate, allowFuture = true, allowPast = true } = options;
      const now = new Date();

      if (minDate) {
        const minDateObj = this.toDate(minDate);
        if (minDateObj && dateObj < minDateObj) {
          errors.push(`Date is before minimum date: ${minDate}`);
        }
      }

      if (maxDate) {
        const maxDateObj = this.toDate(maxDate);
        if (maxDateObj && dateObj > maxDateObj) {
          errors.push(`Date is after maximum date: ${maxDate}`);
        }
      }

      if (!allowFuture && dateObj > now) {
        errors.push('Future dates are not allowed');
      }

      if (!allowPast && dateObj < now) {
        errors.push('Past dates are not allowed');
      }

      return {
        isValid: errors.length === 0,
        errors,
        warnings,
        normalizedDate: dateObj
      };
    } catch (error) {
      return {
        isValid: false,
        errors: [`Validation error: ${error}`],
        warnings: []
      };
    }
  }

  /**
   * Check if date is valid
   */
  isValid(date) {
    const dateObj = this.toDate(date);
    return dateObj !== null && !isNaN(dateObj.getTime());
  }

  /**
   * Check if date is in the past
   */
  isPast(date, options = {}) {
    const dateObj = this.toDate(date);
    if (!dateObj) return false;

    const now = new Date();
    const { includeToday = false } = options;

    if (includeToday) {
      return dateObj <= now;
    }
    return dateObj < now;
  }

  /**
   * Check if date is in the future
   */
  isFuture(date, options = {}) {
    const dateObj = this.toDate(date);
    if (!dateObj) return false;

    const now = new Date();
    const { includeToday = false } = options;

    if (includeToday) {
      return dateObj >= now;
    }
    return dateObj > now;
  }

  /**
   * Check if date is today
   */
  isToday(date, options = {}) {
    const dateObj = this.toDate(date);
    if (!dateObj) return false;

    const today = new Date();
    return dateObj.toDateString() === today.toDateString();
  }

  /**
   * Check if date is weekend
   */
  isWeekend(date, options = {}) {
    const dateObj = this.toDate(date);
    if (!dateObj) return false;

    const day = dateObj.getDay();
    return day === 0 || day === 6; // Sunday or Saturday
  }

  /**
   * Check if date is business day
   */
  isBusinessDay(date, options = {}) {
    return !this.isWeekend(date, options);
  }

  // === TIME COMPARISONS ===

  /**
   * Compare two dates
   */
  compare(date1, date2, options = {}) {
    const dateObj1 = this.toDate(date1);
    const dateObj2 = this.toDate(date2);
    
    if (!dateObj1 || !dateObj2) return 0;

    const { precision = 'milliseconds' } = options;
    
    switch (precision) {
      case 'milliseconds':
        return dateObj1.getTime() - dateObj2.getTime();
      case 'seconds':
        return Math.floor(dateObj1.getTime() / 1000) - Math.floor(dateObj2.getTime() / 1000);
      case 'minutes':
        return Math.floor(dateObj1.getTime() / (1000 * 60)) - Math.floor(dateObj2.getTime() / (1000 * 60));
      case 'hours':
        return Math.floor(dateObj1.getTime() / (1000 * 60 * 60)) - Math.floor(dateObj2.getTime() / (1000 * 60 * 60));
      case 'days':
        return Math.floor(dateObj1.getTime() / (1000 * 60 * 60 * 24)) - Math.floor(dateObj2.getTime() / (1000 * 60 * 60 * 24));
      default:
        return dateObj1.getTime() - dateObj2.getTime();
    }
  }

  // === PERFORMANCE & MONITORING ===

  /**
   * Get performance metrics
   */
  getMetrics() {
    return {
      totalOperations: this.metrics.totalOperations,
      averageProcessingTime: this.metrics.totalOperations > 0 
        ? this.metrics.totalProcessingTime / this.metrics.totalOperations 
        : 0,
      cacheHitRate: this.metrics.cacheHits + this.metrics.cacheMisses > 0
        ? this.metrics.cacheHits / (this.metrics.cacheHits + this.metrics.cacheMisses)
        : 0,
      memoryUsage: this.metrics.memoryUsage,
      errorRate: this.metrics.totalOperations > 0
        ? this.metrics.errors / this.metrics.totalOperations
        : 0
    };
  }

  /**
   * Clear performance cache
   */
  clearCache() {
    this.cache.clear();
  }

  /**
   * Reset performance metrics
   */
  resetMetrics() {
    this.metrics = {
      totalOperations: 0,
      totalProcessingTime: 0,
      cacheHits: 0,
      cacheMisses: 0,
      errors: 0,
      memoryUsage: 0
    };
  }

  // === PRIVATE HELPER METHODS ===

  createSuccessResult(data) {
    return {
      success: true,
      data,
      metrics: {
        processingTime: 0,
        memoryUsage: 0
      }
    };
  }

  createErrorResult(error) {
    return {
      success: false,
      error,
      metrics: {
        processingTime: 0,
        memoryUsage: 0
      }
    };
  }

  updateMetrics(startTime) {
    const processingTime = performance.now() - startTime;
    this.metrics.totalOperations++;
    this.metrics.totalProcessingTime += processingTime;
    this.metrics.memoryUsage = this.cache.size;
  }

  toDate(input) {
    if (!input) return null;
    if (input instanceof Date) return new Date(input);
    if (typeof input === 'string' || typeof input === 'number') {
      const date = new Date(input);
      return isNaN(date.getTime()) ? null : date;
    }
    return null;
  }

  parseWithFormat(dateString, format) {
    // Basic format parsing - can be enhanced
    const patterns = {
      'YYYY-MM-DD': /^(\d{4})-(\d{2})-(\d{2})$/,
      'MM/DD/YYYY': /^(\d{2})\/(\d{2})\/(\d{4})$/,
      'DD/MM/YYYY': /^(\d{2})\/(\d{2})\/(\d{4})$/,
      'YYYY-MM-DD HH:mm:ss': /^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})$/
    };

    const pattern = patterns[format];
    if (!pattern) {
      return new Date(dateString);
    }

    const match = dateString.match(pattern);
    if (!match) {
      return new Date(dateString);
    }

    // Parse based on format
    if (format === 'YYYY-MM-DD') {
      return new Date(parseInt(match[1]), parseInt(match[2]) - 1, parseInt(match[3]));
    } else if (format === 'MM/DD/YYYY') {
      return new Date(parseInt(match[3]), parseInt(match[1]) - 1, parseInt(match[2]));
    } else if (format === 'DD/MM/YYYY') {
      return new Date(parseInt(match[3]), parseInt(match[2]) - 1, parseInt(match[1]));
    }

    return new Date(dateString);
  }

  tryAlternativeParsing(dateString) {
    // Try common date formats
    const formats = [
      /^(\d{4})-(\d{2})-(\d{2})$/,
      /^(\d{2})\/(\d{2})\/(\d{4})$/,
      /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/
    ];

    for (const format of formats) {
      const match = dateString.match(format);
      if (match) {
        if (format.source.includes('\\d{4}-\\d{2}-\\d{2}')) {
          return new Date(parseInt(match[1]), parseInt(match[2]) - 1, parseInt(match[3]));
        } else {
          return new Date(parseInt(match[3]), parseInt(match[1]) - 1, parseInt(match[2]));
        }
      }
    }

    return new Date(dateString);
  }

  getFormatOptions(format, includeTime, includeDate) {
    const baseOptions = {};

    if (includeDate) {
      switch (format) {
        case 'short':
          baseOptions.dateStyle = 'short';
          break;
        case 'medium':
          baseOptions.dateStyle = 'medium';
          break;
        case 'long':
          baseOptions.dateStyle = 'long';
          break;
        case 'full':
          baseOptions.dateStyle = 'full';
          break;
      }
    }

    if (includeTime) {
      switch (format) {
        case 'short':
          baseOptions.timeStyle = 'short';
          break;
        case 'medium':
          baseOptions.timeStyle = 'medium';
          break;
        case 'long':
          baseOptions.timeStyle = 'long';
          break;
        case 'full':
          baseOptions.timeStyle = 'full';
          break;
      }
    }

    return baseOptions;
  }

  formatWithCustomFormat(date, format) {
    // Basic custom format implementation
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return format
      .replace('YYYY', String(year))
      .replace('MM', month)
      .replace('DD', day)
      .replace('HH', hours)
      .replace('mm', minutes)
      .replace('ss', seconds);
  }

  addBusinessDays(date, days) {
    const result = new Date(date);
    let addedDays = 0;

    while (addedDays < Math.abs(days)) {
      result.setDate(result.getDate() + (days > 0 ? 1 : -1));
      if (!this.isWeekend(result)) {
        addedDays++;
      }
    }

    return result;
  }
}

// Export for both CommonJS and ES modules
export default TimeCore;