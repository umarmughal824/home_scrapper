from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_webdriver(proxy=None):
    chrome_options = Options()
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    driver = webdriver.Chrome(options=chrome_options)
    return driver
