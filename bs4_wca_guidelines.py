#wca guidelines page

import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.worldcubeassociation.org/regulations/guidelines.html")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())

recommendation = soup.find_all("span", {"class": "RECOMMENDATION label linked"})
for r in recommendation:
    print(r)

clarification = soup.find_all("span", {"class": "CLARIFICATION label linked"})
for c in clarification:
    print(c)

addition = soup.find_all("span", {"class": "ADDITION label linked"})
for a in addition:
    print(a)

explanation = soup.find_all("span", {"class": "EXPLANATION label linked"})
for e in explanation:
    print(e)

reminder = soup.find_all("span", {"class": "REMINDER label linked"})
for re in reminder:
    print(re)

example = soup.find_all("span", {"class": "EXAMPLE label linked"})
for ex in example:
    print(ex)


#text of one id element
id_1 = soup.find(id="1c3+")
print(id_1.text)

#get all links
for s in soup.find_all("a", href=True):
    print(s)

