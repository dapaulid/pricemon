from store import Store
from product import Product
import html
import re
import json

from bs4 import BeautifulSoup, Comment


class LidlStore(Store):
		
	name = "Lidl"

	def authenticate_impl(self):
		pass

	def get_product_impl(self, url):
		data = self.http_get(url, resp_json=False)

		soup = BeautifulSoup(data, 'html.parser')

		# get name
		name_element = soup.find('li', {'class': 'item product'})
		if not name_element:
			raise ValueError("Name element not found")
		product_name = name_element.text

		# get price
		price_element = soup.find('strong', {'class': 'pricefield__price'})
		if not price_element:
			raise ValueError("Price element not found")
		price = float(price_element.attrs['content'])

		# get quantity
		quantity_element = soup.find('span', {'class': 'pricefield__footer'})
		if not quantity_element:
			raise ValueError("Quantity element not found")
		qfields = quantity_element.text.split(' ') # pro 200g | 100g = 0.83 CHF
		if len(qfields) > 1:
			quantity = qfields[1]
		else:
			# some products do not have quantities missing, we hardcode them here
			missing_quantities = {
				'https://sortiment.lidl.ch/de/vollkorntoast-0021322.html': '500g',
				'https://sortiment.lidl.ch/de/himbeer-konfituere-extra-0183951.html': '450g',
				'https://sortiment.lidl.ch/de/vollmilch-3-5-pasteurisiert-5110077.html': '1l',
				'https://sortiment.lidl.ch/de/tomatenketchup-0155908.html': '500g',
				'https://sortiment.lidl.ch/de/weizentoast-0138779.html': '500g',
				'https://sortiment.lidl.ch/de/lasagne-0161009.html': '800g',
			}
			quantity = missing_quantities[url]
		# end if

		# special senf handling
		if url == 'https://sortiment.lidl.ch/de/senf-0011642.html':
			quantity = quantity.replace('ml', 'g')

		prod = Product(name=product_name, description=None, price=price, quantity=quantity)
		return prod

	def search_impl(self, query):
		return None
# end class

def find_between(s, start, end):
	istart = s.index(start) + len(start)
	iend = s.index(end, istart)
	return s[istart:iend]
