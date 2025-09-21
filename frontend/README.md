# Tesla Stock Forecast App - Frontend

A modern React application with glassmorphism design for Tesla stock forecasting and analysis.

## 🚀 Features

- **Interactive Stock Charts**: Candlestick, line, and volume charts using Chart.js
- **Real-time Data Visualization**: Live stock data with WebSocket support
- **AI-Powered Forecasts**: Machine learning predictions with confidence scores
- **Glassmorphism Design**: Modern UI with blur effects and transparency
- **Mobile Responsive**: Optimized for all device sizes
- **Material-UI Components**: Professional component library integration

## 🛠️ Tech Stack

- **React 18**: Modern React with hooks and functional components
- **Chart.js**: Interactive charts and data visualization
- **Material-UI**: Component library and theming
- **WebSocket**: Real-time data streaming
- **Axios**: HTTP client for API calls
- **CSS3**: Glassmorphism effects and animations

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template with loading screen
├── src/
│   ├── components/         # React components
│   │   ├── Header.js       # Navigation and price display
│   │   ├── StockInfo.js    # Stock metrics and information
│   │   ├── StockChart.js   # Interactive chart component
│   │   └── ForecastPanel.js # AI forecast display
│   ├── styles/
│   │   └── App.css         # Glassmorphism styles
│   ├── App.js              # Main application component
│   └── index.js            # React DOM entry point
├── package.json            # Dependencies and scripts
└── README.md              # This file
```

## 🎨 Design Features

### Glassmorphism Effects
- Semi-transparent backgrounds with blur effects
- Subtle borders and shadows
- Smooth hover animations
- Gradient text effects

### Responsive Design
- Mobile-first approach
- Flexible grid layouts
- Adaptive chart sizing
- Touch-friendly interactions

### Color Scheme
- Primary: #00ff88 (Tesla Green)
- Secondary: #ff6b6b (Alert Red)
- Background: Dark gradient
- Text: High contrast white

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ 
- npm or yarn

### Installation
```bash
cd frontend
npm install
```

### Development
```bash
npm start
```
Opens http://localhost:3000

### Build
```bash
npm run build
```
Creates production build in `build/` folder

### Test
```bash
npm test
```
Runs test suite

## 📊 Components

### Header
- Tesla logo and branding
- Current stock price display
- Price change indicators
- Action buttons (refresh, notifications, settings)

### StockInfo
- Key stock metrics
- Price range visualization
- Volume analysis
- Performance indicators

### StockChart
- Multiple chart types (candlestick, line, volume)
- Interactive tooltips
- Time range selection
- Real-time updates

### ForecastPanel
- AI-powered price predictions
- Confidence scores
- Forecast metrics
- Risk indicators

## 🔧 Configuration

### Environment Variables
Create `.env` file:
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WS_URL=ws://localhost:8000/ws
REACT_APP_TESLA_SYMBOL=TSLA
```

### Chart Configuration
Charts are configured in `StockChart.js`:
- Chart types and options
- Color schemes
- Animation settings
- Responsive behavior

## 📱 Mobile Support

- Responsive breakpoints
- Touch gestures
- Optimized chart sizing
- Mobile navigation

## 🎯 Performance

- Lazy loading for charts
- Optimized re-renders
- Efficient state management
- Minimal bundle size

## 🔮 Future Enhancements

- Real-time WebSocket integration
- Advanced chart indicators
- Portfolio tracking
- News sentiment analysis
- Social media sentiment
- Options analysis

## 📝 Development Notes

- Follows V2 compliance (files < 400 lines)
- Uses functional components with hooks
- Implements proper error boundaries
- Includes loading states
- Mobile-first responsive design

## 🐛 Troubleshooting

### Common Issues
1. **Charts not rendering**: Check Chart.js dependencies
2. **Styling issues**: Verify CSS imports
3. **Build errors**: Clear node_modules and reinstall

### Debug Mode
Set `REACT_APP_DEBUG=true` in `.env` for additional logging

## 📄 License

This project is part of the Agent Cellphone V2 Repository.


