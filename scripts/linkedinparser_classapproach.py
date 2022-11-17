import http.cookiejar as cookielib
import os
import urllib
import re
import string
import urllib.request
import http.cookiejar as cookielib
import httplib2
import traceback

from bs4 import BeautifulSoup
import json

# import secrets from secrets.json in the config folder
with open("./config/secrets.json", encoding="utf-8") as f:
    secrets = json.load(f)
    username = secrets["username"]
    password = secrets["password"]

with open("./config/url_patterns.json", encoding="utf-8") as f:
    url_patterns = json.load(f)
    # the class of each individual person in the search results pages
    person_result_linkedin = url_patterns["entity_on_page_class"]
    # profile_url_pattern = url_patterns['profile_url_pattern']
    # note: .format(companyname) at the end of the following lines for tailored results.
    comp_hiring_manager_search = url_patterns["company_hiring_manager_pattern"]
    comp_recruiting_manager_search = url_patterns["company_recruiting_manager_pattern"]


def copilot_generated_function():
    cookie_filename = "./src/parser.cookies.txt"
    # create a cookie jar
    cookie_jar = cookielib.LWPCookieJar(cookie_filename)
    # if the cookie file exists, load the cookies into the Cookie Jar
    if os.path.isfile(cookie_filename):  # if the cookie file exists
        cookie_jar.load(ignore_discard=True)  # load the cookies from the file
    # create an opener to open pages using the http protocol and to process cookies.
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    # add our headers
    opener.addheaders = [
        ("User-agent", "Mozilla/5.0")
    ]  # [('User-agent', 'Mozilla/5.0')]
    # install our opener (note that this changes the global opener to the one
    # we just made, but you can also just call opener.open() if you want)
    urllib.request.install_opener(
        opener
    )  # install the opener we just made, what does this mean. It means that we are installing the opener we just made as the default opener for urllib2. This means that whenever we call urllib2.urlopen() it will use our opener.
    # what is an opener?
    # An opener is an object that can be used to open URLs.
    # It is a factory for handlers, and is used to open URLs via BaseHandlers.

    # the action/ target from the form
    authentication_url = "https://www.linkedin.com/uas/login-submit"
    # input form fields
    payload = {
        "session_key": username,
        "session_password": password,
        "isJsEnabled": "false",
        "loginCsrfParam": "a4a9a9f0-4d0a-4e3c-9f4c-2f2f2d2c2b2a",
        "source_app": "",
        "trk": "guest_homepage-basic_sign-in-submit",
    }

    # use urllib to encode the payload
    data = urllib.parse.urlencode(payload).encode("utf-8")
    # what is a payload? A payload is the data that is sent to the server.
    # what is data? Data is the payload encoded in a specific format.

    # build our Request object (supplying 'data' makes it a POST)
    req = urllib.request.Request(authentication_url, data)
    # what is a request? A request is a request to the server to do something.
    # what is a response? A response is the server's response to the request.

    # make the request
    # try using 'with' here
    with urllib.request.urlopen(req) as response:
        # the page we were trying to access should now be accessible.
        # we should have a 200 response if everything is ok
        if response.get_code() == 200:
            print("Successfully logged in")
            # save the cookies again
            cookie_jar.save(ignore_discard=True, ignore_expires=True)
            # now that we have the initial cookies set up, we can access authenticated pages
        else:
            print("Could not log in")
            # if we couldn't log in, delete the cookie file
            if os.path.isfile(cookie_filename):
                os.remove(cookie_filename)
            else:
                print("The cookie file was not found")

    # what are cookies?
    # Cookies are small pieces of data that are stored on your computer by your web browser.
    # Cookies are created when you visit a website that uses cookies to keep track of your movements within the site, help you resume where you left off, remember your registered login, theme selection, preferences, and other customization functions.

    perform_inner_actions()

    # what have we done in this function?
    # we have logged into linkedin and saved the contents of the feed to a file, test.html. We have also saved the cookies to a file, parser.cookies.txt. We will use the cookies to access the feed again in the future. We will use the contents of the feed to parse the data we want.


def perform_inner_actions(url, filename):
    # now that we have the initial cookies set up, we can access authenticated pages

    hiring_manager_profiles = []

    # what have we done in this function?

    # "https://www.linkedin.com/feed/"
    # read the response
    # contents = resp.read()
    # if not os.path.exists('./data'): # if the data folder does not exist
    #     os.makedirs('./data') # make the data folder
    # with open('./data/test.html', 'wb') as f: # write the contents to a file
    #     f.write(contents) # write the contents to the file


class LinkedInParser(object):  # class for parsing
    # docstring
    """docstring for LinkedInParser"""

    def __init__(self, login, password):
        """Start up..."""
        self.login = login
        self.password = password
        self.logged_in = False
        self.opener = None
        self.cookie_jar = None
        self.cookie_filename = "./src/parser.cookies.txt"

        # Simulate browser with cookies enabled
        self.cookie_jar = cookielib.MozillaCookieJar(self.cookie_filename)
        if os.access(self.cookie_filename, os.F_OK):
            self.cookie_jar.load()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPRedirectHandler(),
            urllib.request.HTTPHandler(debuglevel=0),
            urllib.request.HTTPSHandler(debuglevel=0),
            urllib.request.HTTPCookieProcessor(self.cookie_jar),
        )
        self.opener.addheaders = [
            (
                "User-agent",
                (
                    "Mozilla/4.0 (compatible; MSIE 6.0; "
                    "Windows NT 5.2; .NET CLR 1.1.4322)"
                ),
            )
        ]

        # Login
        self.loginPage()  # login to linkedin
        print("Logged in")
        title = self.loadTitle()  # load the title of the page
        print(title)  # print the title of the page
        self.logged_in = True
        self.cookie_jar.save()
        # we are now logged in and have saved the cookies

    def loadPage(self, url, data=None):
        """
        Utility function to load HTML from a URL. Deal with HTTP, URL and other errors with try/except blocks. Return the HTML as a string.
        """
        # We'll print the url in case of infinite loop
        # print "Loading URL: %s" % url
        try:
            if data:
                response = self.opener.open(url, data)
            else:
                response = self.opener.open(url)
            html = response.read()
            return html
        except urllib.error.HTTPError as error:  # what is an HTTPError? An HTTPError is an error that occurs when the server returns an HTTP error code.
            print(f"HTTP Error: {error.code} {url}")
            return None
        except urllib.error.URLError as error:  # url error exception handling
            print(f"URL Error: {error.reason} {url}")
            return None
        except Exception as error:  # catch *all* exceptions
            print(f"Generic Exception: {error} {url}")  # Python 3.0
            return None

    def loadSoup(self, url, data=None):
        """
        Combine loading of URL, HTML, and parsing with BeautifulSoup
        """
        html = self.loadPage(url, data)
        soup = BeautifulSoup(html, "html5lib")
        return soup

    def loginPage(self):
        """
        Handle login. This should populate our cookie jar.
        """
        soup = self.loadSoup("https://www.linkedin.com/")
        csrf = soup.find(id="loginCsrfParam-login")["value"]
        login_data = urllib.parse.urlencode(
            {
                "session_key": self.login,
                "session_password": self.password,
                "loginCsrfParam": csrf,
            }
        ).encode("utf8")

        self.loadPage("https://www.linkedin.com/uas/login-submit", login_data)
        return

    def loadTitle(self):
        soup = self.loadSoup("https://www.linkedin.com/feed/")
        return soup.find("title")


# Graham: Where should I be calling the copilot_generated_function() function?
# Copilot: You should call the copilot_generated_function() function in the main function.


def main():  # main function
    print("Beginning Process")
    parser = LinkedInParser(
        username, password
    )  # username and password are in secrets.json
    print("Logged in")
    # * Trying the copilot_generated_function() function
    copilot_generated_function()
    # * Trying the copilot_generated_function() above
    title = parser.loadTitle()  # load the title of the page
    print(title)  # print the title of the page
    print("Ending Process")


if __name__ == "__main__":
    main()  # run the main function
