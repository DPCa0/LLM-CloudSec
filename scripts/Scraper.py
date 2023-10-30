import requests
from bs4 import BeautifulSoup
import json

url = "https://cwe.mitre.org/top25/archive/2023/2023_top25_list.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

cwe_list = []
for item in soup.find_all('span', {'class': 'list_id'}):
    cwe_id = int(item.a.text.split('-')[1])
    name = item.a['title']
    detail_url = "https://cwe.mitre.org" + item.a['href']
    detail_response = requests.get(detail_url)
    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
    detail_divs = detail_soup.find_all('div', {'class': 'detail'})
    description = detail_divs[0].text.strip() if detail_divs else ''
    extended_description = detail_divs[1].text.strip() if len(detail_divs) > 1 else ''

    cwe_list.append({
        "id": cwe_id,
        "name": name,
        "description": description,
        "extended_description": extended_description,
    })

with open('cwe_data.json', 'w') as f:
    json.dump(cwe_list, f, indent=4)
