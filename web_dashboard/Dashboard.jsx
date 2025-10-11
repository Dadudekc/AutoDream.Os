import './Dashboard.css';

import AgentStatus from './AgentStatus';
import Configuration from './Configuration';
import React from 'react';
import RealTimeMonitoring from './RealTimeMonitoring';
import SystemHealth from './SystemHealth';
import V3Pipeline from './V3Pipeline';

const Dashboard = () => {
  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Dream.OS Captain Dashboard</h1>
        <div className="status-indicator">
          <span className="status-dot active"></span>
          <span>System Online</span>
        </div>
      </header>
      
      <main className="dashboard-main">
        <div className="dashboard-grid">
          <div className="dashboard-section">
            <AgentStatus />
          </div>
          <div className="dashboard-section">
            <V3Pipeline />
          </div>
          <div className="dashboard-section">
            <SystemHealth />
          </div>
          <div className="dashboard-section full-width">
            <RealTimeMonitoring />
          </div>
          <div className="dashboard-section">
            <Configuration />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
