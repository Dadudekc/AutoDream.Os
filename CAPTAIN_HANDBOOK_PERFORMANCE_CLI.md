# 📊 **CAPTAIN'S HANDBOOK - PERFORMANCE CLI COMMANDS**

## **Performance Monitoring & Optimization System**
**V2 Compliance**: < 400 lines, single responsibility for performance operations

**Author**: Agent-2 - Architecture & Design Specialist
**Last Updated**: 2025-09-09
**Status**: ACTIVE - Complete Performance CLI Documentation

---

## 🎯 **OVERVIEW**

The Performance CLI system provides comprehensive monitoring, optimization, and dashboard capabilities for the swarm system. All commands support JSON and text output formats with V2 compliance standards.

**Location**: `src/core/performance/performance_cli.py`
**Dependencies**: Performance monitoring system, optimization engine, dashboard system
**Output Formats**: JSON (`--format json`) or Text (default)

---

## 📈 **PERFORMANCE MONITORING COMMANDS**

### **1. Start Performance Monitoring**
```bash
python src/core/performance/performance_cli.py monitor start
```

**Description**: Initializes comprehensive performance monitoring across all system components.

**Parameters**:
- `--interval`: Monitoring interval in seconds (default: 60)
- `--duration`: Monitoring duration in minutes (default: continuous)
- `--format`: Output format (json/text)

**Example**:
```bash
# Start monitoring with 30-second intervals for 2 hours
python src/core/performance/performance_cli.py monitor start --interval 30 --duration 120 --format json
```

**Success Output**:
```
✅ Performance monitoring started successfully
📊 Monitoring ID: monitor_20250909_140000
⏱️ Interval: 30 seconds
📈 Metrics: CPU, Memory, Disk, Network, Response Time
```

### **2. Stop Performance Monitoring**
```bash
python src/core/performance/performance_cli.py monitor stop
```

**Description**: Gracefully stops all active performance monitoring processes.

**Parameters**:
- `--force`: Force stop all monitoring processes
- `--save-data`: Save collected data before stopping (default: true)

**Example**:
```bash
# Stop monitoring and save data
python src/core/performance/performance_cli.py monitor stop --save-data true
```

**Success Output**:
```
✅ Performance monitoring stopped successfully
💾 Data saved to: runtime/performance/metrics_20250909_140000.json
📊 Total metrics collected: 1,247 data points
```

### **3. Get Monitoring Status**
```bash
python src/core/performance/performance_cli.py monitor status
```

**Description**: Displays current monitoring status and active processes.

**Parameters**:
- `--detailed`: Show detailed process information
- `--format`: Output format (json/text)

**Example**:
```bash
# Get detailed monitoring status
python src/core/performance/performance_cli.py monitor status --detailed --format json
```

**Success Output**:
```json
{
  "monitoring_active": true,
  "active_processes": 3,
  "monitoring_id": "monitor_20250909_140000",
  "uptime": "2h 15m",
  "metrics_collected": 1247,
  "alerts_triggered": 2
}
```

### **4. Get Current Metrics**
```bash
python src/core/performance/performance_cli.py monitor metrics
```

**Description**: Retrieves current performance metrics from all monitored components.

**Parameters**:
- `--component`: Specific component to monitor (cpu/memory/disk/network/all)
- `--format`: Output format (json/text)
- `--real-time`: Show real-time metrics (default: true)

**Example**:
```bash
# Get CPU and memory metrics in real-time
python src/core/performance/performance_cli.py monitor metrics --component cpu,memory --real-time true
```

**Success Output**:
```
📊 Current Performance Metrics (2025-09-09 14:15:00)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CPU Usage:       45.2% (4 cores active)
Memory Usage:    2.1GB / 8GB (26.3%)
Disk I/O:        125 MB/s read, 89 MB/s write
Network I/O:     15.2 Mbps in, 8.7 Mbps out
Response Time:   145ms average
Active Threads:  23
```

---

## ⚡ **PERFORMANCE OPTIMIZATION COMMANDS**

### **5. Start Performance Optimization**
```bash
python src/core/performance/performance_cli.py optimize start
```

**Description**: Initiates automated performance optimization across all system components.

**Parameters**:
- `--target`: Optimization target (cpu/memory/disk/network/response/all)
- `--aggressive`: Use aggressive optimization mode
- `--backup`: Create backup before optimization (default: true)

**Example**:
```bash
# Start memory and response time optimization
python src/core/performance/performance_cli.py optimize start --target memory,response --aggressive false
```

**Success Output**:
```
🚀 Performance optimization started
🎯 Targets: Memory, Response Time
⚙️ Mode: Conservative
💾 Backup created: backup/pre_opt_20250909_140000/
📊 Optimization ID: opt_20250909_140000
```

### **6. Stop Performance Optimization**
```bash
python src/core/performance/performance_cli.py optimize stop
```

**Description**: Stops all active optimization processes and applies final optimizations.

**Parameters**:
- `--apply-changes`: Apply pending optimizations (default: true)
- `--rollback`: Rollback to pre-optimization state if issues detected

**Example**:
```bash
# Stop optimization and apply all changes
python src/core/performance/performance_cli.py optimize stop --apply-changes true
```

**Success Output**:
```
✅ Performance optimization completed successfully
📊 Optimizations Applied:
   • Memory usage reduced by 23%
   • Response time improved by 34%
   • CPU utilization optimized by 18%
💾 Changes applied and system stable
```

### **7. Get Optimization Status**
```bash
python src/core/performance/performance_cli.py optimize status
```

**Description**: Shows current optimization status and pending optimizations.

**Parameters**:
- `--detailed`: Show detailed optimization progress
- `--recommendations`: Include optimization recommendations

**Example**:
```bash
# Get detailed optimization status with recommendations
python src/core/performance/performance_cli.py optimize status --detailed --recommendations
```

**Success Output**:
```
⚡ Performance Optimization Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: ACTIVE
Progress: 67% complete
Current Target: Memory Optimization
Optimizations Applied: 12/15
Estimated Completion: 8 minutes

📋 Recommendations:
• Consider enabling aggressive mode for better results
• Memory optimization showing 23% improvement
• Network optimization pending - high impact potential
```

### **8. Get Optimization History**
```bash
python src/core/performance/performance_cli.py optimize history
```

**Description**: Displays historical optimization data and performance improvements.

**Parameters**:
- `--period`: Time period (day/week/month/all)
- `--format`: Output format (json/text)
- `--export`: Export data to file

**Example**:
```bash
# Get weekly optimization history
python src/core/performance/performance_cli.py optimize history --period week --format json --export results.json
```

**Success Output**:
```json
{
  "optimization_history": [
    {
      "date": "2025-09-09",
      "optimizations_applied": 15,
      "performance_improvements": {
        "cpu_reduction": "18%",
        "memory_reduction": "23%",
        "response_time_improvement": "34%"
      },
      "system_stability": "HIGH"
    }
  ],
  "total_optimizations": 45,
  "average_improvement": "25%"
}
```

---

## 📊 **PERFORMANCE DASHBOARD COMMANDS**

### **9. Get Dashboard Summary**
```bash
python src/core/performance/performance_cli.py dashboard summary
```

**Description**: Displays comprehensive performance dashboard summary.

**Parameters**:
- `--period`: Summary period (hour/day/week/month)
- `--detailed`: Include detailed breakdowns
- `--alerts`: Include active alerts

**Example**:
```bash
# Get daily dashboard summary with alerts
python src/core/performance/performance_cli.py dashboard summary --period day --alerts
```

**Success Output**:
```
📊 Performance Dashboard Summary (2025-09-09)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 Overall Performance: EXCELLENT (94/100)

Key Metrics:
• CPU Efficiency: 87%
• Memory Usage: 23%
• Response Time: 145ms
• System Uptime: 99.9%

🚨 Active Alerts: 1
• High memory usage detected in Agent-7 workspace
```

### **10. Get Performance Trends**
```bash
python src/core/performance/performance_cli.py dashboard trends
```

**Description**: Shows performance trends and historical data analysis.

**Parameters**:
- `--metric`: Specific metric to analyze (cpu/memory/response/all)
- `--period`: Analysis period (day/week/month)
- `--forecast`: Include performance forecasting

**Example**:
```bash
# Get response time trends with forecasting
python src/core/performance/performance_cli.py dashboard trends --metric response --period week --forecast
```

**Success Output**:
```
📈 Performance Trends Analysis (Response Time)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current: 145ms (▼ 12% from yesterday)
7-Day Trend: ▼ 23% improvement
Peak: 280ms (2025-09-08 14:30)
Low: 120ms (2025-09-09 09:15)

📊 Forecast (Next 24 hours):
• Expected: 130-150ms range
• Confidence: 89%
• Risk Level: LOW
```

### **11. Get Performance Alerts**
```bash
python src/core/performance/performance_cli.py dashboard alerts
```

**Description**: Displays active performance alerts and warnings.

**Parameters**:
- `--severity`: Alert severity filter (critical/high/medium/low/all)
- `--resolved`: Include resolved alerts
- `--actions`: Include recommended actions

**Example**:
```bash
# Get critical and high alerts with actions
python src/core/performance/performance_cli.py dashboard alerts --severity critical,high --actions
```

**Success Output**:
```
🚨 Active Performance Alerts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 CRITICAL (2 alerts)
• Agent-7 memory usage: 89% (Threshold: 80%)
  📋 Actions: Reduce concurrent processes, enable memory optimization
• Database response time: 450ms (Threshold: 200ms)
  📋 Actions: Optimize queries, check connection pool

🟡 HIGH (3 alerts)
• Network latency: 125ms (Threshold: 100ms)
  📋 Actions: Check network configuration, optimize routing
```

### **12. Export Performance Data**
```bash
python src/core/performance/performance_cli.py dashboard export
```

**Description**: Exports comprehensive performance data for analysis.

**Parameters**:
- `--format`: Export format (json/csv/excel)
- `--period`: Export period (day/week/month/all)
- `--destination`: Export destination path
- `--compress`: Compress exported data

**Example**:
```bash
# Export weekly performance data as compressed JSON
python src/core/performance/performance_cli.py dashboard export --format json --period week --compress --destination reports/
```

**Success Output**:
```
📤 Performance Data Export Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Format: JSON (compressed)
Period: Week (2025-09-02 to 2025-09-09)
Records: 8,459 data points
Size: 2.3MB (compressed: 456KB)
Location: reports/performance_export_20250909_140000.json.gz
```

---

## 🔧 **ADVANCED USAGE PATTERNS**

### **Performance Health Check Workflow**
```bash
# 1. Start monitoring
python src/core/performance/performance_cli.py monitor start --interval 30

# 2. Check current status
python src/core/performance/performance_cli.py monitor status --detailed

# 3. Get dashboard overview
python src/core/performance/performance_cli.py dashboard summary --alerts

# 4. Run optimization if needed
python src/core/performance/performance_cli.py optimize start --target all

# 5. Monitor optimization progress
python src/core/performance/performance_cli.py optimize status --detailed

# 6. Export final report
python src/core/performance/performance_cli.py dashboard export --format json --period day
```

### **Automated Performance Maintenance**
```bash
# Daily performance check script
python src/core/performance/performance_cli.py monitor start --interval 300 --duration 1440
python src/core/performance/performance_cli.py dashboard summary --period day > daily_report.txt
python src/core/performance/performance_cli.py optimize start --target memory,cpu
```

### **Emergency Performance Recovery**
```bash
# Emergency optimization workflow
python src/core/performance/performance_cli.py monitor stop --force
python src/core/performance/performance_cli.py optimize start --target all --aggressive
python src/core/performance/performance_cli.py dashboard alerts --severity critical
```

---

## ⚠️ **TROUBLESHOOTING**

### **Common Issues & Solutions**

**Issue**: Command fails with "Performance system not available"
**Solution**: Ensure performance monitoring system is properly initialized
```bash
# Check system status
python src/core/performance/performance_cli.py monitor status
```

**Issue**: Optimization commands have no effect
**Solution**: Verify optimization engine is running and has proper permissions
```bash
# Check optimization status
python src/core/performance/performance_cli.py optimize status --detailed
```

**Issue**: Dashboard shows incomplete data
**Solution**: Restart monitoring and check data collection
```bash
# Restart monitoring
python src/core/performance/performance_cli.py monitor stop --force
python src/core/performance/performance_cli.py monitor start
```

---

## 📋 **COMMAND QUICK REFERENCE**

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `monitor start` | Start performance monitoring | `--interval`, `--duration` |
| `monitor stop` | Stop performance monitoring | `--save-data`, `--force` |
| `monitor status` | Get monitoring status | `--detailed` |
| `monitor metrics` | Get current metrics | `--component`, `--real-time` |
| `optimize start` | Start performance optimization | `--target`, `--aggressive` |
| `optimize stop` | Stop performance optimization | `--apply-changes` |
| `optimize status` | Get optimization status | `--detailed`, `--recommendations` |
| `optimize history` | Get optimization history | `--period`, `--export` |
| `dashboard summary` | Get dashboard summary | `--period`, `--alerts` |
| `dashboard trends` | Get performance trends | `--metric`, `--forecast` |
| `dashboard alerts` | Get performance alerts | `--severity`, `--actions` |
| `dashboard export` | Export performance data | `--format`, `--compress` |

---

## 🎯 **INTEGRATION WITH SWARM OPERATIONS**

### **Captain's Performance Oversight**
- **Daily Monitoring**: Run dashboard summary daily
- **Weekly Optimization**: Execute full system optimization weekly
- **Alert Response**: Address critical alerts within 1 hour
- **Trend Analysis**: Review performance trends monthly

### **Agent Performance Integration**
- **Agent Check-ins**: Include performance metrics in status updates
- **Load Balancing**: Use performance data for task distribution
- **Resource Allocation**: Optimize based on performance monitoring
- **Health Checks**: Automated performance validation

---

**✅ PERFORMANCE CLI SYSTEM COMPLETE**
**8 Commands Documented | All Workflows Covered | V2 Compliant**

**Ready for swarm performance optimization!** 🚀⚡
