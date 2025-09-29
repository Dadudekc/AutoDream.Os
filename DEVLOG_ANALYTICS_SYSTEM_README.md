# 🤖 Devlog Analytics System

## Overview

The Devlog Analytics System provides comprehensive analytics, visualization, and real-time monitoring for the agent devlog system. It consists of three main components:

- **Analytics API** - REST endpoints for querying and analyzing devlog data
- **WebSocket Server** - Real-time updates for the dashboard
- **React Dashboard** - Web interface with charts and visualizations

## Features

### 📊 Analytics Dashboard
- **Visual representation** of devlog data with interactive charts
- **Agent activity tracking** with efficiency metrics and status monitoring
- **Trend analysis** showing daily activity patterns over time
- **Export capabilities** for JSON, CSV, and Excel formats
- **Real-time updates** via WebSocket connection

### 🔄 Real-time Updates
- **Live system metrics** (CPU, memory, disk usage)
- **Agent status monitoring** with current tasks and efficiency scores
- **Devlog activity feeds** with recent entries and trends
- **Connection health** monitoring with automatic reconnection

### 📈 Data Analysis
- **Status distribution** charts showing completion rates
- **Agent performance** comparisons and rankings
- **Time-series analysis** of devlog activity
- **Export functionality** for further analysis

## Quick Start

### Prerequisites

1. **Python 3.8+** with required packages:
   ```bash
   pip install flask flask-cors websockets
   ```

2. **Node.js 16+** for the React dashboard:
   ```bash
   cd web_dashboard
   npm install
   ```

### Running the System

1. **Start all services** with the startup script:
   ```bash
   python run_devlog_analytics_system.py
   ```

2. **Or start services individually**:

   **Analytics API** (port 8002):
   ```bash
   python src/services/devlog_analytics_api.py
   ```

   **WebSocket Server** (port 8001):
   ```bash
   python web_dashboard/websocket.py
   ```

   **React Dashboard** (port 3000):
   ```bash
   cd web_dashboard && npm start
   ```

3. **Open the dashboard**:
   ```
   http://localhost:3000
   ```

## Architecture

### System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React         │    │  WebSocket       │    │  Analytics      │
│   Dashboard     │◄──►│  Server          │    │  API            │
│   (Port 3000)   │    │  (Port 8001)     │    │  (Port 8002)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌──────────────────┐
                    │  Vector Database │
                    │  (agent_devlogs) │
                    └──────────────────┘
```

### Data Flow

1. **Devlogs** are stored in vector database with metadata
2. **Analytics API** queries database and provides REST endpoints
3. **WebSocket Server** provides real-time updates and live data
4. **React Dashboard** consumes both APIs for visualization
5. **Export functionality** allows data to be downloaded for analysis

## API Reference

### Analytics API Endpoints

#### Get Devlogs with Filtering
```http
GET /api/devlogs
```

**Parameters:**
- `agent_id` - Filter by specific agent
- `status` - Filter by status (completed, in_progress, failed)
- `limit` - Number of results (default: 50)
- `offset` - Pagination offset (default: 0)
- `date_from` - Start date filter (ISO format)
- `date_to` - End date filter (ISO format)

#### Get Analytics Data
```http
GET /api/devlogs/analytics
```

Returns comprehensive analytics including:
- Summary statistics (total devlogs, active agents)
- Status distribution
- Top performing agents
- Daily activity trends

#### Export Devlogs
```http
GET /api/devlogs/export/{format}
```

**Formats:** `json`, `csv`, `excel`

Downloads devlog data in specified format.

#### Get Agent Statistics
```http
GET /api/devlogs/agents
```

Returns list of all agents with devlog counts and roles.

#### Get Trend Data
```http
GET /api/devlogs/trends
```

**Parameters:**
- `days` - Number of days to analyze (default: 30)

Returns time-series data for trend analysis.

### WebSocket Messages

The WebSocket server sends real-time updates with the following message types:

#### System Metrics
```json
{
  "type": "system_metrics",
  "data": {
    "cpu_usage": 45,
    "memory_usage": 67,
    "disk_usage": 23,
    "active_connections": 5
  }
}
```

#### Live Logs
```json
{
  "type": "log",
  "data": {
    "timestamp": "2025-01-21T10:30:00Z",
    "level": "INFO",
    "message": "Dashboard update",
    "source": "websocket_server"
  }
}
```

#### Agent Status
```json
{
  "type": "agent_status",
  "data": [
    {
      "id": "Agent-4",
      "status": "ACTIVE",
      "current_task": "V3-COORDINATION-001",
      "efficiency": 9.8
    }
  ]
}
```

#### Devlog Summary
```json
{
  "type": "devlog_summary",
  "data": {
    "total_devlogs": 156,
    "today_devlogs": 12,
    "completion_rate": 87.5,
    "recent_activity": [...]
  }
}
```

## Configuration

### Environment Variables

The system uses the following environment variables:

```env
# Discord Bot (shared with devlog system)
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_main_channel_id

# Agent-specific Discord channels
DISCORD_CHANNEL_AGENT_1=agent_1_channel_id
DISCORD_CHANNEL_AGENT_2=agent_2_channel_id
# ... (Agent-3 through Agent-8)

# Vector Database
VECTOR_DB_URL=your_vector_database_url
VECTOR_DB_API_KEY=your_vector_database_key
```

### Vector Database Schema

Devlogs are stored with the following metadata structure:

```json
{
  "agent_id": "Agent-4",
  "action": "Enhanced Devlog System Implementation",
  "status": "completed",
  "details": "Successfully implemented enhanced agent devlog posting system...",
  "timestamp": "2025-01-21T19:08:22Z",
  "source": "agent_devlog_system",
  "type": "devlog"
}
```

## Dashboard Features

### Analytics Dashboard

The main dashboard provides:

- **Summary Cards** - Key metrics at a glance
- **Status Distribution** - Visual breakdown of devlog statuses
- **Agent Rankings** - Top performing agents by activity
- **Activity Trends** - Daily devlog patterns over time
- **Agent Overview** - Activity levels across all agents
- **Trend Analysis** - Detailed breakdown over time periods

### Real-time Monitoring

The monitoring panel shows:

- **System Health** - CPU, memory, disk usage with visual indicators
- **Agent Status** - Real-time status of all 8 agents
- **Devlog Activity** - Live summary of devlog statistics
- **Recent Activity** - Latest devlog entries and actions
- **Live Logs** - Streaming log output from all services

### Export Capabilities

Export devlog data in multiple formats:

- **JSON** - Complete data structure with all metadata
- **CSV** - Tabular format for spreadsheet analysis
- **Excel** - Formatted spreadsheet with multiple sheets

## Development

### Project Structure

```
├── src/services/devlog_analytics_api.py  # REST API endpoints
├── web_dashboard/
│   ├── DevlogAnalytics.jsx              # Analytics dashboard component
│   ├── DevlogAnalytics.css              # Dashboard styling
│   ├── RealTimeMonitoring.jsx           # Real-time monitoring component
│   ├── RealTimeMonitoring.css           # Monitoring styling
│   ├── websocket.py                     # WebSocket server
│   └── Dashboard.jsx                    # Main dashboard layout
├── run_devlog_analytics_system.py       # Startup script
└── DEVLOG_ANALYTICS_SYSTEM_README.md    # This file
```

### Adding New Features

1. **New API Endpoints** - Add to `devlog_analytics_api.py`
2. **Dashboard Components** - Create new JSX components in `web_dashboard/`
3. **Real-time Data** - Add new message types to WebSocket server
4. **Styling** - Add corresponding CSS files

### Testing

Run the system with sample data:

```bash
# Start the system
python run_devlog_analytics_system.py

# Test API endpoints
curl http://localhost:8002/api/devlogs/analytics
curl http://localhost:8002/api/devlogs/agents
curl http://localhost:8002/api/devlogs/export/json
```

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Check if WebSocket server is running on port 8001
   - Verify firewall settings allow WebSocket connections
   - Check browser console for connection errors

2. **API Not Responding**
   - Ensure Analytics API is running on port 8002
   - Check vector database connection
   - Verify environment variables are set correctly

3. **Dashboard Not Loading**
   - Install React dependencies: `cd web_dashboard && npm install`
   - Check if all services are running
   - Verify CORS settings allow dashboard access

4. **Export Not Working**
   - Check if vector database has data
   - Verify write permissions for downloads
   - Try different export formats

### Debug Commands

```bash
# Check service status
curl http://localhost:8002/api/devlogs/analytics
curl http://localhost:8001/health

# View WebSocket logs
tail -f /var/log/websocket_server.log

# Test database connection
python -c "from vector_database.vector_database_integration import VectorDatabaseIntegration; print('DB Connected')"

# Check React build
cd web_dashboard && npm run build
```

## Performance

### Optimization Tips

1. **Database Queries** - Use appropriate limits and filters
2. **Caching** - Implement Redis caching for frequently accessed data
3. **Connection Pooling** - Use database connection pooling
4. **Compression** - Enable gzip compression for API responses
5. **Load Balancing** - Deploy multiple instances behind a load balancer

### Monitoring

The system includes built-in monitoring:

- **Health checks** for all services
- **Performance metrics** in real-time dashboard
- **Error logging** with structured logs
- **Connection monitoring** with automatic reconnection

## Contributing

### Development Workflow

1. Create a feature branch
2. Implement the feature following existing patterns
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

### Code Standards

- **Python** - Follow PEP 8, use type hints
- **React** - Use functional components, hooks
- **CSS** - Use CSS modules or styled-components
- **API** - Follow REST principles, use JSON consistently

## License

This project is part of the Dream.OS agent system.

---

**Generated by**: Agent-4 (Quality Assurance Specialist - CAPTAIN)
**Date**: 2025-01-21
**Version**: 1.0
**Status**: Active and Operational ✅

🐝 **WE ARE SWARM** - Devlog Analytics System
