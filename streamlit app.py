# app.py
"""
Streamlit dashboard for Bursa stock (CIMB Group default: 1023.KL)
Improved: volatility KPI, income-statement auto-plot, manager insights, deprecation fixes.
Run:
    pip install streamlit yfinance plotly pandas openpyxl
    streamlit run "streamlit app.py"
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Bursa Stock Dashboard — CIMB (1023.KL)",
                   layout="wide",
                   initial_sidebar_state="expanded")

# ---------------- Helpers ----------------
@st.cache_data
def get_price_data(ticker: str, start: str = None, end: str = None, interval: str = "1d") -> pd.DataFrame:
    tk = yf.Ticker(ticker)
    try:
        if start and end:
            df = tk.history(start=start, end=end, interval=interval)
        else:
            df = tk.history(period="1y", interval=interval)
    except Exception:
        df = pd.DataFrame()
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.reset_index().rename(columns={"Date": "Date"})
    df["Date"] = pd.to_datetime(df["Date"])
    return df

@st.cache_data
def get_financials_yf(ticker: str) -> dict:
    tk = yf.Ticker(ticker)
    res = {"annual": None, "quarterly": None}
    try:
        fin = tk.financials
        if fin is not None and not fin.empty:
            res["annual"] = fin.transpose().reset_index().rename(columns={"index": "Period"})
    except Exception:
        res["annual"] = None
    try:
        qfin = tk.quarterly_financials
        if qfin is not None and not qfin.empty:
            res["quarterly"] = qfin.transpose().reset_index().rename(columns={"index": "Period"})
    except Exception:
        res["quarterly"] = None
    return res

def safe_info(ticker: str) -> dict:
    tk = yf.Ticker(ticker)
    try:
        meta = tk.info
    except Exception:
        meta = {}
    return {
        "longName": meta.get("longName", ticker),
        "sector": meta.get("sector", "N/A"),
        "industry": meta.get("industry", "N/A"),
        "marketCap": meta.get("marketCap", "N/A")
    }

def auto_find_metrics(fin_df: pd.DataFrame):
    """Return (revenue_col, net_col) choices or (None, None)"""
    if fin_df is None or fin_df.empty:
        return None, None
    cols = [c for c in fin_df.columns if c != "Period"]
    lc = [c.lower() for c in cols]
    # Revenue candidates
    rev_keywords = ["revenue", "total revenue", "sales"]
    net_keywords = ["net income", "netprofit", "net profit", "profit/(loss)", "profit"]
    rev_col = None
    net_col = None
    for i, c in enumerate(cols):
        for k in rev_keywords:
            if k in c.lower():
                rev_col = c
                break
        if rev_col:
            break
    for i, c in enumerate(cols):
        for k in net_keywords:
            if k in c.lower():
                net_col = c
                break
        if net_col:
            break
    # Fallbacks: first numeric column(s)
    numeric_cols = [c for c in cols if pd.api.types.is_numeric_dtype(fin_df[c])]
    if rev_col is None and numeric_cols:
        rev_col = numeric_cols[0]
    if net_col is None and len(numeric_cols) > 1:
        net_col = numeric_cols[1]
    return rev_col, net_col

# ---------------- Sidebar controls ----------------
st.sidebar.header("Controls")
ticker = st.sidebar.text_input("Ticker (Yahoo Finance)", value="1023.KL", max_chars=30)

# default last 90 days
end_default = datetime.today()
start_default = end_default - timedelta(days=90)
start_date = st.sidebar.date_input("Start date", start_default)
end_date = st.sidebar.date_input("End date", end_default)
interval = st.sidebar.selectbox("Interval", options=["1d", "1wk", "1mo"], index=0)

ma_options = st.sidebar.multiselect("Moving averages (days)", options=[7, 20, 50, 100], default=[7, 20])
show_volume = st.sidebar.checkbox("Show volume", value=True)

st.sidebar.markdown("---")
uploaded_fin = st.sidebar.file_uploader("Upload income statement CSV/XLSX (optional)", type=["csv", "xlsx"])

# ---------------- Main ----------------
st.title("Bursa Stock Dashboard — CIMB Group (default: 1023.KL)")
st.markdown("Interactive dashboard for OHLC and income statement visuals. Use the sidebar to change controls.")
st.caption("Data source: Yahoo Finance (via yfinance).")


# Fetch data
with st.spinner("Fetching data from Yahoo Finance..."):
    df_price = get_price_data(ticker, start=start_date.strftime("%Y-%m-%d"),
                              end=(end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                              interval=interval)
    fin_dict = get_financials_yf(ticker)
    meta = safe_info(ticker)

if df_price.empty:
    st.error(f"No price data found for ticker `{ticker}`. Check the ticker symbol or try another one.")
    st.stop()

# KPIs
latest_close = df_price.iloc[-1]["Close"]
period_return = (latest_close / df_price.iloc[0]["Close"] - 1) * 100
prev_change = None
if len(df_price) >= 2:
    prev_change = (latest_close / df_price.iloc[-2]["Close"] - 1) * 100

# volatility (annualized)
returns = df_price["Close"].pct_change().dropna()
vol_annual = returns.std() * np.sqrt(252) * 100 if not returns.empty else np.nan

k1, k2, k3, k4 = st.columns([1.4, 1.4, 1.4, 1.4])
k1.metric("Latest Close (MYR)", f"{latest_close:.3f}")
k2.metric(f"Period Return ({start_date} → {end_date})", f"{period_return:.2f} %")
k3.metric("Previous Close % Change", f"{prev_change:.2f} %" if prev_change is not None else "-")
k4.metric("Annualized Volatility", f"{vol_annual:.2f} %")

# Company meta expander
with st.expander("Company info (from Yahoo Finance)"):
    st.write(f"**Name:** {meta.get('longName')}")
    st.write(f"**Sector:** {meta.get('sector')}")
    st.write(f"**Industry:** {meta.get('industry')}")
    st.write(f"**Market Cap:** {meta.get('marketCap')}")

# ---------------- Price charts ----------------
fig = go.Figure()
fig.add_trace(go.Candlestick(x=df_price["Date"],
                             open=df_price["Open"],
                             high=df_price["High"],
                             low=df_price["Low"],
                             close=df_price["Close"],
                             name="OHLC"))

for n in ma_options:
    if n > 0:
        ma_label = f"MA{n}"
        df_price[ma_label] = df_price["Close"].rolling(window=n, min_periods=1).mean()
        fig.add_trace(go.Scatter(x=df_price["Date"], y=df_price[ma_label], mode="lines", name=ma_label, line=dict(width=1)))

fig.update_layout(title=f"{meta.get('longName')} ({ticker}) — Candlestick",
                  xaxis_title="Date", yaxis_title="Price (MYR)",
                  xaxis_rangeslider_visible=False,
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

st.plotly_chart(fig, width="stretch")

if show_volume:
    vol_fig = go.Figure()
    vol_fig.add_trace(go.Bar(x=df_price["Date"], y=df_price["Volume"], name="Volume"))
    vol_fig.update_layout(title="Trading Volume", xaxis_title="Date", yaxis_title="Volume")
    st.plotly_chart(vol_fig, width="stretch")

# ---------------- Financials / Income statement ----------------
st.markdown("---")
st.header("Income Statement / Financials")

fin_df = None
fin_source = None

# prefer uploaded file
if uploaded_fin is not None:
    try:
        if uploaded_fin.name.lower().endswith(".csv"):
            fin_df = pd.read_csv(uploaded_fin)
        else:
            fin_df = pd.read_excel(uploaded_fin)
        fin_source = "uploaded"
    except Exception as e:
        st.error(f"Unable to read uploaded financial file: {e}")
        fin_df = None

# else yfinance annual -> quarterly
if fin_df is None:
    if fin_dict.get("annual") is not None:
        fin_df = fin_dict["annual"]
        fin_source = "yfinance_annual"
    elif fin_dict.get("quarterly") is not None:
        fin_df = fin_dict["quarterly"]
        fin_source = "yfinance_quarterly"

if fin_df is None or fin_df.empty:
    st.info("Income statement not found via yfinance. Upload CSV/XLSX with columns: Period, Revenue, Net Income, etc.")
else:
    st.write(f"**Data source:** {fin_source}")
    st.caption("If required metrics are missing, upload a CSV/XLSX with columns: Period, Revenue, Net Income.")

    # show preview with better formatting
    st.dataframe(fin_df.head().style.format(lambda x: f"{x:,.0f}" if pd.api.types.is_number(x) else x))

    # allow user to pick a metric
    metric_cols = [c for c in fin_df.columns if c != "Period"]
    if not metric_cols:
        st.warning("No numeric metrics detected in financials.")
    else:
        # auto-find revenue & net if possible
        rev_col, net_col = auto_find_metrics(fin_df)
        default_index = 0
        # if rev_col exists and is in list, set as default
        if rev_col and rev_col in metric_cols:
            default_index = metric_cols.index(rev_col)
        selected_metric = st.selectbox("Select metric to plot", options=metric_cols, index=default_index)
        # prepare plot
        plot_df = fin_df[["Period", selected_metric]].copy()
        plot_df[selected_metric] = pd.to_numeric(plot_df[selected_metric], errors="coerce")
        # plot bar chart
        fig_fin = px.bar(plot_df, x="Period", y=selected_metric,
                         labels={"Period": "Period", selected_metric: selected_metric},
                         title=f"{selected_metric} over periods")
        st.plotly_chart(fig_fin, width="stretch")

        # if revenue & net exist, show grouped chart option
        if rev_col and net_col and rev_col in fin_df.columns and net_col in fin_df.columns:
            if st.button("Show Revenue & Net Income (grouped)"):
                df_group = fin_df[["Period", rev_col, net_col]].copy()
                df_group[rev_col] = pd.to_numeric(df_group[rev_col], errors="coerce")
                df_group[net_col] = pd.to_numeric(df_group[net_col], errors="coerce")
                fig_group = px.bar(df_group, x="Period", y=[rev_col, net_col], barmode="group", title="Revenue & Net Income")
                st.plotly_chart(fig_group, width="stretch")

# ---------------- Managerial insights ----------------
st.markdown("---")
st.header("Managerial Insights")
insights = []
# simple auto-insights
insights.append(f"Period return (selected range): **{period_return:.2f}%**.")
insights.append(f"Latest close price: **RM {latest_close:.3f}**.")
insights.append(f"Annualized volatility (close returns): **{vol_annual:.2f}%**.")
# add revenue trend if found
if fin_df is not None and not fin_df.empty:
    rev_col, net_col = auto_find_metrics(fin_df)
    if rev_col:
        # compute simple trend
        try:
            rev_series = pd.to_numeric(fin_df[rev_col], errors="coerce").dropna()
            if len(rev_series) >= 2:
                trend_pct = (rev_series.iloc[-1] / rev_series.iloc[0] - 1) * 100
                insights.append(f"{rev_col} changed by **{trend_pct:.2f}%** between first and last reported period.")
        except Exception:
            pass

for b in insights:
    st.write("- " + b)

# ---------------- Download buttons ----------------
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.download_button("Download price data (CSV)", data=df_price.to_csv(index=False).encode("utf-8"),
                       file_name=f"{ticker}_price.csv", mime="text/csv")
with col2:
    if fin_df is not None and not fin_df.empty:
        st.download_button("Download financials (CSV)", data=fin_df.to_csv(index=False).encode("utf-8"),
                           file_name=f"{ticker}_financials.csv", mime="text/csv")
    else:
        st.write("Financials not available for download.")

# ---------------- Footer notes ----------------
st.markdown("---")
st.write("""
**Notes:**  
- Data fetched from Yahoo Finance via `yfinance`. Financial metric names may vary across companies.  
- If `yfinance` does not provide financials for a ticker, upload CSV/XLSX with columns: `Period`, `Revenue`, `Net Income`, etc.  
- This dashboard is for educational use (assignment) — not investment advice.
""")
