import json
import os
import shutil

import selenium
import time

from database.db_features import add_to_db, get_size_of_profiles_list, get_incompleted_profile_ids
from scrape_linkedin import scrape_in_parallel, ProfileScraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

start = time.time()

cookie = '<your li_at cookies>'
options = Options()
options.add_argument('--headless')
HEADLESS_OPTIONS = {'chrome_options': options}

# with ProfileScraper(cookie=cookie, driver_options=HEADLESS_OPTIONS, driver=webdriver.Chrome) as scraper:
#     # https://www.linkedin.com/in/cuong-dao-duc-79978b107/
#     profile = scraper.scrape(user='hungtrv')
# print(json.dumps(profile.to_dict()))

# If file exists, delete it
if os.path.isdir('tmp_data'):
    shutil.rmtree('tmp_data')

# Insert linkedin id into arrays for sample, or get from db
# profiles = ['hungtrv', 'cuong-dao-79978b107']
profiles = get_incompleted_profile_ids()
while get_size_of_profiles_list() <= 135:
    #output file
    filename = 'profiles.json'
    # scrape script
    scrape_in_parallel(scraper_type=ProfileScraper, items=profiles, output_file=filename, num_instances=2,
                       cookie=cookie)
    # Save all profile into db.
    add_to_db(filename)
    # profiles = get_incompleted_profile_ids()

end = time.time()
print(end - start)
