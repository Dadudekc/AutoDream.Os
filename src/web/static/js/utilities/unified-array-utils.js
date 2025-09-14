/**
 * @fileoverview Unified Array Utilities - JavaScript Adapter for Shared Core
 * @version 3.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 * 
 * JavaScript adapter that uses the shared ArrayCore implementation.
 * Provides a simplified API for JavaScript environments.
 */

import { ArrayCore } from '../../../../core/utilities/shared/array-core.js';

/**
 * Unified Array Utilities Class
 * JavaScript adapter around the shared ArrayCore
 */
export class UnifiedArrayUtils {
  constructor(config = {}) {
    this.core = new ArrayCore(config);
  }

  /**
   * Initialize the array utility with configuration
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

  // === BASIC ARRAY OPERATIONS ===

  /**
   * Create array with specified length and fill value
   */
  create(length, fillValue, options = {}) {
    return this.core.create(length, fillValue, options);
  }

  /**
   * Clone array with optional deep cloning
   */
  clone(array, options = {}) {
    return this.core.clone(array, options);
  }

  /**
   * Merge multiple arrays with options
   */
  merge(arrays, options = {}) {
    return this.core.merge(arrays, options);
  }

  /**
   * Flatten nested arrays
   */
  flatten(array, depth = Infinity, options = {}) {
    return this.core.flatten(array, depth, options);
  }

  // === ARRAY SEARCH & FILTERING ===

  /**
   * Find element in array with predicate
   */
  find(array, predicate, options = {}) {
    return this.core.find(array, predicate, options);
  }

  /**
   * Find all elements matching predicate
   */
  findAll(array, predicate, options = {}) {
    return this.core.findAll(array, predicate, options);
  }

  /**
   * Filter array with predicate
   */
  filter(array, predicate, options = {}) {
    return this.core.filter(array, predicate, options);
  }

  /**
   * Remove duplicates from array
   */
  unique(array, options = {}) {
    return this.core.unique(array, options);
  }

  // === ARRAY SORTING ===

  /**
   * Sort array with advanced options
   */
  sort(array, options = {}) {
    return this.core.sort(array, options);
  }

  // === ARRAY TRANSFORMATION ===

  /**
   * Map array elements
   */
  map(array, mapper, options = {}) {
    return this.core.map(array, mapper, options);
  }

  /**
   * Reduce array to single value
   */
  reduce(array, reducer, initialValue, options = {}) {
    return this.core.reduce(array, reducer, initialValue, options);
  }

  /**
   * Group array elements by key
   */
  groupBy(array, options) {
    return this.core.groupBy(array, options);
  }

  /**
   * Chunk array into smaller arrays
   */
  chunk(array, size, options = {}) {
    return this.core.chunk(array, size, options);
  }

  // === ARRAY ANALYSIS ===

  /**
   * Analyze array statistics
   */
  analyze(array, options = {}) {
    return this.core.analyze(array, options);
  }

  // === ARRAY VALIDATION ===

  /**
   * Validate array against schema
   */
  validate(array, schema) {
    return this.core.validate(array, schema);
  }

  /**
   * Check if array is empty
   */
  isEmpty(array) {
    return this.core.isEmpty(array);
  }

  /**
   * Check if array contains unique values
   */
  isUnique(array, options = {}) {
    return this.core.isUnique(array, options);
  }

  // === ARRAY GENERATION ===

  /**
   * Generate range of numbers
   */
  range(start, end, options = {}) {
    return this.core.range(start, end, options);
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

  /**
   * Optimize array
   */
  optimize(array, options = {}) {
    return this.core.optimize(array, options);
  }

  // === CONVENIENCE METHODS ===

  /**
   * Simple array filtering (backward compatibility)
   */
  filterBy(array, key, value) {
    return array.filter(item => item[key] === value);
  }

  /**
   * Simple array sorting (backward compatibility)
   */
  sortBy(array, key, direction = 'asc') {
    const result = this.sort(array, { key, direction });
    return result.success ? result.data : array;
  }

  /**
   * Simple array grouping (backward compatibility)
   */
  groupByKey(array, key) {
    const result = this.groupBy(array, { key });
    return result.success ? result.data : {};
  }

  /**
   * Simple array chunking (backward compatibility)
   */
  chunkArray(array, size) {
    const result = this.chunk(array, size);
    return result.success ? result.data : [];
  }

  /**
   * Simple array flattening (backward compatibility)
   */
  flattenArray(array) {
    const result = this.flatten(array);
    return result.success ? result.data : array;
  }

  /**
   * Simple array unique (backward compatibility)
   */
  uniqueArray(array) {
    const result = this.unique(array);
    return result.success ? result.data : array;
  }

  /**
   * Simple array range (backward compatibility)
   */
  createRange(start, end, step = 1) {
    const result = this.range(start, end, { step });
    return result.success ? result.data : [];
  }

  /**
   * Simple array statistics (backward compatibility)
   */
  getArrayStats(array) {
    return this.analyze(array, { numeric: true, includeFrequency: true });
  }

  /**
   * Simple array validation (backward compatibility)
   */
  isValidArray(array, options = {}) {
    const result = this.validate(array, options);
    return result.isValid;
  }

  /**
   * Simple array search (backward compatibility)
   */
  findInArray(array, value) {
    const result = this.find(array, value);
    return result.found ? result.value : null;
  }

  /**
   * Simple array search all (backward compatibility)
   */
  findAllInArray(array, value) {
    const result = this.findAll(array, value);
    return result.found ? result.values : [];
  }
}

// Factory function for creating array utils instance
export function createUnifiedArrayUtils(config = {}) {
  return new UnifiedArrayUtils(config);
}

// Export default
export default UnifiedArrayUtils;