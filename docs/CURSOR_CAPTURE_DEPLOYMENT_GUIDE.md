# 🛰️ Cursor Response Capture System - Deployment Guide

## 🎯 Overview

The Cursor Response Capture System provides a reliable pipeline to capture **assistant responses** directly from Cursor's internal database (IndexedDB) and store them into a **normalized SQLite database**. This gives agents continuous access to every conversation message for replay, audit, and downstream orchestration.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Cursor IDE    │    │   CDP Bridge     │    │   SQLite DB     │
│                 │    │   (Python)       │    │                 │
│ --remote-debug  │◄──►│   • WebSocket    │───►│ • Threads       │
│   port=9222     │    │   • IndexedDB    │    │ • Messages      │
│                 │    │   • Normalize    │    │ • Indexes       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   V2 Systems     │
                       │   • Performance  │
                       │   • Health       │
                       │   • Error        │
                       └──────────────────┘
```

## 📋 Prerequisites

### 1. **System Requirements**
- Python 3.7+ (3.8+ recommended)
- Cursor IDE installed
- Network access to localhost:9222
- 100MB+ free disk space for message storage

### 2. **Python Dependencies**
```bash
# Install core dependencies
pip install websocket-client requests

# Install optional enhancements
pip install sqlite-utils better-profanity colorlog psutil watchdog zstandard

# Or install all at once
pip install -r requirements_cursor_capture.txt
```

### 3. **Cursor Configuration**
Cursor must be launched with Chrome DevTools Protocol (CDP) enabled:

```bash
# Windows
Cursor.exe --remote-debugging-port=9222

# macOS
Cursor --remote-debugging-port=9222

# Linux
Cursor --remote-debugging-port=9222
```

## 🚀 Quick Start

### 1. **Launch Cursor with CDP**
```bash
# Close any existing Cursor instances
# Launch with CDP enabled
Cursor --remote-debugging-port=9222
```

### 2. **Verify CDP is Working**
Open a new browser tab and navigate to:
```
http://localhost:9222/json
```

You should see a JSON response with tab information.

### 3. **Run Capture System**
```bash
# Single capture run
python src/core/cursor_response_capture.py --once

# Continuous capture (5-minute intervals)
python src/core/cursor_response_capture.py

# Custom configuration
python src/core/cursor_response_capture.py --cdp-port 9222 --interval 300 --db-path custom/path.db
```

### 4. **Verify Capture**
```bash
# Check database contents
sqlite3 runtime/cursor_capture/cursor_threads.db "SELECT COUNT(*) FROM messages;"

# View recent messages
sqlite3 runtime/cursor_capture/cursor_threads.db "SELECT role, substr(content,1,50) FROM messages ORDER BY created_at DESC LIMIT 5;"
```

## ⚙️ Configuration Options

### **Command Line Arguments**
```bash
python src/core/cursor_response_capture.py [OPTIONS]

Options:
  --cdp-port INT     CDP port for cursor (default: 9222)
  --interval INT     Capture interval in seconds (default: 300)
  --once            Run capture once and exit
  --db-path PATH    Database file path (default: runtime/cursor_capture/cursor_threads.db)
  --help            Show help message
```

### **Environment Variables**
```bash
# Set CDP port
export CURSOR_CDP_PORT=9222

# Set capture interval
export CURSOR_CAPTURE_INTERVAL=300

# Set database path
export CURSOR_DB_PATH=runtime/cursor_capture/cursor_threads.db
```

## 🔧 Production Deployment

### 1. **Service Configuration (Linux/macOS)**
Create systemd service file `/etc/systemd/system/cursor-capture.service`:

```ini
[Unit]
Description=Cursor Response Capture System
After=network.target

[Service]
Type=simple
User=cursor-capture
WorkingDirectory=/opt/cursor-capture
ExecStart=/usr/bin/python3 src/core/cursor_response_capture.py
Restart=always
RestartSec=10
Environment=CURSOR_CDP_PORT=9222
Environment=CURSOR_CAPTURE_INTERVAL=300

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable cursor-capture
sudo systemctl start cursor-capture
sudo systemctl status cursor-capture
```

### 2. **Windows Task Scheduler**
Create a scheduled task that runs every 5 minutes:

```xml
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <TimeTrigger>
      <Repetition>
        <Interval>PT5M</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <StartBoundary>2024-01-01T00:00:00</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>python</Command>
      <Arguments>src\core\cursor_response_capture.py --once</Arguments>
      <WorkingDirectory>C:\path\to\cursor-capture</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
```

### 3. **Docker Deployment**
Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements_cursor_capture.txt .
RUN pip install -r requirements_cursor_capture.txt

# Copy source code
COPY src/ ./src/

# Create runtime directory
RUN mkdir -p runtime/cursor_capture

# Run capture system
CMD ["python", "src/core/cursor_response_capture.py"]
```

**Build and run:**
```bash
docker build -t cursor-capture .
docker run -d --name cursor-capture \
  -v /path/to/cursor-data:/app/runtime/cursor_capture \
  --network host \
  cursor-capture
```

## 📊 Monitoring and Maintenance

### 1. **Health Checks**
```bash
# Check service status
systemctl status cursor-capture

# View logs
journalctl -u cursor-capture -f

# Check database health
sqlite3 runtime/cursor_capture/cursor_threads.db "PRAGMA integrity_check;"
```

### 2. **Performance Monitoring**
The system integrates with V2 performance monitoring:

```python
from src.core.cursor_response_capture import CursorResponseCapture

capture_system = CursorResponseCapture()
stats = capture_system.get_capture_stats()

print(f"Messages captured: {stats['total_messages_captured']}")
print(f"Average capture time: {stats['average_capture_time']:.2f}s")
print(f"Error count: {sum(stats['error_counts'].values())}")
```

### 3. **Database Maintenance**
```sql
-- Check database size
SELECT page_count * page_size as size_bytes
FROM pragma_page_count(), pragma_page_size();

-- Analyze table performance
ANALYZE;

-- Reindex for optimal performance
REINDEX;

-- Clean up old messages (optional)
DELETE FROM messages WHERE created_at < strftime('%s', 'now', '-30 days') * 1000;
```

## 🚨 Troubleshooting

### **Common Issues**

#### 1. **CDP Connection Failed**
```
Error: Cursor CDP not available
```
**Solutions:**
- Ensure Cursor is launched with `--remote-debugging-port=9222`
- Check if port 9222 is available: `netstat -an | grep 9222`
- Restart Cursor with CDP enabled

#### 2. **No Chat Tabs Found**
```
Warning: No chat tabs found. Open a conversation in Cursor.
```
**Solutions:**
- Open a chat conversation in Cursor
- Wait for tab to fully load
- Check if tab URL contains chat indicators

#### 3. **Database Permission Errors**
```
Error: Failed to save message: [Errno 13] Permission denied
```
**Solutions:**
- Check directory permissions: `ls -la runtime/cursor_capture/`
- Ensure write access: `chmod 755 runtime/cursor_capture/`
- Run as appropriate user

#### 4. **High Memory Usage**
**Solutions:**
- Reduce capture interval
- Implement message archiving
- Monitor with V2 performance profiler

### **Debug Mode**
Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Security Considerations

### 1. **Network Security**
- CDP port (9222) should only be accessible locally
- Use firewall rules to restrict access
- Consider VPN for remote access

### 2. **Data Privacy**
- Encrypt sensitive message content
- Implement data retention policies
- Regular security audits

### 3. **Access Control**
- Restrict database access
- Implement user authentication
- Audit log access

## 📈 Scaling and Optimization

### 1. **High-Volume Scenarios**
- Implement message batching
- Use connection pooling
- Consider message queuing

### 2. **Performance Tuning**
- Optimize database indexes
- Implement message compression
- Use SSD storage for database

### 3. **Distributed Deployment**
- Multiple capture instances
- Load balancing
- Centralized monitoring

## 🔄 Updates and Maintenance

### 1. **Regular Updates**
```bash
# Update dependencies
pip install -r requirements_cursor_capture.txt --upgrade

# Update source code
git pull origin main

# Restart service
sudo systemctl restart cursor-capture
```

### 2. **Backup Strategy**
```bash
# Backup database
cp runtime/cursor_capture/cursor_threads.db backup/cursor_threads_$(date +%Y%m%d).db

# Backup configuration
cp config/cursor_capture.json backup/
```

### 3. **Monitoring Alerts**
Set up monitoring for:
- Service availability
- Database size
- Error rates
- Performance metrics

## 📞 Support and Resources

### **Documentation**
- [V2 Coding Standards](../V2_CODING_STANDARDS.md)
- [Performance Profiler](../src/core/performance_profiler.py)
- [Health Monitor](../src/core/health_monitor.py)

### **Testing**
```bash
# Run comprehensive tests
python test_cursor_capture.py

# Run specific test
python -m pytest test_cursor_capture.py::test_database_manager
```

### **Community**
- GitHub Issues
- Discord Community
- Documentation Wiki

---

## 🎯 Success Metrics

- **Reliability**: 99.9% uptime
- **Performance**: <100ms capture time
- **Accuracy**: 100% message capture rate
- **Scalability**: Handle 10,000+ messages/hour
- **Integration**: Seamless V2 system integration

---

**Ready to deploy?** Start with the Quick Start section and gradually move to production deployment as your needs grow.
