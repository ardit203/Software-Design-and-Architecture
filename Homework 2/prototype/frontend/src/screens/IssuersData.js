import React, { useState, useEffect } from 'react';
import axios from 'axios';

const IssuersData = () => {
  const [issuers, setIssuers] = useState([]); // State for issuers list
  const [selectedIssuer, setSelectedIssuer] = useState(''); // State for selected issuer
  const [issuerData, setIssuerData] = useState([]); // State for the data of the selected issuer

  // Fetch issuers on component mount
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/issuers')
      .then((response) => {
        console.log('Fetched issuers:', response.data.issuers); // Debugging: Log the list of issuers
        setIssuers(response.data.issuers);
      })
      .catch((error) => {
        console.error('Error fetching issuers:', error);
      });
  }, []);

  // Fetch data for the selected issuer
  const fetchIssuerData = (issuer) => {
    console.log('Fetching data for issuer:', issuer); // Debugging: Log the issuer being selected
    axios.post('http://127.0.0.1:5000/api/issuer-data', { issuer })
      .then((response) => {
        console.log('API Response for issuer data:', response.data); // Debugging: Log the response data
        setIssuerData(response.data); // Assuming response.data is an array
      })
      .catch((error) => {
        console.error('Error fetching issuer data:', error);
      });
  };

  // Define the desired order of columns
  const columnOrder = [
    'Date',
    'Last trade price',
    'Max',
    'Min',
    'Avg.Price',
    '%chg.',
    'Volume',
    'Turnover in BEST in denars',
    'Total turnover in denars'
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h2>Issuers List</h2>
      <label htmlFor="issuer-select">Select an Issuer:</label>
      <select
        id="issuer-select"
        value={selectedIssuer}
        onChange={(e) => {
          const issuer = e.target.value;
          setSelectedIssuer(issuer);
          fetchIssuerData(issuer); // Fetch data when issuer changes
        }}
        style={{ margin: '10px 0', padding: '5px' }}
      >
        <option value="">-- Select an Issuer --</option>
        {issuers.map((issuer) => (
          <option key={issuer} value={issuer}>
            {issuer}
          </option>
        ))}
      </select>

      <div style={{ marginTop: '20px' }}>
        <h3>Issuer Data</h3>
        {Array.isArray(issuerData) && issuerData.length > 0 ? (
          <table border="1" cellPadding="10" cellSpacing="0" style={{ borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                {/* Render column headers in the specified order */}
                {columnOrder.map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {issuerData.map((row, index) => (
                <tr key={index}>
                  {/* Render values based on the defined column order */}
                  {columnOrder.map((col, i) => (
                    <td key={i}>{row[col]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No data available for the selected issuer.</p>
        )}
      </div>
    </div>
  );
};

export default IssuersData;
