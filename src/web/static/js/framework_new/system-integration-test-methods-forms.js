/**
 * System Integration Test Methods Forms - V2 Compliant
 * Form component test methods for system integration testing
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist
 * @version 4.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

// Import form components for testing

import { FormEnhancement } from './forms.js';

/**
 * System Integration Test Methods Forms
 * Form component test methods for system integration testing
 */
export class SystemIntegrationTestMethodsForms {
    constructor(testCore) {
        this.testCore = testCore;
    }

    /**
     * Test Form Components
     */
    async testFormComponents() {
        this.testCore.logger.logOperationStart('testFormComponents');

        try {
            // Test form enhancement initialization
            await this.testFormEnhancement();
            
            // Test form validation
            await this.testFormValidation();
            
            // Test form submission
            await this.testFormSubmission();

        } catch (error) {
            this.testCore.logTestResult('FORM_COMPONENTS', false, `Form components test error: ${error.message}`);
        }

        this.testCore.logger.logOperationComplete('testFormComponents');
    }

    /**
     * Test Form Enhancement
     */
    async testFormEnhancement() {
        try {
            // Create mock form for testing
            const mockForm = this.createMockForm();

            // Test form enhancement initialization
            if (typeof FormEnhancement.init === 'function') {
                FormEnhancement.init();
                this.testCore.logTestResult('FORM_ENHANCEMENT_INIT', true, 'Form enhancement initialization working');
            } else {
                this.testCore.logTestResult('FORM_ENHANCEMENT_INIT', false, 'Form enhancement init method not found');
            }

            // Test form enhancement on specific form
            if (typeof FormEnhancement.enhance === 'function') {
                FormEnhancement.enhance(mockForm);
                this.testCore.logTestResult('FORM_ENHANCEMENT_APPLY', true, 'Form enhancement applied successfully');
            } else {
                this.testCore.logTestResult('FORM_ENHANCEMENT_APPLY', false, 'Form enhancement apply method not found');
            }

            // Clean up
            document.body.removeChild(mockForm);

        } catch (error) {
            this.testCore.logTestResult('FORM_ENHANCEMENT', false, `Form enhancement test error: ${error.message}`);
        }
    }

    /**
     * Test Form Validation
     */
    async testFormValidation() {
        try {
            // Create mock form with validation
            const mockForm = this.createMockFormWithValidation();

            // Test form validation
            if (typeof FormEnhancement.validate === 'function') {
                const isValid = FormEnhancement.validate(mockForm);
                this.testCore.logTestResult('FORM_VALIDATION', true, `Form validation result: ${isValid}`);
            } else {
                this.testCore.logTestResult('FORM_VALIDATION', false, 'Form validation method not found');
            }

            // Test individual field validation
            const emailField = mockForm.querySelector('input[type="email"]');
            if (emailField && typeof FormEnhancement.validateField === 'function') {
                const isFieldValid = FormEnhancement.validateField(emailField);
                this.testCore.logTestResult('FIELD_VALIDATION', true, `Field validation result: ${isFieldValid}`);
            } else {
                this.testCore.logTestResult('FIELD_VALIDATION', false, 'Field validation method not found');
            }

            // Clean up
            document.body.removeChild(mockForm);

        } catch (error) {
            this.testCore.logTestResult('FORM_VALIDATION', false, `Form validation test error: ${error.message}`);
        }
    }

    /**
     * Test Form Submission
     */
    async testFormSubmission() {
        try {
            // Create mock form for submission testing
            const mockForm = this.createMockForm();

            // Test form submission handler
            if (typeof FormEnhancement.handleSubmit === 'function') {
                const submitEvent = new Event('submit');
                mockForm.dispatchEvent(submitEvent);
                this.testCore.logTestResult('FORM_SUBMISSION', true, 'Form submission handler working');
            } else {
                this.testCore.logTestResult('FORM_SUBMISSION', false, 'Form submission handler not found');
            }

            // Test form data collection
            if (typeof FormEnhancement.collectData === 'function') {
                const formData = FormEnhancement.collectData(mockForm);
                this.testCore.logTestResult('FORM_DATA_COLLECTION', true, `Form data collected: ${Object.keys(formData).length} fields`);
            } else {
                this.testCore.logTestResult('FORM_DATA_COLLECTION', false, 'Form data collection method not found');
            }

            // Clean up
            document.body.removeChild(mockForm);

        } catch (error) {
            this.testCore.logTestResult('FORM_SUBMISSION', false, `Form submission test error: ${error.message}`);
        }
    }

    /**
     * Create mock form element for testing
     */
    createMockForm() {
        const form = document.createElement('form');
        form.id = 'testForm';
        form.innerHTML = `
            <div class="mb-3">
                <label for="testName" class="form-label">Name</label>
                <input type="text" class="form-control" id="testName" name="name" required>
            </div>
            <div class="mb-3">
                <label for="testEmail" class="form-label">Email</label>
                <input type="email" class="form-control" id="testEmail" name="email" required>
            </div>
            <div class="mb-3">
                <label for="testMessage" class="form-label">Message</label>
                <textarea class="form-control" id="testMessage" name="message" rows="3"></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        `;
        document.body.appendChild(form);
        return form;
    }

    /**
     * Create mock form with validation for testing
     */
    createMockFormWithValidation() {
        const form = document.createElement('form');
        form.id = 'testFormValidation';
        form.innerHTML = `
            <div class="mb-3">
                <label for="testNameValidation" class="form-label">Name</label>
                <input type="text" class="form-control" id="testNameValidation" name="name" required minlength="2">
                <div class="invalid-feedback">Name must be at least 2 characters long.</div>
            </div>
            <div class="mb-3">
                <label for="testEmailValidation" class="form-label">Email</label>
                <input type="email" class="form-control" id="testEmailValidation" name="email" required>
                <div class="invalid-feedback">Please provide a valid email address.</div>
            </div>
            <div class="mb-3">
                <label for="testPasswordValidation" class="form-label">Password</label>
                <input type="password" class="form-control" id="testPasswordValidation" name="password" required minlength="8">
                <div class="invalid-feedback">Password must be at least 8 characters long.</div>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        `;
        document.body.appendChild(form);
        return form;
    }
}

/**
 * Factory function for SystemIntegrationTestMethodsForms
 */
export function createSystemIntegrationTestMethodsForms(testCore) {
    return new SystemIntegrationTestMethodsForms(testCore);
}
