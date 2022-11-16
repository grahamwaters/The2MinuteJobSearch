# connect python with webbrowser-chrome
# source: https://www.geeksforgeeks.org/automate-linkedin-connections-using-python/

from selenium import webdriver
# import waiting till element is present in the page functionality
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time # to control how fast the browser executes the code
import random
import pandas as pd
import os

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


#* Action Function for LinkedIn

def harvest(company_url,lamp_df,driver):
    # we are logged in to LinkedIn at this point
    # get the company page
    driver.get(company_url) # get the company page
    # wait for the people you may know section to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".org-people-profiles-module__profile-list")))
    # get the list of people you may know
    people_you_may_know = driver.find_elements_by_css_selector(".org-people-profiles-module__profile-list") # get the list of people you may know
    # these elements are not clickable, so we need to get the url from the href attribute
    # get the list of urls for the people you may know
    people_you_may_know_urls = [person.find_element_by_css_selector("a").get_attribute("href") for person in people_you_may_know]
    # get the list of names for the people you may know
    people_you_may_know_names = [person.find_element_by_css_selector("a").get_attribute("aria-label") for person in people_you_may_know]
    # get the list of titles for the people you may know
    people_you_may_know_titles = [person.find_element_by_css_selector(".org-people-profile-card__profile-title").text for person in people_you_may_know]
    # get the list of companies for the people you may know
    people_you_may_know_companies = [person.find_element_by_css_selector(".org-people-profile-card__profile-subtitle").text for person in people_you_may_know]
    # get the list of locations for the people you may know
    people_you_may_know_locations = [person.find_element_by_css_selector(".org-people-profile-card__profile-location").text for person in people_you_may_know]
    # create a dataframe for the people you may know
    lamp_df = pd.DataFrame({'name':people_you_may_know_names,'title':people_you_may_know_titles,'company':people_you_may_know_companies,'location':people_you_may_know_locations,'url':people_you_may_know_urls})
    # save the dataframe to a csv file in the data folder
    lamp_df.to_csv(f'./data/{company_url.split("/")[-1]}_people_you_may_know.csv',index=False)
    # return the dataframe
    return lamp_df

def get_prefs():
    # get the top 10 companies from the populated lamp_list list.
    if os.exists('./data/lamp_list.csv'):
        lamp_list = pd.read_csv('./data/lamp_list.csv')
        lamp_list = lamp_list.head(10)
    else:
        print('Time to choose some companies to target!')
        # ask the user to choose some companies to target, one by one
        while len(lamp_list) != 10:
            company = input('Enter a company name: ')
            lamp_list.append(company)
        # save the list to a csv file
        lamp_list.to_csv('./data/lamp_list.csv',index=False)
    return lamp_list


def process_flow():
    print("Starting the process flow")
    # load your credentials from secrets.json in the config folder
    with open('./config/secrets.json', encoding = 'utf-8') as f:
        secrets = json.load(f)
    print(f'Secrets have been loaded.')
    # login to LinkedIn using the credentials
    login(secrets)
    #& load the user's
    print("Logged in to LinkedIn, you should see your main feed now.")
    continue_flag = input("y/n: should I continue? ")
    if continue_flag == 'y':
        print("Continuing the process flow")
    else:
        print("Exiting the process flow")
        return

    # create the lamp_df dataframe
    lamp_df = pd.DataFrame(columns=['name','title','company','location','url'])
    print(f'I have cleared out a storage room for our files. It was dusty in there!')

    print(f' -- Stage 1: Harvesting --')
    print(f' Your chosen companies are: {my_companies}')
    print(f'Looking for the hiring managers of these companies for you to connect with.')
    # get the list of hiring managers for each company
    lamp_df = harvest(companies)


process_flow() # run the process flow