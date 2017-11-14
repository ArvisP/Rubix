from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

r = urlopen("https://www.worldcubeassociation.org/competitions")

soup = BeautifulSoup(r, "html.parser")

date_box = soup.find_all('span', attrs={'class': 'date'})
title_box = soup.find_all('p', attrs={'class': 'competition-link'})
location_box = soup.find_all('p', attrs={'class': 'location'})
venue_box = soup.find_all('div', attrs={'class': 'venue-link'})


# date = date_box.text.strip()
# title = title_box.text.strip()
# location = location_box.text.strip()
# venue = venue_box.text.strip()
date_set = []
title_set = []
location_set = []
venue_set = []
for date in date_box:
  date_set.append(date.text.strip())
  
for title in title_box:
  title_set.append(title.text.strip())

for location in location_box:
  location_set.append(location.text.strip())

for venue in venue_box:
  venue_set.append(venue.text.strip())
  
# sys.stdout = open("out2.txt", "w")
print(date_set[0:3])
print(title_set[0:3])
print(location_set[0:3])
print(venue_set[0:3])
  

# print(date_box, title_box, location_box, venue_box)
# print(date, title, location, venue)