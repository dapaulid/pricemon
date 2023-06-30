import requests

import json
import yaml # pip install pyyaml

class Store:
	def __init__(self):
		self.session = requests.session()
		self.authenticate()
		
	def authenticate(self):
		# implemented by subclasses
		pass         

	def get_product(self, id):
		# implemented by subclasses
		return None

	def search(self, query):
		# implemented by subclasses
		return None
	
	def http_get(self, url, resp_headers=False):
		r = self.session.get(url)
		r.raise_for_status()
		data = r.json()
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