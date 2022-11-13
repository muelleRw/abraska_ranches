import requests
from bs4 import BeautifulSoup, SoupStrainer
from map_wrong import map_right_data

url = 'https://clarklandbrokers.com/all-farms-and-ranches-for-sale/'
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

ranches = list()
for card in soup.select('.ult-colum, .col-md-4'):
    ranch = None

    for link in card.select("a"):
        ranch = {
            "name": link.get_text(),
            "page": link['href']
        }
    if ranch is not None and ranch['name'] != '':
        for price in card.select("em"):
            ranch['price'] = price.text
            ranch['details'] = price.parent.text
        ranches.append(ranch)

for ranch in ranches:
    print(ranch)
    page = requests.get(ranch['page'])
    soup = BeautifulSoup(page.content, "html.parser")
    for iframe in soup.select('iframe'):
        if 'mapright' in iframe['src']:
            ranch['map'] = iframe['src']
        elif 'mapright' in iframe['data-lazy-src']:
            ranch['map'] = iframe['data-lazy-src']
    
    if "map" in ranch:
        ranch['geojson'] = map_right_data(ranch['map'])

import json
with open('clark_land_brokers.json', 'w') as f:
    json.dump(ranches,f)