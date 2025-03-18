import os
import yfinance as yf
import logging
from dotenv import load_dotenv
import gspread 
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError
from gspread.exceptions import APIError

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

class Financials:
    def __init__(self, ticker):
        # Get ticker from user and fetch the data about it
        self.ticker = ticker.strip().upper()
        self.data = yf.Ticker(self.ticker)

        # Separate the data into financial statements
        self.income_statement = self.data.income_stmt
        self.balance_sheet = self.data.balance_sheet
        self.cash_flow = self.data.cash_flow       

    def calculate(self):
        # Define the years to process
        years = [0, 1, 2, 3]
        try:
            # Initialize an empty dictionary to store results
            vals = {
                "Retained Earnings": [],
                "Current Ratio": [],
                "Debt To Equity Ratio": [],
                "Net Margin": [],
                "Operating Profit": [],
                "Return On Equity": [],
                "Gross Margin": [],
                "Capital Expenditure Ratio": []
            }

            # Loop over each year and calculate the metrics
            for i in years:
                vals["Retained Earnings"].append(self.balance_sheet.loc["Retained Earnings"].iloc[i])
                vals["Current Ratio"].append(
                    self._safe_divide(
                        self.balance_sheet.loc["Current Assets"].iloc[i],
                        self.balance_sheet.loc["Current Liabilities"].iloc[i]
                    )
                )
                vals["Debt To Equity Ratio"].append(
                    self._safe_divide(
                        self.balance_sheet.loc["Total Debt"].iloc[i],
                        self.balance_sheet.loc["Total Equity Gross Minority Interest"].iloc[i]
                    )
                )
                vals["Net Margin"].append(
                    self._safe_divide(
                        self.income_statement.loc["Net Income"].iloc[i],
                        self.income_statement.loc["Total Revenue"].iloc[i]
                    )
                )
                vals["Operating Profit"].append(
                    self._safe_divide(
                        self.income_statement.loc["Operating Income"].iloc[i],
                        self.income_statement.loc["Total Revenue"].iloc[i]
                    )
                )
                vals["Return On Equity"].append(
                    self._safe_divide(
                        self.income_statement.loc["Net Income"].iloc[i],
                        self.balance_sheet.loc["Total Equity Gross Minority Interest"].iloc[i]
                    )
                )
                vals["Gross Margin"].append(
                    self._safe_divide(
                        self.income_statement.loc["Gross Profit"].iloc[i],
                        self.income_statement.loc["Total Revenue"].iloc[i]
                    )
                )
                vals["Capital Expenditure Ratio"].append(
                    self._safe_divide(
                        self.cash_flow.loc["Capital Expenditure"].iloc[i],
                        self.cash_flow.loc["Operating Cash Flow"].iloc[i]
                    )
                )

            # Get year labels
            year_labels = [self.balance_sheet.columns[i].strftime('%Y') for i in years]
            return {"years": year_labels, "data": vals}

        except Exception as e:
            # Log any errors that occur during calculation
            logging.error(f"An error occurred while calculating financial ratios: {e}", exc_info=True)
            return None
            
  
    
    def _safe_divide(self, num, denom): 
        # Safely divide two numbers, returning None if the denominator is zero or None
        if denom is None or denom == 0:
            return None
        else:
            return round(num / denom, 2)
        
    def update_google_sheet(self): 
        # Load environment variables
        load_dotenv()
        sheet_id = os.getenv("GOOGLE_SHEET_ID")

        if not sheet_id:
            # Log an error if the sheet ID is not found in environment variables
            logging.error("Sheet ID not found in environment variables.")
            return "Sheet ID not found in environment variables."

        try: 
            # Set up Google Sheets API credentials and client
            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
            client = gspread.authorize(creds)
            sheet = client.open_by_key(sheet_id)
            worksheet = sheet.get_worksheet(0)
            
            # Calculate stock data
            stock_data = self.calculate()
            if not stock_data:
                logging.error("Error calculating stock data")
                return "Error calculating stock data"
            
            # Prepare data for Google Sheets
            headers = ["Metric"] + stock_data["years"]
            rows = [headers]
            for metric, values in stock_data["data"].items():
                rows.append([metric] + values)
                
            # Update Google Sheets with the calculated data
            worksheet.append_row([self.ticker])
            worksheet.append_rows(rows)
            
            logging.info("Updated Successfully")
            return "Updated Successfully"
        
        except GoogleAuthError as e:
            # Log Google Authentication errors
            logging.error("Google Authentication Error", exc_info=True)
            return f"Google Authentication Error: {e}"
        except APIError as e:
            # Log Google Sheets API errors
            logging.error("Google Sheets API Error", exc_info=True)
            return f"Google Sheets API Error: {e}"
        except Exception as e: 
            # Log any other errors that occur
            logging.error("An error occurred: ", exc_info=True)
            return f"An Error Occured : {e}"








