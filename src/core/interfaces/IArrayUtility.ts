/**
 * @fileoverview Array Utility Interface - Enterprise-grade array manipulation interface
 * @version 2.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 */

/**
 * Array operation result interface
 */
export interface IArrayResult<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  metrics?: {
    processingTime: number;
    memoryUsage: number;
    cacheHit?: boolean;
  };
}

/**
 * Array search result interface
 */
export interface IArraySearchResult<T = any> {
  found: boolean;
  index: number;
  value?: T;
  indices?: number[];
  values?: T[];
  count: number;
}

/**
 * Array sorting options
 */
export interface IArraySortOptions {
  key?: string | ((item: any) => any);
  direction?: 'asc' | 'desc';
  locale?: string;
  numeric?: boolean;
  caseSensitive?: boolean;
}

/**
 * Array filtering options
 */
export interface IArrayFilterOptions {
  caseSensitive?: boolean;
  exactMatch?: boolean;
  regex?: boolean;
  limit?: number;
  offset?: number;
}

/**
 * Array grouping options
 */
export interface IArrayGroupOptions {
  key?: string | ((item: any) => any);
  sort?: boolean;
  sortDirection?: 'asc' | 'desc';
  preserveOrder?: boolean;
}

/**
 * Array transformation options
 */
export interface IArrayTransformOptions {
  deep?: boolean;
  preserveStructure?: boolean;
  validate?: boolean;
  sanitize?: boolean;
}

/**
 * Array performance options
 */
export interface IArrayPerformanceOptions {
  enableCaching?: boolean;
  maxCacheSize?: number;
  enableMetrics?: boolean;
  batchSize?: number;
}

/**
 * Enterprise Array Utility Interface
 * Provides comprehensive array manipulation, analysis, and transformation capabilities
 */
export interface IArrayUtility {
  /**
   * Initialize the array utility with configuration
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

  // === BASIC ARRAY OPERATIONS ===

  /**
   * Create array with specified length and fill value
   * @param length - Array length
   * @param fillValue - Value to fill array with
   * @param options - Creation options
   */
  create<T>(length: number, fillValue?: T, options?: IArrayTransformOptions): IArrayResult<T[]>;

  /**
   * Clone array with deep or shallow copy
   * @param array - Source array
   * @param options - Clone options
   */
  clone<T>(array: T[], options?: IArrayTransformOptions): IArrayResult<T[]>;

  /**
   * Merge multiple arrays
   * @param arrays - Arrays to merge
   * @param options - Merge options
   */
  merge<T>(arrays: T[][], options?: {
    unique?: boolean;
    preserveOrder?: boolean;
    sort?: boolean;
  }): IArrayResult<T[]>;

  /**
   * Flatten nested arrays
   * @param array - Source array
   * @param depth - Flattening depth
   * @param options - Flatten options
   */
  flatten<T>(array: T[], depth?: number, options?: IArrayTransformOptions): IArrayResult<T[]>;

  // === ARRAY SEARCH & FILTERING ===

  /**
   * Find element in array with advanced options
   * @param array - Source array
   * @param predicate - Search predicate
   * @param options - Search options
   */
  find<T>(array: T[], predicate: ((item: T, index: number) => boolean) | T, options?: IArrayFilterOptions): IArraySearchResult<T>;

  /**
   * Find all matching elements
   * @param array - Source array
   * @param predicate - Search predicate
   * @param options - Search options
   */
  findAll<T>(array: T[], predicate: ((item: T, index: number) => boolean) | T, options?: IArrayFilterOptions): IArraySearchResult<T>;

  /**
   * Filter array with advanced options
   * @param array - Source array
   * @param predicate - Filter predicate
   * @param options - Filter options
   */
  filter<T>(array: T[], predicate: ((item: T, index: number) => boolean) | T, options?: IArrayFilterOptions): IArrayResult<T[]>;

  /**
   * Remove duplicates from array
   * @param array - Source array
   * @param options - Deduplication options
   */
  unique<T>(array: T[], options?: {
    key?: string | ((item: T) => any);
    caseSensitive?: boolean;
    preserveOrder?: boolean;
  }): IArrayResult<T[]>;

  /**
   * Find intersection of arrays
   * @param arrays - Arrays to intersect
   * @param options - Intersection options
   */
  intersection<T>(arrays: T[][], options?: {
    key?: string | ((item: T) => any);
    caseSensitive?: boolean;
  }): IArrayResult<T[]>;

  /**
   * Find difference between arrays
   * @param array1 - First array
   * @param array2 - Second array
   * @param options - Difference options
   */
  difference<T>(array1: T[], array2: T[], options?: {
    key?: string | ((item: T) => any);
    caseSensitive?: boolean;
  }): IArrayResult<T[]>;

  // === ARRAY SORTING ===

  /**
   * Sort array with advanced options
   * @param array - Source array
   * @param options - Sort options
   */
  sort<T>(array: T[], options?: IArraySortOptions): IArrayResult<T[]>;

  /**
   * Sort array by multiple criteria
   * @param array - Source array
   * @param criteria - Array of sort criteria
   */
  sortBy<T>(array: T[], criteria: Array<{
    key: string | ((item: T) => any);
    direction?: 'asc' | 'desc';
    priority?: number;
  }>): IArrayResult<T[]>;

  /**
   * Shuffle array randomly
   * @param array - Source array
   * @param options - Shuffle options
   */
  shuffle<T>(array: T[], options?: {
    seed?: number;
    preserveOriginal?: boolean;
  }): IArrayResult<T[]>;

  // === ARRAY TRANSFORMATION ===

  /**
   * Map array with advanced options
   * @param array - Source array
   * @param mapper - Mapping function
   * @param options - Map options
   */
  map<T, U>(array: T[], mapper: (item: T, index: number) => U, options?: IArrayTransformOptions): IArrayResult<U[]>;

  /**
   * Reduce array with advanced options
   * @param array - Source array
   * @param reducer - Reduction function
   * @param initialValue - Initial value
   * @param options - Reduce options
   */
  reduce<T, U>(array: T[], reducer: (accumulator: U, item: T, index: number) => U, initialValue: U, options?: IArrayTransformOptions): IArrayResult<U>;

  /**
   * Group array by key or function
   * @param array - Source array
   * @param options - Group options
   */
  groupBy<T>(array: T[], options: IArrayGroupOptions): IArrayResult<Record<string, T[]>>;

  /**
   * Chunk array into smaller arrays
   * @param array - Source array
   * @param size - Chunk size
   * @param options - Chunk options
   */
  chunk<T>(array: T[], size: number, options?: {
    preserveRemainder?: boolean;
    fillValue?: T;
  }): IArrayResult<T[][]>;

  /**
   * Zip multiple arrays together
   * @param arrays - Arrays to zip
   * @param options - Zip options
   */
  zip<T>(arrays: T[][], options?: {
    fillValue?: any;
    longest?: boolean;
  }): IArrayResult<T[][]>;

  // === ARRAY ANALYSIS ===

  /**
   * Get array statistics
   * @param array - Source array
   * @param options - Analysis options
   */
  analyze<T>(array: T[], options?: {
    numeric?: boolean;
    includeFrequency?: boolean;
    includeDistribution?: boolean;
  }): {
    length: number;
    isEmpty: boolean;
    hasDuplicates: boolean;
    uniqueCount: number;
    min?: number;
    max?: number;
    average?: number;
    median?: number;
    mode?: any;
    frequency?: Record<string, number>;
    distribution?: Record<string, number>;
  };

  /**
   * Calculate array similarity
   * @param array1 - First array
   * @param array2 - Second array
   * @param options - Similarity options
   */
  similarity<T>(array1: T[], array2: T[], options?: {
    algorithm?: 'jaccard' | 'cosine' | 'euclidean';
    key?: string | ((item: T) => any);
  }): number;

  /**
   * Find array patterns
   * @param array - Source array
   * @param options - Pattern options
   */
  findPatterns<T>(array: T[], options?: {
    minLength?: number;
    maxLength?: number;
    minOccurrences?: number;
  }): Array<{
    pattern: T[];
    indices: number[];
    count: number;
  }>;

  // === ARRAY MANIPULATION ===

  /**
   * Insert element at specific position
   * @param array - Source array
   * @param index - Insert position
   * @param element - Element to insert
   * @param options - Insert options
   */
  insert<T>(array: T[], index: number, element: T, options?: {
    replace?: boolean;
    multiple?: boolean;
  }): IArrayResult<T[]>;

  /**
   * Remove element at specific position
   * @param array - Source array
   * @param index - Remove position
   * @param options - Remove options
   */
  remove<T>(array: T[], index: number, options?: {
    count?: number;
    preserveOrder?: boolean;
  }): IArrayResult<T[]>;

  /**
   * Move element to different position
   * @param array - Source array
   * @param fromIndex - Source position
   * @param toIndex - Target position
   * @param options - Move options
   */
  move<T>(array: T[], fromIndex: number, toIndex: number, options?: {
    preserveOriginal?: boolean;
  }): IArrayResult<T[]>;

  /**
   * Swap elements at positions
   * @param array - Source array
   * @param index1 - First position
   * @param index2 - Second position
   * @param options - Swap options
   */
  swap<T>(array: T[], index1: number, index2: number, options?: {
    preserveOriginal?: boolean;
  }): IArrayResult<T[]>;

  // === ARRAY VALIDATION ===

  /**
   * Validate array structure
   * @param array - Array to validate
   * @param schema - Validation schema
   */
  validate<T>(array: T[], schema?: {
    type?: string;
    minLength?: number;
    maxLength?: number;
    unique?: boolean;
    required?: boolean;
  }): {
    isValid: boolean;
    errors: string[];
    warnings: string[];
  };

  /**
   * Check if array is empty
   * @param array - Array to check
   */
  isEmpty<T>(array: T[]): boolean;

  /**
   * Check if array contains only unique values
   * @param array - Array to check
   * @param options - Uniqueness options
   */
  isUnique<T>(array: T[], options?: {
    key?: string | ((item: T) => any);
    caseSensitive?: boolean;
  }): boolean;

  /**
   * Check if array is sorted
   * @param array - Array to check
   * @param options - Sort check options
   */
  isSorted<T>(array: T[], options?: IArraySortOptions): boolean;

  // === ARRAY GENERATION ===

  /**
   * Generate range of numbers
   * @param start - Start value
   * @param end - End value
   * @param options - Range options
   */
  range(start: number, end: number, options?: {
    step?: number;
    inclusive?: boolean;
  }): IArrayResult<number[]>;

  /**
   * Generate array from function
   * @param length - Array length
   * @param generator - Generator function
   * @param options - Generation options
   */
  generate<T>(length: number, generator: (index: number) => T, options?: IArrayTransformOptions): IArrayResult<T[]>;

  /**
   * Generate random array
   * @param length - Array length
   * @param options - Random generation options
   */
  generateRandom<T>(length: number, options?: {
    type?: 'number' | 'string' | 'boolean';
    min?: number;
    max?: number;
    charset?: string;
  }): IArrayResult<T[]>;

  // === ARRAY UTILITIES ===

  /**
   * Get random element from array
   * @param array - Source array
   * @param options - Random selection options
   */
  random<T>(array: T[], options?: {
    count?: number;
    unique?: boolean;
    seed?: number;
  }): IArrayResult<T | T[]>;

  /**
   * Get array sample
   * @param array - Source array
   * @param size - Sample size
   * @param options - Sampling options
   */
  sample<T>(array: T[], size: number, options?: {
    method?: 'random' | 'systematic' | 'stratified';
    seed?: number;
  }): IArrayResult<T[]>;

  /**
   * Rotate array elements
   * @param array - Source array
   * @param positions - Number of positions to rotate
   * @param options - Rotation options
   */
  rotate<T>(array: T[], positions: number, options?: {
    direction?: 'left' | 'right';
    preserveOriginal?: boolean;
  }): IArrayResult<T[]>;

  /**
   * Reverse array with options
   * @param array - Source array
   * @param options - Reverse options
   */
  reverse<T>(array: T[], options?: {
    preserveOriginal?: boolean;
    deep?: boolean;
  }): IArrayResult<T[]>;

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

  /**
   * Optimize array operations
   * @param array - Array to optimize
   * @param options - Optimization options
   */
  optimize<T>(array: T[], options?: IArrayPerformanceOptions): IArrayResult<T[]>;
}