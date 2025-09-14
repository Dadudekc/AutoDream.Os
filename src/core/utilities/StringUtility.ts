/**
 * @fileoverview String Utility Implementation - Enterprise-grade string manipulation utility
 * @version 2.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 */

import { IStringUtility, IStringResult, IStringValidation, IStringTransformOptions, IStringSearchOptions, IStringFormatOptions } from '../interfaces/IStringUtility';

/**
 * Enterprise String Utility Implementation
 * Provides comprehensive string manipulation, validation, and transformation capabilities
 */
export class StringUtility implements IStringUtility {
  private config: any = {};
  private metrics = {
    totalOperations: 0,
    totalProcessingTime: 0,
    cacheHits: 0,
    cacheMisses: 0,
    errors: 0,
    memoryUsage: 0
  };
  private cache = new Map<string, any>();
  private maxCacheSize = 1000;

  /**
   * Initialize the string utility with configuration
   */
  async initialize(config: any = {}): Promise<void> {
    try {
      this.config = {
        defaultLocale: 'en-US',
        maxCacheSize: 1000,
        enableMetrics: true,
        enableCaching: true,
        ...config
      };
      this.maxCacheSize = this.config.maxCacheSize;
    } catch (error) {
      this.metrics.errors++;
      throw new Error(`StringUtility initialization failed: ${error}`);
    }
  }

  /**
   * Clean up resources and reset state
   */
  async cleanup(): Promise<void> {
    try {
      this.cache.clear();
      this.resetMetrics();
    } catch (error) {
      throw new Error(`StringUtility cleanup failed: ${error}`);
    }
  }

  /**
   * Get utility metadata and capabilities
   */
  getMetadata() {
    return {
      name: 'StringUtility',
      version: '2.0.0',
      capabilities: [
        'caseConversion', 'validation', 'search', 'formatting',
        'encoding', 'analysis', 'generation', 'performance'
      ],
      dependencies: []
    };
  }

  // === BASIC STRING OPERATIONS ===

  /**
   * Convert string to different cases
   */
  toCase(str: string, caseType: 'upper' | 'lower' | 'title' | 'camel' | 'pascal' | 'snake' | 'kebab'): IStringResult {
    const startTime = performance.now();
    
    try {
      if (!str || typeof str !== 'string') {
        return this.createErrorResult('Invalid input string');
      }

      let result: string;
      
      switch (caseType) {
        case 'upper':
          result = str.toUpperCase();
          break;
        case 'lower':
          result = str.toLowerCase();
          break;
        case 'title':
          result = str.replace(/\w\S*/g, (txt) => 
            txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
          );
          break;
        case 'camel':
          result = str.replace(/(?:^\w|[A-Z]|\b\w)/g, (word, index) => 
            index === 0 ? word.toLowerCase() : word.toUpperCase()
          ).replace(/\s+/g, '');
          break;
        case 'pascal':
          result = str.replace(/(?:^\w|[A-Z]|\b\w)/g, (word) => 
            word.toUpperCase()
          ).replace(/\s+/g, '');
          break;
        case 'snake':
          result = str.replace(/\W+/g, ' ')
            .split(/ |\B(?=[A-Z])/)
            .map(word => word.toLowerCase())
            .join('_');
          break;
        case 'kebab':
          result = str.replace(/\W+/g, ' ')
            .split(/ |\B(?=[A-Z])/)
            .map(word => word.toLowerCase())
            .join('-');
          break;
        default:
          return this.createErrorResult(`Unsupported case type: ${caseType}`);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Case conversion failed: ${error}`);
    }
  }

  /**
   * Trim whitespace with advanced options
   */
  trim(str: string, options: { chars?: string; sides?: 'left' | 'right' | 'both' } = {}): IStringResult {
    const startTime = performance.now();
    
    try {
      if (!str || typeof str !== 'string') {
        return this.createErrorResult('Invalid input string');
      }

      const { chars = ' \t\n\r\f\v', sides = 'both' } = options;
      let result = str;

      if (sides === 'left' || sides === 'both') {
        result = result.replace(new RegExp(`^[${this.escapeRegex(chars)}]+`), '');
      }
      if (sides === 'right' || sides === 'both') {
        result = result.replace(new RegExp(`[${this.escapeRegex(chars)}]+$`), '');
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Trim operation failed: ${error}`);
    }
  }

  /**
   * Pad string to specified length
   */
  pad(str: string, length: number, options: { char?: string; side?: 'left' | 'right' | 'both' } = {}): IStringResult {
    const startTime = performance.now();
    
    try {
      if (!str || typeof str !== 'string') {
        return this.createErrorResult('Invalid input string');
      }

      const { char = ' ', side = 'right' } = options;
      const currentLength = str.length;
      
      if (currentLength >= length) {
        return this.createSuccessResult(str);
      }

      const paddingLength = length - currentLength;
      const padding = char.repeat(paddingLength);
      
      let result: string;
      switch (side) {
        case 'left':
          result = padding + str;
          break;
        case 'right':
          result = str + padding;
          break;
        case 'both':
          const leftPad = Math.floor(paddingLength / 2);
          const rightPad = paddingLength - leftPad;
          result = char.repeat(leftPad) + str + char.repeat(rightPad);
          break;
        default:
          return this.createErrorResult(`Unsupported pad side: ${side}`);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Pad operation failed: ${error}`);
    }
  }

  /**
   * Reverse string with encoding support
   */
  reverse(str: string, options: IStringTransformOptions = {}): IStringResult {
    const startTime = performance.now();
    
    try {
      if (!str || typeof str !== 'string') {
        return this.createErrorResult('Invalid input string');
      }

      let result = str;
      
      if (options.trimWhitespace) {
        result = result.trim();
      }
      
      if (options.removeSpecialChars) {
        result = result.replace(/[^\w\s]/g, '');
      }
      
      result = result.split('').reverse().join('');
      
      if (options.maxLength && result.length > options.maxLength) {
        result = result.substring(0, options.maxLength);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Reverse operation failed: ${error}`);
    }
  }

  // === STRING VALIDATION ===

  /**
   * Validate email format
   */
  validateEmail(email: string): IStringValidation {
    try {
      if (!email || typeof email !== 'string') {
        return { isValid: false, errors: ['Invalid input'], warnings: [] };
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      const isValid = emailRegex.test(email);
      const errors: string[] = [];
      const warnings: string[] = [];

      if (!isValid) {
        errors.push('Invalid email format');
      }

      if (email.length > 254) {
        errors.push('Email too long (max 254 characters)');
      }

      if (email.includes('..')) {
        errors.push('Email contains consecutive dots');
      }

      return { isValid, errors, warnings };
    } catch (error) {
      return { isValid: false, errors: [`Validation error: ${error}`], warnings: [] };
    }
  }

  /**
   * Validate URL format
   */
  validateUrl(url: string): IStringValidation {
    try {
      if (!url || typeof url !== 'string') {
        return { isValid: false, errors: ['Invalid input'], warnings: [] };
      }

      const errors: string[] = [];
      const warnings: string[] = [];
      let isValid = true;

      try {
        new URL(url);
      } catch {
        isValid = false;
        errors.push('Invalid URL format');
      }

      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        warnings.push('URL should use HTTPS protocol');
      }

      return { isValid, errors, warnings };
    } catch (error) {
      return { isValid: false, errors: [`Validation error: ${error}`], warnings: [] };
    }
  }

  /**
   * Validate phone number format
   */
  validatePhone(phone: string, format: string = 'US'): IStringValidation {
    try {
      if (!phone || typeof phone !== 'string') {
        return { isValid: false, errors: ['Invalid input'], warnings: [] };
      }

      const cleaned = phone.replace(/\D/g, '');
      const errors: string[] = [];
      const warnings: string[] = [];
      let isValid = true;

      const patterns = {
        US: /^1?[2-9]\d{2}[2-9]\d{2}\d{4}$/,
        EU: /^[1-9]\d{8,14}$/,
        INTERNATIONAL: /^\+?[1-9]\d{1,14}$/
      };

      const pattern = patterns[format as keyof typeof patterns] || patterns.INTERNATIONAL;
      
      if (!pattern.test(cleaned)) {
        isValid = false;
        errors.push(`Invalid ${format} phone number format`);
      }

      if (cleaned.length < 10) {
        warnings.push('Phone number seems too short');
      }

      return { isValid, errors, warnings };
    } catch (error) {
      return { isValid: false, errors: [`Validation error: ${error}`], warnings: [] };
    }
  }

  /**
   * Validate password strength
   */
  validatePassword(password: string, options: {
    minLength?: number;
    requireUppercase?: boolean;
    requireLowercase?: boolean;
    requireNumbers?: boolean;
    requireSpecialChars?: boolean;
  } = {}): IStringValidation {
    try {
      if (!password || typeof password !== 'string') {
        return { isValid: false, errors: ['Invalid input'], warnings: [] };
      }

      const {
        minLength = 8,
        requireUppercase = true,
        requireLowercase = true,
        requireNumbers = true,
        requireSpecialChars = true
      } = options;

      const errors: string[] = [];
      const warnings: string[] = [];

      if (password.length < minLength) {
        errors.push(`Password must be at least ${minLength} characters long`);
      }

      if (requireUppercase && !/[A-Z]/.test(password)) {
        errors.push('Password must contain at least one uppercase letter');
      }

      if (requireLowercase && !/[a-z]/.test(password)) {
        errors.push('Password must contain at least one lowercase letter');
      }

      if (requireNumbers && !/\d/.test(password)) {
        errors.push('Password must contain at least one number');
      }

      if (requireSpecialChars && !/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        errors.push('Password must contain at least one special character');
      }

      if (password.length < 12) {
        warnings.push('Consider using a longer password for better security');
      }

      return { isValid: errors.length === 0, errors, warnings };
    } catch (error) {
      return { isValid: false, errors: [`Validation error: ${error}`], warnings: [] };
    }
  }

  /**
   * Validate JSON string
   */
  validateJson(jsonStr: string): IStringValidation {
    try {
      if (!jsonStr || typeof jsonStr !== 'string') {
        return { isValid: false, errors: ['Invalid input'], warnings: [] };
      }

      const errors: string[] = [];
      const warnings: string[] = [];

      try {
        JSON.parse(jsonStr);
      } catch (parseError) {
        errors.push(`Invalid JSON: ${parseError}`);
      }

      return { isValid: errors.length === 0, errors, warnings };
    } catch (error) {
      return { isValid: false, errors: [`Validation error: ${error}`], warnings: [] };
    }
  }

  /**
   * Validate UUID format
   */
  validateUuid(uuid: string): IStringValidation {
    try {
      if (!uuid || typeof uuid !== 'string') {
        return { isValid: false, errors: ['Invalid input'], warnings: [] };
      }

      const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
      const isValid = uuidRegex.test(uuid);
      const errors: string[] = [];
      const warnings: string[] = [];

      if (!isValid) {
        errors.push('Invalid UUID format');
      }

      return { isValid, errors, warnings };
    } catch (error) {
      return { isValid: false, errors: [`Validation error: ${error}`], warnings: [] };
    }
  }

  // === STRING SEARCH & REPLACE ===

  /**
   * Advanced string search with multiple options
   */
  search(str: string, searchTerm: string, options: IStringSearchOptions = {}): {
    found: boolean;
    matches: Array<{ index: number; length: number; value: string }>;
    count: number;
  } {
    try {
      if (!str || !searchTerm) {
        return { found: false, matches: [], count: 0 };
      }

      const {
        caseSensitive = false,
        wholeWord = false,
        regex = false,
        startIndex = 0,
        endIndex = str.length
      } = options;

      let searchStr = str.substring(startIndex, endIndex);
      let pattern = searchTerm;

      if (!caseSensitive) {
        searchStr = searchStr.toLowerCase();
        pattern = pattern.toLowerCase();
      }

      if (wholeWord) {
        pattern = `\\b${this.escapeRegex(pattern)}\\b`;
      }

      if (!regex) {
        pattern = this.escapeRegex(pattern);
      }

      const regexObj = new RegExp(pattern, caseSensitive ? 'g' : 'gi');
      const matches: Array<{ index: number; length: number; value: string }> = [];
      let match;

      while ((match = regexObj.exec(searchStr)) !== null) {
        matches.push({
          index: match.index + startIndex,
          length: match[0].length,
          value: match[0]
        });
      }

      return {
        found: matches.length > 0,
        matches,
        count: matches.length
      };
    } catch (error) {
      return { found: false, matches: [], count: 0 };
    }
  }

  /**
   * Replace text with advanced options
   */
  replace(str: string, searchTerm: string, replacement: string, options: {
    global?: boolean;
    caseSensitive?: boolean;
    regex?: boolean;
  } = {}): IStringResult {
    const startTime = performance.now();
    
    try {
      if (!str || typeof str !== 'string') {
        return this.createErrorResult('Invalid input string');
      }

      const { global = true, caseSensitive = false, regex = false } = options;
      
      let pattern = searchTerm;
      if (!regex) {
        pattern = this.escapeRegex(pattern);
      }

      const flags = caseSensitive ? (global ? 'g' : '') : (global ? 'gi' : 'i');
      const regexObj = new RegExp(pattern, flags);
      
      const result = str.replace(regexObj, replacement);

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Replace operation failed: ${error}`);
    }
  }

  /**
   * Replace multiple patterns at once
   */
  replaceMultiple(str: string, replacements: Array<{
    search: string;
    replace: string;
    options?: any;
  }>): IStringResult {
    const startTime = performance.now();
    
    try {
      if (!str || typeof str !== 'string') {
        return this.createErrorResult('Invalid input string');
      }

      let result = str;
      
      for (const replacement of replacements) {
        const replaceResult = this.replace(result, replacement.search, replacement.replace, replacement.options);
        if (replaceResult.success) {
          result = replaceResult.data!;
        } else {
          return replaceResult;
        }
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Multiple replace operation failed: ${error}`);
    }
  }

  // === STRING FORMATTING ===

  /**
   * Format string with placeholders
   */
  format(template: string, values: Record<string, any>, options: IStringFormatOptions = {}): IStringResult {
    const startTime = performance.now();
    
    try {
      if (!template || typeof template !== 'string') {
        return this.createErrorResult('Invalid template string');
      }

      let result = template;
      
      for (const [key, value] of Object.entries(values)) {
        const placeholder = new RegExp(`\\{${key}\\}`, 'g');
        result = result.replace(placeholder, String(value));
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Format operation failed: ${error}`);
    }
  }

  /**
   * Format currency
   */
  formatCurrency(amount: number, options: IStringFormatOptions = {}): IStringResult {
    const startTime = performance.now();
    
    try {
      if (typeof amount !== 'number' || isNaN(amount)) {
        return this.createErrorResult('Invalid amount');
      }

      const { locale = 'en-US', currency = 'USD', precision = 2 } = options;
      
      const result = new Intl.NumberFormat(locale, {
        style: 'currency',
        currency,
        minimumFractionDigits: precision,
        maximumFractionDigits: precision
      }).format(amount);

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Currency formatting failed: ${error}`);
    }
  }

  /**
   * Format date string
   */
  formatDate(date: Date | string, options: IStringFormatOptions = {}): IStringResult {
    const startTime = performance.now();
    
    try {
      const dateObj = typeof date === 'string' ? new Date(date) : date;
      
      if (isNaN(dateObj.getTime())) {
        return this.createErrorResult('Invalid date');
      }

      const { locale = 'en-US', dateFormat = 'short' } = options;
      
      const formatOptions: Intl.DateTimeFormatOptions = {
        short: { year: 'numeric', month: 'short', day: 'numeric' },
        long: { year: 'numeric', month: 'long', day: 'numeric' },
        time: { hour: '2-digit', minute: '2-digit' },
        datetime: { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }
      };

      const result = new Intl.DateTimeFormat(locale, formatOptions[dateFormat as keyof typeof formatOptions] || formatOptions.short)
        .format(dateObj);

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Date formatting failed: ${error}`);
    }
  }

  /**
   * Format number with locale support
   */
  formatNumber(number: number, options: IStringFormatOptions = {}): IStringResult {
    const startTime = performance.now();
    
    try {
      if (typeof number !== 'number' || isNaN(number)) {
        return this.createErrorResult('Invalid number');
      }

      const { locale = 'en-US', precision = 2 } = options;
      
      const result = new Intl.NumberFormat(locale, {
        minimumFractionDigits: precision,
        maximumFractionDigits: precision
      }).format(number);

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Number formatting failed: ${error}`);
    }
  }

  // === STRING ENCODING & DECODING ===

  /**
   * Encode string to different formats
   */
  encode(str: string, encoding: 'base64' | 'url' | 'html' | 'unicode'): IStringResult {
    const startTime = performance.now();
    
    try {
      if (!str || typeof str !== 'string') {
        return this.createErrorResult('Invalid input string');
      }

      let result: string;
      
      switch (encoding) {
        case 'base64':
          result = btoa(unescape(encodeURIComponent(str)));
          break;
        case 'url':
          result = encodeURIComponent(str);
          break;
        case 'html':
          result = str.replace(/[&<>"']/g, (match) => {
            const entities: Record<string, string> = {
              '&': '&amp;',
              '<': '&lt;',
              '>': '&gt;',
              '"': '&quot;',
              "'": '&#39;'
            };
            return entities[match];
          });
          break;
        case 'unicode':
          result = str.split('').map(char => 
            '\\u' + char.charCodeAt(0).toString(16).padStart(4, '0')
          ).join('');
          break;
        default:
          return this.createErrorResult(`Unsupported encoding: ${encoding}`);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Encoding failed: ${error}`);
    }
  }

  /**
   * Decode string from different formats
   */
  decode(str: string, encoding: 'base64' | 'url' | 'html' | 'unicode'): IStringResult {
    const startTime = performance.now();
    
    try {
      if (!str || typeof str !== 'string') {
        return this.createErrorResult('Invalid input string');
      }

      let result: string;
      
      switch (encoding) {
        case 'base64':
          result = decodeURIComponent(escape(atob(str)));
          break;
        case 'url':
          result = decodeURIComponent(str);
          break;
        case 'html':
          result = str.replace(/&amp;|&lt;|&gt;|&quot;|&#39;/g, (match) => {
            const entities: Record<string, string> = {
              '&amp;': '&',
              '&lt;': '<',
              '&gt;': '>',
              '&quot;': '"',
              '&#39;': "'"
            };
            return entities[match];
          });
          break;
        case 'unicode':
          result = str.replace(/\\u[\dA-F]{4}/gi, (match) => 
            String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16))
          );
          break;
        default:
          return this.createErrorResult(`Unsupported encoding: ${encoding}`);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Decoding failed: ${error}`);
    }
  }

  /**
   * Hash string using various algorithms
   */
  async hash(str: string, algorithm: 'md5' | 'sha1' | 'sha256' | 'sha512'): Promise<IStringResult> {
    const startTime = performance.now();
    
    try {
      if (!str || typeof str !== 'string') {
        return this.createErrorResult('Invalid input string');
      }

      const encoder = new TextEncoder();
      const data = encoder.encode(str);
      const hashBuffer = await crypto.subtle.digest(algorithm.toUpperCase(), data);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      const result = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Hashing failed: ${error}`);
    }
  }

  // === STRING ANALYSIS ===

  /**
   * Analyze string statistics
   */
  analyze(str: string): {
    length: number;
    wordCount: number;
    lineCount: number;
    charFrequency: Record<string, number>;
    readabilityScore?: number;
    language?: string;
  } {
    try {
      if (!str || typeof str !== 'string') {
        return {
          length: 0,
          wordCount: 0,
          lineCount: 0,
          charFrequency: {}
        };
      }

      const length = str.length;
      const wordCount = str.trim().split(/\s+/).filter(word => word.length > 0).length;
      const lineCount = str.split('\n').length;
      
      const charFrequency: Record<string, number> = {};
      for (const char of str) {
        charFrequency[char] = (charFrequency[char] || 0) + 1;
      }

      // Simple readability score (Flesch-like)
      const sentences = str.split(/[.!?]+/).filter(s => s.trim().length > 0).length;
      const syllables = str.toLowerCase().replace(/[^a-z]/g, '').length * 0.5; // Rough estimate
      const readabilityScore = sentences > 0 ? 206.835 - (1.015 * (wordCount / sentences)) - (84.6 * (syllables / wordCount)) : 0;

      return {
        length,
        wordCount,
        lineCount,
        charFrequency,
        readabilityScore: Math.max(0, Math.min(100, readabilityScore))
      };
    } catch (error) {
      return {
        length: 0,
        wordCount: 0,
        lineCount: 0,
        charFrequency: {}
      };
    }
  }

  /**
   * Extract patterns from string
   */
  extractPatterns(str: string, pattern: string | 'email' | 'url' | 'phone' | 'date'): string[] {
    try {
      if (!str || typeof str !== 'string') {
        return [];
      }

      let regex: RegExp;
      
      if (typeof pattern === 'string') {
        regex = new RegExp(pattern, 'gi');
      } else {
        const patterns = {
          email: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
          url: /https?:\/\/[^\s]+/g,
          phone: /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g,
          date: /\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b/g
        };
        regex = patterns[pattern];
      }

      const matches = str.match(regex) || [];
      return matches;
    } catch (error) {
      return [];
    }
  }

  /**
   * Calculate string similarity
   */
  similarity(str1: string, str2: string, algorithm: 'levenshtein' | 'jaro' | 'cosine' = 'levenshtein'): number {
    try {
      if (!str1 || !str2) {
        return 0;
      }

      switch (algorithm) {
        case 'levenshtein':
          return this.levenshteinSimilarity(str1, str2);
        case 'jaro':
          return this.jaroSimilarity(str1, str2);
        case 'cosine':
          return this.cosineSimilarity(str1, str2);
        default:
          return 0;
      }
    } catch (error) {
      return 0;
    }
  }

  // === STRING MANIPULATION ===

  /**
   * Slice string with advanced options
   */
  slice(str: string, start: number, end?: number, options: {
    preserveWords?: boolean;
    addEllipsis?: boolean;
  } = {}): IStringResult {
    const startTime = performance.now();
    
    try {
      if (!str || typeof str !== 'string') {
        return this.createErrorResult('Invalid input string');
      }

      const { preserveWords = false, addEllipsis = false } = options;
      let result = str.slice(start, end);

      if (preserveWords && end && end < str.length) {
        const lastSpaceIndex = result.lastIndexOf(' ');
        if (lastSpaceIndex > 0) {
          result = result.slice(0, lastSpaceIndex);
        }
      }

      if (addEllipsis && result.length < str.length) {
        result += '...';
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Slice operation failed: ${error}`);
    }
  }

  /**
   * Split string with advanced options
   */
  split(str: string, delimiter: string | RegExp, options: {
    limit?: number;
    trimItems?: boolean;
    removeEmpty?: boolean;
  } = {}): string[] {
    try {
      if (!str || typeof str !== 'string') {
        return [];
      }

      const { limit, trimItems = false, removeEmpty = false } = options;
      
      let result = str.split(delimiter, limit);
      
      if (trimItems) {
        result = result.map(item => item.trim());
      }
      
      if (removeEmpty) {
        result = result.filter(item => item.length > 0);
      }

      return result;
    } catch (error) {
      return [];
    }
  }

  /**
   * Join array of strings
   */
  join(strings: string[], separator: string, options: {
    filterEmpty?: boolean;
    trimItems?: boolean;
  } = {}): IStringResult {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(strings)) {
        return this.createErrorResult('Invalid input array');
      }

      const { filterEmpty = false, trimItems = false } = options;
      
      let processedStrings = strings;
      
      if (trimItems) {
        processedStrings = processedStrings.map(str => str.trim());
      }
      
      if (filterEmpty) {
        processedStrings = processedStrings.filter(str => str.length > 0);
      }

      const result = processedStrings.join(separator);

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Join operation failed: ${error}`);
    }
  }

  // === STRING GENERATION ===

  /**
   * Generate random string
   */
  generateRandom(length: number, options: {
    charset?: string;
    includeUppercase?: boolean;
    includeLowercase?: boolean;
    includeNumbers?: boolean;
    includeSpecial?: boolean;
    excludeSimilar?: boolean;
  } = {}): IStringResult {
    const startTime = performance.now();
    
    try {
      if (typeof length !== 'number' || length <= 0) {
        return this.createErrorResult('Invalid length');
      }

      const {
        charset,
        includeUppercase = true,
        includeLowercase = true,
        includeNumbers = true,
        includeSpecial = false,
        excludeSimilar = true
      } = options;

      let chars = charset || '';
      
      if (!charset) {
        if (includeUppercase) chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        if (includeLowercase) chars += 'abcdefghijklmnopqrstuvwxyz';
        if (includeNumbers) chars += '0123456789';
        if (includeSpecial) chars += '!@#$%^&*()_+-=[]{}|;:,.<>?';
        
        if (excludeSimilar) {
          chars = chars.replace(/[0O1lI]/g, '');
        }
      }

      if (chars.length === 0) {
        return this.createErrorResult('No characters available for generation');
      }

      let result = '';
      for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Random generation failed: ${error}`);
    }
  }

  /**
   * Generate UUID
   */
  generateUuid(version: number = 4): IStringResult {
    const startTime = performance.now();
    
    try {
      let result: string;
      
      if (version === 4) {
        result = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
          const r = Math.random() * 16 | 0;
          const v = c === 'x' ? r : (r & 0x3 | 0x8);
          return v.toString(16);
        });
      } else {
        return this.createErrorResult(`Unsupported UUID version: ${version}`);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`UUID generation failed: ${error}`);
    }
  }

  /**
   * Generate slug from string
   */
  generateSlug(str: string, options: {
    separator?: string;
    maxLength?: number;
    preserveCase?: boolean;
  } = {}): IStringResult {
    const startTime = performance.now();
    
    try {
      if (!str || typeof str !== 'string') {
        return this.createErrorResult('Invalid input string');
      }

      const { separator = '-', maxLength = 50, preserveCase = false } = options;
      
      let result = str;
      
      if (!preserveCase) {
        result = result.toLowerCase();
      }
      
      result = result
        .replace(/[^\w\s-]/g, '')
        .replace(/[\s_-]+/g, separator)
        .replace(/^-+|-+$/g, '');
      
      if (result.length > maxLength) {
        result = result.substring(0, maxLength).replace(/-+$/, '');
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Slug generation failed: ${error}`);
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
  clearCache(): void {
    this.cache.clear();
  }

  /**
   * Reset performance metrics
   */
  resetMetrics(): void {
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

  private createSuccessResult(data: string): IStringResult {
    return {
      success: true,
      data,
      metrics: {
        processingTime: 0,
        memoryUsage: 0
      }
    };
  }

  private createErrorResult(error: string): IStringResult {
    return {
      success: false,
      error,
      metrics: {
        processingTime: 0,
        memoryUsage: 0
      }
    };
  }

  private updateMetrics(startTime: number): void {
    const processingTime = performance.now() - startTime;
    this.metrics.totalOperations++;
    this.metrics.totalProcessingTime += processingTime;
    this.metrics.memoryUsage = this.cache.size;
  }

  private escapeRegex(str: string): string {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  private levenshteinSimilarity(str1: string, str2: string): number {
    const matrix = Array(str2.length + 1).fill(null).map(() => Array(str1.length + 1).fill(null));
    
    for (let i = 0; i <= str1.length; i++) matrix[0][i] = i;
    for (let j = 0; j <= str2.length; j++) matrix[j][0] = j;
    
    for (let j = 1; j <= str2.length; j++) {
      for (let i = 1; i <= str1.length; i++) {
        const indicator = str1[i - 1] === str2[j - 1] ? 0 : 1;
        matrix[j][i] = Math.min(
          matrix[j][i - 1] + 1,
          matrix[j - 1][i] + 1,
          matrix[j - 1][i - 1] + indicator
        );
      }
    }
    
    const maxLength = Math.max(str1.length, str2.length);
    return maxLength === 0 ? 1 : (maxLength - matrix[str2.length][str1.length]) / maxLength;
  }

  private jaroSimilarity(str1: string, str2: string): number {
    if (str1 === str2) return 1;
    
    const matchWindow = Math.floor(Math.max(str1.length, str2.length) / 2) - 1;
    if (matchWindow < 0) return 0;
    
    const str1Matches = new Array(str1.length).fill(false);
    const str2Matches = new Array(str2.length).fill(false);
    
    let matches = 0;
    let transpositions = 0;
    
    for (let i = 0; i < str1.length; i++) {
      const start = Math.max(0, i - matchWindow);
      const end = Math.min(i + matchWindow + 1, str2.length);
      
      for (let j = start; j < end; j++) {
        if (str2Matches[j] || str1[i] !== str2[j]) continue;
        str1Matches[i] = true;
        str2Matches[j] = true;
        matches++;
        break;
      }
    }
    
    if (matches === 0) return 0;
    
    let k = 0;
    for (let i = 0; i < str1.length; i++) {
      if (!str1Matches[i]) continue;
      while (!str2Matches[k]) k++;
      if (str1[i] !== str2[k]) transpositions++;
      k++;
    }
    
    return (matches / str1.length + matches / str2.length + (matches - transpositions / 2) / matches) / 3;
  }

  private cosineSimilarity(str1: string, str2: string): number {
    const getCharFrequency = (str: string) => {
      const freq: Record<string, number> = {};
      for (const char of str.toLowerCase()) {
        freq[char] = (freq[char] || 0) + 1;
      }
      return freq;
    };
    
    const freq1 = getCharFrequency(str1);
    const freq2 = getCharFrequency(str2);
    
    const allChars = new Set([...Object.keys(freq1), ...Object.keys(freq2)]);
    
    let dotProduct = 0;
    let norm1 = 0;
    let norm2 = 0;
    
    for (const char of allChars) {
      const f1 = freq1[char] || 0;
      const f2 = freq2[char] || 0;
      
      dotProduct += f1 * f2;
      norm1 += f1 * f1;
      norm2 += f2 * f2;
    }
    
    return norm1 === 0 || norm2 === 0 ? 0 : dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
  }
}