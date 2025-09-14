/**
 * @fileoverview Unified String Utility - TypeScript Wrapper for Shared Core
 * @version 3.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 * 
 * TypeScript wrapper around the shared StringCore implementation.
 * Provides type safety while using the universal JavaScript core.
 */

import { StringCore } from '../shared/string-core.js';
import { 
  IStringUtility, IStringResult, IStringValidation, IStringTransformOptions, 
  IStringSearchOptions, IStringFormatOptions 
} from '../../interfaces/IStringUtility';

/**
 * Unified String Utility Implementation
 * TypeScript wrapper around the shared StringCore
 */
export class StringUtility implements IStringUtility {
  private core: StringCore;

  constructor(config: any = {}) {
    this.core = new StringCore(config);
  }

  /**
   * Initialize the string utility with configuration
   */
  async initialize(config: any = {}): Promise<void> {
    return this.core.initialize(config);
  }

  /**
   * Clean up resources and reset state
   */
  async cleanup(): Promise<void> {
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
  toCase(str: string, caseType: 'upper' | 'lower' | 'title' | 'camel' | 'pascal' | 'snake' | 'kebab'): IStringResult {
    return this.core.toCase(str, caseType);
  }

  /**
   * Trim whitespace with advanced options
   */
  trim(str: string, options?: { chars?: string; sides?: 'left' | 'right' | 'both' }): IStringResult {
    return this.core.trim(str, options);
  }

  /**
   * Pad string to specified length
   */
  pad(str: string, length: number, options?: { char?: string; side?: 'left' | 'right' | 'both' }): IStringResult {
    return this.core.pad(str, length, options);
  }

  /**
   * Reverse string with encoding support
   */
  reverse(str: string, options?: IStringTransformOptions): IStringResult {
    return this.core.reverse(str, options);
  }

  // === STRING VALIDATION ===

  /**
   * Validate email format
   */
  validateEmail(email: string): IStringValidation {
    return this.core.validateEmail(email);
  }

  /**
   * Validate URL format
   */
  validateUrl(url: string): IStringValidation {
    return this.core.validateUrl(url);
  }

  /**
   * Validate phone number format
   */
  validatePhone(phone: string, format?: string): IStringValidation {
    return this.core.validatePhone(phone, format);
  }

  /**
   * Validate password strength
   */
  validatePassword(password: string, options?: {
    minLength?: number;
    requireUppercase?: boolean;
    requireLowercase?: boolean;
    requireNumbers?: boolean;
    requireSpecialChars?: boolean;
  }): IStringValidation {
    return this.core.validatePassword(password, options);
  }

  /**
   * Validate JSON string
   */
  validateJson(jsonStr: string): IStringValidation {
    return this.core.validateJson(jsonStr);
  }

  /**
   * Validate UUID format
   */
  validateUuid(uuid: string): IStringValidation {
    return this.core.validateUuid(uuid);
  }

  // === STRING SEARCH & REPLACE ===

  /**
   * Advanced string search with multiple options
   */
  search(str: string, searchTerm: string, options?: IStringSearchOptions): {
    found: boolean;
    matches: Array<{ index: number; length: number; value: string }>;
    count: number;
  } {
    return this.core.search(str, searchTerm, options);
  }

  /**
   * Replace text with advanced options
   */
  replace(str: string, searchTerm: string, replacement: string, options?: {
    global?: boolean;
    caseSensitive?: boolean;
    regex?: boolean;
  }): IStringResult {
    return this.core.replace(str, searchTerm, replacement, options);
  }

  /**
   * Replace multiple patterns at once
   */
  replaceMultiple(str: string, replacements: Array<{
    search: string;
    replace: string;
    options?: any;
  }>): IStringResult {
    return this.core.replaceMultiple(str, replacements);
  }

  // === STRING FORMATTING ===

  /**
   * Format string with placeholders
   */
  format(template: string, values: Record<string, any>, options?: IStringFormatOptions): IStringResult {
    return this.core.format(template, values, options);
  }

  /**
   * Format currency
   */
  formatCurrency(amount: number, options?: IStringFormatOptions): IStringResult {
    return this.core.formatCurrency(amount, options);
  }

  /**
   * Format date string
   */
  formatDate(date: Date | string, options?: IStringFormatOptions): IStringResult {
    return this.core.formatDate(date, options);
  }

  /**
   * Format number with locale support
   */
  formatNumber(number: number, options?: IStringFormatOptions): IStringResult {
    return this.core.formatNumber(number, options);
  }

  // === STRING ENCODING & DECODING ===

  /**
   * Encode string to different formats
   */
  encode(str: string, encoding: 'base64' | 'url' | 'html' | 'unicode'): IStringResult {
    return this.core.encode(str, encoding);
  }

  /**
   * Decode string from different formats
   */
  decode(str: string, encoding: 'base64' | 'url' | 'html' | 'unicode'): IStringResult {
    return this.core.decode(str, encoding);
  }

  /**
   * Hash string using various algorithms
   */
  async hash(str: string, algorithm: 'md5' | 'sha1' | 'sha256' | 'sha512'): Promise<IStringResult> {
    return this.core.hash(str, algorithm);
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
    return this.core.analyze(str);
  }

  /**
   * Extract patterns from string
   */
  extractPatterns(str: string, pattern: string | 'email' | 'url' | 'phone' | 'date'): string[] {
    return this.core.extractPatterns(str, pattern);
  }

  /**
   * Calculate string similarity
   */
  similarity(str1: string, str2: string, algorithm?: 'levenshtein' | 'jaro' | 'cosine'): number {
    return this.core.similarity(str1, str2, algorithm);
  }

  // === STRING MANIPULATION ===

  /**
   * Slice string with advanced options
   */
  slice(str: string, start: number, end?: number, options?: {
    preserveWords?: boolean;
    addEllipsis?: boolean;
  }): IStringResult {
    return this.core.slice(str, start, end, options);
  }

  /**
   * Split string with advanced options
   */
  split(str: string, delimiter: string | RegExp, options?: {
    limit?: number;
    trimItems?: boolean;
    removeEmpty?: boolean;
  }): string[] {
    return this.core.split(str, delimiter, options);
  }

  /**
   * Join array of strings
   */
  join(strings: string[], separator: string, options?: {
    filterEmpty?: boolean;
    trimItems?: boolean;
  }): IStringResult {
    return this.core.join(strings, separator, options);
  }

  // === STRING GENERATION ===

  /**
   * Generate random string
   */
  generateRandom(length: number, options?: {
    charset?: string;
    includeUppercase?: boolean;
    includeLowercase?: boolean;
    includeNumbers?: boolean;
    includeSpecial?: boolean;
    excludeSimilar?: boolean;
  }): IStringResult {
    return this.core.generateRandom(length, options);
  }

  /**
   * Generate UUID
   */
  generateUuid(version?: number): IStringResult {
    return this.core.generateUuid(version);
  }

  /**
   * Generate slug from string
   */
  generateSlug(str: string, options?: {
    separator?: string;
    maxLength?: number;
    preserveCase?: boolean;
  }): IStringResult {
    return this.core.generateSlug(str, options);
  }

  // === PERFORMANCE & MONITORING ===

  /**
   * Get performance metrics
   */
  getMetrics(): {
    totalOperations: number;
    averageProcessingTime: number;
    cacheHitRate: number;
    memoryUsage: number;
    errorRate: number;
  } {
    return this.core.getMetrics();
  }

  /**
   * Clear performance cache
   */
  clearCache(): void {
    this.core.clearCache();
  }

  /**
   * Reset performance metrics
   */
  resetMetrics(): void {
    this.core.resetMetrics();
  }
}

// Export for both CommonJS and ES modules
export default StringUtility;