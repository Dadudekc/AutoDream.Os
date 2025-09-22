import './DevlogAnalytics.css';

import React, { useEffect, useState } from 'react';

const DevlogAnalytics = () => {
    const [analytics, setAnalytics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedAgent, setSelectedAgent] = useState('all');
    const [selectedStatus, setSelectedStatus] = useState('all');
    const [trends, setTrends] = useState(null);
    const [agents, setAgents] = useState([]);

    useEffect(() => {
        fetchAnalytics();
        fetchTrends();
        fetchAgents();
    }, []);

    const fetchAnalytics = async () => {
        try {
            setLoading(true);
            const response = await fetch('/api/devlogs/analytics');
            const data = await response.json();

            if (data.success) {
                setAnalytics(data.data);
            } else {
                setError(data.error);
            }
        } catch (err) {
            setError('Failed to fetch analytics data');
        } finally {
            setLoading(false);
        }
    };

    const fetchTrends = async (days = 30) => {
        try {
            const response = await fetch(`/api/devlogs/trends?days=${days}`);
            const data = await response.json();

            if (data.success) {
                setTrends(data.data);
            }
        } catch (err) {
            console.error('Failed to fetch trends data:', err);
        }
    };

    const fetchAgents = async () => {
        try {
            const response = await fetch('/api/devlogs/agents');
            const data = await response.json();

            if (data.success) {
                setAgents(data.data);
            }
        } catch (err) {
            console.error('Failed to fetch agents data:', err);
        }
    };

    const handleExport = async (format) => {
        try {
            const response = await fetch(`/api/devlogs/export/${format}`);
            const blob = await response.blob();

            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `devlogs.${format}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (err) {
            console.error(`Failed to export ${format}:`, err);
        }
    };

    if (loading) {
        return (
            <div className="devlog-analytics">
                <div className="loading">Loading devlog analytics...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="devlog-analytics">
                <div className="error">Error: {error}</div>
            </div>
        );
    }

    return (
        <div className="devlog-analytics">
            <div className="analytics-header">
                <h2>🤖 Agent Devlog Analytics</h2>
                <div className="export-buttons">
                    <button onClick={() => handleExport('json')} className="export-btn">
                        Export JSON
                    </button>
                    <button onClick={() => handleExport('csv')} className="export-btn">
                        Export CSV
                    </button>
                    <button onClick={() => handleExport('excel')} className="export-btn">
                        Export Excel
                    </button>
                </div>
            </div>

            {analytics && (
                <div className="analytics-content">
                    {/* Summary Cards */}
                    <div className="summary-cards">
                        <div className="summary-card">
                            <h3>Total Devlogs</h3>
                            <div className="summary-value">{analytics.summary.total_devlogs}</div>
                        </div>
                        <div className="summary-card">
                            <h3>Active Agents</h3>
                            <div className="summary-value">{analytics.summary.unique_agents}</div>
                        </div>
                        <div className="summary-card">
                            <h3>Avg per Day</h3>
                            <div className="summary-value">
                                {analytics.trends.average_per_day.toFixed(1)}
                            </div>
                        </div>
                        <div className="summary-card">
                            <h3>Success Rate</h3>
                            <div className="summary-value">
                                {((analytics.summary.status_distribution.completed || 0) /
                                  Math.max(1, analytics.summary.total_devlogs) * 100).toFixed(1)}%
                            </div>
                        </div>
                    </div>

                    {/* Status Distribution */}
                    <div className="analytics-section">
                        <h3>Status Distribution</h3>
                        <div className="status-chart">
                            {Object.entries(analytics.summary.status_distribution).map(([status, count]) => (
                                <div key={status} className="status-bar">
                                    <span className="status-label">{status}</span>
                                    <div className="status-progress">
                                        <div
                                            className={`status-fill ${status}`}
                                            style={{
                                                width: `${(count / analytics.summary.total_devlogs) * 100}%`
                                            }}
                                        ></div>
                                    </div>
                                    <span className="status-count">{count}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Top Agents */}
                    <div className="analytics-section">
                        <h3>Top Active Agents</h3>
                        <div className="agents-list">
                            {analytics.top_agents.map((agent, index) => (
                                <div key={agent.agent_id} className="agent-item">
                                    <div className="agent-rank">#{index + 1}</div>
                                    <div className="agent-info">
                                        <div className="agent-id">{agent.agent_id}</div>
                                        <div className="agent-role">{agent.role}</div>
                                    </div>
                                    <div className="agent-count">{agent.count} devlogs</div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Daily Activity Trend */}
                    {analytics.trends.daily_activity.length > 0 && (
                        <div className="analytics-section">
                            <h3>Daily Activity (Last 7 Days)</h3>
                            <div className="activity-chart">
                                {analytics.trends.daily_activity.map((day) => (
                                    <div key={day.date} className="activity-day">
                                        <div className="activity-date">
                                            {new Date(day.date).toLocaleDateString()}
                                        </div>
                                        <div className="activity-bar">
                                            <div
                                                className="activity-fill"
                                                style={{ height: `${(day.count / 10) * 100}px` }}
                                            ></div>
                                        </div>
                                        <div className="activity-count">{day.count}</div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Agents Overview */}
                    {agents.length > 0 && (
                        <div className="analytics-section">
                            <h3>Agent Activity Overview</h3>
                            <div className="agents-overview">
                                <div className="agents-grid">
                                    {agents.slice(0, 8).map((agent) => (
                                        <div key={agent.agent_id} className="agent-overview-card">
                                            <div className="agent-overview-header">
                                                <span className="agent-overview-id">{agent.agent_id}</span>
                                                <span className="agent-overview-count">{agent.devlog_count}</span>
                                            </div>
                                            <div className="agent-overview-role">{agent.role}</div>
                                            <div className="agent-overview-bar">
                                                <div
                                                    className="agent-overview-fill"
                                                    style={{
                                                        width: `${Math.min((agent.devlog_count / Math.max(...agents.map(a => a.devlog_count))) * 100, 100)}%`
                                                    }}
                                                ></div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Trends Analysis */}
                    {trends && (
                        <div className="analytics-section">
                            <h3>Trends Analysis ({trends.period_days} days)</h3>
                            <div className="trends-summary">
                                <div className="trend-item">
                                    <span className="trend-label">Total Devlogs:</span>
                                    <span className="trend-value">{trends.total_devlogs}</span>
                                </div>
                                <div className="trend-item">
                                    <span className="trend-label">Daily Average:</span>
                                    <span className="trend-value">
                                        {(trends.total_devlogs / trends.period_days).toFixed(1)}
                                    </span>
                                </div>
                            </div>

                            {trends.daily_breakdown.length > 0 && (
                                <div className="daily-breakdown">
                                    <h4>Daily Breakdown</h4>
                                    <div className="daily-table">
                                        <div className="daily-header">
                                            <span>Date</span>
                                            <span>Total</span>
                                            <span>Completed</span>
                                            <span>In Progress</span>
                                            <span>Failed</span>
                                            <span>Agents</span>
                                        </div>
                                        {trends.daily_breakdown.slice(-10).map((day) => (
                                            <div key={day.date} className="daily-row">
                                                <span>{new Date(day.date).toLocaleDateString()}</span>
                                                <span>{day.total}</span>
                                                <span>{day.completed}</span>
                                                <span>{day.in_progress}</span>
                                                <span>{day.failed}</span>
                                                <span>{day.unique_agents}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default DevlogAnalytics;
