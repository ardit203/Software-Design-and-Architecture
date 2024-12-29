import "./CSS/FundamentalAnalysis.css";
import React, { useState, useEffect } from "react";
import axios from "axios";





function FundamentalAnalysis() {

  const [message, setMessage] = useState(""); // State for the message
  const [issuers, setIssuers] = useState([]);
  const [selectedIssuer, setSelectedIssuer] = useState("");
  const [text, setText] = useState("")
  const [pdf_text, setPDFText] = useState("")
  
  const [resultStyle, setResultStyle] = useState({}); // State for dynamic styling

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/api/issuers")
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
        .post("http://127.0.0.1:5000/api/sentiment-analyze", {issuer: selectedIssuer})
        .then((response) => {
          // setText('')
          // setPDFText('')
            const data = response.data;
            console.log(data)

            

            // Determine sentiment and recommendation
            let sentimentMessage = "The sentiment analysis indicates a Neutral position.";
            let style={
              backgroundColor: "white",
              borderRadius: "10px",
              boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
              border: "1px solid #ddd",
              // display: "flex",
              padding: "10px",
              justifyContent: "center",
              textAlign: 'cneter',
              margin: "30px 100px",
              fontWeight: 'bold',
              fontSize: '16px',
              fontFamily: "'Exo 2', sans-serif",
              color: "black"
          }

            if (data[0] == 'POSITIVE') {
                sentimentMessage = "The sentiment analysis for " + selectedIssuer + " is Positive, and it indicates a Buy.";
                style['color'] = '#50C878'



            } else if (data[0] == 'NEGATIVE') {
                sentimentMessage = "The sentiment analysis for " + selectedIssuer + " is Negative, and it indicates a Sell.";
                style['color'] = 'rgba(255, 99, 132, 1)'



            }else if (data[0] == 'NEUTRAL-NO-NEWS'){
              sentimentMessage = 'There were no up to date news to confirm the sentiment analysis of ' + selectedIssuer + '.'
              style['color'] = 'black'
              // style['display'] = 'flex'



            }else if(data[0] == 'NO-NEWS-AT-ALL'){
              sentimentMessage = 'There are no news at all to use for the sentiment analysis of ' + selectedIssuer + '.'
              style['color'] = 'rgba(255, 99, 132, 1)'
              // style['display'] = 'flex'
            }

            setText(data[2])
            setPDFText(data[3])
            setMessage(sentimentMessage); // Update the message state
            setResultStyle(style); // Update the style state
            console.log(message)
            console.log(text)
            console.log(pdf_text)
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
                {text && <p className="left">{text}</p> }
                {pdf_text && <p className="left">{pdf_text}</p>} 
      </div>

      {/* <div className="test">
        <p>THE MESSAGE</p>
        <p className="left">THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...THE TEXT...</p>
        <p className="left">THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...THE PDF...</p>
      </div> */}
      
    </div>
    )
  }
  
  export default FundamentalAnalysis;
  