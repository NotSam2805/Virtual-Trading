import my_stock_info as msi
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import my_portfolio as mp

def construct_datetimes(dates_and_times):
    datetimes = []
    times = dates_and_times["time"].values
    dates = dates_and_times["date"].values
    for i in range(len(times)):
        str = dates[i] + " " + times[i]
        dt = datetime.strptime(str, "%d-%m-%Y %H:%M:%S")
        datetimes.append(dt)
    return datetimes

def stock_graph():
    data = msi.get_dataframe()
    stock = input("Stock: ")
    stock_data = data[data["stock"]==stock]
    times = construct_datetimes(stock_data)

    plt.clf()
    plt.plot(times, stock_data["price"])
    plt.title(f"{stock} price")
    plt.xlabel("Date")
    plt.ylabel("USD")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
    plt.show()

def portfolio_graph():
    portfolio = input("Portfolio log: ")
    mp.set_report_log(portfolio)
    data = mp.get_dataframe()
    times = construct_datetimes(data)

    plt.clf()
    plt.plot(times, data["value"])
    plt.title(f"{portfolio} value")
    plt.xlabel("Date")
    plt.ylabel("USD")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
    plt.show()

done = False
while(not(done)):
    inp = input("Make stock graph or portfolio graph? ")
    if(inp == "stock"):
        stock_graph()
    elif(inp == "portfolio"):
        portfolio_graph()
    if(input("done? ") == "y"):
        done = True