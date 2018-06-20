# these should be the only imports you need

import requests
from bs4 import BeautifulSoup

# write your code here
# usage should be python3 part3.py

site = 'https://www.michigandaily.com/'
req_site = requests.get(site)
site_text = req_site.text[922:]
soup = BeautifulSoup(site_text, 'html.parser')

b = soup.aside.find_all('li')

print("Michigan Daily -- MOST READ")
for x in range(len(b)):
	print(b[x].string)
	nexturl = page + (b[x].a.get('href'))
	respurl = requests.get(nexturl).text
	iteratingsoup = BeautifulSoup(respurl, 'html.parser')
	print(" Author:",iteratingsoup.find('div', attrs = {'class':'link'}).contents[0].string)