import React, { useState, useMemo } from 'react';
import {
  Box,
  ToggleButton,
  ToggleButtonGroup,
  Typography,
  Paper,
} from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const StockChart = ({ stockData }) => {
  const [chartType, setChartType] = useState('candlestick');
  const [timeRange, setTimeRange] = useState('30d');

  const chartData = useMemo(() => {
    if (!stockData || stockData.length === 0) return null;

    const labels = stockData.map(d => {
      const date = new Date(d.date);
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });

    if (chartType === 'line') {
      return {
        labels,
        datasets: [
          {
            label: 'Tesla Stock Price',
            data: stockData.map(d => d.close),
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
        ],
      };
    } else if (chartType === 'volume') {
      return {
        labels,
        datasets: [
          {
            label: 'Volume',
            data: stockData.map(d => d.volume),
            backgroundColor: 'rgba(0, 255, 136, 0.6)',
            borderColor: '#00ff88',
            borderWidth: 1,
          },
        ],
      };
    } else {
      // Candlestick-like chart using bar chart
      const ohlcData = stockData.map(d => ({
        x: d.date,
        o: d.open,
        h: d.high,
        l: d.low,
        c: d.close,
      }));

      return {
        labels,
        datasets: [
          {
            label: 'OHLC',
            data: ohlcData,
            backgroundColor: stockData.map(d => 
              d.close >= d.open ? 'rgba(0, 255, 136, 0.8)' : 'rgba(255, 107, 107, 0.8)'
            ),
            borderColor: stockData.map(d => 
              d.close >= d.open ? '#00ff88' : '#ff6b6b'
            ),
            borderWidth: 1,
          },
        ],
      };
    }
  }, [stockData, chartType]);

  const chartOptions = {
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
            if (chartType === 'candlestick') {
              const data = context.raw;
              return [
                `Open: $${data.o}`,
                `High: $${data.h}`,
                `Low: $${data.l}`,
                `Close: $${data.c}`,
              ];
            }
            return `${context.dataset.label}: $${context.parsed.y}`;
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
    interaction: {
      intersect: false,
      mode: 'index',
    },
  };

  const handleChartTypeChange = (event, newChartType) => {
    if (newChartType !== null) {
      setChartType(newChartType);
    }
  };

  const handleTimeRangeChange = (event, newTimeRange) => {
    if (newTimeRange !== null) {
      setTimeRange(newTimeRange);
    }
  };

  if (!chartData) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height={400}>
        <Typography variant="h6" color="text.secondary">
          No chart data available
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      {/* Chart Controls */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h6" color="primary">
          Interactive Stock Charts
        </Typography>
        
        <Box display="flex" gap={2}>
          <ToggleButtonGroup
            value={chartType}
            exclusive
            onChange={handleChartTypeChange}
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
            <ToggleButton value="candlestick">Candlestick</ToggleButton>
            <ToggleButton value="line">Line</ToggleButton>
            <ToggleButton value="volume">Volume</ToggleButton>
          </ToggleButtonGroup>

          <ToggleButtonGroup
            value={timeRange}
            exclusive
            onChange={handleTimeRangeChange}
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
            <ToggleButton value="7d">7D</ToggleButton>
            <ToggleButton value="30d">30D</ToggleButton>
            <ToggleButton value="90d">90D</ToggleButton>
          </ToggleButtonGroup>
        </Box>
      </Box>

      {/* Chart Container */}
      <Paper
        elevation={0}
        sx={{
          p: 2,
          background: 'rgba(255, 255, 255, 0.02)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: 2,
        }}
      >
        <Box height={500} position="relative">
          {chartType === 'line' ? (
            <Line data={chartData} options={chartOptions} />
          ) : (
            <Bar data={chartData} options={chartOptions} />
          )}
        </Box>
      </Paper>

      {/* Chart Info */}
      <Box mt={2} display="flex" justifyContent="space-between" alignItems="center">
        <Typography variant="body2" color="text.secondary">
          {chartType === 'candlestick' && 'Open-High-Low-Close price data'}
          {chartType === 'line' && 'Closing price trend over time'}
          {chartType === 'volume' && 'Trading volume analysis'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Last updated: {new Date().toLocaleString()}
        </Typography>
      </Box>
    </Box>
  );
};

export default StockChart;


