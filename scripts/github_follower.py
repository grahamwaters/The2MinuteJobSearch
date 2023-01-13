# taken from another repository

import random
import re
import json
import time
import datetime
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging

logging.basicConfig(filename="../logs/click.log", level=logging.DEBUG)

url_clicks = {}
with open("../data/url_clicks.csv", "w") as csv_file:
    csv_file.write("URL,Clicks\n")

with open("../config/config.json") as f:
    data = json.load(f)

options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")  # <--- Note the option
options.add_argument("--disable-dev-shm-usage")  # <--- Note the option
options.add_argument("--remote-debugging-port=9222")  # <--- Note the port
# options.add_argument(f'user-data-dir={data["chrome_driver_path"]}') # <--- Note the f-string

driver = webdriver.Chrome(
    executable_path=data["chrome_driver_path"], chrome_options=options
)
driver.get("https://www.github.com/login")

username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "login_field"))
)
password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "password"))
)
username.send_keys(data["github_username"])
time.sleep(random.randint(1, 5))
password.send_keys(data["github_password"])
time.sleep(random.randint(1, 5))
password.send_keys(Keys.RETURN)

# clear the log file
open("click.log", "w").close()

# wait ten seconds for the follow buttons to load
time.sleep(10)
# go to IBM people page
driver.get("https://github.com/orgs/IBM/people")
print(
    "Following you now! Go crazy, but make sure to stay on GitHub until we develop this for more general use."
)
time.sleep(5)  # wait five seconds for the page to load

if driver.current_url in url_clicks:
    if url_clicks[driver.current_url] >= 5:
        time.sleep(3)
        continue
else:
    url_clicks[driver.current_url] = 0

while True:
    # only follow if the url contains a "people" in the url
    if not re.search("people", driver.current_url):
        time.sleep(3)
        continue  # skip to the next iteration of the loop
    follow_buttons = []  # init
    try:
        # Find the buttons
        follow_buttons = driver.find_elements(
            By.CSS_SELECTOR, r"input.btn"
        )  # [5].click() # click the 5th button
        # now find the buttons that are displayed and interactable (not hidden) & also not 'Unfollow' buttons. Also, check that the button is in view currently (not scrolled off the page)
        follow_buttons = [
            button
            for button in follow_buttons
            if button.is_displayed()
            and button.is_enabled()
            and button.get_attribute("value") == "Follow"
            and button.location["y"]
            < driver.execute_script("return window.innerHeight")
        ]
        # now click one of the visible buttons
        follow_buttons[random.randint(0, len(follow_buttons) - 1)].click()
        # logging.info(
        #     f"Follow button clicked at {datetime.now()} url: {driver.current_url}"
        # )
        print(f"Follow button clicked at {datetime.now()} url: {driver.current_url}")
        time.sleep(random.randint(6, 10))
    except ValueError as e:
        pass  # this value error means the follow buttons list is empty and we should just skip to the next iteration of the loop
    except Exception as e:
        pass
    if re.search("yahoo", driver.current_url):
        break


driver.close()
