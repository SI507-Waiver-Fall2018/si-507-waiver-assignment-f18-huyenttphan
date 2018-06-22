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
	nexturl = site + (b[x].a.get('href'))
	respurl = requests.get(nexturl).text
	more_soup = BeautifulSoup(respurl, 'html.parser')
	try:
		author = more_soup.find('div', attrs = {'class':'link'}).contents[0].string
	except Exception:
		author = 'Daily Staff Writer'
		
	print("  by",author)