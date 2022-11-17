import requests
import json
import sys
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert


# to force a page to show all pages of results instead of just 10 per page (default), you can edit the html of the page and add the attribute "data-page-size="1000" to the table tag

# load the config file
with open("config.json") as f:
    config = json.load(f)

# import patterns from url_patterns.json
with open("url_patterns.json") as f:
    url_patterns = json.load(f)
    # the available opetions for degree codes are:
    #'F' for first degree,
    #'S': for second degree,
    #'T': for third degree,
    # these are added to the url pattern:company_hiring_manager_n_degree_pattern to get the url for the hiring managers n degree from the user's profile
# set the city and state
city = config["city"]
state = config["state"]
country = config["country"]


# def mile_one():

#     #* The Process Journey for each Company
#     #& Mile One: Getting started with the hiring managers with selenium and python
#     # Now we begin
#     # We will be using selenium to automate the process of getting the hiring managers
#     # We will be using python to write the code
#     # We will be using chrome to run the code
#     # We will be using the chrome driver to run the code

#     # global variables and constants

#     company_name = "IBM"
#     hiring_pattern = url_patterns[company_name] # get the pattern for the company
#     # fill in the pattern with the city and state and company. The saved pattern is an fstring.
#     url = hiring_pattern.format(company=company_name)
#     print(url)

#     #* On hiring manager page
#     ##* we can filter by proximity to the city and state provided in config.json

#     # set up the chrome driver
#     chrome_options = Options()
#     chrome_options.add_argument("--headless") # run headless
#     chrome_options.add_argument("--window-size=1920x1080") # set the window size
#     chrome_options.add_argument("--disable-gpu") # Last I checked this was necessary.
#     chrome_options.add_argument("--no-sandbox") # linux only
#     chrome_options.add_argument("--disable-dev-shm-usage") # this is for linux
#     chrome_options.add_argument("--disable-extensions") # disable extensions for security
#     chrome_options.add_argument("--disable-dev-shm-usage") # disable dev-shm-usage for security
#     chrome_options.add_argument("--disable-web-security") # disable web security for security

#     # set up the driver
#     driver = webdriver.Chrome(options=chrome_options) # set the driver

#     # get the url
#     driver.get(url)

#     #* On the hiring manager page

#     # get the hiring manager page
#     hiring_manager_page = driver.page_source # get the page source
#     # this is the page source for the hiring manager page for IBM in Austin, TX for example in html
#     # print(hiring_manager_page)

#     #* On the hiring manager page
#     # we can filter by proximity to the city and state provided in config.json
#     # update the url with the city and state
#     # we can also filter by country
#     # update the url with the country
#     updated_url = url + "&location=" + city + "%2C+" + state + "&country=" + country
#     print(updated_url)
#     #? try this url in the browser (it might not work because it is a headless browser so be sure to put it in a try except block)

#     try:
#         # get the updated url
#         driver.get(updated_url)
#     except:
#         # if it doesn't work, then just use the original url
#         driver.get(url)

#     #* On the hiring manager page with the updated url
#     # We should have a list of hiring managers in the city and state near the user. We can get the names of the hiring managers and their emails.

#     # if copilot is correct this will work

#     try:

#         # get the hiring manager pages by finding the links to their profiles and clicking on them
#         hiring_manager_pages = driver.find_elements_by_xpath("//a[@class='link-without-visited-state']") # get the hiring manager pages

#         # get the hiring manager names
#         hiring_manager_names = driver.find_elements_by_xpath("//div[@class='name']") # get the hiring manager names

#         # get the hiring manager emails
#         hiring_manager_emails = driver.find_elements_by_xpath("//div[@class='email']") # get the hiring manager emails

#     except Exception as e:
#         print(e)
#         print("Could not get the hiring manager pages using the copilot method. Trying the old method.")

#     # using requests
#     # get the hiring manager pages
#     # find the links to their profiles and put them in a list called hiring_manager_pages

#     # in the html these links look like this: <a class="link-without-visited-state" href="/company/ibm/people/robert-lee-1a5b4b1b" target="_blank" rel="noopener noreferrer" data-control-name="people_profile_link" data-ember-action="" data-ember-action-100="100">

#     # get the hiring manager pages
#     hiring_manager_pages = driver.find_elements_by_xpath("//a[@class='link-without-visited-state']") # get the hiring manager pages

#     # request the hiring manager pages
#     hiring_manager_pages = [requests.get(hiring_manager_page.get_attribute("href")) for hiring_manager_page in hiring_manager_pages] # request the hiring manager pages

#     # get the hiring manager names
#     hiring_manager_names = driver.find_elements_by_xpath("//div[@class='name']") # get the hiring manager names

#     # get the hiring manager emails
#     hiring_manager_emails = driver.find_elements_by_xpath("//div[@class='email']") # get the hiring manager emails. These are not the actual emails. They are just the first part of the email. We will have to get the rest of the email from the hiring manager page.


def harvest(company_url, lamp_df):

    # request the company url as html with requests and beautiful soup
    company_url_html = requests.get(company_url).text  # request the company url as html
    soup = BeautifulSoup(
        company_url_html, "html.parser"
    )  # parse the html with beautiful soup

    # use the patterns to get the hiring manager names and emails
    # linkedin_url2 pattern in url_patterns.json is useful for finding recruiting managers

    # targeted_search_linkedin_001 - explaining this pattern.
    # looks for people at the company provided with  .format(company name) that are 1st or 2nd degree connections of the user.

    # using

    return lamp_df


def main():
    return
