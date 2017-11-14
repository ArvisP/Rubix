#Results-Rankings page

import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.worldcubeassociation.org/results/events.php")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())

rank_set = []
names_set = []
result_set = []

names = soup.find_all("a", {"class": "p", "href": True})
result = soup.find_all("td", {"class":"R2"})
rank = soup.find_all("td", {"class":"r"})

for rk in rank:
    rank_set.append(rk.text)
for n in names:
    names_set.append(n.text)
for r in result:
    result_set.append(r.text)


print("Rank:")
for j in rank_set:
    print(m)
print("\nPerson:")
for k in names_set:
    print(i)
print("\nResult:")
for l in result_set:
    print(j)


competitions = soup.find_all("a", {"class": "c", "href": True})
for c in competitions:
    print(c.text)