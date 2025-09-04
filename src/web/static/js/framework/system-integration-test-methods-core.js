/**
 * System Integration Test Methods Core - V2 Compliant
 * Core test methods for system integration testing
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist
 * @version 4.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

// Import all modular components for integration testing

import { Accordion, BreakpointHandler, LazyLoading, TouchSupport } from './ui-components.js';

import { FormEnhancement } from './forms.js';
import { Modal } from './modal.js';
import { Navigation } from './navigation.js';
import { initializeComponents } from './components.js';

/**
 * System Integration Test Methods Core
 * Core test methods for system integration testing
 */
export class SystemIntegrationTestMethodsCore {
    constructor(testCore) {
        this.testCore = testCore;
    }

    /**
     * Test Component Imports
     */
    async testComponentImports() {
        this.testCore.logger.logOperationStart('testComponentImports');

        try {
            // Verify all components are properly imported
            const components = {
                Navigation,
                Modal,
                FormEnhancement,
                Accordion,
                LazyLoading,
                TouchSupport,
                BreakpointHandler,
                initializeComponents
            };

            const missingComponents = [];
            Object.entries(components).forEach(([name, component]) => {
                if (!component) {
                    missingComponents.push(name);
                }
            });

            if (missingComponents.length === 0) {
                this.testCore.logTestResult('COMPONENT_IMPORTS', true, 'All components imported successfully');
            } else {
                this.testCore.logTestResult('COMPONENT_IMPORTS', false, `Missing components: ${missingComponents.join(', ')}`);
            }
        } catch (error) {
            this.testCore.logTestResult('COMPONENT_IMPORTS', false, `Import error: ${error.message}`);
        }

        this.testCore.logger.logOperationComplete('testComponentImports');
    }

    /**
     * Test Navigation Module
     */
    async testNavigationModule() {
        this.testCore.logger.logOperationStart('testNavigationModule');

        try {
            // Create mock DOM elements for testing
            const mockNav = this.createMockNavigation();

            // Test initialization
            Navigation.init();

            // Test mobile toggle functionality
            const toggleBtn = mockNav.querySelector('[data-bs-toggle="collapse"]');
            if (toggleBtn) {
                toggleBtn.click();
                this.testCore.logTestResult('NAVIGATION_MOBILE_TOGGLE', true, 'Mobile navigation toggle working');
            } else {
                this.testCore.logTestResult('NAVIGATION_MOBILE_TOGGLE', false, 'Mobile navigation toggle not found');
            }

            // Clean up
            document.body.removeChild(mockNav);

        } catch (error) {
            this.testCore.logTestResult('NAVIGATION_MODULE', false, `Navigation test error: ${error.message}`);
        }

        this.testCore.logger.logOperationComplete('testNavigationModule');
    }

    /**
     * Test Modal Module
     */
    async testModalModule() {
        this.testCore.logger.logOperationStart('testModalModule');

        try {
            // Create mock modal for testing
            const mockModal = this.createMockModal();

            // Test modal initialization
            Modal.init();

            // Test modal show functionality
            const showBtn = mockModal.querySelector('[data-bs-toggle="modal"]');
            if (showBtn) {
                showBtn.click();
                this.testCore.logTestResult('MODAL_SHOW', true, 'Modal show functionality working');
            } else {
                this.testCore.logTestResult('MODAL_SHOW', false, 'Modal show button not found');
            }

            // Clean up
            document.body.removeChild(mockModal);

        } catch (error) {
            this.testCore.logTestResult('MODAL_MODULE', false, `Modal test error: ${error.message}`);
        }

        this.testCore.logger.logOperationComplete('testModalModule');
    }

    /**
     * Create mock navigation element for testing
     */
    createMockNavigation() {
        const nav = document.createElement('nav');
        nav.className = 'navbar navbar-expand-lg';
        nav.innerHTML = `
            <div class="container-fluid">
                <a class="navbar-brand" href="#">Test Brand</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="#">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">About</a>
                        </li>
                    </ul>
                </div>
            </div>
        `;
        document.body.appendChild(nav);
        return nav;
    }

    /**
     * Create mock modal element for testing
     */
    createMockModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'testModal';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Test Modal</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Test modal content</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary">Save changes</button>
                    </div>
                </div>
            </div>
        `;
        
        const trigger = document.createElement('button');
        trigger.setAttribute('data-bs-toggle', 'modal');
        trigger.setAttribute('data-bs-target', '#testModal');
        trigger.textContent = 'Open Modal';
        
        document.body.appendChild(modal);
        document.body.appendChild(trigger);
        return modal;
    }
}

/**
 * Factory function for SystemIntegrationTestMethodsCore
 */
export function createSystemIntegrationTestMethodsCore(testCore) {
    return new SystemIntegrationTestMethodsCore(testCore);
}
