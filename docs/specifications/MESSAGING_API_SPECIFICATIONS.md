# 🔌 Messaging System API Specifications

**Detailed API Documentation for Enhanced Messaging Components**

---

## **📋 API OVERVIEW**

### **Base URL**
```
https://api.dream-os.swarm/messaging/v1
```

### **Authentication**
```
Authorization: Bearer <swarm-token>
X-Agent-ID: <agent-identifier>
```

### **Response Format**
```json
{
  "success": true|false,
  "data": {},
  "error": null|string,
  "timestamp": "2024-01-01T12:00:00.000Z",
  "request_id": "req_123456789",
  "version": "1.1"
}
```

---

## **⚙️ TIMING ENGINE API**

### **GET /timing/status**
Get current timing engine status and calibration data.

**Request:**
```http
GET /timing/status
Accept: application/json
```

**Response:**
```json
{
  "success": true,
  "data": {
    "calibration_status": "active",
    "last_calibration": "2024-01-01T10:30:00.000Z",
    "performance_metrics": {
      "cpu_speed": 3.2,
      "memory_available": 8192,
      "disk_speed": 450,
      "network_latency": 15
    },
    "adaptive_delays": {
      "typing_interval": 0.012,
      "gui_focus_delay": 0.45,
      "clipboard_paste_wait": 0.95,
      "tab_creation_wait": 1.1,
      "agent_inter_delay": 1.0
    },
    "accuracy_score": 0.98,
    "calibration_count": 5
  }
}
```

### **POST /timing/calibrate**
Trigger manual performance calibration.

**Request:**
```http
POST /timing/calibrate
Content-Type: application/json

{
  "force": false,
  "tests": ["cpu", "memory", "network", "gui"],
  "duration_seconds": 30
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "calibration_id": "cal_123456789",
    "status": "running",
    "estimated_completion": "2024-01-01T10:31:30.000Z",
    "progress": {
      "cpu_test": "completed",
      "memory_test": "running",
      "network_test": "pending",
      "gui_test": "pending"
    }
  }
}
```

### **GET /timing/calibration/{id}**
Get calibration results by ID.

**Response:**
```json
{
  "success": true,
  "data": {
    "calibration_id": "cal_123456789",
    "status": "completed",
    "start_time": "2024-01-01T10:30:00.000Z",
    "end_time": "2024-01-01T10:31:30.000Z",
    "results": {
      "cpu_benchmark": {
        "score": 2850,
        "category": "high_performance"
      },
      "memory_benchmark": {
        "available_mb": 8192,
        "speed_mbps": 24000
      },
      "network_benchmark": {
        "latency_ms": 12,
        "bandwidth_mbps": 950
      },
      "gui_benchmark": {
        "focus_time_ms": 450,
        "click_accuracy": 0.99,
        "typing_speed_cps": 85
      }
    },
    "recommended_delays": {
      "typing_interval": 0.012,
      "gui_focus_delay": 0.45,
      "clipboard_paste_wait": 0.95
    }
  }
}
```

---

## **🔄 RETRY & ERROR HANDLING API**

### **GET /retry/config**
Get current retry configuration.

**Response:**
```json
{
  "success": true,
  "data": {
    "max_retries": 3,
    "base_delay": 1.0,
    "backoff_multiplier": 2.0,
    "max_delay": 30.0,
    "retryable_errors": [
      "network_timeout",
      "gui_focus_lost",
      "clipboard_unavailable",
      "coordinate_invalid"
    ],
    "non_retryable_errors": [
      "authentication_failed",
      "permission_denied",
      "invalid_agent_id"
    ]
  }
}
```

### **POST /retry/config**
Update retry configuration.

**Request:**
```json
{
  "max_retries": 5,
  "base_delay": 0.5,
  "backoff_multiplier": 1.5,
  "custom_retryable_errors": ["custom_error_type"]
}
```

### **GET /retry/stats**
Get retry statistics and error patterns.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_attempts": 15420,
    "successful_deliveries": 15234,
    "failed_deliveries": 186,
    "retry_distribution": {
      "0_retries": 14234,
      "1_retry": 987,
      "2_retries": 145,
      "3_retries": 54
    },
    "error_types": {
      "network_timeout": 89,
      "gui_focus_lost": 67,
      "clipboard_unavailable": 23,
      "coordinate_invalid": 7
    },
    "recovery_rate_by_error": {
      "network_timeout": 0.94,
      "gui_focus_lost": 0.89,
      "clipboard_unavailable": 0.96,
      "coordinate_invalid": 0.71
    }
  }
}
```

---

## **📊 OBSERVABILITY & MONITORING API**

### **GET /metrics/summary**
Get real-time messaging system metrics summary.

**Response:**
```json
{
  "success": true,
  "data": {
    "timestamp": "2024-01-01T12:00:00.000Z",
    "period": "1h",
    "overall": {
      "total_messages": 12543,
      "successful_deliveries": 12456,
      "failed_deliveries": 87,
      "success_rate": 0.993,
      "average_latency_ms": 1250,
      "p95_latency_ms": 2300,
      "p99_latency_ms": 4500
    },
    "by_priority": {
      "urgent": {
        "count": 2345,
        "success_rate": 0.997,
        "avg_latency_ms": 850
      },
      "normal": {
        "count": 10198,
        "success_rate": 0.992,
        "avg_latency_ms": 1350
      }
    },
    "by_agent": {
      "Agent-1": {
        "messages_sent": 1456,
        "success_rate": 0.995,
        "avg_latency_ms": 1200
      },
      "Agent-4": {
        "messages_sent": 1890,
        "success_rate": 0.998,
        "avg_latency_ms": 780
      }
    }
  }
}
```

### **GET /metrics/timeseries**
Get time-series metrics data.

**Query Parameters:**
- `metric`: delivery_success_rate, latency, throughput, errors
- `start`: ISO timestamp
- `end`: ISO timestamp
- `interval`: 1m, 5m, 15m, 1h, 1d
- `agent_id`: optional filter

**Response:**
```json
{
  "success": true,
  "data": {
    "metric": "delivery_success_rate",
    "interval": "5m",
    "points": [
      {
        "timestamp": "2024-01-01T11:00:00.000Z",
        "value": 0.994,
        "sample_size": 234
      },
      {
        "timestamp": "2024-01-01T11:05:00.000Z",
        "value": 0.996,
        "sample_size": 245
      }
    ]
  }
}
```

### **GET /logs/search**
Search structured logs with filtering.

**Query Parameters:**
- `level`: DEBUG, INFO, WARN, ERROR
- `agent_id`: filter by agent
- `correlation_id`: filter by request
- `start_time`: ISO timestamp
- `end_time`: ISO timestamp
- `limit`: max results (default 100)
- `offset`: pagination offset

**Response:**
```json
{
  "success": true,
  "data": {
    "total": 1250,
    "limit": 50,
    "offset": 0,
    "logs": [
      {
        "timestamp": "2024-01-01T12:00:15.123Z",
        "level": "INFO",
        "agent_id": "Agent-1",
        "correlation_id": "req_123456789",
        "component": "delivery_engine",
        "message": "Message delivered successfully",
        "metadata": {
          "message_id": "msg_987654321",
          "priority": "urgent",
          "delivery_time_ms": 890,
          "retries": 0
        }
      }
    ]
  }
}
```

### **GET /alerts/active**
Get currently active alerts.

**Response:**
```json
{
  "success": true,
  "data": {
    "alerts": [
      {
        "id": "alert_123",
        "type": "performance_degradation",
        "severity": "warning",
        "title": "High Latency Detected",
        "description": "Average delivery latency > 3s for last 15 minutes",
        "agent_id": "Agent-3",
        "created_at": "2024-01-01T11:45:00.000Z",
        "updated_at": "2024-01-01T12:00:00.000Z",
        "threshold": {
          "metric": "avg_latency_ms",
          "operator": ">",
          "value": 3000,
          "duration_minutes": 15
        },
        "current_value": 3250,
        "acknowledged": false
      }
    ],
    "summary": {
      "total_active": 3,
      "by_severity": {
        "critical": 0,
        "warning": 3,
        "info": 0
      }
    }
  }
}
```

---

## **🤖 AGENT MANAGEMENT API**

### **GET /agents**
Get all agents with current status.

**Response:**
```json
{
  "success": true,
  "data": {
    "agents": [
      {
        "id": "Agent-1",
        "name": "Integration & Core Systems Specialist",
        "status": "online",
        "coordinates": [1269, 481],
        "last_seen": "2024-01-01T11:58:00.000Z",
        "messages_sent": 1456,
        "messages_failed": 12,
        "average_latency_ms": 1200,
        "current_priority": "normal"
      },
      {
        "id": "Agent-4",
        "name": "Captain - Strategic Oversight",
        "status": "online",
        "coordinates": [308, 1000],
        "last_seen": "2024-01-01T11:59:45.000Z",
        "messages_sent": 1890,
        "messages_failed": 3,
        "average_latency_ms": 780,
        "current_priority": "urgent"
      }
    ],
    "summary": {
      "total_agents": 8,
      "online_agents": 8,
      "offline_agents": 0,
      "average_latency_ms": 1150
    }
  }
}
```

### **GET /agents/{id}/status**
Get detailed status for specific agent.

**Response:**
```json
{
  "success": true,
  "data": {
    "agent": {
      "id": "Agent-4",
      "status": "online",
      "health_score": 0.98,
      "performance_metrics": {
        "response_time_ms": 780,
        "success_rate": 0.998,
        "error_rate": 0.002,
        "last_successful_delivery": "2024-01-01T11:59:45.000Z"
      },
      "recent_activity": [
        {
          "timestamp": "2024-01-01T11:59:45.000Z",
          "action": "message_delivered",
          "message_id": "msg_987654321",
          "latency_ms": 750
        }
      ],
      "configuration": {
        "coordinates": [308, 1000],
        "inbox_path": "agent_workspaces/Agent-4/inbox",
        "priority": "captain",
        "timeout_seconds": 30
      }
    }
  }
}
```

### **POST /agents/{id}/priority**
Update agent priority for ordering.

**Request:**
```json
{
  "priority": "urgent",
  "reason": "Crisis response required",
  "duration_minutes": 60
}
```

---

## **📋 MESSAGE MANAGEMENT API**

### **GET /messages/queue**
Get current message queue status.

**Response:**
```json
{
  "success": true,
  "data": {
    "queue_status": {
      "pending_messages": 12,
      "processing_messages": 3,
      "completed_messages": 15678,
      "failed_messages": 23
    },
    "priority_distribution": {
      "urgent": 5,
      "normal": 7
    },
    "agent_distribution": {
      "Agent-1": 2,
      "Agent-4": 3,
      "Agent-7": 7
    },
    "estimated_processing_time": {
      "urgent": "45s",
      "normal": "120s",
      "total": "165s"
    }
  }
}
```

### **GET /messages/{id}**
Get message details by ID.

**Response:**
```json
{
  "success": true,
  "data": {
    "message": {
      "id": "msg_123456789",
      "content": "System status update required",
      "sender": "Captain Agent-4",
      "recipient": "Agent-1",
      "type": "text",
      "priority": "normal",
      "tags": ["captain"],
      "created_at": "2024-01-01T12:00:00.000Z",
      "status": "delivered",
      "delivery_attempts": 1,
      "delivered_at": "2024-01-01T12:00:02.345Z",
      "latency_ms": 2345,
      "metadata": {
        "correlation_id": "req_987654321",
        "source": "cli",
        "mode": "pyautogui"
      }
    }
  }
}
```

### **POST /messages**
Send a new message (alternative to CLI).

**Request:**
```json
{
  "content": "Hello from API",
  "recipient": "Agent-7",
  "type": "text",
  "priority": "normal",
  "tags": ["test"],
  "mode": "pyautogui",
  "metadata": {
    "source": "api",
    "test_message": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message_id": "msg_123456789",
    "status": "queued",
    "estimated_delivery": "2024-01-01T12:00:05.000Z",
    "correlation_id": "req_987654321"
  }
}
```

---

## **🛡️ HEALTH & SYSTEM API**

### **GET /health**
Comprehensive system health check.

**Response:**
```json
{
  "success": true,
  "data": {
    "overall_status": "healthy",
    "components": {
      "timing_engine": {
        "status": "healthy",
        "last_calibration": "2024-01-01T10:30:00.000Z",
        "performance_score": 0.98
      },
      "retry_system": {
        "status": "healthy",
        "success_rate": 0.993,
        "average_retries": 0.15
      },
      "observability": {
        "status": "healthy",
        "metrics_collection": "active",
        "alert_system": "operational"
      },
      "agent_network": {
        "status": "healthy",
        "online_agents": 8,
        "total_agents": 8,
        "average_latency_ms": 1150
      }
    },
    "system_metrics": {
      "cpu_usage_percent": 23,
      "memory_usage_mb": 234,
      "disk_usage_percent": 45,
      "network_connections": 8
    },
    "last_updated": "2024-01-01T12:00:00.000Z"
  }
}
```

### **GET /health/detailed**
Detailed health check with component-specific metrics.

### **GET /config**
Get current system configuration.

**Response:**
```json
{
  "success": true,
  "data": {
    "version": "1.1.0",
    "environment": "production",
    "features": {
      "adaptive_timing": true,
      "retry_logic": true,
      "parallel_delivery": true,
      "observability": true,
      "intelligent_ordering": true
    },
    "limits": {
      "max_concurrent_deliveries": 3,
      "max_retries": 3,
      "max_message_size_kb": 100,
      "timeout_seconds": 30
    },
    "agents": {
      "total_configured": 8,
      "coordinates_validated": true,
      "inbox_paths_accessible": true
    }
  }
}
```

---

## **🔧 CONFIGURATION API**

### **GET /config/timing**
Get timing engine configuration.

**Response:**
```json
{
  "success": true,
  "data": {
    "adaptive_enabled": true,
    "calibration_interval_minutes": 60,
    "performance_thresholds": {
      "cpu_high": 80,
      "memory_high": 90,
      "network_high": 100
    },
    "fallback_delays": {
      "conservative": {
        "typing_interval": 0.05,
        "gui_focus_delay": 1.0,
        "clipboard_paste_wait": 2.0
      },
      "aggressive": {
        "typing_interval": 0.01,
        "gui_focus_delay": 0.2,
        "clipboard_paste_wait": 0.5
      }
    }
  }
}
```

### **PUT /config/timing**
Update timing configuration.

**Request:**
```json
{
  "adaptive_enabled": true,
  "calibration_interval_minutes": 30,
  "performance_thresholds": {
    "cpu_high": 75,
    "memory_high": 85
  }
}
```

---

## **📊 ERROR CODES REFERENCE**

| Code | Description | HTTP Status | Retryable |
|------|-------------|-------------|-----------|
| MSG_001 | Message sent successfully | 200 | N/A |
| MSG_002 | Message queued for delivery | 202 | N/A |
| ERR_001 | Invalid agent ID | 400 | No |
| ERR_002 | Authentication failed | 401 | No |
| ERR_003 | Message too large | 413 | No |
| ERR_004 | Network timeout | 504 | Yes |
| ERR_005 | GUI focus lost | 503 | Yes |
| ERR_006 | Coordinates invalid | 503 | Yes |
| ERR_007 | Clipboard unavailable | 503 | Yes |
| ERR_008 | System overload | 503 | Yes |
| ERR_009 | Configuration error | 500 | No |

---

## **🔄 WEBHOOK INTEGRATIONS**

### **Message Delivery Webhook**
Configure webhooks for delivery events.

**POST /webhooks/delivery**
```json
{
  "url": "https://api.external-service.com/webhook",
  "events": ["delivered", "failed", "retry"],
  "secret": "webhook-secret-token",
  "active": true
}
```

### **Alert Webhook**
Receive alert notifications.

**POST /webhooks/alerts**
```json
{
  "url": "https://api.monitoring-service.com/alerts",
  "alert_types": ["performance", "error", "system"],
  "severities": ["critical", "warning"],
  "active": true
}
```

---

## **📈 RATE LIMITS**

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/messages` | 100/min | per agent |
| `/metrics/*` | 1000/min | per IP |
| `/logs/search` | 100/min | per IP |
| `/health` | unlimited | N/A |

---

## **🔐 SECURITY CONSIDERATIONS**

### **Authentication**
- Bearer token required for all API calls
- Token rotation every 24 hours
- Agent-specific access controls

### **Authorization**
- Agents can only access their own data
- Captain (Agent-4) has read-only access to all
- Admin endpoints require special permissions

### **Data Protection**
- All API calls logged with correlation IDs
- Sensitive data encrypted in transit and at rest
- PII data masked in logs and responses

---

## **📚 SDK & CLIENT LIBRARIES**

### **Python SDK**
```bash
pip install dream-os-messaging-sdk
```

```python
from dream_os.messaging import Client

client = Client(token="your-token", agent_id="Agent-7")

# Send message
response = client.send_message(
    content="Hello swarm!",
    recipient="Agent-1",
    priority="urgent"
)

# Get metrics
metrics = client.get_metrics()

# Monitor health
health = client.get_health()
```

### **JavaScript SDK**
```bash
npm install @dream-os/messaging-sdk
```

```javascript
import { MessagingClient } from '@dream-os/messaging-sdk';

const client = new MessagingClient({
  token: 'your-token',
  agentId: 'Agent-7'
});

// Send message
const response = await client.sendMessage({
  content: 'Hello swarm!',
  recipient: 'Agent-1',
  priority: 'urgent'
});

// Real-time metrics
client.on('metrics', (metrics) => {
  console.log('Updated metrics:', metrics);
});
```

---

**API Version**: 1.1
**Last Updated**: Current Date
**Specification Author**: Agent-7 (Web Development Specialist)

---

**WE. ARE. SWARM.** ⚡🔥
