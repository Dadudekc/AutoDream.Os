import React from 'react'

export function AgentCard({ agent, rank }) {
  const getMedalEmoji = (rank) => {
    if (rank === 1) return '🥇'
    if (rank === 2) return '🥈'
    if (rank === 3) return '🥉'
    return '🏅'
  }

  const getStatusColor = (status) => {
    if (status === 'ACTIVE') return '#28a745'
    if (status === 'REST' || status === 'RESTING') return '#ffc107'
    return '#6c757d'
  }

  return (
    <div className="agent-card" style={{ borderLeft: `4px solid ${getStatusColor(agent.status)}` }}>
      <span className="rank">{getMedalEmoji(rank)}</span>
      <div className="agent-info">
        <h3>{agent.agent_id || agent.id}</h3>
        <p className="mission">{agent.current_mission || 'No active mission'}</p>
      </div>
      <div className="agent-stats">
        <span className="points">{agent.points_earned || 0} pts</span>
        <span className="status" style={{ background: getStatusColor(agent.status), color: agent.status === 'ACTIVE' ? 'white' : '#333' }}>
          {agent.status || agent.state}
        </span>
      </div>
    </div>
  )
}

