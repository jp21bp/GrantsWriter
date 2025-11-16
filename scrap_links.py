##### Clean file for scraping all links associated with main organization
#### Gameplan
    # Step 1:
    # Step 2:


##### Step 1: setup main page
import requests
from bs4 import BeautifulSoup

starter_url = "https://www.laffcharity.org.uk/"
headers = {'User-Agent': "Mozilla/5.0"}

response = requests.get(starter_url, headers=headers)
    # Getting raw webpage
soup = BeautifulSoup(response.text, 'html.parser')
    # Get HTML of webpage


#### Step 2: Getting all the anchors in main page navbar
unique_links = []
    # Creating dictionary to store all links found on navbar
menu = soup.find(id="menu-menu-1")
    # Getting navbar tag
        # All related to main organization
anchors = menu.find_all('a')
    # Gets all anchors in navbar
        # Will be used to create values of "links" dict
for anchor in anchors:
    link = anchor.get('href')
        # link associated with anchor
    if link in unique_links: continue
    unique_links.append(link)
        # All links will be from main organization


#### Step 3: Traverse unique links to find new links
new_links = []
for link in unique_links:
    # print(f"Working on {link}")
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.find(id='main')
    anchors = body.find_all('a')
    for anchor in anchors:
        new_link = anchor.get('href')
        if new_link in unique_links: continue
        elif new_link in new_links: continue
        new_links.append(new_link)

unique_links = unique_links + new_links


#### Step 4: Clean up the unique links to delete internal DB content
important_links = []

for link in unique_links:
    if not link.startswith("http"): continue
    elif "upload" in link: continue
    important_links.append(link)






