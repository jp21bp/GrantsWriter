###### This file will scrap the content from the links retrieved 
            # in scrap_links.py

##### Gameplan
    # Step 1: Import the JSON file that holds extracted links
    # Step 2: Get the BeautifulSoup of each link in ONE org
    # Step 3: Extract contents from the one organzation soup
    # Step 4: Loop over ALL organizations



##### Step 1: Import the JSON file that holds extracted links
import json, requests
from bs4 import BeautifulSoup

with open('all_links.json', 'r') as file:
    org_dict = json.load(file)


##### Step 4: Loop over ALL organizations
headers = {'User-Agent': "Mozilla/5.0"}

for org_name, link_dict in org_dict.items():
    with open(f'{org_name}_contents.txt', 'w') as file:
        for name, link in link_dict.items():
            ##### Step 2: Get the BeautifulSoup of each link in ONE org
            response = requests.get(link, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            if org_name == "mosqoy" or org_name == "sacredvalleyproject":
                body = soup.find('main')
            else:
                body = soup.find(id='main')   
                if not body:
                    body = soup.find('body')
            ##### Step 3: Extract contents from the one organzation soup
            try:
                page_contents = body.get_text(separator='\t', strip=True)
            except:
                continue
            file.write(name + '\n')
            file.write(page_contents + '\n')
            file.write('=' * 30 + '\n')







