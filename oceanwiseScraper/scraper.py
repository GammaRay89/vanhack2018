import urllib2
import csv
import re
from bs4 import BeautifulSoup

url = "file:///Users/josephdeeth/Documents/VanHack2018/oceanwiseScraper/page.html"

page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read(), features="html.parser")

locations = soup.find_all('div', {'class' : 'location-item'})

with open('oceanwise.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['Name', 'Category', 'Phone Number', 'Address', 'Postal Code', 'Website'])
    for l in locations:
		name = l.find('h3', {'class' : 'partner__name'})
		name_string = re.sub('<[^<]+?>', '', str(name))
		name_string = re.sub(r'&(#?)(.+?);', '', name_string)
		category = l.find('div', {'class' : 'partner__category'})
		category_string = re.sub('<[^<]+?>', '', str(category))
		phone = l.find('p', {'class' : 'partner__phone'})
		phone_string = re.sub('<[^<]+?>', '', str(phone))
		address = l.find('p', {'class' : 'partner__address'})
		address_string = re.sub('<[^<]+?>', '', str(address))
		postal = l.find('p', {'class' : 'partner__postal'})
		postal_string = re.sub('<[^<]+?>', '', str(postal))
		website = l.find('a', href=True)
		website_string = re.search(r'href=[\'"]?([^\'" >]+)', str(website))
		if website_string:
			website_string = str(website_string.groups())
			website_string = website_string.replace('(', '')
			website_string = website_string.replace(')', '')
			website_string = website_string.replace(',', '')
			website_string = website_string.replace('\'', '')
		filewriter.writerow([name_string, category_string, phone_string, address_string, postal_string, website_string])




