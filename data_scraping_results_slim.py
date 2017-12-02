import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.worldcubeassociation.org/results/regions.php?regionId=&eventId=&years=&slim=Slim")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())

tables = soup.findChildren("table")

my_table = tables[0]

rows = my_table.findChildren(['th', 'tr'])

for row in rows:
    cells = row.findChildren('td')
    for cell in cells:
        value = cell.string
        print("The value in this cell is %s" % value)


#soup.find("table", {"class": "table-responsive"})
for th in soup.find("th"):
    for tr in soup.find_all("tr"):
        print(tr.text)


for tr in soup.find("tr"):
    for td in soup.find_all("td"):
        print(td.text)


td_set = []
for tr in soup.find("tr"):
    for td in soup.find_all("td"):
        td_set.append(td.text)
#for x in td_set:
#    print(x,sep="\n")

print(td_set[0:7])