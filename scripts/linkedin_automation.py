# connect python with webbrowser-chrome
# source: https://www.geeksforgeeks.org/automate-linkedin-connections-using-python/
import json
import time  # to control how fast the browser executes the code
import random
import os
import pandas as pd

from selenium import webdriver

# import waiting till element is present in the page functionality
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import By
from selenium.webdriver.common.by import By

# import Keys
from selenium.common.exceptions import (
    ElementClickInterceptedException,
)

connect_mode = False


def detect_confirm_button(driver):
    try:
        # detect the confirm button and click it
        driver.find_element_by_css_selector(
            ".artdeco-modal__confirm-dialog-btn"
        ).click()
        return True
    except:
        return False


def login(secrets):
    # login to LinkedIn
    driver = webdriver.Chrome()
    # Login to LinkedIn
    driver.get("https://www.linkedin.com/login")
    time.sleep(random.randint(1, 3))  # sleep for 1 to 3 seconds
    # Getting the login element
    username = driver.find_element_by_css_selector("#username")
    # retrieve the username from secrets.json
    username_cred = secrets["username"]
    # Sending the keys for username
    username.send_keys(username_cred)
    time.sleep(random.randint(1, 3))  # sleep for 1 to 3 seconds
    # Getting the password element
    password = driver.find_element_by_css_selector("#password")
    # retrieve the password from secrets.json
    password_cred = secrets["password"]
    # Sending the keys for password
    password.send_keys(password_cred)
    time.sleep(random.randint(1, 3))  # sleep for 1 to 3 seconds

    # Getting the tag for submit button
    driver.find_element_by_css_selector(".btn__primary--large").click()
    time.sleep(random.randint(4, 7))  # sleep for 4 to 7 seconds
    detect_confirm_button(driver)  # if the confirm button is present, click it
    time.sleep(random.randint(1, 5))  # sleep for 4 to 7 seconds
    return driver


# * Action Function for LinkedIn
# @limit(1, 60) # limit the function to 1 call per 60 seconds
def harvest(company_url, lamp_df, driver, url_patterns, company_name="", group_name="", list_name = ""):
    # we are logged in to LinkedIn at this point
    # get the company page

    """
    harvest the company page for the company_url provided and update the lamp_df dataframe with the results, which should be the information for the hiring managers at the company as listed on the company page (company_url).

    :param company_url: the url for the company page
    :type company_url: str
    :param lamp_df: the dataframe to update with the results
    :type lamp_df: pandas.DataFrame
    :param driver: the selenium driver
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver
    :return: the updated dataframe
    :rtype: pandas.DataFrame
    """
    # css_tag1 = 'driver.find_elements_by_css_selector("#main > div.org-grid__content-height-enforcer > div > div.artdeco-card.pb2 > div.display-flex.full-width.justify-space-between.align-items-center.pt5.ph5")[0].get_attribute'

    # scrolling options for random choice
    scroll_options = [
        "window.scrollTo(0, document.body.scrollHeight);",
    ]
    steady_scroll = ["window.scrollTo(0, document.body.scrollHeight/8);"]

    if group_name != "":
        company_url = group_name # if the company_url is a group, use the group name instead (which is a url)
    elif list_name != "":
        company_url = list_name # if the company_url is a list, use the list name instead (which is a url)
    # & go to the required page
    driver.get(company_url)  # get the company page
    # wait for the people you may know section to load
    WebDriverWait(driver, 90).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "org-grid__content-height-enforcer")
        )
    )
    time.sleep(5)  # sleep for 5 seconds
    # get the list of people you may know

    # scroll down incrementally (using some randomness) to emulate human behavior until you reach the bottom of the page.
    # get the height of the page
    last_height = driver.execute_script("return document.body.scrollHeight")
    iterations = 0  # keep track of the number of iterations to prevent infinite loops
    while True:
        inner_command = random.choice(scroll_options)
        driver.execute_script(inner_command)  # scroll down
        # wait to load the page
        time.sleep(random.randint(1, 3))  # sleep for 1 to 3 seconds
        # calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if (
            new_height == last_height or iterations == 5
        ):  # if the page has reached the bottom, break the loop and continue
            break
        iterations += 1
        last_height = new_height

    print("Scrolling complete, now looking for people on the page")
    # get the list of people you may know
    people = driver.find_elements_by_css_selector(
        ".org-people-profile-card__profile-title.t-black.t-bold"
    )

    # get the buttons on the page to click
    button_class = url_patterns["buttons"]  # get the button class
    # check the inner text of the button to see if it is "Connect"/"Message" or "Follow" or "Pending"
    buttons = driver.find_elements_by_css_selector(button_class)  # get the buttons
    last_connect_time = (
        time.time()
    )  # keep track of the last time you connected to prevent spamming the connect button
    # loop through the people and connect with them
    for button in buttons:
        if button.text == "Follow":
            button.click()
            time.sleep(random.randint(1, 3))
            # detect the confirm button and click it
            detect_confirm_button(driver)
            time.sleep(random.randint(1, 3))
        elif (
            button.text == "Connect"
        ):  # if the button says "Connect" then we only click it if we have not clicked more than 3 times in the last 5 minutes
            # get the current time
            current_time = time.time()
            # check if the current time is within 5 minutes of the last time we clicked the connect button
            if (
                current_time - last_connect_time > 300
            ):  # if it has been more than 5 minutes since the last time we clicked the connect button
                button.click()
                time.sleep(random.randint(1, 3))
                # detect the confirm button and click it
                detect_confirm_button(driver)
                time.sleep(random.randint(1, random.randint(3, 5)))
                # update the last_connect_time
                last_connect_time = current_time
            else:  # if it has been less than 5 minutes since the last time we clicked the connect button
                continue
        elif (
            button.text == "Message"
        ):  # if the button says "Message" then we only click it if we have not clicked more than 3 times in the last 5 minutes
            pass  # we will not click the message button

        elif (
            button.text == "Pending"
        ):  # if the button says "Pending" then we only click it if we have not clicked more than 3 times in the last 5 minutes
            pass  # we will not click the pending button
        else:
            pass

    people_you_may_know = driver.find_elements_by_css_selector(
        ".org-people-profiles-module__profile-list"
    )  # get the list of people you may know
    # these elements are not clickable, so we need to get the url from the href attribute

    # either people or people_you_may_know will be empty, but not both
    if len(people) > 0:  # if there are people on the page
        people_you_may_know = people
    elif len(people_you_may_know) > 0:  # if there are people you may know on the page
        pass
    else:  # if there are no people or people you may know on the page
        people_you_may_know = []  # set the people_you_may_know to an empty list

    driver.find_elements_by_css_selector(
        "#main > div.org-grid__content-height-enforcer > div > div.artdeco-card.pb2 > div.display-flex.full-width.justify-space-between.align-items-center.pt5.ph5"
    )[0].get_attribute("href")
    # get the list of urls for the people you may know
    people_you_may_know_urls = [
        person.get_attribute("href") for person in people_you_may_know
    ]  # get the list of urls for the people you may know
    # save the dataframe to a csv file in the data folder
    # make a directory for the csv files for the company name if it doesn't exist
    if not os.path.exists(f"./data/{company_name}"):
        os.makedirs(f"./data/{company_name}")
    lamp_df.to_csv(
        f'./data/lamp_df_v1.csv', index=False
    )

    # while the url still contains the company name, keep gathering information while the user navigates the website. Follow anyone with a follow button and collect all names and urls.

    # while the url still contains the company name, keep gathering information while the user navigates the website. Follow anyone with a follow button and collect all names and urls.
    # print('Watching for new people to follow, have fun exploring the website! Let me do the work for you.')
    print("Sit back and relax, watch my magic as I follow people for you!")
    headless_mode = False  # set to True to run in headless mode
    total_follows = 0  # keep track of the total number of follows
    while company_name in driver.current_url:
        # get the list of people you may know

        inner_command = random.choice(scroll_options)
        driver.execute_script(inner_command)
        # wait to load the page
        # sleep a random number of seconds to emulate human behavior (between 1 and 3 seconds)
        time.sleep(random.randint(1, 9))
        # get the height of the page
        # last_height = driver.execute_script("return document.body.scrollHeight")

        # if this_height != last_height:
        #     last_scroll_time = time.time()
        #     this_height = last_height
        #     headless_mode = False # if the user has moved the page, then we are no longer in headless mode
        iterations = (
            0  # keep track of the number of iterations to prevent infinite loops
        )

        people = driver.find_elements_by_css_selector(
            ".org-people-profile-card__profile-title.t-black.t-bold"
        )
        # get the buttons on the page to click
        button_class = url_patterns["buttons"]
        # check the inner text of the button to see if it is "Connect"/"Message" or "Follow" or "Pending"
        # find follow buttons by the text "Follow"
        follow_buttons = driver.find_elements_by_xpath("//*[text()='Follow']")
        # find connect buttons by the text "Connect"
        last_connect_time = (
            time.time()
        )  # keep track of the last time you connected to prevent spamming the connect button
        # loop through the people and connect with them
        for button in follow_buttons:
            if button.text == "Follow":
                try:
                    button.click()
                    time.sleep(random.randint(1, 3))
                    # detect the confirm button and click it
                    # detect_confirm_button(driver)
                    print("Followed a new person!",end=' ')  # print a message to the user
                    # get the person's information
                    try:
                        lamp_df = get_more_details(driver, lamp_df, company_name)
                    except Exception as error:
                        print(error)
                    time.sleep(random.randint(1, 3))
                    total_follows += 1  # increment the total number of follows
                except ElementClickInterceptedException:
                    pass

            elif (
                button.text == "Connect" and connect_mode == True
            ):  # if the button says "Connect" then we only click it if we have not clicked more than 3 times in the last 5 minutes
                # get the current time
                current_time = time.time()
                # check if the current time is within 5 minutes of the last time we clicked the connect button
                if current_time - last_connect_time > 300:
                    try:
                        button.click()
                        time.sleep(random.randint(1, 3))
                        # detect the confirm button and click it
                        print(
                            "Connected with a new person!"
                        )  # print a message to the user
                        # print(f'Connected with user: {}'.format('username'))
                        detect_confirm_button(driver)
                        time.sleep(random.randint(1, random.randint(3, 5)))
                        # update the last_connect_time
                        last_connect_time = current_time
                    except ElementClickInterceptedException:
                        pass
                else:
                    continue
            elif button.text == "Message":
                pass
            elif button.text == "Pending":
                pass
            else:
                pass
        if total_follows > 20 or iterations > 30:
            print(
                f"Total follows: {total_follows} is greater than 20. Moving to next Company."
            )
            total_follows = 0
            break
        time.sleep(random.randint(2, 10))
    # return the dataframe

    return lamp_df


def get_more_details(driver, lamp_df, company_name):
    """
    get_more_details is a function that gets more details about the people you may know.

    on this page there are many <li > elements with the class "grid grid__col--lg-8 pt5 pr4 m0 block" each of which contains a user's information.
        # we want to get the inner text of each of these elements and save it to a dictionary with the key being the name of the person and the value being that user's name and position and url. We will save this dictionary to a csv file.
        # get the list of <li> elements

    :param driver: _description_
    :type driver: _type_
    :param lamp_df: _description_
    :type lamp_df: _type_
    :param company_name: _description_
    :type company_name: _type_
    :return: _description_
    :rtype: _type_
    """
    li_elements = driver.find_elements_by_css_selector(
        ".grid.grid__col--lg-8.pt5.pr4.m0.block"
    )
    # loop through the list of <li> elements
    for li in li_elements:
        # get the text of the <li> element
        li_text = li.text
        # split the text by the new line character
        li_text = li_text.split("\n")
        # get the name of the person
        name = li_text[0]
        # get the position of the person
        position = li_text[1]
        # get the url of the person
        url = li.find_element_by_css_selector("a").get_attribute("href")
        # add the person to the dataframe if they are not already in the dataframe
        if name not in lamp_df["name"].values:
            # add using concat to avoid SettingWithCopyWarning
            lamp_df = pd.concat(
                [
                    lamp_df,
                    pd.DataFrame(
                        {
                            "name": [name],
                            "position": [position],
                            "url": [url],
                            "company": [company_name]
                        }
                    ),
                ]
            )
            print(f' {name} a {position} at {company_name}')
    # make a directory for the csv files for the company name if it doesn't exist
    if not os.path.exists(f"./data/{company_name}"):
        os.makedirs(f"./data/{company_name}")

    # save the dataframe to a csv file in the data folder
    lamp_df.to_csv(
        f'./data/{company_name}/lamp_df.csv', index=False
    )

    # return the dataframe

    return lamp_df



# def fill_lamp_list(company_name):
#     # get the top 10 companies from the populated lamp_list list.
#     # make a directory for the csv files for the company name if it doesn't exist
#     if not os.path.exists(f"./data/{company_name}"):
#         os.makedirs(f"./data/{company_name}")
#     # check if the lamp_list file exists
#     if os.path.exists("./data/{company_name}/lamp_list.csv"):  # check if the file exists
#         lamp_list = pd.read_csv("./data/{company_name}/lamp_list.csv")
#         lamp_list = lamp_list.head(10)
#     else:  # if the file does not exist, create it
#         print("Time to choose some companies to target!")
#         # ask the user to choose some companies to target, one by one
#         while len(lamp_list) != 10:
#             company = input(f"{len(lamp_list)}. Enter a company name: ")
#             lamp_list.append(company)  # add the company to the list
#         # save the list to a csv file
#         lamp_list.to_csv("./data/{company_name}/lamp_list.csv", index=False)
#     return lamp_list


def process_flow():
    """
    process_flow is the main function that runs the process flow
    :return: None
    :rtype: None
    """
    print("Starting the process flow")
    # load your credentials from secrets.json in the config folder
    with open("./config/secrets.json", encoding="utf-8") as f:
        secrets = json.load(f)
    print("Secrets have been loaded.")
    print("User preferences have been loaded.")

    # load the list of companies to target (eventually)
    my_companies = [
        "ibm",
        "google",
        "apple",
        "microsoft",
        "facebook",
        "amazon",
        "netflix",
        "nvidia",
        "intel",
        "oracle",
        "openteams",
        "meta",
        "crowdstrike",
        "twitter",
        "tesla-motors",
        "uber",
        "lyft",
        "airbnb",
        "palo-alto-networks",
    ]
    my_groups = [
        "https://www.linkedin.com/groups/961087/"
    ]
    my_lists = [
        "https://www.linkedin.com/search/results/COMPANIES/?companyHqGeo=%5B%22104472865%22%2C%2290000064%22%5D&industryCompanyVertical=%5B%221594%22%2C%226%22%2C%224%22%5D&keywords=python&origin=FACETED_SEARCH&sid=tyE"
    ]

    print("Preferences have been loaded.")
    driver = login(secrets)
    print("Logged in to LinkedIn, you should see your main feed now.")
    # continue_flag = input("y/n: should I continue? ")
    continue_flag = "y"  # for now, we will assume the user wants to continue
    if continue_flag == "y":
        print("Continuing the process flow")
    else:
        print("Exiting the process flow")
        return

    # load the url patterns in config/url_patterns.json
    with open("./config/url_patterns.json", encoding="utf-8") as f:
        url_patterns = json.load(f)
    print("URL patterns have been loaded.")

    # create the lamp_df dataframe
    lamp_df = pd.DataFrame(columns=["name", "title", "company", "location", "url"])
    print("I have cleared out a storage room for our files. It was dusty in there!")
    # get the list of companies to target
    # lamp_list = get_prefs()
    print(" -- Stage 1: Harvesting --")
    print(f" Your chosen companies are: {my_companies}")
    print("Looking for the hiring managers of these companies for you to connect with.")
    # loop through the companies in the list
    # each url follows the company_hiring_manager_pattern pattern in the config file (url_patterns.json)
    # shuffle the list of companies
    random.shuffle(my_companies)
    # my_companies = shuffled_companies
    pattern_url = url_patterns["company_hiring_manager_pattern"]
    for company in my_companies:
        try:
            print(f" -- Company: {company} --")
            company_url = pattern_url.format(
                str(company).lower()
            )  # create the url for the company
            print(f"Company URL: {company_url}")
            print(f"Company Name: {company}")
            # harvest the data for the company and update the lamp_df dataframe
            # company_url,lamp_df,driver,url_patterns
            lamp_df = harvest(
                company_url=company_url,
                driver=driver,
                lamp_df=lamp_df,
                url_patterns=url_patterns,
                company_name = company
            )
            print(f" -- Completed harvesting for {company} --")
            # sleep for a random amount of time
            time.sleep(random.randint(1, 3))  # sleep for a random amount of time
        except Exception as e:
            print(f"Error: {e}")
            pass

    print(" -- Stage 2: Austin Section --")
    temp_df = lamp_df.copy()
    pattern_url = url_patterns["austin_company"]
    for company in my_companies:
        try:
            print(f" -- Company: {company} --")
            company_url = pattern_url.format(
                str(company).lower()
            )  # create the url for the company
            print(f"Company URL: {company_url}")
            print(f"Company Name: {company}")
            # harvest the data for the company and update the lamp_df dataframe
            # company_url,lamp_df,driver,url_patterns
            lamp_df = harvest(
                company_url=company_url,
                driver=driver,
                lamp_df=lamp_df,
                url_patterns=url_patterns,
                company_name = company
            )
            print(f" -- Completed harvesting for {company} --")
            # sleep for a random amount of time
            time.sleep(random.randint(1, 3))  # sleep for a random amount of time
        except Exception as e:
            print(f"Error: {e}")
            pass

    print(" -- Stage 3: Data Scientist Section --")

    pattern_url = url_patterns["data_scientists"]
    for company in my_companies:
        try:
            print(f" -- Company: {company} --")
            company_url = pattern_url.format(
                str(company).lower()
            )  # create the url for the company
            print(f"Company URL: {company_url}")
            print(f"Company Name: {company}")
            # harvest the data for the company and update the lamp_df dataframe
            # company_url,lamp_df,driver,url_patterns
            lamp_df = harvest(
                company_url=company_url,
                driver=driver,
                lamp_df=lamp_df,
                url_patterns=url_patterns,
                company_name = company
            )
            print(f" -- Completed harvesting for {company} --")
            # sleep for a random amount of time
            time.sleep(random.randint(1, 3))  # sleep for a random amount of time
        except Exception as e:
            print(f"Error: {e}")
            pass

    # update the temp_df with the new data
    temp_df = temp_df.append(lamp_df)
    # remove duplicates
    lamp_df = temp_df.drop_duplicates()
    # reset the index
    lamp_df = lamp_df.reset_index(drop=True)

    print(f' -- Stage 4: Groups --')
    temp_df = lamp_df.copy()
    # go to the group pages and harvest the data from there
    for group in my_groups:
        try:
            print(f' -- Group: {group} --')
            # harvest the data for the group and update the lamp_df dataframe
            lamp_df = harvest(
                company_url=group,
                driver=driver,
                lamp_df=lamp_df,
                url_patterns=url_patterns,
                group_name = group
            )
            print(f' -- Completed harvesting for {group} --')
            # sleep for a random amount of time
            time.sleep(random.randint(1, 3))  # sleep for a random amount of time
        except Exception as e:
            print(f'Error: {e}')
            pass
    print(" -- Completed harvesting for all companies --")
    # saving the dataframe to a csv file

    # update the temp_df with the new data
    temp_df = temp_df.append(lamp_df)
    # remove duplicates
    lamp_df = temp_df.drop_duplicates()
    # reset the index
    lamp_df = lamp_df.reset_index(drop=True)

    # make a directory for the csv files for the company name if it doesn't exist
    if not os.path.exists(f"./data/{company_name}"):
        os.makedirs(f"./data/{company_name}")
    lamp_df.to_csv("./data/{company_name}/lamp_df.csv", index=False)
    print(" -- Saved the dataframe to a csv file --")
    # update the temp_df with the new data
    temp_df = temp_df.append(lamp_df)
    # remove duplicates
    lamp_df = temp_df.drop_duplicates()
    # reset the index
    lamp_df = lamp_df.reset_index(drop=True)

    print(" -- Stage 5: Lists --")
    temp_df = lamp_df.copy()
    # go to the list pages and harvest the data from there
    for list in my_lists:
        try:
            print(f' -- List: {list} --')
            # harvest the data for the list and update the lamp_df dataframe
            lamp_df = harvest(
                company_url=list,
                driver=driver,
                lamp_df=lamp_df,
                url_patterns=url_patterns,
                list_name = list
            )
            print(f' -- Completed harvesting for {list} --')
            # sleep for a random amount of time
            time.sleep(random.randint(1, 3))  # sleep for a random amount of time
        except Exception as e:
            print(f'Error: {e}')
            pass
    print(" -- Completed harvesting for all companies, groups, and lists --")
    # saving the dataframe to a csv file
    # make a directory for the csv files for the company name if it doesn't exist
    if not os.path.exists(f"./data/{company_name}"):
        os.makedirs(f"./data/{company_name}")
    lamp_df.to_csv("./data/{company_name}/full_lamp_df.csv", index=False)

    # update the temp_df with the new data
    temp_df = temp_df.append(lamp_df)
    # remove duplicates
    lamp_df = temp_df.drop_duplicates()
    # reset the index
    lamp_df = lamp_df.reset_index(drop=True)



    return lamp_df

def main():
    lamp_df = process_flow()  # run the process flow
    return lamp_df


if __name__ == "__main__":
    main()


#follow_if_this_text_onprofile