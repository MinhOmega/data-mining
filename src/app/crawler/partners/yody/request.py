import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver


class YodyRequest:
    def __init__(self):
        self.url = "https://api.newfashion.com.vn"
        self.driver = self._get_driver()
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self.driver:
            self.driver.close()
            self.driver.quit()
            self.driver = None

    def _get_driver(self) -> WebDriver:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=options)
        return driver

    def get(self, uri: str):
        return self.session.get(url=self.url + uri, headers=self.headers)
    
    def post(self, uri: str, data: dict):
        return self.session.post(url=self.url + uri, headers=self.headers, data=data)