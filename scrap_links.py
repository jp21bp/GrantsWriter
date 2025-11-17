##### Clean file for scraping all links associated with main organization

'''      GAMEPLAN 1
#### Gameplan 1
    # Step 1. Hardcode the URL main webpage
    # Step 2. Get a list of URLS associated with main webpage
    # Step 3. Setup scraping fcn to get URL contents
    # Step 4. Cleanup HTML to make it more human readible
    # Step 5. Save human readible info into separate text file
    # Issue with Gameplan 1

##### Step 1
starter_url = "https://www.laffcharity.org.uk/",
headers = {'User-Agent': "Mozilla/5.0"}


##### Step 2
import requests
from bs4 import BeautifulSoup

response = requests.get(starter_url, headers=headers)
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
    contents = anchor.contents()
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
        if link not in visited:
            response = requests.get(link, headers=headers)
                # Get raw webpage contents
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


#### Issue with Gameplan 1
    # This gameplan only extracts material from the main organization
    # BUT there are 3 partner organizations that also hold important info
    # Recall agent goal:
        # This'll be an agent that develops a grant for main organization
    # Thus, it'll be important for agent to also be aware about info
            # from the partner organizations
'''





















































'''     GAMEPLAN 2
#### Gameplan 2
    # Step 1: Setup main page
    # Step 2: Getting all the anchors in main page navbar
    # Step 3: Traverse unique links to find new links
    # Step 4: Clean up the unique links to delete internal picture content
    # Issue with gameplan 2


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


#### Step 4: Clean up the unique links to delete internal picture content
important_links = []

for link in unique_links:
    if not link.startswith("http"): continue
    elif "upload" in link: continue
    important_links.append(link)

#### Issue with this gameplan 2:
    # Returns a list of important, unique links
    # But some of those links are useless or outdated
    # It'll take a while to test all links to see which are valuable
'''




























































#### Gameplan 3
    # Step 1: Setting up urls from main org. and partner orgs.
    # Step 2: Create function to find unique links from a list of <a> anchors
    # Step 3: Create function to scrape the links of a URL
    # Step 4: Apply both functions to the main urls in step 2
    # Step 5: Place the results in a text file using 'json' module
    # Known issues:
        # All sites have <nav> tag, except mantay
        # Sacred Valley only has sub-domain names to their page
            # Thus, the domain name will need to be added to them
            # Sacred Valley is probably a single-page appplication


#### Step 1: Setting up urls from main org. and partner orgs.
import requests, json
from bs4 import BeautifulSoup

main_urls =[
    "https://www.laffcharity.org.uk/",
    "https://www.mantay.org/",
    "https://www.mosqoy.org/",
    "https://www.sacredvalleyproject.org/"
]

org_links = {}
    #Used to store links with each organization
    #Schema:
        # {organization_name: {link_name: link}}
        #I.e., the name to the link will also be extracted


#### Step 2: Create function to find unique links from a list of <a> anchors
def find_unique_dict(anchors_list: list[str]) -> dict:
    links_visited = []   #Links already visited
    unique_dict = {}    # Schema: {link_name: link}
    for anchor in anchors_list:
        link = anchor.get('href')
        if link in links_visited: continue
        links_visited.append(link)
        page_name = anchor.get_text()
        unique_dict[page_name] = link
    return unique_dict


#### Step 3: Create function to scrape the links of a URL
def scrape_links(url: str) -> dict:
    headers = {'User-Agent': "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
        #HTTP Response
    soup = BeautifulSoup(response.text, 'html.parser')
        #HTML version of response
    navbar = soup.find('nav')
        # <nav> is where the site's links are at
    if url == "https://www.mantay.org/":
        # "mantay" doesn't have <nav> tag
        navbar = soup.find(id='menu-main-menu')
    anchors = navbar.find_all('a')
        # Finding all anchors associated with the page
    return find_unique_dict(anchors)


#### Step 4: Apply both functions to the main urls in step 2
for url in main_urls:
    org_name = url.split(".")[1]
        # Scrapped organization name from it's website URL
        # Ex: "https://www.laffcharity.org.uk/"
            #-> ['https://www', 'laffcharity', 'org', 'uk']
            #-> "laffcharity"
    org_links[org_name] = scrape_links(url)


#### Step 5: Place the results in a text file using 'json' module
with open('all_links.json', 'w') as file:
    json.dump(org_links, file, indent=4)

















