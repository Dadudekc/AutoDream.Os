import { layoutUtils } from './framework/layout.js';
import { events } from './framework/events.js';
import { components, initializeComponents } from './framework/components.js';
import { config, breakpoints } from './framework/config.js';

const ResponsiveFramework = {
    version: '1.0.0',
    breakpoints,
    components,
    events,
    utils: layoutUtils,
    config,
    init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                initializeComponents();
                events.trigger('framework.ready');
            });
        } else {
            initializeComponents();
            events.trigger('framework.ready');
        }
    }
};

window.ResponsiveFramework = ResponsiveFramework;
window.RF = ResponsiveFramework;

ResponsiveFramework.init();

export default ResponsiveFramework;
