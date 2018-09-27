import urllib2
import csv
import re
import requests
from bs4 import BeautifulSoup

url = "http://seafood.ocean.org/seafood/browse/"

page = requests.get(url)
c = page.content
soup = BeautifulSoup(c, features="html.parser")

urls = soup.find_all('div', {'class' : 'flex-grid__item'})

urls2 = []
for url in urls:
	url = str(url.find('a')['href'])
	urls2.append(url)

with open('fish.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['Name', 'Variety', 'Image Path', 'Recommended?', 'Method', 'Location', 'Rating'])
    for string in urls2:
		p = requests.get(string)
		s = BeautifulSoup(p.content, features="html.parser")

		name = "None"
		name = s.find('h2', {'class' : 'seafood-intro__title'})
		if name:
			name = re.sub('<[^<]+?>', '', str(name))
			name = re.sub(r'&(#?)(.+?);', '', name)
			name = name.strip()

		img = s.find('div', {'class' : 'seafood-intro__image'})
		img = img.find('img')
		img_url = str(img['src'])
		# download image from url
		img_name = re.sub('/', '', name) + '.png'
		img_name = img_name.replace(' ', '')
		img_name = img_name.lower()
		img_name = './images/' + img_name
		#f = open(img_name, 'wb')
		#f.write(requests.get(img_url).content)
		#f.close()
		img_path = img_name


		variety = "None"
		variety = s.find('div', {'class' : 'item-list__section item-list__section--type'})
		if variety:
			variety = variety.find('p', {'class' : 'item-list__subtitle'})
			variety_string = re.sub('<[^<]+?>', '', str(variety))
			variety_string = re.sub(r'&(#?)(.+?);', '', variety_string)

		method = "None"
		method = s.find('div', {'class' : 'item-list__section item-list__section--method'})
		if method:
			method = method.find('p', {'class' : 'item-list__subtitle'})
			if method.find('p', {'class' : 'item-list__content'}):
				method = method + method.find('p', {'class' : 'item-list__content'})
			method = re.sub('<[^<]+?>', '', str(method))
			method = method.strip()

		location = "None"
		location = s.find('div', {'class' : 'item-list__section item-list__section--location'})
		if location:
			location = location.find('p', {'class' : 'item-list__subtitle'})
			location = re.sub('<[^<]+?>', '', str(location))

		rating = "None"
		rating = s.find('p', {'class' : 'item-list__rating'})
		if rating:
			number = str(rating)
			number = number.replace('\n', '')
			number = re.search('</span>(.*)</p>', number).groups()
			number = str(number)
			number = number.replace('/', '')
			number = number.replace('(', '')
			number = number.replace(')', '')
			number = number.replace('\'', '')
			number = number.replace(',', '')
			rating = rating.find('span')
			rating = re.sub('<[^<]+?>', '', str(rating))
			# if rating is a range, take average
			if '-' in rating:
				a,b = rating.split("-")
				a = a.replace(' ', '')
				b = b.replace(' ', '')
				rating = (float(a) + float(b)) / 2
				rating = round(rating, 1)
			# if there's a denominator (there's only 5 or 10), make the rating out of 5 instead of 10
			if (number):
				number = number.strip()
				try:
					if (int(number) == 10):
						rating = float(rating)
						rating = rating / 2
						rating = round(rating, 1)
				except ValueError:
					print "Not an int"

		recommendation = "None"
		recommendation = s.find('img', {'class' : 'item-list__icon'})
		if recommendation:
			recommendation = str(recommendation['title'])

		filewriter.writerow([name, variety_string, img_path, recommendation, method, location, rating])




