import React, { useState, useEffect } from 'react'

export function GitHubBook() {
  const [bookData, setBookData] = useState(null)
  const [filter, setFilter] = useState('all')
  
  useEffect(() => {
    fetch('/api/github-book')
      .then(res => res.json())
      .then(data => setBookData(data))
  }, [])

  if (!bookData) return <div>Loading...</div>

  const repos = bookData.repos || []
  const filtered = filter === 'all' ? repos : 
    filter === 'jackpot' ? bookData.jackpots : 
    repos.filter(r => r.category === filter)

  return (
    <div className="github-book-section">
      <h2>📚 GitHub Book</h2>
      <p className="coverage">{bookData.coverage} coverage</p>
      
      <div className="filter-buttons">
        <button onClick={() => setFilter('all')} className={filter === 'all' ? 'active' : ''}>
          All
        </button>
        <button onClick={() => setFilter('jackpot')} className={filter === 'jackpot' ? 'active' : ''}>
          🎰 Jackpots
        </button>
        <button onClick={() => setFilter('high-value')} className={filter === 'high-value' ? 'active' : ''}>
          High Value
        </button>
      </div>

      <div className="repos-grid">
        {filtered.map((repo, i) => (
          <div key={i} className="repo-card">
            <h3>{repo.name}</h3>
            <p className="repo-desc">{repo.description || 'No description'}</p>
            {repo.roi && <span className="repo-roi">ROI: {repo.roi}</span>}
            {repo.value && <span className="repo-value">{repo.value}</span>}
          </div>
        ))}
      </div>
    </div>
  )
}

