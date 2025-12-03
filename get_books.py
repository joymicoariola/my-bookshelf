import mechanicalsoup
import logging
import time
import datetime


# Setup Logging
logging.basicConfig(filename="get_titles.log", level=logging.INFO, filemode="w")

# Setup URLs configs in the Global Scope because Flask cannot see it within the __if name__
goodreads_url = ""
read_shelf_url = ""
to_read_shelf_url = ""


# -------------------------------------------------------------------


def get_last_run_date():
   """
   Gets the last run date of the Goodreads scraper.
   """


   # Use datetime to get the day the Goodreads scraper was last run
   get_date = datetime.datetime.now()


   # Make the date pretty for the UI
   month = get_date.strftime("%B")
   day = get_date.day
   year = get_date.year
   return(f"{month} {day}, {year}.")




# -------------------------------------------------------------------




def create_browser(goodreads_url):
   """
   Creates the browser object to access the Goodreads page. Uses user_agent in order to
   mimic a real browser to avoid 403 errors as browser detects this scraper as a bot.


   [Parameters]
   goodreads_url -> string


   [Returns]
   browser -> The MechancialSoup special Browser Object


   """


   browser = mechanicalsoup.StatefulBrowser()


   # Prevent 403 error, set the User-Agent to look like a real browser (Chrome on Windows)
   user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


   browser.session.headers.update({
       'User-Agent': user_agent
   })


   # Now query to get access to the website
   response = browser.open(goodreads_url)


   # Check if it worked
   if response.status_code == 200:
       logging.info("Success! Connected to the website.")
   else:
       logging.error(f"Failed with error: {response.status_code}")
   return browser


# -------------------------------------------------------------------


def scrape_read_shelf(browser, read_shelf_url):
   """
   Navigates to the "Read" shelf to scrape the book titles.


   [Parameters]
   browser -> The special Browser Object created in create_browser()
   read_shelf_url -> The specific URL for the "Read" shelf


   [Returns]
   clean_titles -> A Python list of strings
   """


   # Browse to "read" shelf
   response = browser.open(read_shelf_url)


   # Check if it worked
   if response.status_code == 200:
       logging.info("Success! Correctly followed link to 'Read' books shelf")
   else:
       logging.error(f"Failed with error: {response.status_code}")


   # 1. Book_titles is a LIST (A container)
   book_titles = browser.page.select("td.field.title a")


   # 2. Loop through the list to pick up ONE ITEM
   clean_titles = []
   for link in book_titles:


       # Use . get() to prevent crashing if a title is missing
       # 3. "link" is a TAG OBJECT (The suitcase)
       # It allows us to reach into its internal dictionary of attributes using .get()
       title_text = link.get("title")


       # Found the title text!
       if title_text:
           clean_titles.append(title_text)
           logging.info(title_text)
       # Error catching if the title is not available
       else:
           logging.warning("Found a book link, but it had no title attribute to scrape.")
   logging.info(f"Scraping complete. Found: {len(clean_titles)} books.")
   return clean_titles


# -------------------------------------------------------------------


def scrape_to_read_shelf(browser, to_read_shelf_url):
   """
   Navigates to the "Read" shelf to scrape the book titles.


   [Parameters]
   browser -> The special Browser Object created in create_browser()
   to_read_shelf_url -> The specific URL for the "Read" shelf


   [Returns]
   clean_titles -> A Python list of strings
   """

   # Browse to "read" shelf
   response = browser.open(to_read_shelf_url)

   # Check if it worked
   if response.status_code == 200:
       logging.info("Success! Correctly followed link to 'To-Read' books shelf")
   else:
       logging.error(f"Failed with error: {response.status_code}")


   # 1. Book_titles is a LIST (A container)
   book_titles = browser.page.select("td.field.title a")


   # 2. Loop through the list to pick up ONE ITEM
   clean_titles = []
   for link in book_titles:


       # Use . get() to prevent crashing if a title is missing
       # 3. "link" is a TAG OBJECT (The suitcase)
       # It allows us to reach into its internal dictionary of attributes using .get()
       title_text = link.get("title")


       # Found the title text!
       if title_text:
           clean_titles.append(title_text)
           logging.info(title_text)
       # Error catching if the title is not available
       else:
           logging.warning("Found a book link, but it had no title attribute to scrape.")
   logging.info(f"Scraping complete. Found: {len(clean_titles)} books.")
   return clean_titles


# -------------------------------------------------------------------
# THE MAIN EXECUTION BLOCK
# -------------------------------------------------------------------


if __name__ == "__main__":


   print(get_last_run_date())


   # Create the tool (The Browser, the special Mechanical Soup object)
   my_browser = create_browser(goodreads_url)


   # Use the tool to get the title of the books
   my_books_read = scrape_read_shelf(my_browser, read_shelf_url)
   my_books_to_read = scrape_to_read_shelf(my_browser, to_read_shelf_url)


   # Print to check for success
   print(f"\nFinal Result: {my_books_read}")
   print(f"\nFinal Result: {my_books_to_read}")


