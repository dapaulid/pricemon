from store import Store
from product import Product
import html
import re
import json

from bs4 import BeautifulSoup


class CoopStore(Store):
		
	def authenticate_impl(self):
		pass

	def get_product_impl(self, id):
		data = self.http_get(id, resp_json=False)
		data = html.unescape(data.decode())
		info = json.loads(find_between(data, '<!-- Product schema -->\n    <script type="application/ld+json">', '</script>'))

		soup = BeautifulSoup(data, 'html.parser')
		quantity_info_element = soup.find('div', {'class': 'productBasicInfo__quantity-info'})
		if not quantity_info_element:
			raise ValueError("Product quantity information not found")
		quantity_element = quantity_info_element.find('span', {'itemprop': 'value'})
		if not quantity_element:
			raise ValueError("Product quantity not found")
		quantity = quantity_element.text.strip()
		unit = quantity_element.next_sibling.strip()
		quantity = f"{quantity}{unit}"

		prod = Product(name=info['name'], description=None, price=info['offers']['price'], quantity=quantity)
		return prod

	def search_impl(self, query):
		return None
# end class

def find_between(s, start, end):
	istart = s.index(start) + len(start)
	iend = s.index(end, istart)
	return s[istart:iend]
