from selenium import webdriver
import pandas as pd
from datetime import datetime
import re
import webbrowser
import requests
from bs4 import BeautifulSoup
import time

csv_file = "stock_data.csv"

def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    return webdriver.Chrome(options=options)

def get_current_price(stock, ask = True):
    url = f"https://uk.finance.yahoo.com/quote/{stock}/"
    headers = {'user-agent':'Mozilla/5.0 \
               (Windows NT 10.0; Win64; x64) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/84.0.4147.105 Safari/537.36'}
    page = requests.get(url,headers=headers)
    time.sleep(2)
    
    #with open("test.html" ,"w", errors="ignore") as f:
    #    f.write(page.text)
    price = re.search(f"data-testid=\"qsp-price\">([0-9\.]+) </span>", page.text)
    hour = datetime.now().time().hour
    #print(hour)
    if(hour >= 20):
        #print("using post")
        price = re.search(f"data-testid=\"qsp-post-price\">([0-9\.]+) </span>", page.text)
    if(8 <= hour <= 13):
        price = re.search(f"data-testid=\"qsp-pre-price\">([0-9\.]+) </span>", page.text)

    if(not(price)):
        if(not ask):
            return False
        return get_current_price_temp(stock)
    return price.group(1)

#def get_current_price(stock):
#    url = f"https://www.google.com/search?q={stock}+price"
#    
#    driver = initialize_driver()
#    driver.get(url)
#    content = driver.page_source
#    print(content)
#    price = re.search("<span>([0-9\.]+)</span>", content)
#    return price

def get_current_price_temp(stock):
    url = f"https://uk.finance.yahoo.com/quote/{stock}/"
    webbrowser.open(url)
    return input(f"Enter the price for {stock}:")

def write_to_file(data, file):
    with open(file, "w") as f:
        f.write(data)

def append_to_file(data, file):
    with open(file, "a") as f:
        f.write(data)

def save_stock_data(stocks, file, ask = True):
    for i in range(0,len(stocks)):
        price = get_current_price(stocks[i], ask)
        if(price):
            now = datetime.now()
            date = now.date().strftime("%d-%m-%Y")
            time = now.time().strftime("%H:%M:%S")
            stock_data = f"{stocks[i]},{price},{date},{time}\n"
            append_to_file(stock_data, file)
            stock_data = ""

def get_stocks():
    data = get_dataframe()
    stocks = data["stock"].unique()
    return stocks

def get_stock_history(stock, data):
    return data[data["stock"] == stock]

def get_date(date, data):
    return data[data["date"] == date]

def get_stock_at_date(stock, date, data):
    stock_data = get_stock_history(stock, data)
    return stock_data[stock_data["date"] == date]

def get_dataframe():
    return pd.read_csv(csv_file)

def get_price(stock):
    data = get_dataframe()
    history = get_stock_history(stock, data)
    prices = history["price"].values
    return prices[len(prices) - 1]

def calc_how_much_can_buy(stock, money):
    price = get_price(stock)
    return money/price
