import requests
import timeit
import math

import json
import yaml # pip install pyyaml

from product import Product
class Timer:
    def __init__(self, label):
        self.label = label
    
    def __enter__(self):
        print(self.label)
        self.start_time = timeit.default_timer()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = timeit.default_timer()
        execution_time = (end_time - self.start_time) * 1000
        print(f"  took {execution_time:.2f} ms")

class Store:
	def __init__(self):
		self.session = requests.session()
		self.authenticate_impl()

	def authenticate_impl(self):
		# implemented by subclasses
		pass         

	def get_product(self, url):
		try:
			return self.get_product_impl(url)
		except Exception as e:
			print("error: failed to get product %s\n  %s" % (url, e))
			return Product(name=id, description=None, price=math.nan, quantity=math.nan)

	def get_product_impl(self, id):
		# implemented by subclasses
		return None

	def search(self, query):
		return self.search_impl(query)

	def search_impl(self, query):
		# implemented by subclasses
		return None
	
	def http_get(self, url, resp_json=True, resp_headers=False):
		
		print("fetching " + url)
		start_time = timeit.default_timer()
		r = self.session.get(url)
		elapsed = (timeit.default_timer() - start_time) * 1000 # ms
		size = len(r.content)
		print("  took %0.2f ms for %0.3f KB" % (elapsed, size / 1000))
		r.raise_for_status()
		data = r.json() if resp_json else r.content
		#print(yaml.dump(data, allow_unicode=True))		
		if resp_headers:
			return data, r.headers
		else:
			return data
	# end function

	def http_post(self, url, data):
		r = self.session.post(url, json=data)
		r.raise_for_status()
		data = r.json()
		return data
	# end function

# end class