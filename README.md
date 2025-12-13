# Bursa Stock Dashboard (CIMB Group 1023.KL)

This project is an interactive Streamlit dashboard developed for visualising Bursa Malaysia stock data and selected financial information. The dashboard retrieves historical stock prices and income statement data from Yahoo Finance using the yfinance library and presents them through interactive charts and key performance indicators.

This project was developed as part of the SQIT5043 Programming for Analytics course.

---

## Project Objectives

The main objectives of this project are:
- To visualise historical stock price data including open, high, low, close, and trading volume
- To display income statement data to support managerial understanding of company performance
- To demonstrate the use of Python, Streamlit, and data visualisation libraries in building an interactive dashboard

---

## Selected Company

- **Company:** CIMB Group Holdings Berhad  
- **Ticker:** 1023.KL  
- **Market:** Bursa Malaysia  

CIMB Group was selected due to its relevance as a major financial institution in Malaysia and the availability of market and financial data from Yahoo Finance.

---

## Features

The application provides a comprehensive and interactive interface for stock analysis:
- Interactive Controls: Users can select the stock Ticker, Date Range, Interval (1d, 1wk, 1mo), and toggle Moving Averages (MA).
- OHLC Visualization: Displays stock movements using a Candlestick Chart with optional Moving Average overlays (e.g., MA7, MA20).
- Performance KPIs: Shows essential metrics like Latest Close Price, Period Return, Previous Close % Change, and Annualized Volatility.
- Financial Data Integration: Automatically fetches annual or quarterly Income Statement data from Yahoo Finance.
- Custom Financial Input: Includes a file uploader to accept CSV/Excel files for financial data when the online source is incomplete or missing.
- Financial Charting: Generates bar charts for user-selected financial metrics (like Revenue or Net Income) and a grouped comparison chart.
- Managerial Insights: Provides simple, auto-generated textual insights based on price and financial trends.

## Technologies Used

- Python
- Streamlit
- yfinance (Yahoo Finance API)
- Pandas
- NumPy
- Plotly
- Matplotlib
- Draw.io (workflow diagram)

---

## Project Structure
bursa-stock-dashboard/
│
├── app.py # Main Streamlit dashboard
├── Stock Data.py # Supporting script for price data testing
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── images/ # Screenshots and flowchart
│ ├── dashboard_main.png
│ ├── volume_financials.png
│ ├── revenue_grouped.png
│ └── flowchart.png


## How to Run the Dashboard

### 1. Install dependencies
Install the required Python packages using pip:

pip install streamlit yfinance plotly pandas numpy openpyxl

### 2. Run the Application
Navigate to the directory containing streamlit app.py and execute the following command:

streamlit run "streamlit app.py"

The application will automatically open in your web browser, typically at
http://localhost:8501

Repository Content
File Name,                                                Description
streamlit app.py,    The main Python script containing the Streamlit application logic, data fetching, processing, and visualization.
Stock Data.py,       A separate script used to test data retrieval and initial plotting of company metadata and closing prices.

