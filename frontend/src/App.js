import React, { useState, useEffect } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, Container, Typography, Paper } from '@mui/material';
import Header from './components/Header';
import StockChart from './components/StockChart';
import StockInfo from './components/StockInfo';
import ForecastPanel from './components/ForecastPanel';
import './styles/App.css';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00ff88',
    },
    secondary: {
      main: '#ff6b6b',
    },
    background: {
      default: '#0a0a0a',
      paper: 'rgba(255, 255, 255, 0.05)',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
    },
    h2: {
      fontWeight: 600,
      fontSize: '2rem',
    },
  },
});

function App() {
  const [stockData, setStockData] = useState(null);
  const [forecastData, setForecastData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Simulate data loading
    const loadData = async () => {
      try {
        setIsLoading(true);
        // Mock data for now - will be replaced with real API calls
        const mockStockData = generateMockStockData();
        const mockForecastData = generateMockForecastData();
        
        setStockData(mockStockData);
        setForecastData(mockForecastData);
        setError(null);
      } catch (err) {
        setError('Failed to load stock data');
        console.error('Error loading data:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  const generateMockStockData = () => {
    const data = [];
    const basePrice = 250;
    const now = new Date();
    
    for (let i = 30; i >= 0; i--) {
      const date = new Date(now);
      date.setDate(date.getDate() - i);
      
      const open = basePrice + (Math.random() - 0.5) * 20;
      const close = open + (Math.random() - 0.5) * 10;
      const high = Math.max(open, close) + Math.random() * 5;
      const low = Math.min(open, close) - Math.random() * 5;
      const volume = Math.floor(Math.random() * 1000000) + 500000;
      
      data.push({
        date: date.toISOString().split('T')[0],
        open: parseFloat(open.toFixed(2)),
        high: parseFloat(high.toFixed(2)),
        low: parseFloat(low.toFixed(2)),
        close: parseFloat(close.toFixed(2)),
        volume: volume,
      });
    }
    
    return data;
  };

  const generateMockForecastData = () => {
    const data = [];
    const basePrice = stockData ? stockData[stockData.length - 1].close : 250;
    const now = new Date();
    
    for (let i = 1; i <= 30; i++) {
      const date = new Date(now);
      date.setDate(date.getDate() + i);
      
      const trend = Math.sin(i * 0.1) * 0.02;
      const volatility = (Math.random() - 0.5) * 0.05;
      const price = basePrice * (1 + trend + volatility);
      
      data.push({
        date: date.toISOString().split('T')[0],
        price: parseFloat(price.toFixed(2)),
        confidence: Math.max(0.6, 1 - (i * 0.02)),
      });
    }
    
    return data;
  };

  if (isLoading) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box 
          display="flex" 
          justifyContent="center" 
          alignItems="center" 
          minHeight="100vh"
          sx={{ background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%)' }}
        >
          <Typography variant="h4" color="primary">
            Loading Tesla Stock Data...
          </Typography>
        </Box>
      </ThemeProvider>
    );
  }

  if (error) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box 
          display="flex" 
          justifyContent="center" 
          alignItems="center" 
          minHeight="100vh"
          sx={{ background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%)' }}
        >
          <Typography variant="h4" color="error">
            {error}
          </Typography>
        </Box>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box 
        sx={{ 
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
        }}
      >
        <Header />
        
        <Container maxWidth="xl" sx={{ py: 4 }}>
          <Box display="flex" flexDirection="column" gap={4}>
            {/* Stock Information Panel */}
            <Paper 
              elevation={0}
              sx={{ 
                p: 3,
                background: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: 2,
              }}
            >
              <StockInfo stockData={stockData} />
            </Paper>

            {/* Main Chart Section */}
            <Paper 
              elevation={0}
              sx={{ 
                p: 3,
                background: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: 2,
              }}
            >
              <Typography variant="h4" gutterBottom color="primary" sx={{ mb: 3 }}>
                Tesla Stock Price Chart
              </Typography>
              <StockChart stockData={stockData} />
            </Paper>

            {/* Forecast Panel */}
            <Paper 
              elevation={0}
              sx={{ 
                p: 3,
                background: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: 2,
              }}
            >
              <ForecastPanel forecastData={forecastData} />
            </Paper>
          </Box>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;


