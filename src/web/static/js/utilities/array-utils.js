/**
 * Array Utilities Module - V2 Compliant
 * Array and object manipulation functions
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class ArrayUtils {
    constructor(logger = console) {
        this.logger = logger;
    }

    /**
     * Chunk array into smaller arrays
     */
    chunk(array, size) {
        try {
            if (!Array.isArray(array)) {
                throw new Error('First argument must be an array');
            }
            if (typeof size !== 'number' || size <= 0) {
                throw new Error('Size must be a positive number');
            }

            const chunks = [];
            for (let i = 0; i < array.length; i += size) {
                chunks.push(array.slice(i, i + size));
            }
            return chunks;
        } catch (error) {
            this.logger.error('Array chunking failed', error);
            return [array];
        }
    }

    /**
     * Remove duplicates from array
     */
    unique(array, keyFn = null) {
        try {
            if (!Array.isArray(array)) {
                throw new Error('First argument must be an array');
            }

            if (keyFn) {
                const seen = new Set();
                return array.filter(item => {
                    const key = keyFn(item);
                    if (seen.has(key)) {
                        return false;
                    }
                    seen.add(key);
                    return true;
                });
            }

            return [...new Set(array)];
        } catch (error) {
            this.logger.error('Array unique operation failed', error);
            return array;
        }
    }

    /**
     * Shuffle array elements
     */
    shuffle(array) {
        try {
            if (!Array.isArray(array)) {
                throw new Error('First argument must be an array');
            }

            const shuffled = [...array];
            for (let i = shuffled.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
            }
            return shuffled;
        } catch (error) {
            this.logger.error('Array shuffling failed', error);
            return array;
        }
    }

    /**
     * Group array elements by key
     */
    groupBy(array, keyFn) {
        try {
            if (!Array.isArray(array)) {
                throw new Error('First argument must be an array');
            }

            return array.reduce((groups, item) => {
                const key = typeof keyFn === 'function' ? keyFn(item) : item[keyFn];
                if (!groups[key]) {
                    groups[key] = [];
                }
                groups[key].push(item);
                return groups;
            }, {});
        } catch (error) {
            this.logger.error('Array grouping failed', error);
            return {};
        }
    }

    /**
     * Sort array by multiple criteria
     */
    sortBy(array, sortFns) {
        try {
            if (!Array.isArray(array)) {
                throw new Error('First argument must be an array');
            }

            const fns = Array.isArray(sortFns) ? sortFns : [sortFns];

            return [...array].sort((a, b) => {
                for (const fn of fns) {
                    const result = fn(a, b);
                    if (result !== 0) {
                        return result;
                    }
                }
                return 0;
            });
        } catch (error) {
            this.logger.error('Array sorting failed', error);
            return array;
        }
    }

    /**
     * Find item by property value
     */
    findBy(array, property, value) {
        try {
            if (!Array.isArray(array)) {
                throw new Error('First argument must be an array');
            }

            return array.find(item => item && item[property] === value);
        } catch (error) {
            this.logger.error('Array find operation failed', error);
            return undefined;
        }
    }

    /**
     * Filter array by multiple conditions
     */
    filterBy(array, conditions) {
        try {
            if (!Array.isArray(array)) {
                throw new Error('First argument must be an array');
            }

            return array.filter(item => {
                return Object.entries(conditions).every(([key, value]) => {
                    if (typeof value === 'function') {
                        return value(item[key]);
                    }
                    return item[key] === value;
                });
            });
        } catch (error) {
            this.logger.error('Array filtering failed', error);
            return [];
        }
    }

    /**
     * Deep clone array or object
     */
    deepClone(obj) {
        try {
            if (obj === null || typeof obj !== 'object') {
                return obj;
            }

            if (obj instanceof Date) {
                return new Date(obj);
            }

            if (Array.isArray(obj)) {
                return obj.map(item => this.deepClone(item));
            }

            const cloned = {};
            for (const key in obj) {
                if (obj.hasOwnProperty(key)) {
                    cloned[key] = this.deepClone(obj[key]);
                }
            }
            return cloned;
        } catch (error) {
            this.logger.error('Deep clone failed', error);
            return obj;
        }
    }

    /**
     * Flatten nested arrays
     */
    flatten(array, depth = Infinity) {
        try {
            if (!Array.isArray(array)) {
                throw new Error('First argument must be an array');
            }

            return array.flat(depth);
        } catch (error) {
            this.logger.error('Array flattening failed', error);
            return array;
        }
    }

    /**
     * Get random element from array
     */
    random(array) {
        try {
            if (!Array.isArray(array) || array.length === 0) {
                throw new Error('First argument must be a non-empty array');
            }

            return array[Math.floor(Math.random() * array.length)];
        } catch (error) {
            this.logger.error('Random element selection failed', error);
            return undefined;
        }
    }

    /**
     * Check if array contains item
     */
    contains(array, item, comparator = null) {
        try {
            if (!Array.isArray(array)) {
                throw new Error('First argument must be an array');
            }

            if (comparator) {
                return array.some(element => comparator(element, item));
            }

            return array.includes(item);
        } catch (error) {
            this.logger.error('Array contains check failed', error);
            return false;
        }
    }
}

// Factory function for creating array utils instance
export function createArrayUtils(logger = console) {
    return new ArrayUtils(logger);
}
