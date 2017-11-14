#Contact page

import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.worldcubeassociation.org/contact")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())

soup.find_all(href=True)

emails = soup.select('a[href^=mailto:]')
for e in emails:
    print(e.text)
