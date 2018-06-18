import json

import selenium
from scrape_linkedin import ProfileScraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

cookie = '<Your LI_AT cookie>'

options = Options()
options.add_argument('--headless')
HEADLESS_OPTIONS = {'chrome_options': options}

with ProfileScraper(cookie=cookie, driver_options=HEADLESS_OPTIONS, driver=webdriver.Chrome) as scraper:
    # https://www.linkedin.com/in/cuong-dao-duc-79978b107/
    profile = scraper.scrape(user='hungtrv')
print(json.dumps(profile.to_dict()))
