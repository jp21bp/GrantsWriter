###### Web Scraper file
    # This file will be used for the web scraper tool

##### Genereal steps
    # 1. Hardcode the URL main webpage
    # 2. Get a list of URLS associated with main webpage
    # 3. Setup scraping fcn to get URL contents and put into one big text file
    # 4. Cleanup HTML to make it more human readible
    # 5. Save human readible info into separate text file

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
    # Getting raw webpage
soup = BeautifulSoup(response.text, 'html.parser')
    # Get HTML of webpage

#### Getting all the anchors in page navbar
links = {}
    # Creating dictionary to store all links found on navbar
menu = soup.find(id="menu-menu-1")
    # Getting navbar tag
anchors = menu.find_all('a')
    # Gets all anchors in navbar
        # Will be used to create values of "links" dict

for anchor in anchors:  # Loops through all found anchors
    contents = anchor.contents
        # Returns anything (including other tags) inside "a" tag
            # Will be used to create KEYS of "links"
    link_name = contents[0]
        # Usually string, non-tag content is first item
    href = anchor.get('href')
        # link associated with anchor
            # Used to create values of "links"
    if link_name in links:
        if href in links[link_name]: continue
        links[link_name].append(href)
    else:
        links[link_name] = [href]

# for k,v in links.items():
#     print(f"Link Name: {k}")
#     print(f"Links: {v}")
#     print('\n\n')

##### Step 3 - 5
    # 3. Will go through ALL links and extract the content
    # 4. Will make extracted content human readible
    # 5. Content will be placed on one big text file
    
visited = []
    # Will be used to store the links that've already been visited

try:
    file = open("LAFF_webpage_contents.txt", "x")
        # Create file
except:
    file = open("LAFF_webpage_contents.txt", "a")
        # Open file for appending

for name, link_list in links.items():
    for link in link_list:
        response = requests.get(link, headers=headers)
            # Get raw webpage contents
        if link not in visited:
            visited.append(link)
                # Assume link gets visited
            soup = BeautifulSoup(response.text, 'html.parser')
                # Turn raw webpage into HTML format
            body = soup.find(id="main")
                # Get the body of the webpage
            page_contents = body.get_text(separator="\t",strip=True)
            
            file.write(name + "\n")
            file.write(page_contents + "\n")
            file.write("=" * 30 + "\n")












