import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [swarmStatus, setSwarmStatus] = useState(null)
  const [leaderboard, setLeaderboard] = useState([])

  useEffect(() => {
    // Fetch swarm status
    fetch('http://localhost:8000/api/swarm-status')
      .then(res => res.json())
      .then(data => setSwarmStatus(data))
    
    // Fetch leaderboard
    fetch('http://localhost:8000/api/leaderboard')
      .then(res => res.json())
      .then(data => setLeaderboard(data.leaderboard))
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <h1>🐝 WE ARE SWARM</h1>
        <p>Collective Intelligence in Action</p>
      </header>

      {swarmStatus && (
        <div className="swarm-status">
          <h2>Swarm Status</h2>
          <p>Total Points: {swarmStatus.total_points}</p>
          <p>Active Agents: {swarmStatus.active_agents}/{swarmStatus.total_agents}</p>
          <p>Status: {swarmStatus.status}</p>
        </div>
      )}

      <div className="leaderboard">
        <h2>🏆 Leaderboard</h2>
        {leaderboard.map(agent => (
          <div key={agent.agent_id} className="agent-card">
            <span className="rank">{agent.rank}</span>
            <span className="agent-id">{agent.agent_id}</span>
            <span className="points">{agent.points} pts</span>
            <span className="status">{agent.status}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App

