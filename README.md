🚀 Overview

This project is an interactive financial analytics dashboard built using Streamlit to analyze Bursa Malaysia stock performance.

It integrates real-time market data, financial statements, and key performance indicators (KPIs) to support data-driven investment decision-making.

Unlike basic dashboards, this project combines price trends, volatility analysis, and financial performance into a unified analytical tool.

---

🎯 Problem Statement

Investors and analysts often struggle to interpret large volumes of stock and financial data effectively.

This project addresses that challenge by providing an interactive and intuitive dashboard that transforms raw financial data into actionable insights, enabling better investment and strategic decisions.

---

🎯 Project Objectives

The main objectives of this project are:
- To visualise historical stock price data including open, high, low, close, and trading volume
- To display income statement data to support managerial understanding of company performance
- To demonstrate the use of Python, Streamlit, and data visualisation libraries in building an interactive dashboard

---

💰 Selected Company

- **Company:** CIMB Group Holdings Berhad  
- **Ticker:** 1023.KL  
- **Market:** Bursa Malaysia  

CIMB Group was selected due to its relevance as a major financial institution in Malaysia and the availability of market and financial data from Yahoo Finance.

---

💡 Key Features

📊 Market Data Analysis
- Interactive candlestick chart (OHLC)
- Historical price trend visualization
- Adjustable date range and time interval

---

📈 Technical Indicators
* Moving Averages (MA7, MA20, MA50, MA100)
* Trend analysis for identifying market direction

---

📉 Risk & Performance Metrics
* Latest closing price
* Period return (%)
* Daily price change (%)
* Annualized volatility (risk indicator)

---

🧾 Financial Analysis
* Income statement integration (annual / quarterly)
* Revenue and net income visualization
* Support for custom financial data upload (CSV/XLSX)

---

🧠 Managerial Insights

* Automated insights based on:
* Price trends
* Volatility
* Financial performance

---

🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- yfinance (Yahoo Finance API)

---

🧠 Analytical Value

This project goes beyond basic visualization by combining:

* Descriptive Analytics → understanding price trends
* Diagnostic Analytics → analyzing financial performance
* Risk Analysis → evaluating volatility

It demonstrates how data analytics can be applied in a financial context to support investment decisions and strategic analysis.

---

📂 Project Structure
The application follows a structured data pipeline to ensure data consistency and functionality.
- User Inputs: Accept controls for the stock (e.g., 1023.KL for CIMB), dates, and display options.
- Fetch Price Data: Retrieve OHLC (Open, High, Low, Close) and Volume data using the yfinance library.
- Fetch/Load Financial Data: Attempt to get Annual/Quarterly financial data from yfinance, or use the uploaded CSV/XLSX file as a fallback.
- Data Processing: Calculate Moving Averages, percentage returns, and standardize numeric financial fields.
- Compute KPIs: Calculate and display key metrics like volatility and period returns.
- Generate Visuals & Insights: Render interactive Plotly charts (Candlestick, Volume, Bar charts) and display automated managerial insights.

---

▶️ How to Run

1. Install dependencies
Install the required Python packages using pip:

pip install streamlit yfinance plotly pandas numpy openpyxl

2. Run the Application
Navigate to the directory containing streamlit app.py and execute the following command:

streamlit run "streamlit app.py"

The application will automatically open in your web browser, typically at
http://localhost:8501

---

📊 Example Use Cases

* Analyze stock performance over time
* Evaluate risk using volatility metrics
* Compare financial performance across periods
* Support data-driven investment decisions

---

🔥 Future Improvements

* Stock comparison (multi-ticker analysis)
* Advanced technical indicators (RSI, MACD)
* Predictive modeling for price forecasting
* Deployment as a web application

---

👩‍💻 Author

Siti Sarah binti Mohd Affandi
Master in Operations Research & Analytics 

---

⚠️ Disclaimer

- This dashboard is developed for educational and analytical purposes only.
 It does not constitute financial or investment advice.
