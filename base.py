from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import selenium
import time
import bs4


class Webdriver(object):

    def __init__(
            self,
            driver_path: str,
            headless: bool
    ):
        options = Options()
        if headless:
            options.headless = True
        prefs = {
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': False,
            'safebrowsing.disable_download_protection': True}
        options.add_experimental_option('prefs', prefs)
        self.driver = selenium.webdriver.Chrome(driver_path, options=options)
        self.driver.set_window_size(1024, 600)
        self.driver.maximize_window()

    def goto(
            self,
            url: str
    ):
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, 600)

    def get_soup(
            self
    ):
        return bs4.BeautifulSoup(self.driver.page_source, "lxml")

    def get_page_source(
            self
    ):
        return self.driver.page_source

    def click(
            self,
            xpath: str,
            tries: int = 10,
            timeout: int = 3
    ):
        if not hasattr(self, "wait"):
            raise ValueError("Wait not found.")
        for _ in range(tries):
            try:
                ef = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                time.sleep(timeout)
                ef.click()
                return 0
            except Exception:
                time.sleep(timeout)
        raise ValueError(f"Webdriver: (Click @{xpath}) | Exited with code 1.")

    def get_table(
            self,
            name: str,
            attrs: dict,
            exclude: list = [],
            min_rows: int = 5,
    ):
        soup = self.get_soup()

        # Removing elements which contains text that can harm
        # table read.
        if len(exclude) > 0:
            for ename in exclude:
                try:
                    for found in soup.find_all(ename):
                        found.decompose()
                except Exception:
                    pass

        # Reading the table.
        table = pd.read_html(str(soup.find(name, attrs)))[0]
        n = table.shape[0]
        if n >= min_rows:
            return table
        raise ValueError(f"WebDriver (Get-Table) | Exited with code 1.")
