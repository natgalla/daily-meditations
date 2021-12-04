import requests
from bs4 import BeautifulSoup as bs
import pymongo
import datetime

# establish DB connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.spiritual
db.meditations.drop()
collection = db.meditations

# set to current date
year = 2021
month = 11
day_of_month = 30
start_time = datetime.datetime(year, month, day_of_month, 0, 0, 0, 0)

# url to scrape for thich nhat hanh
url = "https://www.brainyquote.com/authors/thich-nhat-hanh-quotes"

# get html from response
response = requests.get(url)
soup = bs(response.content, 'html.parser')

# retrieve quote blocks
results = soup.findAll('a',class_='b-qt')

# gather thich nhat hanh quotes from html
thich_quotes = []
for result in results:
    quote = result.text
    quote = quote.replace('\n', '')
    thich_quotes.append(quote)


# url to scrape for gospel of thomas
url = "https://www.gospels.net/thomas/"
# get html from response
response = requests.get(url)
soup = bs(response.content, 'html.parser')

# retrieve quote blocks
results = soup.findAll('p')

# array for storing sayings and empty string for sayings stored in multiple p tags
got_sayings = []
saying = ''
saying_number = 0

# loop over results
for result in results:
    # strip results of noise
    text_block = result.text.replace('\n', '')
    text_block = text_block.replace('\\', '')
    text_block = text_block.replace('"', '')

    # append the final saying and break the loop when sayings are over
    if "According to Thomas" in text_block:
        got_sayings.append(saying)
        break
    # when a new saying starts, append current saying to got_sayings and wipe saying string
    elif "Saying" in text_block:
        if saying_number > 0:
            got_sayings.append(saying)
        saying_number += 1
        saying = ''
    # if there is text in the text_block, add it to the current saying
    elif len(text_block) > 5 and saying_number > 0:
        saying += f'{text_block} '

# pack the scraped data into a dict
data_obj = {
    'thich_quotes' : thich_quotes,
    'got_sayings' : got_sayings,
    'thich_quote' : thich_quotes[0],
    'got_saying' : got_sayings[0],
    'thich_stale' : [thich_quotes[0]],
    'got_stale' : [got_sayings[0]],
    'meta' : {
        'last_refresh' : start_time
    }
}

# store the dict in mongo
collection.insert_one(data_obj)

# print the mongo db collection to the console to validate storage
quotes = db.meditations.find()
for quote in quotes:
    print(quote)
