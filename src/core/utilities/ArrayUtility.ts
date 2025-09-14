/**
 * @fileoverview Array Utility Implementation - Enterprise-grade array manipulation utility
 * @version 2.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 */

import { 
  IArrayUtility, IArrayResult, IArraySearchResult, IArraySortOptions, 
  IArrayFilterOptions, IArrayGroupOptions, IArrayTransformOptions 
} from '../interfaces/IArrayUtility';

/**
 * Enterprise Array Utility Implementation
 * Provides comprehensive array manipulation, analysis, and transformation capabilities
 */
export class ArrayUtility implements IArrayUtility {
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

  async initialize(config: any = {}): Promise<void> {
    try {
      this.config = {
        maxCacheSize: 1000,
        enableMetrics: true,
        enableCaching: true,
        ...config
      };
      this.maxCacheSize = this.config.maxCacheSize;
    } catch (error) {
      this.metrics.errors++;
      throw new Error(`ArrayUtility initialization failed: ${error}`);
    }
  }

  async cleanup(): Promise<void> {
    try {
      this.cache.clear();
      this.resetMetrics();
    } catch (error) {
      throw new Error(`ArrayUtility cleanup failed: ${error}`);
    }
  }

  getMetadata() {
    return {
      name: 'ArrayUtility',
      version: '2.0.0',
      capabilities: [
        'search', 'filter', 'sort', 'transform', 'analysis',
        'manipulation', 'validation', 'generation', 'performance'
      ],
      dependencies: []
    };
  }

  // === BASIC ARRAY OPERATIONS ===

  create<T>(length: number, fillValue?: T, options: IArrayTransformOptions = {}): IArrayResult<T[]> {
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

  clone<T>(array: T[], options: IArrayTransformOptions = {}): IArrayResult<T[]> {
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

  merge<T>(arrays: T[][], options: {
    unique?: boolean;
    preserveOrder?: boolean;
    sort?: boolean;
  } = {}): IArrayResult<T[]> {
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

  flatten<T>(array: T[], depth: number = Infinity, options: IArrayTransformOptions = {}): IArrayResult<T[]> {
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

  find<T>(array: T[], predicate: ((item: T, index: number) => boolean) | T, options: IArrayFilterOptions = {}): IArraySearchResult<T> {
    try {
      if (!Array.isArray(array)) {
        return { found: false, index: -1, count: 0 };
      }

      const { offset = 0, limit } = options;
      const searchArray = array.slice(offset, limit ? offset + limit : undefined);
      
      let index = -1;
      let value: T | undefined;
      
      if (typeof predicate === 'function') {
        index = searchArray.findIndex(predicate as (item: T, index: number) => boolean);
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

  findAll<T>(array: T[], predicate: ((item: T, index: number) => boolean) | T, options: IArrayFilterOptions = {}): IArraySearchResult<T> {
    try {
      if (!Array.isArray(array)) {
        return { found: false, index: -1, count: 0 };
      }

      const indices: number[] = [];
      const values: T[] = [];
      
      array.forEach((item, index) => {
        let matches = false;
        
        if (typeof predicate === 'function') {
          matches = (predicate as (item: T, index: number) => boolean)(item, index);
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

  filter<T>(array: T[], predicate: ((item: T, index: number) => boolean) | T, options: IArrayFilterOptions = {}): IArrayResult<T[]> {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(array)) {
        return this.createErrorResult('Invalid input array');
      }

      const { offset = 0, limit } = options;
      let result: T[];
      
      if (typeof predicate === 'function') {
        result = array.filter(predicate as (item: T, index: number) => boolean);
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

  unique<T>(array: T[], options: {
    key?: string | ((item: T) => any);
    caseSensitive?: boolean;
    preserveOrder?: boolean;
  } = {}): IArrayResult<T[]> {
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

  sort<T>(array: T[], options: IArraySortOptions = {}): IArrayResult<T[]> {
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

  map<T, U>(array: T[], mapper: (item: T, index: number) => U, options: IArrayTransformOptions = {}): IArrayResult<U[]> {
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

  reduce<T, U>(array: T[], reducer: (accumulator: U, item: T, index: number) => U, initialValue: U, options: IArrayTransformOptions = {}): IArrayResult<U> {
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

  groupBy<T>(array: T[], options: IArrayGroupOptions): IArrayResult<Record<string, T[]>> {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(array)) {
        return this.createErrorResult('Invalid input array');
      }

      const { key, sort = false, sortDirection = 'asc' } = options;
      const groups: Record<string, T[]> = {};
      
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

  chunk<T>(array: T[], size: number, options: {
    preserveRemainder?: boolean;
    fillValue?: T;
  } = {}): IArrayResult<T[][]> {
    const startTime = performance.now();
    
    try {
      if (!Array.isArray(array) || size <= 0) {
        return this.createErrorResult('Invalid input parameters');
      }

      const { preserveRemainder = true, fillValue } = options;
      const result: T[][] = [];
      
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

  analyze<T>(array: T[], options: {
    numeric?: boolean;
    includeFrequency?: boolean;
    includeDistribution?: boolean;
  } = {}): {
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

      const result: any = {
        length,
        isEmpty,
        hasDuplicates,
        uniqueCount
      };

      if (numeric && length > 0) {
        const numbers = array.filter(item => typeof item === 'number') as number[];
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
    try {
      const errors: string[] = [];
      const warnings: string[] = [];
      
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

  isEmpty<T>(array: T[]): boolean {
    return !Array.isArray(array) || array.length === 0;
  }

  isUnique<T>(array: T[], options?: {
    key?: string | ((item: T) => any);
    caseSensitive?: boolean;
  }): boolean {
    if (!Array.isArray(array)) return false;
    return this.removeDuplicates(array, options).length === array.length;
  }

  // === ARRAY GENERATION ===

  range(start: number, end: number, options: {
    step?: number;
    inclusive?: boolean;
  } = {}): IArrayResult<number[]> {
    const startTime = performance.now();
    
    try {
      const { step = 1, inclusive = true } = options;
      const result: number[] = [];
      
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

  clearCache(): void {
    this.cache.clear();
  }

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

  optimize<T>(array: T[], options?: any): IArrayResult<T[]> {
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

  private createSuccessResult<T>(data: T): IArrayResult<T> {
    return {
      success: true,
      data,
      metrics: {
        processingTime: 0,
        memoryUsage: 0
      }
    };
  }

  private createErrorResult(error: string): IArrayResult {
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

  private deepClone<T>(obj: T): T {
    if (obj === null || typeof obj !== 'object') return obj;
    if (obj instanceof Date) return new Date(obj.getTime()) as any;
    if (obj instanceof Array) return obj.map(item => this.deepClone(item)) as any;
    if (typeof obj === 'object') {
      const cloned: any = {};
      for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
          cloned[key] = this.deepClone(obj[key]);
        }
      }
      return cloned;
    }
    return obj;
  }

  private flattenArray<T>(array: T[], depth: number): T[] {
    if (depth <= 0) return array;
    
    return array.reduce((acc: T[], item) => {
      if (Array.isArray(item)) {
        acc.push(...this.flattenArray(item, depth - 1));
      } else {
        acc.push(item);
      }
      return acc;
    }, []);
  }

  private removeDuplicates<T>(array: T[], options?: {
    key?: string | ((item: T) => any);
    caseSensitive?: boolean;
    preserveOrder?: boolean;
  }): T[] {
    const { key, caseSensitive = true, preserveOrder = true } = options || {};
    
    if (!key) {
      return preserveOrder 
        ? [...new Set(array)]
        : Array.from(new Set(array));
    }

    const seen = new Set();
    const result: T[] = [];
    
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

  private calculateFrequency<T>(array: T[]): Record<string, number> {
    const frequency: Record<string, number> = {};
    
    for (const item of array) {
      const key = String(item);
      frequency[key] = (frequency[key] || 0) + 1;
    }
    
    return frequency;
  }
}