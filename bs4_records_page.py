#wca records page

import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.worldcubeassociation.org/results/regions.php")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())

soup.find_all("div", {"class": "table-responsive"})

for s in soup.find_all("a"):
    print(s.get("href"))


for anchor in soup.find_all("a"):
    print(anchor.text)


data = soup.find_all("tr", {"class": "e"})
for d in data:
    print(d.text)


