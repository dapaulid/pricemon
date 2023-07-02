from store import Store
from product import Product
import html
import re
import json

from bs4 import BeautifulSoup, Comment


class CoopStore(Store):
		
	name = "Coop"

	def authenticate_impl(self):
		pass

	def get_product_impl(self, url):
		data = self.http_get(url, resp_json=False)

		soup = BeautifulSoup(data, 'html.parser')

		# get product info containing price
		product_schema = soup.find(text=lambda text: isinstance(text, Comment) and 'Product schema' in text)
		info = json.loads(html.unescape(product_schema.find_next_sibling().text))

		# get quantity
		quantity_info_element = soup.find('div', {'class': 'productBasicInfo__quantity-info'})
		if not quantity_info_element:
			raise ValueError("Product quantity information not found")
		quantity_element = quantity_info_element.find('span', {'itemprop': 'value'})
		if not quantity_element:
			raise ValueError("Product quantity not found")
		quantity = quantity_element.text.strip() + quantity_element.next_sibling.strip()

		prod = Product(name=info['name'], description=None, price=info['offers']['price'], quantity=quantity)
		return prod

	def search_impl(self, query):
		return None
# end class

def find_between(s, start, end):
	istart = s.index(start) + len(start)
	iend = s.index(end, istart)
	return s[istart:iend]
