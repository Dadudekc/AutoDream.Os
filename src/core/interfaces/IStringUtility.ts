/**
 * @fileoverview String Utility Interface - Enterprise-grade string manipulation interface
 * @version 2.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 */

/**
 * String manipulation result interface
 */
export interface IStringResult {
  success: boolean;
  data?: string;
  error?: string;
  metrics?: {
    processingTime: number;
    memoryUsage: number;
    cacheHit?: boolean;
  };
}

/**
 * String validation result interface
 */
export interface IStringValidation {
  isValid: boolean;
  errors: string[];
  warnings: string[];
  suggestions?: string[];
}

/**
 * String transformation options
 */
export interface IStringTransformOptions {
  preserveCase?: boolean;
  trimWhitespace?: boolean;
  removeSpecialChars?: boolean;
  encoding?: 'utf8' | 'ascii' | 'base64';
  maxLength?: number;
}

/**
 * String search options
 */
export interface IStringSearchOptions {
  caseSensitive?: boolean;
  wholeWord?: boolean;
  regex?: boolean;
  startIndex?: number;
  endIndex?: number;
}

/**
 * String formatting options
 */
export interface IStringFormatOptions {
  locale?: string;
  currency?: string;
  dateFormat?: string;
  numberFormat?: string;
  precision?: number;
}

/**
 * Enterprise String Utility Interface
 * Provides comprehensive string manipulation, validation, and transformation capabilities
 */
export interface IStringUtility {
  /**
   * Initialize the string utility with configuration
   * @param config - Configuration options
   */
  initialize(config?: any): Promise<void>;

  /**
   * Clean up resources and reset state
   */
  cleanup(): Promise<void>;

  /**
   * Get utility metadata and capabilities
   */
  getMetadata(): {
    name: string;
    version: string;
    capabilities: string[];
    dependencies: string[];
  };

  // === BASIC STRING OPERATIONS ===

  /**
   * Convert string to different cases
   * @param str - Input string
   * @param caseType - Target case type
   */
  toCase(str: string, caseType: 'upper' | 'lower' | 'title' | 'camel' | 'pascal' | 'snake' | 'kebab'): IStringResult;

  /**
   * Trim whitespace with advanced options
   * @param str - Input string
   * @param options - Trimming options
   */
  trim(str: string, options?: { chars?: string; sides?: 'left' | 'right' | 'both' }): IStringResult;

  /**
   * Pad string to specified length
   * @param str - Input string
   * @param length - Target length
   * @param options - Padding options
   */
  pad(str: string, length: number, options?: { char?: string; side?: 'left' | 'right' | 'both' }): IStringResult;

  /**
   * Reverse string with encoding support
   * @param str - Input string
   * @param options - Reversal options
   */
  reverse(str: string, options?: IStringTransformOptions): IStringResult;

  // === STRING VALIDATION ===

  /**
   * Validate email format
   * @param email - Email string to validate
   */
  validateEmail(email: string): IStringValidation;

  /**
   * Validate URL format
   * @param url - URL string to validate
   */
  validateUrl(url: string): IStringValidation;

  /**
   * Validate phone number format
   * @param phone - Phone number to validate
   * @param format - Expected format (US, EU, etc.)
   */
  validatePhone(phone: string, format?: string): IStringValidation;

  /**
   * Validate password strength
   * @param password - Password to validate
   * @param options - Validation criteria
   */
  validatePassword(password: string, options?: {
    minLength?: number;
    requireUppercase?: boolean;
    requireLowercase?: boolean;
    requireNumbers?: boolean;
    requireSpecialChars?: boolean;
  }): IStringValidation;

  /**
   * Validate JSON string
   * @param jsonStr - JSON string to validate
   */
  validateJson(jsonStr: string): IStringValidation;

  /**
   * Validate UUID format
   * @param uuid - UUID string to validate
   */
  validateUuid(uuid: string): IStringValidation;

  // === STRING SEARCH & REPLACE ===

  /**
   * Advanced string search with multiple options
   * @param str - Input string
   * @param searchTerm - Term to search for
   * @param options - Search options
   */
  search(str: string, searchTerm: string, options?: IStringSearchOptions): {
    found: boolean;
    matches: Array<{ index: number; length: number; value: string }>;
    count: number;
  };

  /**
   * Replace text with advanced options
   * @param str - Input string
   * @param searchTerm - Term to replace
   * @param replacement - Replacement text
   * @param options - Replace options
   */
  replace(str: string, searchTerm: string, replacement: string, options?: {
    global?: boolean;
    caseSensitive?: boolean;
    regex?: boolean;
  }): IStringResult;

  /**
   * Replace multiple patterns at once
   * @param str - Input string
   * @param replacements - Array of replacement patterns
   */
  replaceMultiple(str: string, replacements: Array<{
    search: string;
    replace: string;
    options?: any;
  }>): IStringResult;

  // === STRING FORMATTING ===

  /**
   * Format string with placeholders
   * @param template - String template with placeholders
   * @param values - Values to insert
   * @param options - Formatting options
   */
  format(template: string, values: Record<string, any>, options?: IStringFormatOptions): IStringResult;

  /**
   * Format currency
   * @param amount - Numeric amount
   * @param options - Currency formatting options
   */
  formatCurrency(amount: number, options?: IStringFormatOptions): IStringResult;

  /**
   * Format date string
   * @param date - Date object or string
   * @param options - Date formatting options
   */
  formatDate(date: Date | string, options?: IStringFormatOptions): IStringResult;

  /**
   * Format number with locale support
   * @param number - Number to format
   * @param options - Number formatting options
   */
  formatNumber(number: number, options?: IStringFormatOptions): IStringResult;

  // === STRING ENCODING & DECODING ===

  /**
   * Encode string to different formats
   * @param str - Input string
   * @param encoding - Target encoding
   */
  encode(str: string, encoding: 'base64' | 'url' | 'html' | 'unicode'): IStringResult;

  /**
   * Decode string from different formats
   * @param str - Encoded string
   * @param encoding - Source encoding
   */
  decode(str: string, encoding: 'base64' | 'url' | 'html' | 'unicode'): IStringResult;

  /**
   * Hash string using various algorithms
   * @param str - Input string
   * @param algorithm - Hash algorithm
   */
  hash(str: string, algorithm: 'md5' | 'sha1' | 'sha256' | 'sha512'): IStringResult;

  // === STRING ANALYSIS ===

  /**
   * Analyze string statistics
   * @param str - Input string
   */
  analyze(str: string): {
    length: number;
    wordCount: number;
    lineCount: number;
    charFrequency: Record<string, number>;
    readabilityScore?: number;
    language?: string;
  };

  /**
   * Extract patterns from string
   * @param str - Input string
   * @param pattern - Regex pattern or pattern type
   */
  extractPatterns(str: string, pattern: string | 'email' | 'url' | 'phone' | 'date'): string[];

  /**
   * Calculate string similarity
   * @param str1 - First string
   * @param str2 - Second string
   * @param algorithm - Similarity algorithm
   */
  similarity(str1: string, str2: string, algorithm?: 'levenshtein' | 'jaro' | 'cosine'): number;

  // === STRING MANIPULATION ===

  /**
   * Slice string with advanced options
   * @param str - Input string
   * @param start - Start index
   * @param end - End index
   * @param options - Slice options
   */
  slice(str: string, start: number, end?: number, options?: {
    preserveWords?: boolean;
    addEllipsis?: boolean;
  }): IStringResult;

  /**
   * Split string with advanced options
   * @param str - Input string
   * @param delimiter - Split delimiter
   * @param options - Split options
   */
  split(str: string, delimiter: string | RegExp, options?: {
    limit?: number;
    trimItems?: boolean;
    removeEmpty?: boolean;
  }): string[];

  /**
   * Join array of strings
   * @param strings - Array of strings
   * @param separator - Join separator
   * @param options - Join options
   */
  join(strings: string[], separator: string, options?: {
    filterEmpty?: boolean;
    trimItems?: boolean;
  }): IStringResult;

  // === STRING GENERATION ===

  /**
   * Generate random string
   * @param length - String length
   * @param options - Generation options
   */
  generateRandom(length: number, options?: {
    charset?: string;
    includeUppercase?: boolean;
    includeLowercase?: boolean;
    includeNumbers?: boolean;
    includeSpecial?: boolean;
    excludeSimilar?: boolean;
  }): IStringResult;

  /**
   * Generate UUID
   * @param version - UUID version (1, 4, etc.)
   */
  generateUuid(version?: number): IStringResult;

  /**
   * Generate slug from string
   * @param str - Input string
   * @param options - Slug generation options
   */
  generateSlug(str: string, options?: {
    separator?: string;
    maxLength?: number;
    preserveCase?: boolean;
  }): IStringResult;

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
  };

  /**
   * Clear performance cache
   */
  clearCache(): void;

  /**
   * Reset performance metrics
   */
  resetMetrics(): void;
}