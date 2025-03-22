import React, { useEffect, useState } from "react";
import axios from "axios";

const BACKEND_URL = "http://127.0.0.1:5000";

function App() {
  const [transactions, setTransactions] = useState([]);
  const [summary, setSummary] = useState([]);

  useEffect(() => {
    axios.get(`${BACKEND_URL}/transactions`)
      .then(response => setTransactions(response.data))
      .catch(error => console.error("Error fetching transactions:", error));

    axios.get(`${BACKEND_URL}/summary`)
      .then(response => setSummary(response.data))
      .catch(error => console.error("Error fetching summary:", error));
  }, []);

  return (
    <div>
      <h1>Financial Dashboard</h1>
      <h2>Transaction Summary</h2>
      <ul>
        {summary.map((item, index) => (
          <li key={index}>
            {item.year} {item.month}: Income: ${item.total_income}, Expense: ${item.total_expense}, Net: ${item.net_cashflow}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
