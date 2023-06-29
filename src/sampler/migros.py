import requests
import json
import yaml # pip install pyyaml
from collections import namedtuple

from tabulate import tabulate, SEPARATING_LINE

import helpers

basket = helpers.load_config("config/baskets/blick.yaml")


Product = namedtuple("Product", "name description price quantity")

class MigrosStore:
	def __init__(self):
		self.session = requests.session()
		self.authenticate()
		
	def authenticate(self):
		r, headers = self.http_get("https://www.migros.ch/authentication/public/v1/api/guest?ignoreAuthModule=true&rememberme=true")
		self.session.headers.update({'leshopch': headers['leshopch']})            

	def get_product(self, id):
		data, _ = self.http_get("https://www.migros.ch/product-display/public/v2/product-detail?storeType=OFFLINE&warehouseId=2&region=national&ongoingOfferDate=2023-06-28T00:00:00&migrosIds=%s" % id)
		if not data:
			raise Exception("no product found with id %s" % id)
		prod = Product(name=data[0]['name'], description=data[0].get('description'), price=data[0]['offer']['price'].get('value'), quantity=data[0]['offer'].get('quantity'))
		return prod

	def search(self, query):
		data = {"regionId":"national","language":"de","productIds":[],"query":query,"sortFields":[],"sortOrder":"asc","algorithm":"DEFAULT","filters":{}}
		r = self.session.post("https://www.migros.ch/onesearch-oc-seaapi/public/v5/search", json=data)
		r.raise_for_status()
		data = r.json()
		uids = ",".join(str(uid) for uid in data['productIds'])
		data, _ = self.http_get("https://www.migros.ch/product-display/public/v3/product-cards?uids=%s&storeType=OFFLINE&region=national&ongoingOfferDate=2023-06-29T00:00:00" % uids)
		migrosIds = [e['migrosId'] for e in data]
		return migrosIds
	def http_get(self, url):
		r = self.session.get(url)
		r.raise_for_status()
		data = r.json()
		#print(yaml.dump(data, allow_unicode=True))		
		return data, r.headers

# end class

store = MigrosStore()

total_price = 0.0
table = []
for name, entry in basket.items():
	prod = store.get_product(entry['migrosId'])
	factor = helpers.divide_quantity(entry['quantity'], prod.quantity)
	norm_price = prod.price * factor
	total_price += norm_price
	table.append([name, entry['quantity'], helpers.format_price(norm_price)])
table.append(SEPARATING_LINE)
table.append(["TOTAL (%d items)" % len(basket), "", helpers.format_price(total_price)])

print(tabulate(table, headers=["product", "quantity", "Migros"], colalign=("left", "left", "right")))
