import React, { useState, useEffect } from "react";
import axios from "axios";
import "./CSS/IssuersData.css";
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
import zoomPlugin from "chartjs-plugin-zoom";

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

const IssuersData = () => {
  const [issuers, setIssuers] = useState([]);
  const [selectedIssuer, setSelectedIssuer] = useState("");
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const [issuerData, setIssuerData] = useState([]);
  const [selectedFeature, setSelectedFeature] = useState("");
  const [chartData, setChartData] = useState(null);
  const [chartHeight, setChartHeight] = useState();
  const [showDiv, setShowDiv] = useState(false);

  useEffect(() => {
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

  const fetchIssuerData = () => {
    if (!selectedIssuer || !fromDate || !toDate) {
      alert("Please select an issuer and specify both From and To dates.");
      return;
    }

    axios
      .post(`${process.env.REACT_APP_BACKEND_HOST}/api/issuer-data`, {
        issuer: selectedIssuer,
        from_date: fromDate,
        to_date: toDate,
      })
      .then((response) => {
        setIssuerData(response.data);
        setShowDiv(true);
        console.log(issuerData);
      })
      .catch((error) => {
        console.error("Error fetching issuer data:", error);
      });
  };

  const generateChartData = () => {
    setChartHeight(60);
    if (!issuerData[1] || !selectedFeature) {
      alert("Please select a feature and ensure data is available.");
      return;
    }
    console.log(selectedFeature);
    const data = {
      labels: issuerData[1].map((row) => row["Date"]),
      datasets: [
        {
          label: selectedFeature,
          data: issuerData[1].map((row) => row[selectedFeature]),
          borderColor: "#4A90E2",
          backgroundColor: "#7AB8F5",
          pointRadius: 6,
          pointHoverRadius: 6,
          borderWidth: 2,
          tension: 0.4,
          fill: false,
        },
      ],
    };
    setChartData(data);
  };

  const columnOrder = [
    "Date",
    "Last trade price",
    "Max",
    "Min",
    "Avg.Price",
    "%chg.",
    "Volume",
    "Turnover in BEST in denars",
    "Total turnover in denars",
  ];

  return (
    <div>
      <div className="header-2">
        <strong>Issuers Data</strong>
      </div>

      {/* ISSUER DATA */}
      <div className="issuers-data-2">
        <div className="table-info-2">
          <div className="search-2">
            <label htmlFor="issuer-select-2">Symbol</label>
            <br />
            <select
              className="input-2"
              id="issuer-select-2"
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

          <div className="from-date-2">
            <label>From date</label>
            <br />
            <input
              className="input-2"
              type="date"
              value={fromDate}
              onChange={(e) => setFromDate(e.target.value)}
            />
          </div>

          <div className="to-date-2">
            <label>To date</label>
            <br />
            <input
              className="input-2"
              type="date"
              value={toDate}
              onChange={(e) => setToDate(e.target.value)}
            />
          </div>

          <div className="find-2">
            <button className="btn-2" onClick={fetchIssuerData}>
              Find
            </button>
          </div>
        </div>

        <div
          className="table-container-2"
          style={{
            maxHeight: "400px", // Limit the height of the container
            overflowY: "auto", // Enable vertical scrolling for the table body
          }}
        >
          {Array.isArray(issuerData[0]) && issuerData[0].length > 0 ? (
            <table className="table-2">
              <thead style={{ position: "sticky", top: "0" }}>
                <tr>
                  {columnOrder.map((col) => (
                    <th key={col}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {issuerData[0].map((row, index) => (
                  <tr key={index}>
                    {columnOrder.map((col, i) => (
                      <td key={i}>{row[col]}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="no-data-2">
              No data available for the selected issuer.
            </p>
          )}
        </div>
      </div>

      {showDiv && (
        <div className="Apear-After">
          <div className="header-2-2">
            <strong>Visualization</strong>
          </div>

          {/* ISSUER VISUALIZATION */}
          <div className="issuers-vis-2">
            <div className="table-info-vis-2">
              <div className="search-vis-2">
                <label htmlFor="feature-select-2">Feature</label>
                <br />
                <select
                  className="input-2"
                  id="feature-select-2"
                  value={selectedFeature}
                  onChange={(e) => setSelectedFeature(e.target.value)}
                >
                  <option value="">-- Select a Feature --</option>
                  {columnOrder.slice(1).map((feature) => (
                    <option key={feature} value={feature}>
                      {feature}
                    </option>
                  ))}
                </select>
              </div>

              <div className="find-vis-2">
                <button className="btn-2" onClick={generateChartData}>
                  Generate
                </button>
              </div>
            </div>

            <div
              className="chart-container-2"
              style={{
                height: `${chartHeight}vh`,
                transition: "height 0.3s ease",
              }}
            >
              {chartData ? (
                <Line
                  id="chart-id-2"
                  data={chartData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: { position: "top" },
                      title: {
                        display: true,
                        text: `Feature: ${selectedFeature}`,
                        font: { size: 16 },
                      },

                      zoom: {
                        pan: { enabled: true, mode: "x" },
                        zoom: {
                          wheel: { enabled: true },
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
                          text: "Value",
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
              ) : (
                <div className="no-data-2">
                  <p>No chart data available</p>
                </div>
              )}
            </div>
            <div className="reset-2">
              <button
                className="btn-2"
                onClick={() => {
                  const chartInstance = ChartJS.getChart("chart-id-2");
                  if (chartInstance) {
                    chartInstance.resetZoom();
                  }
                }}
              >
                Reset Zoom
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default IssuersData;
