import React, { useState, useEffect } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import "./CSS/StockPrediction.css";
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

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend,
  CategoryScale
);

function StockPrediction() {
  const [issuers, setIssuers] = useState([]);
  const [selectedIssuer, setSelectedIssuer] = useState("");
  const [selectedTime, setSelectedTime] = useState("");
  const [tableData, setTableData] = useState([]);
  const [chartData, setChartData] = useState(null);
  const [chartHeight, setChartHeight] = useState();
  const [showDiv, setShowDiv] = useState(false);

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_BACKEND_HOST}/api/prediction-issuers`)
      .then((response) => {
        setIssuers(response.data || []);
      })
      .catch((error) => {
        console.error("Error fetching issuers:", error);
        setIssuers([]);
      });
  }, []);

  const prediction = () => {
    if (!selectedIssuer || !selectedTime) {
      alert("Please select all options before predicting.");
      return;
    }

    const requestData = { issuer: selectedIssuer, timeframe: selectedTime };

    axios
      .post(`${process.env.REACT_APP_BACKEND_HOST}/api/prediction`, requestData)
      .then((response) => {
        setTableData(response.data);
        console.log(tableData);
        generateChartData(response.data);
        setChartHeight(60);
        setShowDiv(true);
      })
      .catch((error) => {
        console.error("Error analyzing data:", error);
      });
  };

  const generateChartData = (data) => {
    const historical = data[0] || [];
    const predicted = data[1] || [];
    const allDates = data[3] || [];

    const historicalPrices = allDates.map(
      (date) =>
        historical.find((d) => d.Date === date)?.["Last trade price"] || null
    );
    const predictedPrices = allDates.map(
      (date) =>
        predicted.find((d) => d.Date === date)?.["Last trade price"] || null
    );

    setChartData({
      labels: allDates,
      datasets: [
        {
          label: "Historical Prices",
          data: historicalPrices,
          borderColor: "#4A90E2",
          backgroundColor: "#7AB8F5",
          borderWidth: 2,
          tension: 0.4,
          fill: false,
          pointRadius: 6,
          pointHoverRadius: 6,
        },
        {
          label: "Predicted Prices",
          data: predictedPrices,
          borderColor: "#50C878",
          backgroundColor: "#98FF98",
          borderWidth: 2,
          tension: 0.4,
          fill: false,
          pointRadius: 6,
          pointHoverRadius: 6,
        },
      ],
    });
  };

  return (
    <div>
      <div className="prediction-header">
        <strong>LSTM Prediction</strong>
      </div>

      <div className="prediction-container">
        <div className="prediction-info">
          <div className="search-4">
            <label htmlFor="issuer-select-4">Symbol</label>
            <br />
            <select
              className="input-4"
              id="issuer-select-4"
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

          <div className="search-4">
            <label htmlFor="time-select-4">Days</label>
            <br />
            <select
              className="input-4"
              id="time-select-4"
              value={selectedTime}
              onChange={(e) => setSelectedTime(e.target.value)}
            >
              <option value="">-- Select Timeframe --</option>
              <option value="1">1 Days</option>
              <option value="2">2 Days</option>
              <option value="3">3 Days</option>
              <option value="4">4 Days</option>
              <option value="5">5 Days</option>
              <option value="10">10 Days</option>
            </select>
          </div>

          <div className="find-4">
            <button className="btn-4" onClick={prediction}>
              Predict
            </button>
          </div>
        </div>
      </div>

      {showDiv && (
        <div>
          <div className="prediction-header">
            <strong>Metrics</strong>
          </div>

          <div className="where-table-is-prediction">
            {tableData.length === 0 ? (
              <p className="no-data-text">No data available</p>
            ) : (
              <div class="table-container">
                <div className="table-section">
                  <div className="section-header" id="hd2">

                  <div className="table-cell" id="hd">Date</div>
                    <div className="table-cell" id="hd">
                      Predicted Price
                    </div>
                  </div>
                  {tableData[4]?.map((row, index) => (
                    <div className="table-row" key={index}>
                      <div className="table-cell">{row["Date"]}</div>
                      <div className="table-cell">
                        {row["Last trade price"]}
                      </div>
                    </div>
                  ))}
                </div>

                {/* <!-- Evaluation Metrics Section --> */}
                <div className="table-section">
                  <div className="section-header">Evaluation Metrics</div>

                  <div className="table-row">
                    <div className="table-cell">R2 Score</div>
                    <div className="table-cell">
                      {tableData[2][0]["r2_score"]}
                    </div>
                  </div>

                  <div className="table-row">
                    <div className="table-cell">Explained Variance Score</div>
                    <div className="table-cell">
                      {tableData[2][0]["Explained Variance Score"]}
                    </div>
                  </div>

                  <div className="table-row">
                    <div className="table-cell">Mean Squared Error</div>
                    <div className="table-cell">
                      {tableData[2][0]["Mean Squared Error"]}
                    </div>
                  </div>

                  <div className="table-row">
                    <div className="table-cell">Mean Absolute Error</div>
                    <div className="table-cell">
                      {tableData[2][0]["Mean Absolute Error"]}
                    </div>
                  </div>

                  <div className="table-row">
                    <div className="table-cell">
                      Mean Absolute Percentage Error
                    </div>
                    <div className="table-cell">
                      {tableData[2][0]["Mean Absolute Percentage Error"]}
                    </div>
                  </div>

                  <div className="table-row">
                    <div className="table-cell">Mean Squared Log Error</div>
                    <div className="table-cell">
                      {tableData[2][0]["Mean Squared Log Error"]}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="prediction-header">
            <strong>Visualization</strong>
          </div>
          <div
            className="chart-container-prediction"
            style={{
              height: `${chartHeight}vh`, // Dynamic height based on state
              transition: "height 0.3s ease", // Smooth height transition
            }}
          >
            {chartData ? (
              <Line
                data={chartData}
                id="prediction-id"
                className="chart"
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: { position: "top" },
                    title: {
                      display: true,
                      text: `Price Prediction Chart`,
                      font:{ size: 16}
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
                      title: { display: true, text: "Date", font:{ size: 16} },
                      ticks: {
                        font: {
                          size: 14, // Change this value to increase font size
                        },
                      },
                    },
                    y: {
                      title: { display: true, text: "Price", font:{ size: 16} },
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
              <p className="no-data-text-prediction">No chart data available</p>
            )}
          </div>

          <div className="reset-prediction">
            <button
              className="btn-4"
              onClick={() => {
                const chartInstance = ChartJS.getChart("prediction-id");
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

export default StockPrediction;
