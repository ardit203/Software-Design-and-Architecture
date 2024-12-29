import "./CSS/Home.css";
import { Link } from "react-router-dom";

import IssuersData from "./IssuersData";
import TechnicalAnalysis from "./TechnicalAnalysis";
import FundamentalAnalysis from "./FundamentalAnalysis";
import StockPrediction from "./StockPrediction";

function Home() {
  return (
    <div className="home-container">
      <div className="header-text">
        <span>Welcome to Macedonian Stock Exchange Analyzer</span>
      </div>

      <div className="main">
        {/* <div className="cp">
          <div className="cp-title">
            <span>Current Performance</span>
          </div>

          <div className="cp-placeholder"></div>
        </div>

        
        <div className="latest-news">
          <div className="latest-news-title">
            <span>Latest News</span>
          </div>

          <div className="latest-news-placeholder"></div>
        </div> */}
        <div class="intro-container">
    <div class="grid-container">

      <div class="grid-item">
        <h2>Explore Issuers' Data</h2>
        <p>Access detailed stock information for Macedonian companies.</p>
        <Link to="/issuers-data" className="btn">Go to Issuers Data</Link>
      </div>

      

      <div class="grid-item">
        <h2>Analyze Stock Trends</h2>
        <p>Use advanced technical indicators to forecast market behavior.</p>
        <Link to="/technical-analysis" className="btn">Go to Technical Analysis</Link>
      </div>

      <div class="grid-item">
        <h2>Fundamental Analysis</h2>
        <p>Evaluate the sentiment around companies based on news and trends.</p>
        <Link to="/fundamental-analysis" className="btn">Go to Fundamental Analysis</Link>
      </div>

      <div class="grid-item">
        <h2>Predict Future Stock Prices with LSTM</h2>
        <p>Harness the power of LSTM networks to forecast stock price movements for smarter investment strategies.</p>
        <Link to="/stock-prediction" className="btn">Go to Stock Prediction</Link>
      </div>

    </div>

    <div class="intro-footer">
      <p>&copy; 2024 Macedonian Stock Exchange Analysis Hub. All rights reserved.</p>
    </div>
  </div>



      </div>
    </div>
  );
}

export default Home;
