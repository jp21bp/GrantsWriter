###### Web Scraper file
    # This file will be used for the web scraper tool

##### Genereal steps
    # 1. Hardcode the URLS
    # 2. Setup scraping fcn to get URL contents
    # 3. Cleanup HTML to make it more human readible
    # 4. Save human readible info into separate folder

##### Step 1
URLS = [
    "https://www.laffcharity.org.uk/",
    "https://en.wikipedia.org/wiki/%22Hello,_World!%22_program",
    "https://google.com"
]
headers = {'User-Agent': "Mozilla/5.0"}


##### Step 2
import requests
from bs4 import BeautifulSoup

response = requests.get(URLS[0], headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')













