/**
 * Array Utilities Module - V2 Compliant
 * Array utility functions extracted from utilities-consolidated.js
 * V2 Compliance: ≤400 lines for compliance
 *
 * @author Agent-7 - Web Development Specialist
 * @version 3.0.0 - V2 COMPLIANCE REFACTORED
 * @license MIT
 */

/**
 * Array Utilities Class
 * V2 Compliance: Extracted from monolithic 1263-line file
 */
export class ArrayUtils {
    constructor() {
        this.name = 'ArrayUtils';
        this.cache = new Map();
    }

    /**
     * Remove duplicates from array
     */
    unique(array) {
        const cacheKey = `unique_${JSON.stringify(array)}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        const result = [...new Set(array)];
        this.cache.set(cacheKey, result);
        return result;
    }

    /**
     * Chunk array into smaller arrays
     */
    chunk(array, size) {
        const cacheKey = `chunk_${JSON.stringify(array)}_${size}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        const chunks = [];
        for (let i = 0; i < array.length; i += size) {
            chunks.push(array.slice(i, i + size));
        }

        this.cache.set(cacheKey, chunks);
        return chunks;
    }

    /**
     * Flatten nested arrays
     */
    flatten(array) {
        const cacheKey = `flatten_${JSON.stringify(array)}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        const result = array.reduce((flat, item) => {
            return flat.concat(Array.isArray(item) ? this.flatten(item) : item);
        }, []);

        this.cache.set(cacheKey, result);
        return result;
    }

    /**
     * Group array by key
     */
    groupBy(array, key) {
        const cacheKey = `groupBy_${JSON.stringify(array)}_${key}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        const result = array.reduce((groups, item) => {
            const group = item[key];
            groups[group] = groups[group] || [];
            groups[group].push(item);
            return groups;
        }, {});

        this.cache.set(cacheKey, result);
        return result;
    }

    /**
     * Sort array by key
     */
    sortBy(array, key, direction = 'asc') {
        const cacheKey = `sortBy_${JSON.stringify(array)}_${key}_${direction}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        const result = array.sort((a, b) => {
            const aVal = a[key];
            const bVal = b[key];
            if (direction === 'desc') {
                return bVal > aVal ? 1 : -1;
            }
            return aVal > bVal ? 1 : -1;
        });

        this.cache.set(cacheKey, result);
        return result;
    }

    /**
     * Filter array by condition
     */
    filterBy(array, condition) {
        if (typeof condition === 'function') {
            return array.filter(condition);
        }

        if (typeof condition === 'object') {
            return array.filter(item => {
                return Object.entries(condition).every(([key, value]) => {
                    return item[key] === value;
                });
            });
        }

        return array;
    }

    /**
     * Find item in array
     */
    findBy(array, condition) {
        if (typeof condition === 'function') {
            return array.find(condition);
        }

        if (typeof condition === 'object') {
            return array.find(item => {
                return Object.entries(condition).every(([key, value]) => {
                    return item[key] === value;
                });
            });
        }

        return undefined;
    }

    /**
     * Map array with transformation
     */
    mapBy(array, transform) {
        if (typeof transform === 'string') {
            return array.map(item => item[transform]);
        }

        if (typeof transform === 'function') {
            return array.map(transform);
        }

        return array;
    }

    /**
     * Reduce array to single value
     */
    reduceBy(array, reducer, initialValue) {
        return array.reduce(reducer, initialValue);
    }

    /**
     * Get array statistics
     */
    getStats(array) {
        if (!Array.isArray(array) || array.length === 0) {
            return {
                length: 0,
                min: null,
                max: null,
                sum: 0,
                average: 0,
                median: null
            };
        }

        const sorted = [...array].sort((a, b) => a - b);
        const sum = array.reduce((acc, val) => acc + val, 0);

        return {
            length: array.length,
            min: Math.min(...array),
            max: Math.max(...array),
            sum: sum,
            average: sum / array.length,
            median: sorted.length % 2 === 0
                ? (sorted[sorted.length / 2 - 1] + sorted[sorted.length / 2]) / 2
                : sorted[Math.floor(sorted.length / 2)]
        };
    }

    /**
     * Shuffle array
     */
    shuffle(array) {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }

    /**
     * Sample random items from array
     */
    sample(array, count = 1) {
        const shuffled = this.shuffle(array);
        return shuffled.slice(0, count);
    }

    /**
     * Remove items from array
     */
    remove(array, items) {
        if (!Array.isArray(items)) {
            items = [items];
        }
        return array.filter(item => !items.includes(item));
    }

    /**
     * Insert item at index
     */
    insertAt(array, index, item) {
        const result = [...array];
        result.splice(index, 0, item);
        return result;
    }

    /**
     * Remove item at index
     */
    removeAt(array, index) {
        const result = [...array];
        result.splice(index, 1);
        return result;
    }

    /**
     * Replace item at index
     */
    replaceAt(array, index, item) {
        const result = [...array];
        result[index] = item;
        return result;
    }

    /**
     * Get unique values by key
     */
    uniqueBy(array, key) {
        const seen = new Set();
        return array.filter(item => {
            const value = item[key];
            if (seen.has(value)) {
                return false;
            }
            seen.add(value);
            return true;
        });
    }

    /**
     * Partition array into two arrays
     */
    partition(array, predicate) {
        const truthy = [];
        const falsy = [];

        array.forEach(item => {
            if (predicate(item)) {
                truthy.push(item);
            } else {
                falsy.push(item);
            }
        });

        return [truthy, falsy];
    }

    /**
     * Zip arrays together
     */
    zip(...arrays) {
        const maxLength = Math.max(...arrays.map(arr => arr.length));
        const result = [];

        for (let i = 0; i < maxLength; i++) {
            result.push(arrays.map(arr => arr[i]));
        }

        return result;
    }

    /**
     * Unzip array of arrays
     */
    unzip(zippedArray) {
        if (zippedArray.length === 0) return [];

        const result = [];
        const maxLength = Math.max(...zippedArray.map(arr => arr.length));

        for (let i = 0; i < maxLength; i++) {
            result.push(zippedArray.map(arr => arr[i]));
        }

        return result;
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
    }

    /**
     * Get cache size
     */
    getCacheSize() {
        return this.cache.size;
    }
}

// Export default instance
export default new ArrayUtils();
