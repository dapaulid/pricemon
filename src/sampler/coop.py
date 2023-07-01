from store import Store
from product import Product
import html
import re
import json

class CoopStore(Store):
		
	def authenticate(self):
		pass

	def get_product(self, id):
		data = self.http_get("https://www.coop.ch/" + id, resp_json=False)
		data = html.unescape(data.decode())
		info = json.loads(find_between(data, '<!-- Product schema -->\n    <script type="application/ld+json">', '</script>'))
		print(info['name'])
		prod = Product(name=info['name'], description=None, price=info['offers']['price'], quantity=None)
		return prod

	def search(self, query):
		return None
# end class

def find_between(s, start, end):
	istart = s.index(start) + len(start)
	iend = s.index(end, istart)
	return s[istart:iend]
