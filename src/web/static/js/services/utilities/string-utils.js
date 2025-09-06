/**
 * String Utilities - V2 Compliant Module
 * String manipulation and formatting functions
 * MODULAR: ~95 lines (V2 compliant)
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE MODULAR EXTRACTION
 * @license MIT
 */

export class StringUtils {
    constructor() {
        this.logger = new UnifiedLoggingSystem("StringUtils");
    }

    /**
     * Capitalize first letter of string
     */
    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    /**
     * Convert to camelCase
     */
    toCamelCase(str) {
        return str
            .replace(/(?:^\w|[A-Z]|\b\w)/g, (word, index) => {
                return index === 0 ? word.toLowerCase() : word.toUpperCase();
            })
            .replace(/\s+/g, '');
    }

    /**
     * Convert to kebab-case
     */
    toKebabCase(str) {
        return str
            .replace(/([a-z])([A-Z])/g, '$1-$2')
            .replace(/[\s_]+/g, '-')
            .toLowerCase();
    }

    /**
     * Truncate string with ellipsis
     */
    truncate(str, maxLength = 100, suffix = '...') {
        if (str.length <= maxLength) return str;
        return str.slice(0, maxLength - suffix.length) + suffix;
    }

    /**
     * Remove extra whitespace
     */
    normalizeWhitespace(str) {
        return str.replace(/\s+/g, ' ').trim();
    }
}
