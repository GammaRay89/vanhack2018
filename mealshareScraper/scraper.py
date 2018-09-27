import urllib2
import csv
import re
from bs4 import BeautifulSoup

url = "file:///Users/josephdeeth/Documents/VanHack2018/mealshareScraper/page.html"

page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read(), features="html.parser")

locations = soup.find_all('div', {'class' : 'restaurant'})

with open('mealshare.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['Name', 'Lat', 'Long', 'Phone Number', 'Address'])
    for l in locations:
		name = l.find('span')
		name_string = re.sub('<[^<]+?>', '', str(name))
		name_string = re.sub(r'&(#?)(.+?);', '', name_string)
		lat = str(l['data-lat'])
		lng = str(l['data-lng'])
		phone_address = l.find('p', {'class' : 'address'})
		phone_string = 'None'
		if phone_address:
			phone = phone_address.find('a')
			phone_string = re.sub('<[^<]+?>', '', str(phone))
		address_string = re.search('<p class="address">(.*)<br/>', str(phone_address))
		if address_string:
			address_string = str(address_string.groups())
			address_string = address_string.replace('(', '')
			address_string = address_string.replace(')', '')
			address_string = address_string.replace(',', '')
			address_string = address_string.replace('\'', '')
		filewriter.writerow([name_string, lat, lng, phone_string, address_string])
