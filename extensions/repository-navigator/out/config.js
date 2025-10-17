"use strict";
/**
 * Repository Navigator Configuration
 * ====================================
 *
 * User-configurable options for the Repository Navigator extension.
 *
 * Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
 * Date: 2025-10-16
 * Task: VSCode Extension Enhancement (Task #2 from queue)
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.RepositoryNavigatorConfig = exports.DEFAULT_CONFIG = exports.ConfigKey = void 0;
exports.getConfig = getConfig;
const vscode = __importStar(require("vscode"));
/**
 * Configuration keys for the extension
 */
var ConfigKey;
(function (ConfigKey) {
    ConfigKey["AutoRefresh"] = "repositoryNavigator.autoRefresh";
    ConfigKey["RefreshInterval"] = "repositoryNavigator.refreshInterval";
    ConfigKey["ShowHealthStatus"] = "repositoryNavigator.showHealthStatus";
    ConfigKey["ExpandByDefault"] = "repositoryNavigator.expandByDefault";
    ConfigKey["EnableImportHelper"] = "repositoryNavigator.enableImportHelper";
    ConfigKey["MetadataPath"] = "repositoryNavigator.metadataPath";
})(ConfigKey || (exports.ConfigKey = ConfigKey = {}));
/**
 * Default configuration values
 */
exports.DEFAULT_CONFIG = {
    autoRefresh: true,
    refreshInterval: 30000, // 30 seconds
    showHealthStatus: true,
    expandByDefault: false,
    enableImportHelper: true,
    metadataPath: '.vscode/repo-integrations.json',
};
/**
 * Configuration manager for Repository Navigator
 */
class RepositoryNavigatorConfig {
    constructor() {
        this.config = vscode.workspace.getConfiguration();
    }
    /**
     * Get configuration value
     */
    get(key, defaultValue) {
        return this.config.get(key, defaultValue);
    }
    /**
     * Update configuration value
     */
    async update(key, value, target = vscode.ConfigurationTarget.Workspace) {
        await this.config.update(key, value, target);
    }
    /**
     * Get auto-refresh setting
     */
    getAutoRefresh() {
        return this.get(ConfigKey.AutoRefresh, exports.DEFAULT_CONFIG.autoRefresh);
    }
    /**
     * Get refresh interval (milliseconds)
     */
    getRefreshInterval() {
        return this.get(ConfigKey.RefreshInterval, exports.DEFAULT_CONFIG.refreshInterval);
    }
    /**
     * Get show health status setting
     */
    getShowHealthStatus() {
        return this.get(ConfigKey.ShowHealthStatus, exports.DEFAULT_CONFIG.showHealthStatus);
    }
    /**
     * Get expand by default setting
     */
    getExpandByDefault() {
        return this.get(ConfigKey.ExpandByDefault, exports.DEFAULT_CONFIG.expandByDefault);
    }
    /**
     * Get enable import helper setting
     */
    getEnableImportHelper() {
        return this.get(ConfigKey.EnableImportHelper, exports.DEFAULT_CONFIG.enableImportHelper);
    }
    /**
     * Get metadata file path
     */
    getMetadataPath() {
        return this.get(ConfigKey.MetadataPath, exports.DEFAULT_CONFIG.metadataPath);
    }
    /**
     * Reset all settings to defaults
     */
    async resetToDefaults() {
        for (const [key, value] of Object.entries(exports.DEFAULT_CONFIG)) {
            const configKey = `repositoryNavigator.${key}`;
            await this.update(configKey, value);
        }
    }
}
exports.RepositoryNavigatorConfig = RepositoryNavigatorConfig;
/**
 * Get configuration instance
 */
function getConfig() {
    return new RepositoryNavigatorConfig();
}
//# sourceMappingURL=config.js.map