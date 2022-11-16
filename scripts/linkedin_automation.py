# connect python with webbrowser-chrome
# source: https://www.geeksforgeeks.org/automate-linkedin-connections-using-python/

from selenium import webdriver
import json
import time # to control how fast the browser executes the code
import random

def detect_confirm_button(driver):
    try:
        # detect the confirm button and click it
        driver.find_element_by_css_selector(".artdeco-modal__confirm-dialog-btn").click()
        return True
    except:
        return False

def login(secrets):
    # login to LinkedIn
    driver = webdriver.Chrome()
    # Login to LinkedIn
    driver.get("https://www.linkedin.com/login")
    time.sleep(random.randint(1, 3)) # sleep for 1 to 3 seconds
    # Getting the login element
    username = driver.find_element_by_css_selector("#username")
    # retrieve the username from secrets.json
    username_cred = secrets['username']
    # Sending the keys for username
    username.send_keys(username_cred)
    time.sleep(random.randint(1, 3)) # sleep for 1 to 3 seconds
    # Getting the password element
    password = driver.find_element_by_css_selector("#password")
    # retrieve the password from secrets.json
    password_cred = secrets['password']
    # Sending the keys for password
    password.send_keys(password_cred)
    time.sleep(random.randint(1, 3)) # sleep for 1 to 3 seconds

    # Getting the tag for submit button
    driver.find_element_by_css_selector(".btn__primary--large").click()
    time.sleep(random.randint(4, 7)) # sleep for 4 to 7 seconds
    detect_confirm_button(driver) # if the confirm button is present, click it
    time.sleep(random.randint(1, 5)) # sleep for 4 to 7 seconds
    return


def process_flow():
    print("Starting the process flow")
    # load your credentials from secrets.json in the config folder
    with open('../config/secrets.json', encoding = 'utf-8') as f:
        secrets = json.load(f)
    print(f'Secrets have been loaded.')
    # login to LinkedIn using the credentials
    login(secrets)
    print("Logged in to LinkedIn, you should see your main feed now.")
    continue_flag = input("y/n: should I continue? ")
    if continue_flag == 'y':
        print("Continuing the process flow")
    else:
        print("Exiting the process flow")
        return
