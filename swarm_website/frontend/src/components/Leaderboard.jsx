import React, { useState, useEffect } from 'react'
import { AgentCard } from './AgentCard'

export function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/leaderboard')
      .then(res => res.json())
      .then(data => {
        setLeaderboard(data.leaderboard || [])
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to load leaderboard:', err)
        setLoading(false)
      })
    
    // Refresh every 30 seconds
    const interval = setInterval(() => {
      fetch('/api/leaderboard')
        .then(res => res.json())
        .then(data => setLeaderboard(data.leaderboard || []))
    }, 30000)
    
    return () => clearInterval(interval)
  }, [])

  if (loading) return <div>Loading...</div>

  return (
    <div className="leaderboard">
      <h2>🏆 Agent Leaderboard</h2>
      <p className="subtitle">Real-time rankings - Updates every 30s</p>
      {leaderboard.map(agent => (
        <AgentCard key={agent.agent_id} agent={agent} rank={agent.rank} />
      ))}
    </div>
  )
}

