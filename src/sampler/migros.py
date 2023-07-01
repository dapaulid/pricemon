from store import Store
from product import Product

class MigrosStore(Store):
		
	def authenticate_impl(self):
		r, headers = self.http_get("https://www.migros.ch/authentication/public/v1/api/guest?ignoreAuthModule=true&rememberme=true", resp_headers=True)
		self.session.headers.update({'leshopch': headers['leshopch']})            

	def get_product_impl(self, id):
		data = self.http_get("https://www.migros.ch/product-display/public/v2/product-detail?storeType=OFFLINE&warehouseId=2&region=national&ongoingOfferDate=2023-06-28T00:00:00&migrosIds=%s" % id)
		if not data:
			raise Exception("no product found with id %s" % id)
		prod = Product(name=data[0]['name'], description=data[0].get('description'), price=data[0]['offer']['price'].get('value'), quantity=data[0]['offer'].get('quantity'))
		return prod

	def search_impl(self, query):
		data = {"regionId":"national","language":"de","productIds":[],"query":query,"sortFields":[],"sortOrder":"asc","algorithm":"DEFAULT","filters":{}}
		data = self.http_post("https://www.migros.ch/onesearch-oc-seaapi/public/v5/search", data)
		uids = ",".join(str(uid) for uid in data['productIds'])
		data, _ = self.http_get("https://www.migros.ch/product-display/public/v3/product-cards?uids=%s&storeType=OFFLINE&region=national&ongoingOfferDate=2023-06-29T00:00:00" % uids)
		migrosIds = [e['migrosId'] for e in data]
		return migrosIds
# end class
