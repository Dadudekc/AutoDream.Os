import React, { useState, useMemo } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  LinearProgress,
  ToggleButton,
  ToggleButtonGroup,
  Paper,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Timeline,
  Psychology,
} from '@mui/icons-material';
import { Line } from 'react-chartjs-2';

const ForecastPanel = ({ forecastData }) => {
  const [forecastType, setForecastType] = useState('price');
  const [timeHorizon, setTimeHorizon] = useState('30d');

  const forecastChartData = useMemo(() => {
    if (!forecastData || forecastData.length === 0) return null;

    const labels = forecastData.map(d => {
      const date = new Date(d.date);
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });

    return {
      labels,
      datasets: [
        {
          label: 'Forecasted Price',
          data: forecastData.map(d => d.price),
          borderColor: '#00ff88',
          backgroundColor: 'rgba(0, 255, 136, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#00ff88',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
        {
          label: 'Confidence Band',
          data: forecastData.map(d => d.price * (1 + d.confidence * 0.1)),
          borderColor: 'rgba(0, 255, 136, 0.3)',
          backgroundColor: 'rgba(0, 255, 136, 0.05)',
          borderWidth: 1,
          fill: '+1',
          tension: 0.4,
          pointRadius: 0,
        },
      ],
    };
  }, [forecastData]);

  const forecastOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          color: '#ffffff',
          font: {
            size: 12,
          },
        },
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#ffffff',
        bodyColor: '#ffffff',
        borderColor: '#00ff88',
        borderWidth: 1,
        callbacks: {
          label: function(context) {
            if (context.datasetIndex === 0) {
              return `Forecast: $${context.parsed.y.toFixed(2)}`;
            } else {
              return `Confidence: ${(forecastData[context.dataIndex].confidence * 100).toFixed(1)}%`;
            }
          },
        },
      },
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        ticks: {
          color: '#ffffff',
          maxTicksLimit: 8,
        },
      },
      y: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        ticks: {
          color: '#ffffff',
          callback: function(value) {
            return '$' + value.toFixed(2);
          },
        },
      },
    },
  };

  const forecastMetrics = useMemo(() => {
    if (!forecastData || forecastData.length === 0) return null;

    const currentPrice = forecastData[0].price;
    const futurePrice = forecastData[forecastData.length - 1].price;
    const priceChange = futurePrice - currentPrice;
    const priceChangePercent = (priceChange / currentPrice) * 100;
    const avgConfidence = forecastData.reduce((sum, d) => sum + d.confidence, 0) / forecastData.length;

    return {
      currentPrice,
      futurePrice,
      priceChange,
      priceChangePercent,
      avgConfidence,
    };
  }, [forecastData]);

  const handleForecastTypeChange = (event, newType) => {
    if (newType !== null) {
      setForecastType(newType);
    }
  };

  const handleTimeHorizonChange = (event, newHorizon) => {
    if (newHorizon !== null) {
      setTimeHorizon(newHorizon);
    }
  };

  if (!forecastData || !forecastChartData || !forecastMetrics) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height={400}>
        <Typography variant="h6" color="text.secondary">
          No forecast data available
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom color="primary">
        AI-Powered Stock Forecast
      </Typography>

      {/* Forecast Controls */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box display="flex" gap={2}>
          <ToggleButtonGroup
            value={forecastType}
            exclusive
            onChange={handleForecastTypeChange}
            size="small"
            sx={{
              '& .MuiToggleButton-root': {
                color: 'white',
                borderColor: 'rgba(255, 255, 255, 0.3)',
                '&.Mui-selected': {
                  backgroundColor: 'primary.main',
                  color: 'black',
                },
              },
            }}
          >
            <ToggleButton value="price">Price Forecast</ToggleButton>
            <ToggleButton value="sentiment">Sentiment</ToggleButton>
            <ToggleButton value="volatility">Volatility</ToggleButton>
          </ToggleButtonGroup>

          <ToggleButtonGroup
            value={timeHorizon}
            exclusive
            onChange={handleTimeHorizonChange}
            size="small"
            sx={{
              '& .MuiToggleButton-root': {
                color: 'white',
                borderColor: 'rgba(255, 255, 255, 0.3)',
                '&.Mui-selected': {
                  backgroundColor: 'primary.main',
                  color: 'black',
                },
              },
            }}
          >
            <ToggleButton value="7d">7 Days</ToggleButton>
            <ToggleButton value="30d">30 Days</ToggleButton>
            <ToggleButton value="90d">90 Days</ToggleButton>
          </ToggleButtonGroup>
        </Box>
      </Box>

      {/* Forecast Metrics */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              background: 'rgba(255, 255, 255, 0.03)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: 2,
            }}
          >
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <Timeline sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="body2" color="text.secondary">
                  Current Price
                </Typography>
              </Box>
              <Typography variant="h6" fontWeight="bold">
                ${forecastMetrics.currentPrice.toFixed(2)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              background: 'rgba(255, 255, 255, 0.03)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: 2,
            }}
          >
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <TrendingUp sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="body2" color="text.secondary">
                  Forecasted Price
                </Typography>
              </Box>
              <Typography variant="h6" fontWeight="bold">
                ${forecastMetrics.futurePrice.toFixed(2)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              background: 'rgba(255, 255, 255, 0.03)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: 2,
            }}
          >
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                {forecastMetrics.priceChange > 0 ? (
                  <TrendingUp sx={{ mr: 1, color: 'success.main' }} />
                ) : (
                  <TrendingDown sx={{ mr: 1, color: 'error.main' }} />
                )}
                <Typography variant="body2" color="text.secondary">
                  Expected Change
                </Typography>
              </Box>
              <Typography 
                variant="h6" 
                fontWeight="bold"
                color={forecastMetrics.priceChange > 0 ? 'success.main' : 'error.main'}
              >
                {forecastMetrics.priceChange > 0 ? '+' : ''}${forecastMetrics.priceChange.toFixed(2)}
                <br />
                <Typography variant="body2" component="span">
                  ({forecastMetrics.priceChange > 0 ? '+' : ''}{forecastMetrics.priceChangePercent.toFixed(2)}%)
                </Typography>
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              background: 'rgba(255, 255, 255, 0.03)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: 2,
            }}
          >
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <Psychology sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="body2" color="text.secondary">
                  AI Confidence
                </Typography>
              </Box>
              <Typography variant="h6" fontWeight="bold">
                {(forecastMetrics.avgConfidence * 100).toFixed(1)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={forecastMetrics.avgConfidence * 100}
                sx={{
                  mt: 1,
                  height: 6,
                  borderRadius: 3,
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: 'primary.main',
                  },
                }}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Forecast Chart */}
      <Paper
        elevation={0}
        sx={{
          p: 2,
          background: 'rgba(255, 255, 255, 0.02)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: 2,
        }}
      >
        <Box height={400} position="relative">
          <Line data={forecastChartData} options={forecastOptions} />
        </Box>
      </Paper>

      {/* Forecast Disclaimer */}
      <Box mt={2}>
        <Typography variant="body2" color="text.secondary" align="center">
          * This forecast is generated by AI algorithms and should not be considered as financial advice. 
          Past performance does not guarantee future results. Please consult with a financial advisor before making investment decisions.
        </Typography>
      </Box>
    </Box>
  );
};

export default ForecastPanel;


