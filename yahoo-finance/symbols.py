from dotenv import load_dotenv
from base import Webdriver
import pandas as pd
load_dotenv()
import pickle
import math
import json
import time
import re
import os


if __name__ == "__main__":

    xpaths = json.load(open("xpaths.json"))
    wd = Webdriver(driver_path="../chromedriver.exe", headless=False)

    for exchange in xpaths:

        t0 = time.time()
        print(f"Starting... Exchange: {exchange}")

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

        for xpath in xpaths[exchange]:
            wd.click(xpath)

        wd.click(os.getenv("FIND_STOCKS_BUTTON"))
        wd.click(os.getenv("OPEN_NUMBER_OF_RECORDS_WINDOW_BUTTON"))
        wd.click(os.getenv("SELECT_SHOW_100_RECORDS_BUTTON"))

        # Inferred number of pages to search based
        # on screener message.
        n_found = int(re.compile("\d+").findall(re.compile("of\s\d+\sresults") \
            .findall(wd.get().find("span", {"class": "Mstart(15px) Fw(500) Fz(s)"})
            .getText())[0])[0])
        n_pages = math.ceil(n_found / 100)

        # Iterate through (n_pages - 1)...
        results = []
        for i in range(n_pages - 1):
            table = wd.get_table("div", {"id": "scr-res-table"},
                                 exclude=["span"], min_rows=100)
            wd.click(os.getenv("NEXT_PAGE_BUTTON"))
            results.append(table)
            time.sleep(10)

        # Last page, observations <= 100, min_rows = 1.
        table = wd.get_table("div", {"id": "scr-res-table"},
                             exclude=["span"], min_rows=1)
        results.append(table)
        t1 = time.time()
        duration = t1 - t0
        print(f"Terminated! time: {round(duration, 2)} second(s).")

        # Save to Json...
        data = list(pd.concat(results)[["Symbol", "Name"]]\
                 .drop_duplicates('Symbol').itertuples(index=False, name=None))

        pickle.dump(data, open(f"metadata/{exchange}.bin", "wb"), -1)
        time.sleep(5)
