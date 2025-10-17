import React, { useState, useEffect } from 'react'

export function SwarmBrain() {
  const [brainData, setBrainData] = useState(null)
  
  useEffect(() => {
    fetch('/api/swarm-brain')
      .then(res => res.json())
      .then(data => setBrainData(data))
  }, [])

  if (!brainData) return <div>Loading...</div>

  return (
    <div className="swarm-brain-section">
      <h2>🧠 Swarm Brain</h2>
      <div className="brain-stats">
        <div className="stat-card">
          <h3>{brainData.protocols}</h3>
          <p>Protocols</p>
        </div>
        <div className="stat-card">
          <h3>{brainData.procedures}</h3>
          <p>Procedures</p>
        </div>
        <div className="stat-card">
          <h3>{brainData.learnings}</h3>
          <p>Learnings</p>
        </div>
        <div className="stat-card">
          <h3>{brainData.decisions}</h3>
          <p>Decisions</p>
        </div>
      </div>
      <div className="recent-learnings">
        <h3>Recent Learnings</h3>
        {brainData.recent?.map((item, i) => (
          <div key={i} className="learning-item">
            <span className="learning-date">{item.date}</span>
            <span className="learning-title">{item.title}</span>
            <span className="learning-agent">{item.agent}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

