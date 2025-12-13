# Step 1: Install yfinance if not already installed
# pip install yfinance matplotlib

import yfinance as yf
import matplotlib.pyplot as plt

# Step 2: Define the stock ticker for CIMB Group
ticker = "1023.KL"   # CIMB Group's Yahoo Finance ticker

# Step 3: Create a Ticker object
stock = yf.Ticker(ticker)

# Step 4: Fetch historical data (last 3 months)
hist = stock.history(period="3mo")   # Options: '1mo', '6mo', '1y', '5y', 'max'

# Step 5: Display basic company information (using safe .get() access)
info = stock.info

print("===== Company Info =====")
print("Company Name:", info.get("longName", "N/A"))
print("Sector:", info.get("sector", "N/A"))
print("Industry:", info.get("industry", "N/A"))
print("Market Cap:", info.get("marketCap", "N/A"))
print("========================\n")

# Step 6: Plot closing price
plt.figure(figsize=(10,5))
plt.plot(hist.index, hist["Close"], marker='o', linestyle='-', label="Closing Price")

plt.title(f"{info.get('longName', 'CIMB Group')} ({ticker}) - Closing Prices (Last 3 Months)")
plt.xlabel("Date")
plt.ylabel("Price (MYR)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()
