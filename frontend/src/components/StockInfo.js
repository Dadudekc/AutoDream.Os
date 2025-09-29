import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  VolumeUp,
  ShowChart,
} from '@mui/icons-material';

const StockInfo = ({ stockData }) => {
  if (!stockData || stockData.length === 0) {
    return (
      <Typography variant="h6" color="text.secondary">
        No stock data available
      </Typography>
    );
  }

  const latestData = stockData[stockData.length - 1];
  const previousData = stockData[stockData.length - 2];

  const priceChange = latestData.close - previousData.close;
  const priceChangePercent = (priceChange / previousData.close) * 100;

  const dayHigh = Math.max(...stockData.map(d => d.high));
  const dayLow = Math.min(...stockData.map(d => d.low));
  const avgVolume = stockData.reduce((sum, d) => sum + d.volume, 0) / stockData.length;

  const metrics = [
    {
      title: 'Current Price',
      value: `$${latestData.close.toFixed(2)}`,
      change: priceChange,
      changePercent: priceChangePercent,
      icon: <ShowChart />,
    },
    {
      title: 'Day High',
      value: `$${dayHigh.toFixed(2)}`,
      icon: <TrendingUp />,
    },
    {
      title: 'Day Low',
      value: `$${dayLow.toFixed(2)}`,
      icon: <TrendingDown />,
    },
    {
      title: 'Volume',
      value: `${(latestData.volume / 1000000).toFixed(1)}M`,
      icon: <VolumeUp />,
    },
    {
      title: 'Avg Volume',
      value: `${(avgVolume / 1000000).toFixed(1)}M`,
      icon: <VolumeUp />,
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom color="primary">
        Tesla Inc. (TSLA)
      </Typography>

      <Grid container spacing={3}>
        {metrics.map((metric, index) => (
          <Grid item xs={12} sm={6} md={2.4} key={index}>
            <Card
              sx={{
                background: 'rgba(255, 255, 255, 0.03)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: 2,
                height: '100%',
              }}
            >
              <CardContent>
                <Box display="flex" alignItems="center" mb={1}>
                  {metric.icon}
                  <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                    {metric.title}
                  </Typography>
                </Box>

                <Typography variant="h6" fontWeight="bold" mb={1}>
                  {metric.value}
                </Typography>

                {metric.change !== undefined && (
                  <Box display="flex" alignItems="center">
                    <Chip
                      label={`${metric.change > 0 ? '+' : ''}${metric.change.toFixed(2)} (${metric.change > 0 ? '+' : ''}${metric.changePercent.toFixed(2)}%)`}
                      color={metric.change > 0 ? 'success' : 'error'}
                      size="small"
                    />
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Price Range Indicator */}
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Price Range (30 Days)
        </Typography>
        <Box position="relative" height={20} bgcolor="rgba(255, 255, 255, 0.1)" borderRadius={1}>
          <LinearProgress
            variant="determinate"
            value={((latestData.close - dayLow) / (dayHigh - dayLow)) * 100}
            sx={{
              height: 20,
              borderRadius: 1,
              background: 'linear-gradient(90deg, #ff6b6b 0%, #00ff88 100%)',
              '& .MuiLinearProgress-bar': {
                background: 'rgba(255, 255, 255, 0.3)',
              },
            }}
          />
          <Box
            position="absolute"
            top="50%"
            left={`${((latestData.close - dayLow) / (dayHigh - dayLow)) * 100}%`}
            sx={{
              transform: 'translate(-50%, -50%)',
              width: 12,
              height: 12,
              bgcolor: 'primary.main',
              borderRadius: '50%',
              border: '2px solid white',
            }}
          />
        </Box>
        <Box display="flex" justifyContent="space-between" mt={1}>
          <Typography variant="body2" color="text.secondary">
            ${dayLow.toFixed(2)}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            ${dayHigh.toFixed(2)}
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};

export default StockInfo;
