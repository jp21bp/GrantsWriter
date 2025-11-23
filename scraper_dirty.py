# ###### Web Scraper file
#     # This file will be used for the web scraper tool

# ##### Genereal steps
#     # 1. Hardcode the URL main webpage
#     # 2. Get a list of URLS associated with main webpage
#     # 3. Setup scraping fcn to get URL contents
#     # 4. Cleanup HTML to make it more human readible
#     # 5. Save human readible info into separate text file

# ##### Step 1
# URLS = [
#     "https://www.laffcharity.org.uk/",
#     "https://www.laffcharity.org.uk/resources/volunteer-resources/",
#     'https://www.laffcharity.org.uk/events/',
#     "https://en.wikipedia.org/wiki/%22Hello,_World!%22_program",
#     "https://google.com"
# ]

# headers = {'User-Agent': "Mozilla/5.0"}


# ##### Step 2
# import requests
# from bs4 import BeautifulSoup

# response = requests.get(URLS[2], headers=headers)

# #### Analyzing response
# # print(response) #<Response[200]>
# # print(response.status_code) # 200

# # methods = []
# # for attr in dir(response):
# #     if attr.startswith("_"): continue
# #     methods.append(attr)

# # print(methods)
# #     #output
# #     #['apparent_encoding', 'close', 'connection', 'content', 
# #     # 'cookies', 'elapsed', 'encoding', 'headers', 'history', 
# #     # 'is_permanent_redirect', 'is_redirect', 'iter_content', 
# #     # 'iter_lines', 'json', 'links', 'next', 'ok', 
# #     # 'raise_for_status', 'raw', 'reason', 'request', 'status_code',
# #     #  'text', 'url']


# # print('\n\n')
# # # print(response.text)    #returns HTML content
# # # print('\n\n')
# # print(response.url) #Returns URL
# # print(response.reason)  # OK/Forbidden
# # print(response.headers) #Rturns metadata

# soup = BeautifulSoup(response.text, 'html.parser')

# #### Analyzing beautiful soup

# # print(type(soup))   #bs4.BeautifulSoup
# # print(soup.prettify)    #structured print of HTML

# # print(soup.find(class_="collapse navbar-collapse"))
# ### Exploring "bs4.element.Tag"
# links = soup.find(id="menu-menu-1")
# # print(type(links))  #bs4.element.Tag
# # print(links.get_text)   #gets HTML of that "id" section
# # print(links.contents)   #returns list
# # print(len(links.contents))  #Returns 14, in this case

# # for link in links.contents:
# #     print(link)

# ### Analyzing "a" tags
# anchors = links.find_all('a')  

# # print(type(anchors))    #bs4.element.ResultSet, also a list
# # print(len(anchors))     # 40, in this case

# # for i, anchor in enumerate(anchors):
# #     print(f"iterations {i}")
# #     print(anchor)
# #     print('\n')
# #     print(anchor.contents)
# #     print('\n')
# #     # href = anchor.find('href')
# #     href = anchor.get('href')
# #     print(href)
# #     print('\n\n')
# #     if i == 10: break

# ##### Step 2.1: getting anchor links from web navbar
#     #I.e., creating a dict for "links"

# links = {}
# for anchor in anchors:
#     contents = anchor.contents
#         # Returns anything (including other tags) inside "a" tag
#     link_name = contents[0]
#         # Usually string, non-tag content is first item
#     href = anchor.get('href')
#     if link_name in links:
#         if href in links[link_name]: continue
#         links[link_name].append(href)
#     else:
#         links[link_name] = [href]

# # for k,v in links.items():
# #     print(f"Key: {k}")
# #     print(f"Links: {v}")
# #     print('\n\n')











# ##### Step 3
# # print("STEP 3")
# # # print(soup.prettify())
# # body = soup.find(id="main")
# # # print(body.prettify())
# # # print(body.get_text(strip=True))
# # print(body.get_text(separator="\t", strip=True))









# ##### TODO: add more links to the "links"
#     # I.e, these are links assciated with LAFF
#         # Ex: partner organiazation
#     # This would have to be done through the search of the page

# visited = [] # Stores links already visited
# new_anchors = []
# for name, link_list in links.items():
#     for link in link_list:
#         if link not in visited:
#             response = requests.get(link, headers=headers)
#                 # Get raw webpage contents
#             visited.append(link)
#                 # Assume link gets visited
#             soup = BeautifulSoup(response.text, 'html.parser')
#                 # Turn raw webpage into HTML format
#             body = soup.find(id="main")
#                 # Get the body of the webpage
#             # page_contents = body.get_text(separator="\t",strip=True)
#             anchors = body.find_all('a')
#                 # Returns a list
#             new_anchors.append(anchors)
#                 # "new_anchors" will be a list of list



# def flatten(matrix):
#     # Turns 2d list -> 2d list
#     flat_list = []
#     for row in matrix:
#         flat_list += row
#     return flat_list

# new_anchors = flatten(new_anchors)

# print("New anchors")
# # for anchor in new_anchors:
# #     print(anchor)
# #     print('\n\n')

# unseen_anchors=[]
# for anchor in new_anchors:
#     link = anchor.get('href')
#     # print(link)
#     if link in visited: continue
#     elif "uploads" in str(link):
#         continue
#         # Has pics/data from database
#         # Not actually links
#     visited.append(link)
#     unseen_anchors.append(anchor)

# for anchor in unseen_anchors:
#     name = anchor.get_text()
#     link = anchor.get('href')
#     print(f"Name: {name}")
#     print(f"Link: {link}")
#     print('\n')




# # new_links={}
# #     # Stores links found while traversing organization's page
# # for anchor in new_anchors:
# #     href = anchor.get('href')
# #     if href in visited:continue
# #     visited.append(href)
# #     contents = anchor.contents()
# #     link_name = contents[0]
# #     new_links[link_name] = href

# # for k,v in new_links.items():
# #     print(f"Key: {k}")
# #     print(f"Link: {v}")
# #     print('\n\n')











































# ###### Second scraper
# ##### New gameplan
#     # Go through ALL links first
#         # Before extracting any info
#     # Then organize the links by organization name
#         # EX: link.startswith("laff"): laff_links.append(link)
#         # Better to use a dictionary
#     # After all possble links have been seen, THEN extract info


# ##### Step 1
# starter_url = "https://www.laffcharity.org.uk/"
# headers = {'User-Agent': "Mozilla/5.0"}


# ##### Step 2
# import requests
# from bs4 import BeautifulSoup

# response = requests.get(starter_url, headers=headers)
#     # Getting raw webpage
# soup = BeautifulSoup(response.text, 'html.parser')
#     # Get HTML of webpage

# #### Flatten fcn
# def flatten(matrix):
#     # Turns 2d list -> 2d list
#     flat_list = []
#     for row in matrix:
#         flat_list += row
#     return flat_list



# #### Getting all the anchors in page navbar
# unique_links = []
#     # Creating dictionary to store all links found on navbar
# menu = soup.find(id="menu-menu-1")
#     # Getting navbar tag
#         # All related to main organization
# anchors = menu.find_all('a')
#     # Gets all anchors in navbar
#         # Will be used to create values of "links" dict
# for anchor in anchors:
#     link = anchor.get('href')
#         # link associated with anchor
#     if link in unique_links: continue
#     unique_links.append(link)
#         # All links will be from main organization


# print(unique_links)
#     # All links will be from main organization
# new_links = []

# #### Traverse links to find new links
# for link in unique_links:
#     # print(f"Working on {link}")
#     response = requests.get(link, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     body = soup.find(id='main')
#     anchors = body.find_all('a')
#     for anchor in anchors:
#         new_link = anchor.get('href')
#         if new_link in unique_links: continue
#         elif new_link in new_links: continue
#         new_links.append(new_link)


# #### Reviewing the unique link anchors
# print("\nNEW LINKS\n")
# for link in new_links:
#     print(link)


















































###### Third scraper
    # NEW new gameplan
    # simply scrape the important sites, which will be hard coded
##### Webpage design issues:
    # Mantay not have <nav>, while others do
    # SacredValley doesn't have domain name in links
        # It's probably a single page application (SPA)

# import requests
# from bs4 import BeautifulSoup

# main_urls =[
#     "https://www.laffcharity.org.uk/",
#     "https://www.mantay.org/",
#     "https://www.mosqoy.org/",
#     "https://www.sacredvalleyproject.org/"
# ]




# org_links = {}
#     #USed to store links with each organization




# def find_unique_links(anchors_list: list[str]) -> dict:
#     unique_links = []
#     unique_dict = {}
#     for anchor in anchors_list:
#         link = anchor.get('href')
#         if link in unique_links: continue
#         unique_links.append(link)
#         page_name = anchor.get_text()
#         unique_dict[page_name] = link
#     return unique_dict


# def scrape_links(url: str) -> list:
#     headers = {'User-Agent': "Mozilla/5.0"}
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     # unique_links = []
#     navbar = soup.find('nav')
#     if url == "https://www.mantay.org/":
#         navbar = soup.find(id='menu-main-menu')
#         # print('changed navbar')
#     anchors = navbar.find_all('a')
#     # print(type(anchors))
#     # print(anchors[0:2])
#     # print(anchors[0].get('href'))

#     # print(anchors[0].get_text())
#     # anch = anchors[0]
#     # content = anch.contents
#     # print(content[0])
#     # print(type(anch.contents()))
#     return find_unique_links(anchors)

#     # print(navbar.prettify())
#     # print(soup.prettify())

# ## hard to do a fcn
#     # can't assume all sites structured same way
#     # After research I can see that all use <nav> tag
#         # except mantay orgnization

# for url in main_urls:
#     org_name = url.split(".")[1]
#     # print(org_name)
#     org_links[org_name] = scrape_links(url)
#     # print(f"Organization: {url}" + '\n')
#     # scrape_links(url)
#     # print('\n' * 20)


# #### Fixing sacred valley issue

# # svp_links = []
# # for link in org_links['sacredvalleyproject']:
# #     link = 'https://www.sacredvalleyproject.org' + link
# #     svp_links.append(link)
# # # print(svp_links)
# # org_links['sacredvalleyproject'] = svp_links


# for k,v in org_links.items():
#     print(f"Org: {k}")
#     print("Links:")
#     for name, link in v.items():
#         print(f"Name: {name}\tLink: {link}")
#     print('\n'*3)























































###### Scraping the link contents

import json, requests
from bs4 import BeautifulSoup

# with open('./links_and_documents/all_links.json', 'r') as file:
#     org_dict = json.load(file)

# # for k,v in org_dict.items():
# #     print(f"org: {k}")
# #     for name, link in v.items():
# #         print(f"name: {name}\tlink: {link}")

# # print(org_dict.keys())


# ### Recall, each page is structured diff.
#     # So we need to find the "body" of each page
#     # SVP has <main> tag
#     # moswoy has <main> tag
#     # mantay has id='main'
#         # body = soup.find(id='main')   
#         # if not body:
#         #     body = soup.find('body')
#     # Laff has id='main'


# ### Extract 1 link
# orgs_names = []
# for org in org_dict.keys():
#     orgs_names.append(org)

# # org_name = org_dict[orgs_names[1]]
# headers = {'User-Agent': "Mozilla/5.0"}

# for org_name, link_dict in org_dict.items():
#     if org_name != "sacredvalleyproject": continue
#     with open(f'{org_name}_contents.txt', 'w') as file:
#         for name, link in link_dict.items():
#             # print(org_name)
#             response = requests.get(link, headers=headers)
#             soup = BeautifulSoup(response.text, 'html.parser')
#             if org_name == "mosqoy" or org_name == "sacredvalleyproject":
#                 # print('there')
#                 body = soup.find('main')
#             else:
#                 # print('here')
#                 body = soup.find(id='main')   
#                 if not body:
#                     body = soup.find('body')
#             # body = soup
#             try:
#                 page_contents = body.get_text(separator='\t', strip=True)
#             except:
#                 continue
#             # break
#             file.write(name + '\n')
#             file.write(page_contents + '\n')
#             file.write('=' * 30 + '\n')
#             # break
#         # break



url = 'https://www.mosqoy.org/faq-1'
headers = {'User-Agent': "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)
# print('\n'*20)
body = soup.find_all('body')
# page_contents = body.get_text(separator='\t', strip=True)
for found in body:
    page_contents = found.get_text(separator='\t', strip=True)
    print(page_contents)
    print('\n' * 20)



























