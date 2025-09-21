
import React, { useState, useEffect } from 'react';

const V3Pipeline = () => {
  const [contracts, setContracts] = useState([]);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    fetchContracts();
    const interval = setInterval(fetchContracts, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchContracts = async () => {
    try {
      const response = await fetch('/api/v3-contracts');
      const data = await response.json();
      setContracts(data);
      
      // Calculate overall progress
      const totalProgress = data.reduce((sum, contract) => sum + contract.progress, 0);
      setProgress(totalProgress / data.length);
    } catch (error) {
      console.error('Error fetching contracts:', error);
    }
  };

  return (
    <div className="v3-pipeline">
      <h2>V3 Pipeline Progress</h2>
      <div className="progress-bar">
        <div className="progress-fill" style={{width: `${progress}%`}}></div>
        <span>{progress.toFixed(1)}%</span>
      </div>
      <div className="contracts-list">
        {contracts.map(contract => (
          <div key={contract.id} className="contract-card">
            <h3>{contract.id}: {contract.title}</h3>
            <p>Status: {contract.status}</p>
            <p>Progress: {contract.progress}%</p>
            <p>Agent: {contract.assigned_agent}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default V3Pipeline;
