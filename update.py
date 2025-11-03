import my_stock_info as msi
import my_portfolio as mp
print("Fetching prices...")
msi.save_stock_data(msi.get_stocks(), msi.csv_file, False)

portfolios = ["my_portfolio_log.txt", "my_2nd_portfolio.txt", "top5_portfolio_log.txt"]
print("Updating portfolios...")
for portfolio in portfolios:
    mp.set_report_log(portfolio)
    mp.load()
    mp.save_report()