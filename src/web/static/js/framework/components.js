// Import modular components for V2 compliance
import { Navigation } from './navigation.js';
import { Modal } from './modal.js';
import { FormEnhancement } from './forms.js';
import { Accordion, LazyLoading, TouchSupport, BreakpointHandler } from './ui-components.js';

export const components = {};

// Maintain backward compatibility by re-exporting components
components.Navigation = Navigation;

components.Modal = Modal;

components.Accordion = Accordion;

components.LazyLoading = LazyLoading;

components.TouchSupport = TouchSupport;

components.BreakpointHandler = BreakpointHandler;

components.FormEnhancement = FormEnhancement;

export function initializeComponents() {
    Object.keys(components).forEach(name => {
        const component = components[name];
        if (component && typeof component.init === 'function') {
            component.init();
        }
    });
}

