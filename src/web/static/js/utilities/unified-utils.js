/**
 * @fileoverview Unified Utilities Index - JavaScript Exports
 * @version 3.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 * 
 * Central export point for all unified utility classes.
 * Provides a single import point for JavaScript environments.
 */

// Import all unified utility classes
import { UnifiedStringUtils } from './unified-string-utils.js';
import { UnifiedArrayUtils } from './unified-array-utils.js';
import { UnifiedTimeUtils } from './unified-time-utils.js';
import { UnifiedLoggingUtils } from './unified-logging-utils.js';

// Export all unified utility classes
export { UnifiedStringUtils } from './unified-string-utils.js';
export { UnifiedArrayUtils } from './unified-array-utils.js';
export { UnifiedTimeUtils } from './unified-time-utils.js';
export { UnifiedLoggingUtils } from './unified-logging-utils.js';

// Create default instances
export const stringUtils = new UnifiedStringUtils();
export const arrayUtils = new UnifiedArrayUtils();
export const timeUtils = new UnifiedTimeUtils();
export const loggingUtils = new UnifiedLoggingUtils();

// Export factory functions
export function createStringUtils(config = {}) {
  return new UnifiedStringUtils(config);
}

export function createArrayUtils(config = {}) {
  return new UnifiedArrayUtils(config);
}

export function createTimeUtils(config = {}) {
  return new UnifiedTimeUtils(config);
}

export function createLoggingUtils(config = {}) {
  return new UnifiedLoggingUtils(config);
}

// Export all utilities as a single object
export const unifiedUtils = {
  string: stringUtils,
  array: arrayUtils,
  time: timeUtils,
  logging: loggingUtils,
  
  // Factory methods
  createString: createStringUtils,
  createArray: createArrayUtils,
  createTime: createTimeUtils,
  createLogging: createLoggingUtils
};

// Default export
export default unifiedUtils;