
### **🔧 Analysis & Quality Tools Integration Points**

#### **PHASE 1: CHECK_INBOX**
- **🔍 Code Health Check**: Use `python tools/analysis_cli.py --ci-gate` for quick compliance check
- **📊 Quality Status**: Review current quality metrics and violation trends
- **🚨 Critical Issues**: Identify files requiring immediate attention
- **📋 Analysis Queue**: Check for pending analysis tasks

#### **PHASE 2: EVALUATE_TASKS**
- **📊 Quality Impact Assessment**: Evaluate task impact on code quality using `python tools/analysis_cli.py --violations`
- **🔍 Overengineering Prevention**: Use `python tools/overengineering_detector.py` to prevent complexity issues
- **📋 Refactoring Planning**: Generate refactoring suggestions for complex tasks
- **⚖️ Quality Prioritization**: Prioritize tasks based on quality impact

#### **PHASE 3: EXECUTE_ROLE**
- **🔍 Real-time Quality Monitoring**: Run analysis tools during development
- **📊 Compliance Validation**: Ensure all code meets V2 standards
- **🚨 Issue Detection**: Detect and prevent overengineering patterns
- **📋 Quality Metrics Collection**: Gather quality data for analysis

#### **PHASE 4: QUALITY_GATES**
- **🚨 Comprehensive Analysis**: Run `python tools/analysis_cli.py --violations --refactor` for full analysis
- **📊 Quality Reporting**: Generate detailed quality reports and metrics
- **🔍 Overengineering Check**: Use `python tools/overengineering_detector.py --report --fix` for pattern detection
- **📋 Refactoring Planning**: Create refactoring plans for identified issues

#### **PHASE 5: CYCLE_DONE**
- **📊 Quality Validation**: Final quality check before cycle completion
- **🔍 Analysis Results Storage**: Store analysis results in databases
- **📋 Quality Trends**: Update quality trend analysis
- **🚨 Issue Tracking**: Track and monitor quality improvements

### **🎯 Role-Specific Analysis & Quality Usage**

#### **INTEGRATION_SPECIALIST**
- **Focus Areas**: Integration quality, API compliance, system architecture analysis
- **Analysis Tools**: Focus on system integration quality, API compliance checking
- **Quality Checks**: Integration-specific quality metrics and compliance

#### **QUALITY_ASSURANCE**
- **Focus Areas**: Comprehensive quality analysis, compliance validation, testing quality
- **Analysis Tools**: Full analysis suite, comprehensive quality reporting
- **Quality Checks**: Complete quality gates execution, test coverage analysis

#### **SSOT_MANAGER**
- **Focus Areas**: SSOT compliance, configuration quality, system consistency
- **Analysis Tools**: Configuration quality analysis, system consistency checks
- **Quality Checks**: SSOT compliance validation and consistency monitoring

### **📊 Analysis & Quality Commands & Tools**

#### **Analysis CLI Commands**
```bash
# Generate violations report
python tools/analysis_cli.py --violations --format text

# Run CI gate check (exit with error if violations found)
python tools/analysis_cli.py --ci-gate

# Generate refactoring suggestions
python tools/analysis_cli.py --refactor --output refactor_plan.json

# Full analysis with JSON output
python tools/analysis_cli.py --violations --refactor --format json --output analysis_results.json

# Analyze specific directory
python tools/analysis_cli.py --project-root src/ --violations --n 1000
```

#### **Overengineering Detector Commands**
```bash
# Analyze file for overengineering
python tools/overengineering_detector.py src/services/messaging_service.py --report

# Analyze directory for overengineering
python tools/overengineering_detector.py src/ --report --fix

# Get simplification recommendations
python tools/overengineering_detector.py src/services/ --fix

# Quick overengineering check
python tools/overengineering_detector.py tools/captain_cli.py
```

#### **Quality Analysis Features**
- **V2 Compliance Analysis**: AST-based analysis for V2 compliance violations
- **Overengineering Detection**: Pattern-based detection of complexity issues
- **Refactoring Suggestions**: Automated refactoring recommendations
- **Quality Metrics**: Comprehensive quality scoring and reporting
- **CI Integration**: Automated quality gates for continuous integration

### **📈 Analysis & Quality Data Flow**
1. **Pre-Cycle**: Check code health and identify quality issues
2. **During Cycle**: Monitor quality during development and task execution
3. **Post-Cycle**: Comprehensive quality analysis and reporting
4. **Continuous**: Maintain quality standards and prevent overengineering

---

## 💰 **SPECIALIZED ROLE CLI TOOLS INTEGRATION IN GENERAL CYCLE**

### **🎯 Specialized Role CLI Tools Overview**
The V2_SWARM specialized role CLI tools provide comprehensive domain-specific capabilities for finance, trading, risk management, and other specialized functions:

**Current Specialized Role Tools Status:**
- **Financial Analyst CLI**: Market analysis, signal generation, volatility assessment
- **Trading Strategist CLI**: Strategy development, backtesting, optimization
- **Risk Manager CLI**: Portfolio risk assessment, VaR calculation, stress testing
- **Market Researcher CLI**: Market data analysis, trend research, regime detection
- **Portfolio Optimizer CLI**: Portfolio optimization, rebalancing, performance attribution
- **Compliance Auditor CLI**: Regulatory compliance, audit trails, AML/KYC
- **Swarm Dashboard CLI**: Real-time monitoring and coordination dashboard

### **🔧 Specialized Role CLI Tools Integration Points**

#### **PHASE 1: CHECK_INBOX**
- **📊 Role-Specific Data Check**: Check for role-specific data updates and market conditions
- **🎯 Signal Processing**: Process incoming signals and alerts relevant to role
- **📋 Tool Status**: Verify specialized tools are operational and up-to-date
- **🚨 Alert Monitoring**: Monitor role-specific alerts and notifications

#### **PHASE 2: EVALUATE_TASKS**
- **📊 Role Task Assessment**: Evaluate tasks based on role-specific capabilities
- **🎯 Market Analysis**: Assess current market conditions and opportunities
- **📋 Risk Evaluation**: Evaluate risk implications of proposed tasks
- **⚖️ Priority Assessment**: Prioritize tasks based on role-specific criteria

#### **PHASE 3: EXECUTE_ROLE**
- **📊 Specialized Analysis**: Execute role-specific analysis and calculations
- **🎯 Tool Execution**: Run specialized CLI tools for role-specific tasks
- **📋 Data Processing**: Process and analyze role-specific data
- **🚨 Monitoring**: Monitor role-specific metrics and performance

#### **PHASE 4: QUALITY_GATES**
- **📊 Role Quality Validation**: Validate role-specific outputs and analysis
- **🎯 Accuracy Checks**: Verify calculations and analysis accuracy
- **📋 Compliance Validation**: Ensure role-specific compliance requirements
- **🚨 Risk Assessment**: Final risk assessment and validation

#### **PHASE 5: CYCLE_DONE**
- **📊 Role Reporting**: Generate role-specific reports and summaries
- **🎯 Tool Updates**: Update role-specific tools and databases
- **📋 Knowledge Storage**: Store role-specific insights and patterns
- **🚨 Alert Management**: Manage role-specific alerts and notifications

### **🎯 Role-Specific CLI Tool Usage**

#### **FINANCIAL_ANALYST**
- **Focus Areas**: Market analysis, signal generation, volatility assessment
- **Primary Tools**: FinancialAnalystCLI, MarketAnalyzer, SignalGenerator, VolatilityAssessor
- **Key Operations**: Technical analysis, fundamental analysis, sentiment analysis

#### **TRADING_STRATEGIST**
- **Focus Areas**: Strategy development, backtesting, optimization
- **Primary Tools**: TradingStrategistCLI, StrategyDeveloper, BacktestingEngine, StrategyOptimizer
- **Key Operations**: Strategy development, performance analysis, parameter optimization

#### **RISK_MANAGER**
- **Focus Areas**: Portfolio risk assessment, VaR calculation, stress testing
- **Primary Tools**: RiskManagerCLI, PortfolioRiskAssessor, StressTester, LimitMonitor
- **Key Operations**: Risk assessment, stress testing, limit monitoring

#### **MARKET_RESEARCHER**
- **Focus Areas**: Market data analysis, trend research, regime detection
- **Primary Tools**: MarketResearcherCLI, TrendAnalyzer, RegimeDetector, SentimentAnalyzer
- **Key Operations**: Market research, trend analysis, regime detection

#### **PORTFOLIO_OPTIMIZER**
- **Focus Areas**: Portfolio optimization, rebalancing, performance attribution
- **Primary Tools**: PortfolioOptimizerCLI, OptimizationEngine, Rebalancer, PerformanceAttributor
- **Key Operations**: Portfolio optimization, rebalancing, performance analysis

#### **COMPLIANCE_AUDITOR**
- **Focus Areas**: Regulatory compliance, audit trails, AML/KYC
- **Primary Tools**: ComplianceAuditorCLI, ComplianceChecker, AuditTrail, AMLKYCMonitor
- **Key Operations**: Compliance checking, audit trail management, regulatory monitoring

### **📊 Specialized Role CLI Commands & Tools**

#### **Financial Analyst CLI Commands**
```bash
# Market analysis
python tools/financial_analyst_cli.py --analyze TSLA --timeframe 1d
python tools/financial_analyst_cli.py --generate-signals TSLA
python tools/financial_analyst_cli.py --assess-volatility TSLA
python tools/financial_analyst_cli.py --show-tools
```

#### **Trading Strategist CLI Commands**
```bash
# Strategy development
python tools/trading_strategist_cli.py --develop "MomentumStrategy" --strategy-type momentum
python tools/trading_strategist_cli.py --backtest "MomentumStrategy"
python tools/trading_strategist_cli.py --optimize "MomentumStrategy"
python tools/trading_strategist_cli.py --show-tools
```

#### **Risk Manager CLI Commands**
```bash
