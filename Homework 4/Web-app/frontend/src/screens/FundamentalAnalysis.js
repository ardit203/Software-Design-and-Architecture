import "./CSS/FundamentalAnalysis.css";
import React, { useState, useEffect } from "react";
import axios from "axios";

function FundamentalAnalysis() {
  const [message, setMessage] = useState(""); // State for the message
  const [issuers, setIssuers] = useState([]);
  const [selectedIssuer, setSelectedIssuer] = useState("");
  const [resultStyle, setResultStyle] = useState({}); // State for dynamic styling

  useEffect(() => {
    // get(`${process.env.REACT_APP_BACKEND_HOST}/api/issuers`)
    axios
      .get(`${process.env.REACT_APP_BACKEND_HOST}/api/issuers`)
      .then((response) => {
        setIssuers(response.data || []);
      })
      .catch((error) => {
        console.error("Error fetching issuers:", error);
        setIssuers([]);
      });
  }, []);

  const fundamental = () => {
    if (!selectedIssuer) {
      alert("Please select an issuer!");
      return;
    }

    axios
      .post(`${process.env.REACT_APP_BACKEND_HOST}/api/sentiment-analyze`, {
        issuer: selectedIssuer,
      })
      .then((response) => {
        const data = response.data;
        console.log(data);

        // Determine sentiment and recommendation
        let sentimentMessage =
          "The sentiment analysis indicates a Neutral position.";
        let style = {
          backgroundColor: "white",
          borderRadius: "0.625em", // Replaced 10px with em
          boxShadow: "0 0.125em 0.25em rgba(0, 0, 0, 0.1)", // Replaced px with em
          border: "0.0625em solid #ddd", // Replaced px with em
          // display: "flex",
          padding: "0.625em", // Replaced 10px with em
          justifyContent: "center",
          textAlign: "center", // Fixed typo from 'cneter' to 'center'
          margin: "2% 15%", // Replaced 30px 300px with %
          fontWeight: "bold",
          fontSize: "1rem", // Replaced 16px with rem
          fontFamily: "'Exo 2', sans-serif",
          color: "white",
        };

        if (data[0]["Label"] == "POSITIVE") {
          sentimentMessage =
            "The sentiment analysis for " +
            selectedIssuer +
            " is Positive, and it indicates a Buy.";
          style["backgroundColor"] = "#28a745";
        } else if (data[0]["Label"] == "NEGATIVE") {
          sentimentMessage =
            "The sentiment analysis for " +
            selectedIssuer +
            " is Negative, and it indicates a Sell.";
          style["backgroundColor"] = "#dc3545";
        } else if (data[0]["Label"] == "NEUTRAL-NO-NEWS") {
          sentimentMessage =
            "There were no up to date news to confirm the sentiment analysis of " +
            selectedIssuer +
            ".";
          style["backgroundColor"] = "#6c757d";
        }

        setMessage(sentimentMessage); // Update the message state
        setResultStyle(style); // Update the style state
        console.log(message);
      })
      .catch((error) => {
        console.error("Error fetching issuer data:", error);
        setMessage("An error occurred while fetching data.");
        setResultStyle({ color: "black", backgroundColor: "lightcoral" }); // Error style
      });
  };

  return (
    <div>
      <div className="fundamental-header">
        <strong>Fundamental Analysis</strong>
      </div>

      <div className="fundamental-container">
        <div className="fundamental-info">
          <div className="search-3">
            <label htmlFor="issuer-select-3">Symbol</label>
            <br />
            <select
              className="input-3"
              id="issuer-select-3"
              value={selectedIssuer}
              onChange={(e) => setSelectedIssuer(e.target.value)}
            >
              <option value="">-- Select an Issuer --</option>
              {issuers.map((issuer) => (
                <option key={issuer} value={issuer}>
                  {issuer}
                </option>
              ))}
            </select>
          </div>

          <div className="find-3">
            <button className="btn-2" onClick={fundamental}>
              Find
            </button>
          </div>
        </div>
      </div>

      <div className="result" style={resultStyle}>
        {message && <p className="message">{message}</p>}
      </div>
    </div>
  );
}

export default FundamentalAnalysis;
