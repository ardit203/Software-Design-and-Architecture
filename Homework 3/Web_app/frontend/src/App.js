import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./screens/Home";
import IssuersData from "./screens/IssuersData";
import TechnicalAnalysis from "./screens/TechnicalAnalysis";
import FundamentalAnalysis from "./screens/FundamentalAnalysis";
import StockPrediction from "./screens/StockPrediction";
import "./App.css";
import GitHubLogo from "./acc/github-logo.png";

console.log(
  Home,
  IssuersData,
  TechnicalAnalysis,
  FundamentalAnalysis,
  StockPrediction
);

function App() {
  return (
    <Router>
      <div className="app-container">
        {/* Header and Navigation  style={{ width: '100%' }}*/}
        <nav>
          <div className="nav-container">
            <table className="nav-table">
              <thead>
                <tr>
                  <td>
                    <a href="/" className="MSE-Analyzer">
                      MSE Analyzer
                    </a>
                  </td>
                  <td align="right">
                    <Link to="/" className="nav-link">
                      Home
                    </Link>
                    <Link to="/issuers-data" className="nav-link">
                      Issuers Data
                    </Link>
                    <Link to="/technical-analysis" className="nav-link">
                      Technical Analysis
                    </Link>
                    <Link to="/fundamental-analysis" className="nav-link">
                      Fundamental Analysis
                    </Link>
                    <Link to="/stock-prediction" className="nav-link">
                      Stock Prediction
                    </Link>
                  </td>
                </tr>
              </thead>
            </table>
          </div>
        </nav>

        {/* Main Content */}
        <div className="content-container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/issuers-data" element={<IssuersData />} />
            <Route path="/technical-analysis" element={<TechnicalAnalysis />} />
            <Route
              path="/fundamental-analysis"
              element={<FundamentalAnalysis />}
            />
            <Route path="/stock-prediction" element={<StockPrediction />} />
          </Routes>
        </div>

        {/* Footer */}
        <footer>
          <div className="footer-container">
            <div className="footer-email-container">
              <strong className="footer-text-spc">Contact Info</strong>
              <br />
              <p>
                <a
                  href="mailto:arditselmani203@gmail.com"
                  className="footer-text"
                >
                  arditselmani203@gmail.com
                </a>
                <br />
                <a href="mailto:sabribrahimi@gmail.com" className="footer-text">
                  sabribrahimi@gmail.com
                </a>
                <br />
                <a href="mailto:hamdiademi@gmail.com" className="footer-text">
                  hamdiademi@gmail.com
                </a>
                <br />
              </p>
            </div>

            <div className="footer-github-container">
              <a
                href="https://github.com/ardit203/Software-Design-and-Architecture/tree/main"
                className="footer-text" target="blank"
              >
                <img
                  src={GitHubLogo}
                  height="60px"
                  width="60px"
                  alt="GitHub Logo - View the project on GitHub"
                />
                <br />
                View Project on GitHub
              </a>
            </div>

            <div className="footer-links-container">
              <strong className="footer-text-spc">Resources</strong>
              <br />
              <p>
                <a href="/privacy-policy" className="footer-text">
                  Privacy Policy
                </a>
                <br />
                <a href="/terms" className="footer-text">
                  Terms of Service
                </a>
                <br />
                <a href="/documentation" className="footer-text">
                  Documentation
                </a>
                <br />
              </p>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
