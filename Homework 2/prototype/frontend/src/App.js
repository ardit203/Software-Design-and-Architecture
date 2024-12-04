import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './screens/Home';
import IssuersData from './screens/IssuersData';
import TechnicalAnalysis from './screens/TechnicalAnalysis';
import FundamentalAnalysis from './screens/FundamentalAnalysis';
import StockPrediction from './screens/StockPrediction';

function App() {
  return (
    <Router>
      <div>
        
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/issuers-data">Issuers Data</Link></li>
            <li><Link to="/technical-analysis">Technical Analysis</Link></li>
            <li><Link to="/fundamental-analysis">Fundamental Analysis</Link></li>
            <li><Link to="/stock-prediction">Stock Prediction</Link></li>
          </ul>
        </nav>

        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/issuers-data" element={<IssuersData />} />
          <Route path="/technical-analysis" element={<TechnicalAnalysis />} />
          <Route path="/fundamental-analysis" element={<FundamentalAnalysis />} />
          <Route path="/stock-prediction" element={<StockPrediction />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
