import React, { useEffect, useState } from 'react';

const RealTimeMonitoring = () => {
  const [logs, setLogs] = useState([]);
  const [metrics, setMetrics] = useState({});

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8001');
    
    ws.onopen = () => {
      console.log('WebSocket connected');
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'log') {
        setLogs(prev => [...prev.slice(-99), data.log]);
      } else if (data.type === 'metric') {
        setMetrics(data.metrics);
      }
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    return () => ws.close();
  }, []);

  return (
    <div className="real-time-monitoring">
      <h2>Real-Time Monitoring</h2>
      <div className="metrics-panel">
        <h3>Live Metrics</h3>
        <div className="metrics-grid">
          {Object.entries(metrics).map(([key, value]) => (
            <div key={key} className="metric-item">
              <span>{key}: {value}</span>
            </div>
          ))}
        </div>
      </div>
      <div className="logs-panel">
        <h3>Live Logs</h3>
        <div className="logs-container">
          {logs.map((log, index) => (
            <div key={index} className={`log-entry ${log.level}`}>
              <span className="timestamp">{log.timestamp}</span>
              <span className="message">{log.message}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RealTimeMonitoring;
