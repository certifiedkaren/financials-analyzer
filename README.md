Financials Analyzer

A Python tool that retrieves stock financial data using Yahoo Finance (yfinance) and updates Google Sheets automatically. It fetches income statements, balance sheets, and cash flow data, calculates key financial ratios, and organizes everything for easy analysis.

📌 Features

✅ Fetches stock financials from Yahoo Finance
✅ Updates Google Sheets in real-time
✅ Calculates essential financial ratios
✅ Handles multiple tickers efficiently
✅ Simple and customizable

🔧 Setup & Installation

1. Clone the repository

git clone https://github.com/certifiedkaren/financials-analyzer.git
cd financials-analyzer

2. Install dependencies

pip install -r requirements.txt

3. Set up your .env file

Create a .env file in the project directory and add your Google Sheets ID:

GOOGLE_SHEET_ID=your_google_sheet_id_here

4. Add your Google Sheets API credentials

Place your credentials.json file (Google Sheets API credentials) in the project directory.

5. Run the script

python main.py


📊 Financial Ratios Calculated

Retained Earnings

Current Ratio (Liquidity check)

Debt-to-Equity Ratio (Leverage measure)

Net Margin (Profitability)

Operating Profit Margin

Return on Equity (ROE)

Gross Margin

Capital Expenditure Ratio

