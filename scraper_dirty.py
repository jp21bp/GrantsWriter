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

#### Analyzing response
# print(response) #<Response[200]>
# print(response.status_code) # 200

# methods = []
# for attr in dir(response):
#     if attr.startswith("_"): continue
#     methods.append(attr)

# print(methods)
#     #output
#     #['apparent_encoding', 'close', 'connection', 'content', 
#     # 'cookies', 'elapsed', 'encoding', 'headers', 'history', 
#     # 'is_permanent_redirect', 'is_redirect', 'iter_content', 
#     # 'iter_lines', 'json', 'links', 'next', 'ok', 
#     # 'raise_for_status', 'raw', 'reason', 'request', 'status_code',
#     #  'text', 'url']


# print('\n\n')
# # print(response.text)    #returns HTML content
# # print('\n\n')
# print(response.url) #Returns URL
# print(response.reason)  # OK/Forbidden
# print(response.headers) #Rturns metadata

soup = BeautifulSoup(response.text, 'html.parser')

#### Analyzing beautiful soup

# print(type(soup))   #bs4.BeautifulSoup
# print(soup.prettify)    #structured print of HTML

# print(soup.find(class_="collapse navbar-collapse"))
### Exploring "bs4.element.Tag"
links = soup.find(id="menu-menu-1")
# print(type(links))  #bs4.element.Tag
# print(links.get_text)   #gets HTML of that "id" section
# print(links.contents)   #returns list
# print(len(links.contents))  #Returns 14, in this case

# for link in links.contents:
#     print(link)

### Analyzing "a" tags
anchors = links.find_all('a')  

# print(type(anchors))    #bs4.element.ResultSet, also a list
# print(len(anchors))     # 40, in this case

# for i, anchor in enumerate(anchors):
#     print(f"iterations {i}")
#     print(anchor)
#     print('\n')
#     print(anchor.contents)
#     print('\n')
#     # href = anchor.find('href')
#     href = anchor.get('href')
#     print(href)
#     print('\n\n')
#     if i == 10: break

##### Step 2.1: getting anchor links from web navbar
    #I.e., creating a dict for "links"

links = {}
for anchor in anchors:
    contents = anchor.contents
        # Returns anything (including other tags) inside "a" tag
    link_name = contents[0]
        # Usually string, non-tag content is first item
    href = anchor.get('href')
    if link_name in links:
        if href in links[link_name]: continue
        links[link_name].append(href)
    else:
        links[link_name] = [href]

for k,v in links.items():
    print(f"Key: {k}")
    print(f"Links: {v}")
    print('\n\n')











##### Step 3













