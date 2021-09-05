from bs4 import BeautifulSoup
import sys
import requests
import json

query = sys.argv[1]

# print(query)
url = 'https://arxiv.org/search/?query='+query + \
    '&searchtype=all&abstracts=show&order=-announced_date_first&size=50'

# print(url)

res = requests.get(url)

bs = BeautifulSoup(res.text, 'html.parser')

ret = {"items": []}

papers = bs.find_all(name='p', class_='list-title')

for i in range(len(papers)):
    if i>9:
        break
    abs_url = papers[i].find('a').get('href')
    abs_res = requests.get(abs_url)
    abs_bs = BeautifulSoup(abs_res.text, 'html.parser')
    title = abs_bs.title.text
    abstract = abs_bs.find('blockquote').text
    item = {
        "title": title[13:],
        "subtitle": abstract[12:],
        'arg': abs_url
    }
    ret['items'].append(item)

sys.stdout.write(json.dumps(ret))
