/**
 * @fileoverview Unified Array Utility - TypeScript Wrapper for Shared Core
 * @version 3.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 * 
 * TypeScript wrapper around the shared ArrayCore implementation.
 * Provides type safety while using the universal JavaScript core.
 */

import { ArrayCore } from '../shared/array-core.js';
import { 
  IArrayUtility, IArrayResult, IArraySearchResult, IArraySortOptions, 
  IArrayFilterOptions, IArrayGroupOptions, IArrayTransformOptions 
} from '../../interfaces/IArrayUtility';

/**
 * Unified Array Utility Implementation
 * TypeScript wrapper around the shared ArrayCore
 */
export class ArrayUtility implements IArrayUtility {
  private core: ArrayCore;

  constructor(config: any = {}) {
    this.core = new ArrayCore(config);
  }

  /**
   * Initialize the array utility with configuration
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

  // === BASIC ARRAY OPERATIONS ===

  /**
   * Create array with specified length and fill value
   */
  create<T>(length: number, fillValue?: T, options?: IArrayTransformOptions): IArrayResult<T[]> {
    return this.core.create(length, fillValue, options);
  }

  /**
   * Clone array with optional deep cloning
   */
  clone<T>(array: T[], options?: IArrayTransformOptions): IArrayResult<T[]> {
    return this.core.clone(array, options);
  }

  /**
   * Merge multiple arrays with options
   */
  merge<T>(arrays: T[][], options?: {
    unique?: boolean;
    preserveOrder?: boolean;
    sort?: boolean;
  }): IArrayResult<T[]> {
    return this.core.merge(arrays, options);
  }

  /**
   * Flatten nested arrays
   */
  flatten<T>(array: T[], depth?: number, options?: IArrayTransformOptions): IArrayResult<T[]> {
    return this.core.flatten(array, depth, options);
  }

  // === ARRAY SEARCH & FILTERING ===

  /**
   * Find element in array with predicate
   */
  find<T>(array: T[], predicate: ((item: T, index: number) => boolean) | T, options?: IArrayFilterOptions): IArraySearchResult<T> {
    return this.core.find(array, predicate, options);
  }

  /**
   * Find all elements matching predicate
   */
  findAll<T>(array: T[], predicate: ((item: T, index: number) => boolean) | T, options?: IArrayFilterOptions): IArraySearchResult<T> {
    return this.core.findAll(array, predicate, options);
  }

  /**
   * Filter array with predicate
   */
  filter<T>(array: T[], predicate: ((item: T, index: number) => boolean) | T, options?: IArrayFilterOptions): IArrayResult<T[]> {
    return this.core.filter(array, predicate, options);
  }

  /**
   * Remove duplicates from array
   */
  unique<T>(array: T[], options?: {
    key?: string | ((item: T) => any);
    caseSensitive?: boolean;
    preserveOrder?: boolean;
  }): IArrayResult<T[]> {
    return this.core.unique(array, options);
  }

  // === ARRAY SORTING ===

  /**
   * Sort array with advanced options
   */
  sort<T>(array: T[], options?: IArraySortOptions): IArrayResult<T[]> {
    return this.core.sort(array, options);
  }

  // === ARRAY TRANSFORMATION ===

  /**
   * Map array elements
   */
  map<T, U>(array: T[], mapper: (item: T, index: number) => U, options?: IArrayTransformOptions): IArrayResult<U[]> {
    return this.core.map(array, mapper, options);
  }

  /**
   * Reduce array to single value
   */
  reduce<T, U>(array: T[], reducer: (accumulator: U, item: T, index: number) => U, initialValue: U, options?: IArrayTransformOptions): IArrayResult<U> {
    return this.core.reduce(array, reducer, initialValue, options);
  }

  /**
   * Group array elements by key
   */
  groupBy<T>(array: T[], options: IArrayGroupOptions): IArrayResult<Record<string, T[]>> {
    return this.core.groupBy(array, options);
  }

  /**
   * Chunk array into smaller arrays
   */
  chunk<T>(array: T[], size: number, options?: {
    preserveRemainder?: boolean;
    fillValue?: T;
  }): IArrayResult<T[][]> {
    return this.core.chunk(array, size, options);
  }

  // === ARRAY ANALYSIS ===

  /**
   * Analyze array statistics
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
  } {
    return this.core.analyze(array, options);
  }

  // === ARRAY VALIDATION ===

  /**
   * Validate array against schema
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
  } {
    return this.core.validate(array, schema);
  }

  /**
   * Check if array is empty
   */
  isEmpty<T>(array: T[]): boolean {
    return this.core.isEmpty(array);
  }

  /**
   * Check if array contains unique values
   */
  isUnique<T>(array: T[], options?: {
    key?: string | ((item: T) => any);
    caseSensitive?: boolean;
  }): boolean {
    return this.core.isUnique(array, options);
  }

  // === ARRAY GENERATION ===

  /**
   * Generate range of numbers
   */
  range(start: number, end: number, options?: {
    step?: number;
    inclusive?: boolean;
  }): IArrayResult<number[]> {
    return this.core.range(start, end, options);
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

  /**
   * Optimize array
   */
  optimize<T>(array: T[], options?: any): IArrayResult<T[]> {
    return this.core.optimize(array, options);
  }
}

// Export for both CommonJS and ES modules
export default ArrayUtility;