import React, { useState, useEffect } from "react";
import axios from "axios";
import "./CSS/TechnicalAnalysis.css";

import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
} from "chart.js";
import zoomPlugin from "chartjs-plugin-zoom"; // Import zoom plugin

// Register necessary Chart.js components, including the Zoom plugin
ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  zoomPlugin
);

function TechnicalAnalysis() {
  const [issuers, setIssuers] = useState([]);
  const [selectedIssuer, setSelectedIssuer] = useState("");
  const [selectedIndicator, setSelectedIndicator] = useState("");
  const [fromDate, setFromDate] = useState(null); // State for "From date"
  const [tableData, setTableData] = useState([]);
  const [chartHeight, setChartHeight] = useState(); // Default height for the chart container
  const [showDiv, setShowDiv] = useState(false);

  // Fetch issuers from backend
  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_BACKEND_HOST}/api/issuers`)
      .then((response) => {
        console.log("Fetched issuers:", response.data); // Debugging: Log the list of issuers
        // setIssuers(response.data.issuers);
        setIssuers(response.data || []); // Ensure it's an array
      })
      .catch((error) => {
        console.error("Error fetching issuers:", error);
      });
  }, []);

  // Handle Analyze button click
  const handleAnalyze = () => {
    if (!selectedIssuer || !selectedIndicator) {
      alert("Please select all options before analyzing.");
      return;
    }

    const requestData = {
      issuer: selectedIssuer,
      indicator: selectedIndicator,
      from_date: fromDate,
    };
    console.log(selectedIssuer);
    console.log(selectedIndicator);
    console.log(fromDate);
    axios
      .post(`${process.env.REACT_APP_BACKEND_HOST}/api/tech-analyze`, requestData)
      .then((response) => {
        console.log("Response Data:", response.data); // Check the response structure
        setTableData(response.data); // Ensure tableData is an array
        setChartHeight(60);
        setShowDiv(true);
      })
      .catch((error) => {
        console.error("Error analyzing data:", error);
      });
  };

  const getChartData = () => {
    if (tableData.length === 0) return null;
    return {
      labels: tableData.map((row) => row["Date"]), // x-axis labels (Dates)
      datasets: [
        {
          label: "1 Day " + selectedIndicator || "Indicator", // Dataset 2: Indicator values
          data: tableData.map((row) => row["1 Day " + selectedIndicator]),
          borderColor: "rgba(255, 99, 132, 1)", // Line color

          backgroundColor: "rgba(255, 99, 132, 0.2)", // Fill color (optional)
          borderWidth: 2, // Line thickness
          tension: 0.4, // Smooth line
          fill: false,
          pointRadius: 6,
          pointHoverRadius: 6, // No area fill
        },
        {
          label: "1 Week " + selectedIndicator || "Indicator", // Dataset 2: Indicator values
          data: tableData.map((row) => row["1 Week " + selectedIndicator]),
          borderColor: "#4A90E2",
          backgroundColor: "#7AB8F5", // Fill color (optional)
          borderWidth: 2, // Line thickness
          tension: 0.4, // Smooth line
          fill: false,
          pointRadius: 6,
          pointHoverRadius: 6, // No area fill
        },
        {
          label: "1 Month " + selectedIndicator || "Indicator", // Dataset 2: Indicator values
          data: tableData.map((row) => row["1 Month " + selectedIndicator]),
          borderColor: "#50C878", // Line color

          backgroundColor: "#98FF98", // Fill color (optional)
          borderWidth: 2, // Line thickness
          tension: 0.4, // Smooth line
          fill: false,
          pointRadius: 6,
          pointHoverRadius: 6, // No area fill
        },
      ],
    };
  };

  return (
    <div className="tech">
      <div className="h-text">
        <strong>Technical Analysis</strong>
      </div>

      <div className="main-container">
        <div className="indicator-info">
          <div className="issuers-search">
            <label htmlFor="issuer-select">Symbol</label>
            <br />
            <select
              className="input"
              id="issuer-select"
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

          <div className="indicator-search">
            <label htmlFor="indicator-select">Indicator</label>
            <br />
            <select
              className="input"
              id="indicator-select"
              value={selectedIndicator}
              onChange={(e) => setSelectedIndicator(e.target.value)}
            >
              <option value="">-- Select an Indicator --</option>
              <optgroup label="Moving Averages">
                <option value="SMA">Simple Moving Average</option>
                <option value="EMA">Exponential Moving Average</option>
                <option value="WMA">Weighted Moving Average</option>
                <option value="HMA">Hull Moving Average</option>
                <option value="TEMA">
                  Triple Exponential Moving Average
                </option>
              </optgroup>
              <optgroup label="Oscillators">
                <option value="RSI">Relative Strength Index</option>
                <option value="STOCH">Stochastic Oscillator</option>
                <option value="CCI">Commodity Channel Index</option>
                <option value="Williams %R">
                  Williams %R
                </option>
                <option value="CMO">Chande Momentum Oscillator</option>
              </optgroup>

              {/* Add other indicators */}
            </select>
          </div>
          <div className="from-date">
            <label>From date</label>
            <br />
            <input
              className="input"
              type="date"
              value={fromDate}
              onChange={(e) => setFromDate(e.target.value)}
            />
          </div>
          <div className="analyze-btn">
            <button className="btn" onClick={handleAnalyze}>
              Analyze
            </button>
          </div>
        </div>

        <div className="where-table-is">
          {tableData.length === 0 ? (
            <p className="no-data-text">No data available</p>
          ) : (
            <table className="table-tech">
              <thead>
                <tr>
                  <th>Issuer</th>
                  <th>Indicator</th>
                  <th>1 Day Signal</th>
                  <th>1 Week Signal</th>
                  <th>1 Month Signal</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{selectedIssuer}</td>
                  <td>{selectedIndicator}</td>
                  <td>
                    {
                      tableData[tableData.length - 1][
                        "1 Day " + selectedIndicator + " Signals"
                      ]
                    }
                  </td>
                  <td>
                    {
                      tableData[tableData.length - 1][
                        "1 Week " + selectedIndicator + " Signals"
                      ]
                    }
                  </td>
                  <td>
                    {
                      tableData[tableData.length - 1][
                        "1 Month " + selectedIndicator + " Signals"
                      ]
                    }
                  </td>
                </tr>
              </tbody>
            </table>
          )}
        </div>
      </div>

      {showDiv && (
        <div>
          <div className="f-text">
            <strong>Visualization</strong>
          </div>
          <div
            className="chart-container"
            style={{
              height: `${chartHeight}vh`, // Dynamic height based on state
              transition: "height 0.3s ease", // Smooth height transition
            }}
          >
            {tableData.length === 0 ? (
              <p className="no-data-text">No chart data available</p>
            ) : (
              <Line
                id="chart-id"
                className="chart"
                data={getChartData()}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: { position: "top" },
                    title: {
                      display: true,
                      text: `Technical Analysis Chart - ${selectedIssuer} (${selectedIndicator})`,
                      font: { size: 16 },
                    },
                    zoom: {
                      pan: {
                        enabled: true,
                        mode: "x",
                      },
                      zoom: {
                        wheel: {
                          enabled: true,
                        },
                        pinch: {
                          enabled: true,
                        },
                        mode: "x",
                      },
                    },
                  },
                  scales: {
                    x: {
                      title: {
                        display: true,
                        text: "Date",
                        font: { size: 16 },
                      },
                      ticks: {
                        font: {
                          size: 14, // Change this value to increase font size
                        },
                      },
                    },
                    y: {
                      title: {
                        display: true,
                        text: "Price",
                        font: { size: 16 },
                      },
                      ticks: {
                        font: {
                          size: 14, // Change this value to increase font size
                        },
                      },
                    },
                  },
                }}
              />
            )}
          </div>
          <div className="reset">
            <button
              className="btn"
              onClick={() => {
                const chartInstance = ChartJS.getChart("chart-id");
                if (chartInstance) {
                  chartInstance.resetZoom();
                }
              }}
            >
              Reset Zoom
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default TechnicalAnalysis;
