from stock import Financials


user_input = input("Ticker: ")
stock = Financials(user_input)
print(stock.update_google_sheet())

 
 
