import json

import selenium
from scrape_linkedin import scrape_in_parallel, ProfileScraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

cookie = '<>'

options = Options()
options.add_argument('--headless')
HEADLESS_OPTIONS = {'chrome_options': options}

# with ProfileScraper(cookie=cookie, driver_options=HEADLESS_OPTIONS, driver=webdriver.Chrome) as scraper:
#     # https://www.linkedin.com/in/cuong-dao-duc-79978b107/
#     profile = scraper.scrape(user='hungtrv')
# print(json.dumps(profile.to_dict()))

profiles = ['hungtrv', 'cuong-dao-duc-79978b107']
scrape_in_parallel(scraper_type=ProfileScraper, items=profiles, output_file='profiles.json', num_instances=2,
                   cookie=cookie)
