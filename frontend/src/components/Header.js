import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  IconButton,
  Chip,
} from '@mui/material';
import {
  TrendingUp,
  Refresh,
  Settings,
  Notifications,
} from '@mui/icons-material';

const Header = () => {
  const currentPrice = 247.68;
  const change = 5.23;
  const changePercent = 2.16;

  return (
    <AppBar 
      position="static" 
      elevation={0}
      sx={{
        background: 'rgba(0, 0, 0, 0.3)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
      }}
    >
      <Toolbar>
        {/* Logo and Title */}
        <Box display="flex" alignItems="center" flexGrow={1}>
          <TrendingUp sx={{ mr: 2, color: 'primary.main' }} />
          <Typography variant="h5" component="div" fontWeight="bold">
            Tesla Stock Forecast
          </Typography>
        </Box>

        {/* Current Price Display */}
        <Box display="flex" alignItems="center" mr={3}>
          <Typography variant="h6" sx={{ mr: 2 }}>
            TSLA
          </Typography>
          <Typography variant="h5" sx={{ mr: 1 }}>
            ${currentPrice}
          </Typography>
          <Chip
            label={`${change > 0 ? '+' : ''}${change} (${change > 0 ? '+' : ''}${changePercent}%)`}
            color={change > 0 ? 'success' : 'error'}
            size="small"
            sx={{ ml: 1 }}
          />
        </Box>

        {/* Action Buttons */}
        <Box display="flex" alignItems="center">
          <IconButton color="inherit" title="Refresh Data">
            <Refresh />
          </IconButton>
          <IconButton color="inherit" title="Notifications">
            <Notifications />
          </IconButton>
          <IconButton color="inherit" title="Settings">
            <Settings />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;


