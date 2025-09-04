#!/usr/bin/env node

/**
 * V2 Compliance Test Script
 * Tests ESLint configuration with sample files
 */

import { execSync } from 'child_process';
import { writeFileSync, mkdirSync, rmSync } from 'fs';
import { join } from 'path';

console.log('🧪 Testing V2 Compliance ESLint Configuration...\n');

// Create test directory
const testDir = 'test-v2-compliance';
const testFile = join(testDir, 'test-file.js');

try {
  // Create test directory
  mkdirSync(testDir, { recursive: true });

  // Create a test file that should pass V2 compliance
  const compliantCode = `/**
 * V2 Compliant Test File
 * This file should pass all ESLint rules
 */

// Simple utility function (under 30 lines)
export function validateEmail(email) {
  if (!email) return false;
  if (typeof email !== 'string') return false;

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Another small function
export function formatUserName(firstName, lastName) {
  if (!firstName || !lastName) return '';

  return firstName.trim() + ' ' + lastName.trim();
}

// Simple class (single responsibility)
export class UserValidator {
  constructor() {
    this.errors = [];
  }

  validate(user) {
    this.errors = [];

    if (!user.email) {
      this.errors.push('Email is required');
    } else if (!validateEmail(user.email)) {
      this.errors.push('Invalid email format');
    }

    if (!user.name) {
      this.errors.push('Name is required');
    }

    return this.errors.length === 0;
  }

  getErrors() {
    return [...this.errors];
  }
}
`;

  writeFileSync(testFile, compliantCode);

  console.log('✅ Created V2 compliant test file');
  console.log('📊 Running ESLint on test file...\n');

  // Run ESLint on the test file
  const eslintCommand = 'npx eslint "' + testFile + '" --max-warnings 0';
  const result = execSync(eslintCommand, { encoding: 'utf8' });

  console.log('🎉 SUCCESS: Test file passed all V2 compliance checks!');
  console.log('📋 ESLint Output:', result || '(no output - all good)');

} catch (error) {
  console.log('❌ ESLint check failed:');
  console.log(error.stdout || error.message);
} finally {
  // Clean up test files
  try {
    rmSync(testDir, { recursive: true, force: true });
    console.log('\n🧹 Cleaned up test files');
  } catch (cleanupError) {
    console.log('⚠️  Could not clean up test files:', cleanupError.message);
  }
}

console.log('\n✨ V2 Compliance test completed!');
console.log('💡 To run full project check: npm run lint:v2');
console.log('📊 To check LOC distribution: npm run loc:check');
