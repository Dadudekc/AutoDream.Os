/**
 * @fileoverview Shared Array Utilities Core - Universal JavaScript Implementation
 * @version 3.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 * 
 * Universal array utility functions that work in both Node.js and browser environments.
 * This is the core implementation that both TypeScript and JavaScript utilities will use.
 */

/**
 * Universal Array Utilities Core
 * Provides comprehensive array manipulation, analysis, and transformation capabilities
 * Works in both Node.js and browser environments
 */
export class ArrayCore {
  constructor(config = {}) {
    this.config = {
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
   * Initialize the array utility with configuration
   */
  async initialize(config = {}) {
    try {
      this.config = { ...this.config, ...config };
      this.maxCacheSize = this.config.maxCacheSize;
    } catch (error) {
      this.metrics.errors++;
      throw new Error(`ArrayCore initialization failed: ${error}`);
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
      throw new Error(`ArrayCore cleanup failed: ${error}`);
    }
  }

  /**
   * Get utility metadata and capabilities
   */
  getMetadata() {
    return {
      name: 'ArrayCore',
      version: '3.0.0',
      capabilities: [
        'search', 'filter', 'sort', 'transform', 'analysis',
        'manipulation', 'validation', 'generation', 'performance'
      ],
      dependencies: []
    };
  }

  // === BASIC ARRAY OPERATIONS ===

  /**
   * Create array with specified length and fill value
   */
  create(length, fillValue, options = {}) {
    const startTime = performance.now();
    
    try {
      if (typeof length !== 'number' || length < 0) {
        return this.createErrorResult('Invalid length');
      }

      const result = Array(length).fill(fillValue);
      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Array creation failed: ${error}`);
    }
  }

  /**
   * Clone array with optional deep cloning
   */
  clone(array, options = {}) {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(array)) {
        return this.createErrorResult('Invalid input array');
      }

      const result = options.deep ? this.deepClone(array) : [...array];
      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Array cloning failed: ${error}`);
    }
  }

  /**
   * Merge multiple arrays with options
   */
  merge(arrays, options = {}) {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(arrays)) {
        return this.createErrorResult('Invalid input arrays');
      }

      let result = arrays.flat();
      
      if (options.unique) {
        result = this.removeDuplicates(result);
      }
      
      if (options.sort) {
        result.sort();
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Array merge failed: ${error}`);
    }
  }

  /**
   * Flatten nested arrays
   */
  flatten(array, depth = Infinity, options = {}) {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(array)) {
        return this.createErrorResult('Invalid input array');
      }

      const result = this.flattenArray(array, depth);
      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Array flatten failed: ${error}`);
    }
  }

  // === ARRAY SEARCH & FILTERING ===

  /**
   * Find element in array with predicate
   */
  find(array, predicate, options = {}) {
    try {
      if (!Array.isArray(array)) {
        return { found: false, index: -1, count: 0 };
      }

      const { offset = 0, limit } = options;
      const searchArray = array.slice(offset, limit ? offset + limit : undefined);
      
      let index = -1;
      let value;
      
      if (typeof predicate === 'function') {
        index = searchArray.findIndex(predicate);
        value = index >= 0 ? searchArray[index] : undefined;
      } else {
        index = searchArray.indexOf(predicate);
        value = index >= 0 ? searchArray[index] : undefined;
      }

      return {
        found: index >= 0,
        index: index >= 0 ? index + offset : -1,
        value,
        count: index >= 0 ? 1 : 0
      };
    } catch (error) {
      return { found: false, index: -1, count: 0 };
    }
  }

  /**
   * Find all elements matching predicate
   */
  findAll(array, predicate, options = {}) {
    try {
      if (!Array.isArray(array)) {
        return { found: false, index: -1, count: 0 };
      }

      const indices = [];
      const values = [];
      
      array.forEach((item, index) => {
        let matches = false;
        
        if (typeof predicate === 'function') {
          matches = predicate(item, index);
        } else {
          matches = item === predicate;
        }
        
        if (matches) {
          indices.push(index);
          values.push(item);
        }
      });

      return {
        found: indices.length > 0,
        index: indices[0] || -1,
        indices,
        values,
        count: indices.length
      };
    } catch (error) {
      return { found: false, index: -1, count: 0 };
    }
  }

  /**
   * Filter array with predicate
   */
  filter(array, predicate, options = {}) {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(array)) {
        return this.createErrorResult('Invalid input array');
      }

      const { offset = 0, limit } = options;
      let result;
      
      if (typeof predicate === 'function') {
        result = array.filter(predicate);
      } else {
        result = array.filter(item => item === predicate);
      }
      
      if (offset > 0 || limit) {
        result = result.slice(offset, limit ? offset + limit : undefined);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Array filter failed: ${error}`);
    }
  }

  /**
   * Remove duplicates from array
   */
  unique(array, options = {}) {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(array)) {
        return this.createErrorResult('Invalid input array');
      }

      const result = this.removeDuplicates(array, options);
      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Array unique failed: ${error}`);
    }
  }

  // === ARRAY SORTING ===

  /**
   * Sort array with advanced options
   */
  sort(array, options = {}) {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(array)) {
        return this.createErrorResult('Invalid input array');
      }

      const { key, direction = 'asc', locale = 'en-US', numeric = false, caseSensitive = true } = options;
      const result = [...array];
      
      result.sort((a, b) => {
        let aVal = key ? (typeof key === 'function' ? key(a) : a[key]) : a;
        let bVal = key ? (typeof key === 'function' ? key(b) : b[key]) : b;
        
        if (!caseSensitive && typeof aVal === 'string' && typeof bVal === 'string') {
          aVal = aVal.toLowerCase();
          bVal = bVal.toLowerCase();
        }
        
        if (numeric && typeof aVal === 'number' && typeof bVal === 'number') {
          return direction === 'asc' ? aVal - bVal : bVal - aVal;
        }
        
        if (typeof aVal === 'string' && typeof bVal === 'string') {
          return direction === 'asc' 
            ? aVal.localeCompare(bVal, locale)
            : bVal.localeCompare(aVal, locale);
        }
        
        if (aVal < bVal) return direction === 'asc' ? -1 : 1;
        if (aVal > bVal) return direction === 'asc' ? 1 : -1;
        return 0;
      });

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Array sort failed: ${error}`);
    }
  }

  // === ARRAY TRANSFORMATION ===

  /**
   * Map array elements
   */
  map(array, mapper, options = {}) {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(array)) {
        return this.createErrorResult('Invalid input array');
      }

      const result = array.map(mapper);
      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Array map failed: ${error}`);
    }
  }

  /**
   * Reduce array to single value
   */
  reduce(array, reducer, initialValue, options = {}) {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(array)) {
        return this.createErrorResult('Invalid input array');
      }

      const result = array.reduce(reducer, initialValue);
      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Array reduce failed: ${error}`);
    }
  }

  /**
   * Group array elements by key
   */
  groupBy(array, options) {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(array)) {
        return this.createErrorResult('Invalid input array');
      }

      const { key, sort = false, sortDirection = 'asc' } = options;
      const groups = {};
      
      array.forEach(item => {
        const groupKey = key 
          ? (typeof key === 'function' ? key(item) : item[key])
          : String(item);
        
        if (!groups[groupKey]) {
          groups[groupKey] = [];
        }
        groups[groupKey].push(item);
      });
      
      if (sort) {
        Object.keys(groups).sort((a, b) => {
          return sortDirection === 'asc' ? a.localeCompare(b) : b.localeCompare(a);
        });
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(groups);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Array groupBy failed: ${error}`);
    }
  }

  /**
   * Chunk array into smaller arrays
   */
  chunk(array, size, options = {}) {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(array) || size <= 0) {
        return this.createErrorResult('Invalid input parameters');
      }

      const { preserveRemainder = true, fillValue } = options;
      const result = [];
      
      for (let i = 0; i < array.length; i += size) {
        const chunk = array.slice(i, i + size);
        
        if (!preserveRemainder && chunk.length < size && fillValue !== undefined) {
          while (chunk.length < size) {
            chunk.push(fillValue);
          }
        }
        
        if (preserveRemainder || chunk.length === size) {
          result.push(chunk);
        }
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Array chunk failed: ${error}`);
    }
  }

  // === ARRAY ANALYSIS ===

  /**
   * Analyze array statistics
   */
  analyze(array, options = {}) {
    try {
      if (!Array.isArray(array)) {
        return {
          length: 0,
          isEmpty: true,
          hasDuplicates: false,
          uniqueCount: 0
        };
      }

      const { numeric = false, includeFrequency = false, includeDistribution = false } = options;
      const length = array.length;
      const isEmpty = length === 0;
      const uniqueArray = this.removeDuplicates(array);
      const hasDuplicates = uniqueArray.length !== length;
      const uniqueCount = uniqueArray.length;

      const result = {
        length,
        isEmpty,
        hasDuplicates,
        uniqueCount
      };

      if (numeric && length > 0) {
        const numbers = array.filter(item => typeof item === 'number');
        if (numbers.length > 0) {
          result.min = Math.min(...numbers);
          result.max = Math.max(...numbers);
          result.average = numbers.reduce((sum, num) => sum + num, 0) / numbers.length;
          
          const sorted = [...numbers].sort((a, b) => a - b);
          const mid = Math.floor(sorted.length / 2);
          result.median = sorted.length % 2 === 0 
            ? (sorted[mid - 1] + sorted[mid]) / 2 
            : sorted[mid];
        }
      }

      if (includeFrequency) {
        result.frequency = this.calculateFrequency(array);
      }

      return result;
    } catch (error) {
      return {
        length: 0,
        isEmpty: true,
        hasDuplicates: false,
        uniqueCount: 0
      };
    }
  }

  // === ARRAY VALIDATION ===

  /**
   * Validate array against schema
   */
  validate(array, schema) {
    try {
      const errors = [];
      const warnings = [];
      
      if (!Array.isArray(array)) {
        errors.push('Input is not an array');
        return { isValid: false, errors, warnings };
      }

      if (schema) {
        const { minLength, maxLength, unique, required } = schema;
        
        if (required && array.length === 0) {
          errors.push('Array is required but empty');
        }
        
        if (minLength !== undefined && array.length < minLength) {
          errors.push(`Array length ${array.length} is less than minimum ${minLength}`);
        }
        
        if (maxLength !== undefined && array.length > maxLength) {
          errors.push(`Array length ${array.length} exceeds maximum ${maxLength}`);
        }
        
        if (unique && this.removeDuplicates(array).length !== array.length) {
          errors.push('Array contains duplicate values');
        }
      }

      return {
        isValid: errors.length === 0,
        errors,
        warnings
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
   * Check if array is empty
   */
  isEmpty(array) {
    return !Array.isArray(array) || array.length === 0;
  }

  /**
   * Check if array contains unique values
   */
  isUnique(array, options) {
    if (!Array.isArray(array)) return false;
    return this.removeDuplicates(array, options).length === array.length;
  }

  // === ARRAY GENERATION ===

  /**
   * Generate range of numbers
   */
  range(start, end, options = {}) {
    const startTime = performance.now();
    
    try {
      const { step = 1, inclusive = true } = options;
      const result = [];
      
      const actualEnd = inclusive ? end : end - 1;
      
      for (let i = start; i <= actualEnd; i += step) {
        result.push(i);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Range generation failed: ${error}`);
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

  /**
   * Optimize array
   */
  optimize(array, options) {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(array)) {
        return this.createErrorResult('Invalid input array');
      }

      // Basic optimization: remove duplicates and sort
      const optimized = this.removeDuplicates(array).sort();
      
      this.updateMetrics(startTime);
      return this.createSuccessResult(optimized);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Array optimization failed: ${error}`);
    }
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

  deepClone(obj) {
    if (obj === null || typeof obj !== 'object') return obj;
    if (obj instanceof Date) return new Date(obj.getTime());
    if (obj instanceof Array) return obj.map(item => this.deepClone(item));
    if (typeof obj === 'object') {
      const cloned = {};
      for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
          cloned[key] = this.deepClone(obj[key]);
        }
      }
      return cloned;
    }
    return obj;
  }

  flattenArray(array, depth) {
    if (depth <= 0) return array;
    
    return array.reduce((acc, item) => {
      if (Array.isArray(item)) {
        acc.push(...this.flattenArray(item, depth - 1));
      } else {
        acc.push(item);
      }
      return acc;
    }, []);
  }

  removeDuplicates(array, options) {
    const { key, caseSensitive = true, preserveOrder = true } = options || {};
    
    if (!key) {
      return preserveOrder 
        ? [...new Set(array)]
        : Array.from(new Set(array));
    }

    const seen = new Set();
    const result = [];
    
    for (const item of array) {
      let keyValue = typeof key === 'function' ? key(item) : item[key];
      
      if (!caseSensitive && typeof keyValue === 'string') {
        keyValue = keyValue.toLowerCase();
      }
      
      if (!seen.has(keyValue)) {
        seen.add(keyValue);
        result.push(item);
      }
    }
    
    return result;
  }

  calculateFrequency(array) {
    const frequency = {};
    
    for (const item of array) {
      const key = String(item);
      frequency[key] = (frequency[key] || 0) + 1;
    }
    
    return frequency;
  }
}

// Export for both CommonJS and ES modules
export default ArrayCore;