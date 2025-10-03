# 🤖 **DYNAMIC ROLE ASSIGNMENT SYSTEM**

## **🎯 OPERATING ORDER v2.0 - DYNAMIC ROLES**

**"WE ARE SWARM"** operates with **dynamic role assignment** where Captain Agent-4 assigns roles per task, enabling flexible resource utilization and eliminating role bottlenecks.

## **🔄 Role Assignment Process**

1. **Captain Agent-4** assigns roles via direct PyAutoGUI messages
2. **Agents receive role assignments** and wake up immediately
3. **Agents load role-specific protocols** from configuration files
4. **Agents adapt behavior** based on assigned role
5. **Agents execute tasks** with role-specific protocols
6. **Agents send acknowledgments** back to Captain

## **📋 Available Role Categories**

### **Core Roles (Always Available)**
- **CAPTAIN**: Strategic oversight, emergency intervention, role assignment
- **SSOT_MANAGER**: Single source of truth validation and management
- **COORDINATOR**: Inter-agent coordination and communication

### **Technical Roles (Assigned Per Task)**
- **INTEGRATION_SPECIALIST**: System integration and interoperability
- **ARCHITECTURE_SPECIALIST**: System design and architectural decisions
- **INFRASTRUCTURE_SPECIALIST**: DevOps, deployment, monitoring
- **WEB_DEVELOPER**: Frontend/backend web development
- **DATA_ANALYST**: Data processing, analysis, reporting
- **QUALITY_ASSURANCE**: Testing, validation, compliance

### **Finance & Trading Roles (Assigned Per Task)**
- **FINANCIAL_ANALYST**: Market analysis, signal generation, volatility assessment
- **TRADING_STRATEGIST**: Strategy development, backtesting, optimization
- **RISK_MANAGER**: Portfolio risk assessment, VaR calculation, stress testing
- **MARKET_RESEARCHER**: Market data analysis, trend research, regime detection
- **PORTFOLIO_OPTIMIZER**: Portfolio optimization, rebalancing, performance attribution
- **COMPLIANCE_AUDITOR**: Regulatory compliance, audit trails, AML/KYC

### **Operational Roles (Assigned Per Task)**
- **TASK_EXECUTOR**: General task execution and implementation
- **RESEARCHER**: Investigation, analysis, documentation
- **TROUBLESHOOTER**: Problem diagnosis and resolution
- **OPTIMIZER**: Performance improvement and optimization

## **👥 Agent Capabilities Matrix**

| Agent | Available Roles | Primary Capabilities |
|-------|----------------|---------------------|
| Agent-1 | INTEGRATION_SPECIALIST, TASK_EXECUTOR, TROUBLESHOOTER, COORDINATOR | Integration, Core Systems |
| Agent-2 | ARCHITECTURE_SPECIALIST, RESEARCHER, OPTIMIZER, QUALITY_ASSURANCE | Architecture, Design |
| Agent-3 | INFRASTRUCTURE_SPECIALIST, TASK_EXECUTOR, TROUBLESHOOTER | Infrastructure, DevOps |
| Agent-5 | SSOT_MANAGER, COORDINATOR, DATA_ANALYST, BUSINESS_INTELLIGENCE | SSOT, System Integration, Business Intelligence |
| Agent-6 | COORDINATOR, COMMUNICATION_SPECIALIST, TASK_EXECUTOR | Communication, Coordination |
| Agent-7 | WEB_DEVELOPER, TASK_EXECUTOR, TRADING_STRATEGIST, PORTFOLIO_OPTIMIZER | Web Development, Trading |
| Agent-8 | INTEGRATION_SPECIALIST, RISK_MANAGER, COMPLIANCE_AUDITOR | System Integration, Risk Management |

## **🎯 Captain Agent-4 Authority**
- **Exclusive role assignment authority**
- **Dynamic role switching** based on task requirements
- **Emergency override capabilities**
- **System coordination and oversight**

## **Role Assignment Commands**
- **Assign role**: `python src/services/role_assignment/role_assignment_service.py --assign-role --agent [AGENT] --role [ROLE] --task "[TASK]" --duration "[DURATION]"`
- **List roles**: `python src/services/role_assignment/role_assignment_service.py --list-roles`
- **Check capabilities**: `python src/services/role_assignment/role_assignment_service.py --list-capabilities --agent [AGENT]`
- **Active assignments**: `python src/services/role_assignment/role_assignment_service.py --active-assignments`

🐝 **WE ARE SWARM** - Dynamic role assignment system operational!
