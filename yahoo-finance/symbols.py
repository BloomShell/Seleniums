from dotenv import load_dotenv
from base import Webdriver
load_dotenv()
import os


if __name__ == "__main__":

    wd = Webdriver(driver_path="../chromedriver.exe", headless=False)
    wd.goto("https://finance.yahoo.com/screener/new")
    wd.click(os.getenv("ACCEPT_PRIVACY_BUTTON"))

    # Remove all the default filters...
    for _ in range(4):
        wd.click(os.getenv("REMOVE_FIRST_FILTER_BUTTON"))

    # Open the Filters Window...
    wd.click(os.getenv("ADD_FILTER_BUTTON"))

    # Add 'Exchange' as a filter...
    wd.click(os.getenv("ADD_EXCHANGE_FILTER_BUTTON"))

    # Close the Filters Window...
    wd.click(os.getenv("CLOSE_FILTERS_BUTTON"))

    # Open the Exchange filter window...
    wd.click(os.getenv("ADD_EXCHANGES_BUTTON"))
