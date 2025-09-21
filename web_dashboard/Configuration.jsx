
import React, { useState, useEffect } from 'react';

const Configuration = () => {
  const [config, setConfig] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const response = await fetch('/api/configuration');
      const data = await response.json();
      setConfig(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching config:', error);
    }
  };

  const updateConfig = async (key, value) => {
    try {
      await fetch('/api/configuration', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ [key]: value })
      });
      setConfig(prev => ({ ...prev, [key]: value }));
    } catch (error) {
      console.error('Error updating config:', error);
    }
  };

  return (
    <div className="configuration">
      <h2>Configuration</h2>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <div className="config-form">
          {Object.entries(config).map(([key, value]) => (
            <div key={key} className="config-item">
              <label>{key}:</label>
              <input
                type="text"
                value={value}
                onChange={(e) => updateConfig(key, e.target.value)}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Configuration;
