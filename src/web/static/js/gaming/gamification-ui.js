/**
 * Gamification UI - Dream.OS Integration
 * XP, Skills, Quests, and Achievement System
 * 
 * V2 Compliance: Modern, responsive gamification interface
 * Author: Agent-7 - Repository Cloning Specialist
 * Version: 1.0.0 - C-084 Implementation
 * License: MIT
 */

// ================================
// GAMIFICATION UI SYSTEM
// ================================

/**
 * Main Gamification UI Controller
 */
export class GamificationUI {
    constructor(options = {}) {
        this.container = options.container || document.getElementById('gamificationContainer');
        this.config = {
            enableAnimations: options.enableAnimations !== false,
            autoRefresh: options.autoRefresh !== false,
            refreshInterval: options.refreshInterval || 30000,
            theme: options.theme || 'dark'
        };
        
        this.state = {
            currentXP: 0,
            currentLevel: 1,
            totalXP: 0,
            skills: [],
            activeQuests: [],
            completedQuests: [],
            achievements: []
        };
        
        this.refreshTimer = null;
    }
    
    /**
     * Initialize the gamification UI
     */
    async initialize() {
        console.log('🎮 Initializing Gamification UI...');
        
        try {
            await this.loadPlayerData();
            this.renderUI();
            this.setupEventListeners();
            
            if (this.config.autoRefresh) {
                this.startAutoRefresh();
            }
            
            console.log('✅ Gamification UI initialized');
        } catch (error) {
            console.error('❌ Failed to initialize Gamification UI:', error);
            throw error;
        }
    }
    
    /**
     * Load player data from backend
     */
    async loadPlayerData() {
        try {
            const response = await fetch('/api/gaming/player/status');
            const data = await response.json();
            
            this.state.currentXP = data.current_xp || 0;
            this.state.currentLevel = data.level || 1;
            this.state.totalXP = data.total_xp || 0;
            this.state.skills = data.skills || [];
            this.state.activeQuests = data.active_quests || [];
            this.state.completedQuests = data.completed_quests || [];
            this.state.achievements = data.achievements || [];
            
        } catch (error) {
            console.warn('⚠️ Failed to load player data:', error);
        }
    }
    
    /**
     * Render complete UI
     */
    renderUI() {
        if (!this.container) return;
        
        this.container.innerHTML = `
            <div class="gamification-dashboard ${this.config.theme}">
                <div class="gamification-header">
                    <h2>🎮 Agent Progress</h2>
                </div>
                
                <div class="gamification-content">
                    ${this.renderXPSection()}
                    ${this.renderSkillsSection()}
                    ${this.renderQuestsSection()}
                    ${this.renderAchievementsSection()}
                </div>
            </div>
        `;
        
        if (this.config.enableAnimations) {
            this.addAnimations();
        }
    }
    
    /**
     * Render XP and Level section
     */
    renderXPSection() {
        const xpForNextLevel = this.calculateXPForNextLevel(this.state.currentLevel);
        const progress = (this.state.currentXP / xpForNextLevel) * 100;
        
        return `
            <div class="xp-section card">
                <div class="level-badge">
                    <span class="level-number">Level ${this.state.currentLevel}</span>
                </div>
                
                <div class="xp-info">
                    <div class="xp-text">
                        <span class="current-xp">${this.formatNumber(this.state.currentXP)}</span>
                        <span class="separator">/</span>
                        <span class="max-xp">${this.formatNumber(xpForNextLevel)}</span>
                        <span class="xp-label">XP</span>
                    </div>
                    
                    <div class="xp-bar-container">
                        <div class="xp-bar" style="width: ${progress}%">
                            <span class="xp-percentage">${Math.round(progress)}%</span>
                        </div>
                    </div>
                </div>
                
                <div class="total-xp">
                    Total XP: ${this.formatNumber(this.state.totalXP)}
                </div>
            </div>
        `;
    }
    
    /**
     * Render Skills section
     */
    renderSkillsSection() {
        const skillsHTML = this.state.skills.map(skill => `
            <div class="skill-item" data-skill="${skill.name}">
                <div class="skill-icon">${skill.icon || '⚡'}</div>
                <div class="skill-details">
                    <div class="skill-name">${skill.name}</div>
                    <div class="skill-level">Level ${skill.level}</div>
                    <div class="skill-progress-bar">
                        <div class="skill-progress" style="width: ${skill.progress}%"></div>
                    </div>
                </div>
                <div class="skill-points">+${skill.bonus}</div>
            </div>
        `).join('');
        
        return `
            <div class="skills-section card">
                <h3>⚡ Skills</h3>
                <div class="skills-grid">
                    ${skillsHTML || '<div class="no-skills">No skills unlocked yet</div>'}
                </div>
            </div>
        `;
    }
    
    /**
     * Render Quests section
     */
    renderQuestsSection() {
        const activeQuestsHTML = this.state.activeQuests.map(quest => `
            <div class="quest-item ${quest.priority}" data-quest-id="${quest.id}">
                <div class="quest-header">
                    <span class="quest-title">${quest.title}</span>
                    <span class="quest-reward">+${quest.xp_reward} XP</span>
                </div>
                <div class="quest-description">${quest.description}</div>
                <div class="quest-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${quest.progress}%"></div>
                    </div>
                    <span class="progress-text">${quest.progress}%</span>
                </div>
            </div>
        `).join('');
        
        return `
            <div class="quests-section card">
                <h3>📋 Active Quests</h3>
                <div class="quests-list">
                    ${activeQuestsHTML || '<div class="no-quests">No active quests</div>'}
                </div>
                <div class="completed-count">
                    ✅ Completed: ${this.state.completedQuests.length}
                </div>
            </div>
        `;
    }
    
    /**
     * Render Achievements section
     */
    renderAchievementsSection() {
        const achievementsHTML = this.state.achievements.slice(0, 5).map(achievement => `
            <div class="achievement-item ${achievement.unlocked ? 'unlocked' : 'locked'}">
                <div class="achievement-icon">${achievement.icon || '🏆'}</div>
                <div class="achievement-info">
                    <div class="achievement-name">${achievement.name}</div>
                    <div class="achievement-desc">${achievement.description}</div>
                </div>
            </div>
        `).join('');
        
        return `
            <div class="achievements-section card">
                <h3>🏆 Achievements</h3>
                <div class="achievements-grid">
                    ${achievementsHTML || '<div class="no-achievements">No achievements yet</div>'}
                </div>
                <div class="achievements-count">
                    ${this.state.achievements.filter(a => a.unlocked).length} / ${this.state.achievements.length}
                </div>
            </div>
        `;
    }
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Quest click handlers
        this.container.querySelectorAll('.quest-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const questId = e.currentTarget.dataset.questId;
                this.showQuestDetails(questId);
            });
        });
        
        // Skill hover handlers
        this.container.querySelectorAll('.skill-item').forEach(item => {
            item.addEventListener('mouseenter', (e) => {
                const skillName = e.currentTarget.dataset.skill;
                this.showSkillTooltip(skillName, e);
            });
        });
    }
    
    /**
     * Calculate XP required for next level
     */
    calculateXPForNextLevel(level) {
        // Formula: level * 100 + (level - 1) * 50
        return level * 100 + (level - 1) * 50;
    }
    
    /**
     * Format large numbers
     */
    formatNumber(num) {
        if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return num.toString();
    }
    
    /**
     * Add animations to elements
     */
    addAnimations() {
        this.container.querySelectorAll('.card').forEach((card, index) => {
            card.style.animation = `slideInUp 0.5s ease ${index * 0.1}s both`;
        });
        
        this.container.querySelectorAll('.xp-bar').forEach(bar => {
            bar.style.animation = 'fillProgress 1s ease-out';
        });
    }
    
    /**
     * Show quest details modal
     */
    showQuestDetails(questId) {
        const quest = this.state.activeQuests.find(q => q.id === questId);
        if (!quest) return;
        
        // Create modal overlay
        const modal = document.createElement('div');
        modal.className = 'quest-modal-overlay';
        modal.innerHTML = `
            <div class="quest-modal">
                <div class="quest-modal-header">
                    <h3>${quest.title}</h3>
                    <button class="quest-modal-close">&times;</button>
                </div>
                <div class="quest-modal-body">
                    <p class="quest-description">${quest.description}</p>
                    <div class="quest-progress">
                        <div class="quest-progress-bar" style="width: ${quest.progress}%"></div>
                    </div>
                    <p class="quest-progress-text">${quest.progress}% Complete</p>
                    <div class="quest-rewards">
                        <strong>Rewards:</strong> ${quest.rewards} XP
                    </div>
                </div>
            </div>
        `;
        
        // Add close handlers
        const closeBtn = modal.querySelector('.quest-modal-close');
        closeBtn.onclick = () => modal.remove();
        modal.onclick = (e) => { if (e.target === modal) modal.remove(); };
        
        document.body.appendChild(modal);
    }
    
    /**
     * Show skill tooltip
     */
    showSkillTooltip(skillName, event) {
        const skill = this.state.skills.find(s => s.name === skillName);
        if (!skill) return;
        
        // Remove existing tooltips
        const existing = document.querySelector('.skill-tooltip');
        if (existing) existing.remove();
        
        // Create tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'skill-tooltip';
        tooltip.innerHTML = `
            <div class="skill-tooltip-header">${skill.name}</div>
            <div class="skill-tooltip-body">
                <div class="skill-level">Level ${skill.level}</div>
                <div class="skill-xp">${skill.current_xp} / ${skill.required_xp} XP</div>
                <div class="skill-progress-bar">
                    <div class="skill-progress-fill" style="width: ${(skill.current_xp / skill.required_xp * 100)}%"></div>
                </div>
            </div>
        `;
        
        // Position near cursor
        tooltip.style.position = 'fixed';
        tooltip.style.left = `${event.clientX + 10}px`;
        tooltip.style.top = `${event.clientY + 10}px`;
        
        document.body.appendChild(tooltip);
        
        // Auto-remove after 3 seconds or on mouse leave
        setTimeout(() => tooltip.remove(), 3000);
        event.target.onmouseleave = () => tooltip.remove();
    }
    
    /**
     * Start auto-refresh timer
     */
    startAutoRefresh() {
        this.refreshTimer = setInterval(() => {
            this.refresh();
        }, this.config.refreshInterval);
    }
    
    /**
     * Refresh UI data
     */
    async refresh() {
        await this.loadPlayerData();
        this.renderUI();
        this.setupEventListeners();
    }
    
    /**
     * Cleanup
     */
    destroy() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
        if (this.container) {
            this.container.innerHTML = '';
        }
    }
}

// ================================
// FACTORY FUNCTION
// ================================

/**
 * Create gamification UI instance
 */
export function createGamificationUI(options) {
    return new GamificationUI(options);
}

// ================================
// INITIALIZATION
// ================================

/**
 * Initialize gamification UI on page load
 */
export async function initializeGamificationUI(containerId = 'gamificationContainer') {
    const container = document.getElementById(containerId);
    if (!container) {
        console.warn('⚠️ Gamification container not found');
        return null;
    }
    
    const ui = new GamificationUI({ container });
    await ui.initialize();
    return ui;
}



