/**
 * @fileoverview Time Utility Interface - Enterprise-grade time manipulation interface
 * @version 2.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 */

/**
 * Time operation result interface
 */
export interface ITimeResult {
  success: boolean;
  data?: any;
  error?: string;
  metrics?: {
    processingTime: number;
    memoryUsage: number;
    cacheHit?: boolean;
  };
}

/**
 * Time format options
 */
export interface ITimeFormatOptions {
  locale?: string;
  timeZone?: string;
  format?: 'short' | 'medium' | 'long' | 'full' | 'custom';
  customFormat?: string;
  includeTime?: boolean;
  includeDate?: boolean;
  includeTimezone?: boolean;
}

/**
 * Time calculation options
 */
export interface ITimeCalculationOptions {
  unit?: 'milliseconds' | 'seconds' | 'minutes' | 'hours' | 'days' | 'weeks' | 'months' | 'years';
  precision?: number;
  absolute?: boolean;
  businessDays?: boolean;
  excludeWeekends?: boolean;
  excludeHolidays?: boolean;
}

/**
 * Time validation options
 */
export interface ITimeValidationOptions {
  minDate?: Date | string;
  maxDate?: Date | string;
  allowFuture?: boolean;
  allowPast?: boolean;
  businessHours?: boolean;
  timezone?: string;
}

/**
 * Time range options
 */
export interface ITimeRangeOptions {
  start: Date | string;
  end: Date | string;
  step?: number;
  unit?: 'milliseconds' | 'seconds' | 'minutes' | 'hours' | 'days' | 'weeks' | 'months' | 'years';
  inclusive?: boolean;
  businessDays?: boolean;
}

/**
 * Enterprise Time Utility Interface
 * Provides comprehensive time manipulation, formatting, and calculation capabilities
 */
export interface ITimeUtility {
  /**
   * Initialize the time utility with configuration
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

  // === TIME CREATION & PARSING ===

  /**
   * Create date from various input formats
   * @param input - Date input (string, number, Date object)
   * @param options - Creation options
   */
  create(input?: any, options?: {
    timezone?: string;
    locale?: string;
    format?: string;
  }): ITimeResult;

  /**
   * Parse date string with format detection
   * @param dateString - Date string to parse
   * @param options - Parsing options
   */
  parse(dateString: string, options?: {
    format?: string;
    timezone?: string;
    locale?: string;
    strict?: boolean;
  }): ITimeResult;

  /**
   * Get current date/time
   * @param options - Current time options
   */
  now(options?: {
    timezone?: string;
    format?: string;
    precision?: 'milliseconds' | 'seconds';
  }): ITimeResult;

  /**
   * Get UTC date/time
   * @param options - UTC options
   */
  utc(options?: {
    format?: string;
    precision?: 'milliseconds' | 'seconds';
  }): ITimeResult;

  // === TIME FORMATTING ===

  /**
   * Format date with various options
   * @param date - Date to format
   * @param options - Formatting options
   */
  format(date: Date | string, options?: ITimeFormatOptions): ITimeResult;

  /**
   * Format date as relative time (e.g., "2 hours ago")
   * @param date - Date to format
   * @param options - Relative formatting options
   */
  formatRelative(date: Date | string, options?: {
    baseDate?: Date | string;
    locale?: string;
    precision?: 'seconds' | 'minutes' | 'hours' | 'days' | 'weeks' | 'months' | 'years';
    includeSuffix?: boolean;
  }): ITimeResult;

  /**
   * Format date for display in different locales
   * @param date - Date to format
   * @param locale - Target locale
   * @param options - Locale formatting options
   */
  formatLocale(date: Date | string, locale: string, options?: {
    format?: 'short' | 'medium' | 'long' | 'full';
    timezone?: string;
    includeTime?: boolean;
  }): ITimeResult;

  /**
   * Format date as ISO string
   * @param date - Date to format
   * @param options - ISO formatting options
   */
  formatISO(date: Date | string, options?: {
    includeTime?: boolean;
    includeTimezone?: boolean;
    precision?: 'milliseconds' | 'seconds';
  }): ITimeResult;

  // === TIME CALCULATIONS ===

  /**
   * Add time to date
   * @param date - Base date
   * @param amount - Amount to add
   * @param options - Addition options
   */
  add(date: Date | string, amount: number, options?: ITimeCalculationOptions): ITimeResult;

  /**
   * Subtract time from date
   * @param date - Base date
   * @param amount - Amount to subtract
   * @param options - Subtraction options
   */
  subtract(date: Date | string, amount: number, options?: ITimeCalculationOptions): ITimeResult;

  /**
   * Calculate difference between dates
   * @param date1 - First date
   * @param date2 - Second date
   * @param options - Difference calculation options
   */
  difference(date1: Date | string, date2: Date | string, options?: ITimeCalculationOptions): ITimeResult;

  /**
   * Calculate age from birth date
   * @param birthDate - Birth date
   * @param options - Age calculation options
   */
  age(birthDate: Date | string, options?: {
    currentDate?: Date | string;
    precision?: 'years' | 'months' | 'days';
    includeTime?: boolean;
  }): ITimeResult;

  // === TIME VALIDATION ===

  /**
   * Validate date format and value
   * @param date - Date to validate
   * @param options - Validation options
   */
  validate(date: any, options?: ITimeValidationOptions): {
    isValid: boolean;
    errors: string[];
    warnings: string[];
    normalizedDate?: Date;
  };

  /**
   * Check if date is valid
   * @param date - Date to check
   */
  isValid(date: any): boolean;

  /**
   * Check if date is in the past
   * @param date - Date to check
   * @param options - Past check options
   */
  isPast(date: Date | string, options?: {
    includeToday?: boolean;
    timezone?: string;
  }): boolean;

  /**
   * Check if date is in the future
   * @param date - Date to check
   * @param options - Future check options
   */
  isFuture(date: Date | string, options?: {
    includeToday?: boolean;
    timezone?: string;
  }): boolean;

  /**
   * Check if date is today
   * @param date - Date to check
   * @param options - Today check options
   */
  isToday(date: Date | string, options?: {
    timezone?: string;
  }): boolean;

  /**
   * Check if date is weekend
   * @param date - Date to check
   * @param options - Weekend check options
   */
  isWeekend(date: Date | string, options?: {
    timezone?: string;
  }): boolean;

  /**
   * Check if date is business day
   * @param date - Date to check
   * @param options - Business day check options
   */
  isBusinessDay(date: Date | string, options?: {
    timezone?: string;
    excludeHolidays?: boolean;
  }): boolean;

  // === TIME COMPARISONS ===

  /**
   * Compare two dates
   * @param date1 - First date
   * @param date2 - Second date
   * @param options - Comparison options
   */
  compare(date1: Date | string, date2: Date | string, options?: {
    precision?: 'milliseconds' | 'seconds' | 'minutes' | 'hours' | 'days';
    timezone?: string;
  }): number;

  /**
   * Check if date is between two dates
   * @param date - Date to check
   * @param start - Start date
   * @param end - End date
   * @param options - Between check options
   */
  isBetween(date: Date | string, start: Date | string, end: Date | string, options?: {
    inclusive?: boolean;
    timezone?: string;
  }): boolean;

  /**
   * Get minimum date from array
   * @param dates - Array of dates
   * @param options - Min calculation options
   */
  min(dates: (Date | string)[], options?: {
    timezone?: string;
  }): ITimeResult;

  /**
   * Get maximum date from array
   * @param dates - Array of dates
   * @param options - Max calculation options
   */
  max(dates: (Date | string)[], options?: {
    timezone?: string;
  }): ITimeResult;

  // === TIME RANGES ===

  /**
   * Generate date range
   * @param options - Range generation options
   */
  range(options: ITimeRangeOptions): ITimeResult;

  /**
   * Get start of time period
   * @param date - Base date
   * @param period - Time period
   * @param options - Start calculation options
   */
  startOf(date: Date | string, period: 'year' | 'month' | 'week' | 'day' | 'hour' | 'minute' | 'second', options?: {
    timezone?: string;
  }): ITimeResult;

  /**
   * Get end of time period
   * @param date - Base date
   * @param period - Time period
   * @param options - End calculation options
   */
  endOf(date: Date | string, period: 'year' | 'month' | 'week' | 'day' | 'hour' | 'minute' | 'second', options?: {
    timezone?: string;
  }): ITimeResult;

  /**
   * Get business days in range
   * @param start - Start date
   * @param end - End date
   * @param options - Business days options
   */
  businessDays(start: Date | string, end: Date | string, options?: {
    timezone?: string;
    excludeHolidays?: boolean;
    includeStart?: boolean;
    includeEnd?: boolean;
  }): ITimeResult;

  // === TIME CONVERSIONS ===

  /**
   * Convert timezone
   * @param date - Date to convert
   * @param fromTimezone - Source timezone
   * @param toTimezone - Target timezone
   * @param options - Conversion options
   */
  convertTimezone(date: Date | string, fromTimezone: string, toTimezone: string, options?: {
    format?: string;
  }): ITimeResult;

  /**
   * Convert to timestamp
   * @param date - Date to convert
   * @param options - Timestamp options
   */
  toTimestamp(date: Date | string, options?: {
    unit?: 'milliseconds' | 'seconds';
    timezone?: string;
  }): ITimeResult;

  /**
   * Convert from timestamp
   * @param timestamp - Timestamp to convert
   * @param options - Conversion options
   */
  fromTimestamp(timestamp: number, options?: {
    unit?: 'milliseconds' | 'seconds';
    timezone?: string;
  }): ITimeResult;

  // === TIME UTILITIES ===

  /**
   * Get timezone information
   * @param timezone - Timezone identifier
   * @param options - Timezone options
   */
  getTimezoneInfo(timezone: string, options?: {
    date?: Date | string;
  }): {
    name: string;
    offset: number;
    abbreviation: string;
    isDST: boolean;
  };

  /**
   * Get available timezones
   * @param options - Timezone list options
   */
  getTimezones(options?: {
    includeAbbreviations?: boolean;
    groupByRegion?: boolean;
  }): string[] | Record<string, string[]>;

  /**
   * Get business hours for date
   * @param date - Date to check
   * @param options - Business hours options
   */
  getBusinessHours(date: Date | string, options?: {
    timezone?: string;
    customHours?: {
      start: string;
      end: string;
    };
  }): {
    isBusinessHours: boolean;
    start: Date;
    end: Date;
    nextStart?: Date;
    nextEnd?: Date;
  };

  /**
   * Calculate working time between dates
   * @param start - Start date
   * @param end - End date
   * @param options - Working time options
   */
  workingTime(start: Date | string, end: Date | string, options?: {
    timezone?: string;
    businessHours?: {
      start: string;
      end: string;
    };
    excludeWeekends?: boolean;
    excludeHolidays?: boolean;
  }): ITimeResult;

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
}