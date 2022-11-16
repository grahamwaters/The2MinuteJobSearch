# connect python with webbrowser-chrome
# source: https://www.geeksforgeeks.org/automate-linkedin-connections-using-python/

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui as pag
import json
import time # to control how fast the browser executes the code
import random
from ratelimit import limits, sleep_and_retry

# load your credentials from secrets.json in the config folder
with open('./config/secrets.json', encoding = 'utf-8') as f:
    secrets = json.load(f)
    username_cred = secrets['username']
    password_cred = secrets['password']

def login():

    # Getting the login element
    username = driver.find_element_by_id("login-email")
    # Sending the keys for username
    username.send_keys(username_cred)
    time.sleep(random.randint(1, 3)) # sleep for 1 to 3 seconds

    # Getting the password element
    password = driver.find_element_by_id("login-password")

    # Sending the keys for password
    password.send_keys(password_cred)
    time.sleep(random.randint(1, 3)) # sleep for 1 to 3 seconds

    # Getting the tag for submit button
    driver.find_element_by_id("login-submit").click()
    time.sleep(random.randint(4, 7)) # sleep for 4 to 7 seconds


def goto_network():
    driver.find_element_by_id("mynetwork-tab-icon").click()



def main():

    # url of LinkedIn
    url = "http://linkedin.com/"

    # url of LinkedIn network page
    network_url = "http://linkedin.com / mynetwork/"

    # path to browser web driver
    driver_path = "/Volumes/Backups of Grahams IMAC/chromedriver.exe"

    # defining the driver
    global driver
    gecko_driver = "~/usr/local/bin/geckodriver"
    chrome_driver = "~/usr/local/bin/chromedriver"
    try:
        firefox_driver = webdriver.Firefox(executable_path = gecko_driver)
    except Exception:
        chrome_driver = webdriver.Chrome(executable_path = chrome_driver)
    print("Driver loaded")

    driver.get(url)

# Driver's code
if __name__ == "__main__":
    main()