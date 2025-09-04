/**
 * Navigation Configuration Manager - Navigation Setup Module
 * Manages navigation configuration and item definitions
 * V2 Compliance: Under 300-line limit achieved
 *
 * @author Agent-3 - Infrastructure & DevOps Specialist
 * @version 1.0.0 - V2 Compliance Navigation Config
 * @license MIT
 */

/**
 * Navigation configuration constants
 */
export const NAVIGATION_CONFIG = {
    defaultView: 'overview',
    navElementId: 'dashboardNav',
    contentElementId: 'dashboardContent',
    navigationClass: 'dashboard-navigation'
};

/**
 * Navigation items configuration
 */
export const NAVIGATION_ITEMS = new Map([
    ['overview', {
        label: 'Overview',
        icon: 'fas fa-home',
        view: 'overview',
        description: 'System overview and key metrics'
    }],
    ['agent_performance', {
        label: 'Agent Performance',
        icon: 'fas fa-users',
        view: 'agent_performance',
        description: 'Individual agent performance metrics'
    }],
    ['contract_status', {
        label: 'Contract Status',
        icon: 'fas fa-file-contract',
        view: 'contract_status',
        description: 'Active contracts and completion status'
    }],
    ['system_health', {
        label: 'System Health',
        icon: 'fas fa-heartbeat',
        view: 'system_health',
        description: 'System health and monitoring'
    }]
]);

/**
 * Get navigation configuration
 */
export function getNavigationConfig() {
    return { ...NAVIGATION_CONFIG };
}

/**
 * Get navigation items
 */
export function getNavigationItems() {
    return new Map(NAVIGATION_ITEMS);
}

/**
 * Get navigation item by key
 */
export function getNavigationItem(key) {
    return NAVIGATION_ITEMS.get(key);
}

/**
 * Get all navigation item keys
 */
export function getNavigationItemKeys() {
    return Array.from(NAVIGATION_ITEMS.keys());
}

/**
 * Get default view
 */
export function getDefaultView() {
    return NAVIGATION_CONFIG.defaultView;
}

/**
 * Get navigation element ID
 */
export function getNavigationElementId() {
    return NAVIGATION_CONFIG.navElementId;
}

/**
 * Get content element ID
 */
export function getContentElementId() {
    return NAVIGATION_CONFIG.contentElementId;
}

/**
 * Validate navigation item
 */
export function isValidNavigationItem(key) {
    return NAVIGATION_ITEMS.has(key);
}

