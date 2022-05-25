# WIP
import requests, re
from bs4 import BeautifulSoup

import tokens #delete this
token = tokens.get_value() # Paste token here

prefix = "https://api.twitter.com/2/tweets/"

url = "https://twitter.com/rT8ChfHbFiesRdN/status/1528212239223644160?s=20&t=QvZ-h8GNLrtMzWWv5DgntQ" # Input URL

api_request = prefix+re.findall(r'\/(\d*)\?', url)[0]+"?expansions=author_id,attachments.media_keys&media.fields=url"

head = {
    "Authorization": "Bearer "+token
}
page = requests.get(api_request,headers=head).content
print(page.decode())