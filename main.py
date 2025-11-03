import my_stock_info as msi
import my_portfolio as mp

def print_values():
    for stock in stocks_to_track:
        if(mp.get_amount(stock)):
            value = msi.get_price(stock) * mp.get_amount(stock)
            print(f"Value of {stock}: {value}")
    print("\n")

stocks_to_track = ["NVDA","AAPL","MSFT","AMZN","META", "GOOGL", "NFLX", "AMD", "RACE", "IBM", "TM", "MA", "WMT"]
str = ""
for stock in stocks_to_track:
    str += stock + ", "
print("Currently tracking: " + str[:-2])
if(input("Add any stocks to track? ") == "y"):
    done = False
    while(not done):
        ans = input("Stock: ")
        if(ans == "n"):
            done = True
        else:
            stocks_to_track.append()
print("Fetching prices...")
msi.save_stock_data(stocks_to_track, msi.csv_file)
print("\n")

portfolios = ["my_portfolio_log.txt", "my_2nd_portfolio.txt", "top5_portfolio_log.txt"]
str = ""
for portfolio in portfolios:
    str += portfolio + ", "
print("Current portfolios: " + str[:-2])
if(input("Add a portfolio? ") == "y"):
    done = False
    while(not done):
        ans = input("Portfolio log: ")
        if(ans == "n"):
            done = True
        else:
            portfolios.append()


for portfolio in portfolios:
    p_done = "n"
    while(not(p_done == "y")):
        print(f"Portfolio: {portfolio}\n")
        mp.set_report_log(portfolio)
        mp.load()
        print(mp.get_report())
        print_values()
        #mp.add_funds(float(input("Add cash: ")))
        
        if(input("Buy any stocks? ") == "y"):
            done = "n"
            while(done != "y"):
                stock = input("Stock: ")
                amount = float(input("Spend: "))
                done = input("Done? ")
                mp.buy(stock, msi.calc_how_much_can_buy(stock, amount))

        print(mp.get_report())
        mp.save_report()
        print_values()

        if(input("Sell any stocks? ") == "y"):
            done = "n"
            while(done != "y"):
                stock = input("Stock: ")
                value = msi.get_price(stock) * mp.get_amount(stock)
                print(f"Value of {stock}: {value}")
                amount = float(input("Gain: "))
                done = input("Done? ")
                mp.sell(stock, msi.calc_how_much_can_buy(stock, amount))

        print(mp.get_report())
        mp.save_report()

        print_values()
        p_done = input("Done with this portfolio? ")