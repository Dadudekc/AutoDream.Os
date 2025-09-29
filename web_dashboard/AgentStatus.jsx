
import React, { useState, useEffect } from 'react';

const AgentStatus = () => {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAgents();
    const interval = setInterval(fetchAgents, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await fetch('/api/agents');
      const data = await response.json();
      setAgents(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching agents:', error);
    }
  };

  return (
    <div className="agent-status">
      <h2>Agent Status</h2>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <div className="agents-grid">
          {agents.map(agent => (
            <div key={agent.id} className={`agent-card ${agent.status.toLowerCase()}`}>
              <div className="agent-header">
                <h3>{agent.id}</h3>
                <div className={`status-indicator ${agent.status.toLowerCase()}`}></div>
              </div>
              <div className="agent-details">
                <p className="specialization">{agent.specialization}</p>
                <p className="team">Team: {agent.team}</p>
                <p className="task">Current Task: {agent.current_task}</p>
                <div className="efficiency-bar">
                  <span>Efficiency: {agent.efficiency}/10</span>
                  <div className="efficiency-progress">
                    <div
                      className="efficiency-fill"
                      style={{width: `${(agent.efficiency / 10) * 100}%`}}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AgentStatus;
