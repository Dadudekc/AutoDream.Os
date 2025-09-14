/**
 * @fileoverview Unified Utilities Index - TypeScript Exports
 * @version 3.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 * 
 * Central export point for all unified utility classes.
 * Provides a single import point for TypeScript environments.
 */

// Export all unified utility classes
export { StringUtility } from './StringUtility';
export { ArrayUtility } from './ArrayUtility';
export { TimeUtility } from './TimeUtility';
export { LoggingUtility } from './LoggingUtility';

// Export default instances for convenience
import { StringUtility } from './StringUtility';
import { ArrayUtility } from './ArrayUtility';
import { TimeUtility } from './TimeUtility';
import { LoggingUtility } from './LoggingUtility';

// Create default instances
export const stringUtils = new StringUtility();
export const arrayUtils = new ArrayUtility();
export const timeUtils = new TimeUtility();
export const loggingUtils = new LoggingUtility();

// Export factory functions
export function createStringUtility(config?: any) {
  return new StringUtility(config);
}

export function createArrayUtility(config?: any) {
  return new ArrayUtility(config);
}

export function createTimeUtility(config?: any) {
  return new TimeUtility(config);
}

export function createLoggingUtility(config?: any) {
  return new LoggingUtility(config);
}

// Export all utilities as a single object
export const unifiedUtils = {
  string: stringUtils,
  array: arrayUtils,
  time: timeUtils,
  logging: loggingUtils,
  
  // Factory methods
  createString: createStringUtility,
  createArray: createArrayUtility,
  createTime: createTimeUtility,
  createLogging: createLoggingUtility
};

// Default export
export default unifiedUtils;