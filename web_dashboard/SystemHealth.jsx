import React, { useEffect, useState } from 'react';

const SystemHealth = () => {
  const [health, setHealth] = useState({});
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchHealth = async () => {
    try {
      const response = await fetch('/api/system-health');
      const data = await response.json();
      setHealth(data.health);
      setAlerts(data.alerts);
    } catch (error) {
      console.error('Error fetching health:', error);
    }
  };

  const getHealthColor = (value) => {
    if (value < 50) return '#44ff44';
    if (value < 80) return '#ffaa00';
    return '#ff4444';
  };

  return (
    <div className="system-health">
      <h2>System Health</h2>
      <div className="health-metrics">
        <div className="health-metric">
          <h4>CPU Usage</h4>
          <div className="health-value" style={{color: getHealthColor(health.cpu || 0)}}>
            {health.cpu || 0}%
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{
                width: `${health.cpu || 0}%`,
                background: `linear-gradient(90deg, ${getHealthColor(health.cpu || 0)}, ${getHealthColor(health.cpu || 0)}88)`
              }}
            ></div>
          </div>
        </div>
        <div className="health-metric">
          <h4>Memory Usage</h4>
          <div className="health-value" style={{color: getHealthColor(health.memory || 0)}}>
            {health.memory || 0}%
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{
                width: `${health.memory || 0}%`,
                background: `linear-gradient(90deg, ${getHealthColor(health.memory || 0)}, ${getHealthColor(health.memory || 0)}88)`
              }}
            ></div>
          </div>
        </div>
        <div className="health-metric">
          <h4>Disk Usage</h4>
          <div className="health-value" style={{color: getHealthColor(health.disk || 0)}}>
            {health.disk || 0}%
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{
                width: `${health.disk || 0}%`,
                background: `linear-gradient(90deg, ${getHealthColor(health.disk || 0)}, ${getHealthColor(health.disk || 0)}88)`
              }}
            ></div>
          </div>
        </div>
      </div>
      {alerts.length > 0 && (
        <div className="alerts">
          <h3>System Alerts</h3>
          {alerts.map((alert, index) => (
            <div key={index} className={`alert alert-${alert.severity}`}>
              <strong>{alert.severity.toUpperCase()}:</strong> {alert.message}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SystemHealth;
