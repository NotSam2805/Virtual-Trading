from datetime import datetime
import my_stock_info as msi
import re
import pandas as pd

cash = 0
stocks_held = {}
report_log = "portfolio_log.txt"

def set_report_log(file):
    global report_log
    report_log = file

def write_to_file(data, file):
    with open(file, "w") as f:
        f.write(data)

def append_to_file(data, file):
    with open(file, "a") as f:
        f.write(data)

def get_value():
    value = cash
    for x in stocks_held:
        value += stocks_held[x] * msi.get_price(x)
    return value

def buy(stock, amount):
    cost = msi.get_price(stock) * amount
    global cash
    if(cost > cash):
        return False
    cash -= cost
    if(stock in stocks_held.keys()):
        old_number = stocks_held[stock]
        stocks_held.update({stock: old_number + amount})
        return True
    else:
        stocks_held.update({stock: amount})

def sell(stock, amount):
    global cash
    if not(stock in stocks_held.keys()):
        return False
    if(stocks_held[stock] < amount):
        return False
    old_amount = stocks_held[stock]
    value = msi.get_price(stock) * amount
    cash += value
    if(old_amount - amount <= 0):
        stocks_held.pop(stock)
        return True
    stocks_held.update({stock: (old_amount - amount)})
    return True

def get_report():
    now = datetime.now()
    date = now.date().strftime("%d-%m-%Y")
    time = now.time().strftime("%H:%M:%S")
    value = get_value()
    report = "----------------------\n"
    report += f"{date} @ {time}\n"
    report += f"Current value: {value}\n"
    report += f"Cash held: {cash}\n"
    for x in stocks_held:
        amount = stocks_held[x]
        report += f"{x}: {amount}\n"
    report +="----------------------\n"
    return report

def save_report():
    append_to_file(get_report(), report_log)

def read_last_report():
    with open(report_log, "r") as f:
        lines = f.readlines()
        report = ""
        in_report = False
        for line in lines:
            if(line == "----------------------\n"):
                if not(in_report):
                    report = ""
                in_report = not(in_report)
            if(in_report):
                report+=line
        return report

def load_from_report(report):
    global cash
    stocks_held.clear()
    cash_str = re.search("Cash held: (.+)\n", report)
    cash = float(cash_str.group(1))
    lines = report.splitlines()
    for line in lines:
        if not(("@" in line) or ("Current value" in line) or ("Cash held" in line) or (line == "----------------------")):
            split = line.split(": ")
            key = split[0]
            value = float(split[1])
            stocks_held.update({key: value})

def add_funds(money):
    global cash
    cash += money

def remove_funds(amount):
    cash -= amount

def get_amount(stock):
    if not(stock in stocks_held.keys()):
        return False
    return stocks_held[stock]

def get_data_from_report(report):
    lines = report.splitlines()
    date = datetime.now()
    value = 0
    for line in lines:
        if not(line == "----------------------"):
            if("@" in line):
                date = datetime.strptime(line, "%d-%m-%Y @ %H:%M:%S")
            if("Current value: " in line):
                str = line.split(":")[1]
                str = str[:-1]
                value = float(str)
    date_str = date.date().strftime("%d-%m-%Y")
    time_str = date.time().strftime("%H:%M:%S")
    return(date_str, time_str, value)

def get_dataframe():
    report_dates = []
    report_times = []
    report_values = []
    with open(report_log, "r") as f:
        lines = f.readlines()
        report = ""
        in_report = False
        for line in lines:
            if(line == "----------------------\n"):
                if not(in_report):
                    (x,y,z) = get_data_from_report(report)
                    report_dates.append(x)
                    report_times.append(y)
                    report_values.append(z)
                    report = ""
                in_report = not(in_report)
            if(in_report):
                report+=line
    report_values.pop(0)
    report_dates.pop(0)
    report_times.pop(0)
    return pd.DataFrame({"date":report_dates, "time":report_times, "value":report_values})

def load():
    load_from_report(read_last_report())