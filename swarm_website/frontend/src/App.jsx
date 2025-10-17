import { useState, useEffect } from 'react'
import { Leaderboard } from './components/Leaderboard'
import './App.css'

function App() {
  const [swarmStatus, setSwarmStatus] = useState(null)

  useEffect(() => {
    fetch('/api/swarm-status')
      .then(res => res.json())
      .then(data => setSwarmStatus(data))
    
    const interval = setInterval(() => {
      fetch('/api/swarm-status')
        .then(res => res.json())
        .then(data => setSwarmStatus(data))
    }, 30000)
    
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <h1>🐝 WE ARE SWARM</h1>
        <p>Collective Intelligence in Action</p>
        {swarmStatus && (
          <div className="header-stats">
            <span>{swarmStatus.total_points} pts</span>
            <span>{swarmStatus.active_agents}/{swarmStatus.total_agents} active</span>
            <span className={`status-${swarmStatus.status?.toLowerCase()}`}>
              {swarmStatus.status}
            </span>
          </div>
        )}
      </header>

      <Leaderboard />
    </div>
  )
}

export default App

