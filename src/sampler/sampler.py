from tabulate import tabulate, SEPARATING_LINE

import helpers
from product import Product
from migros import MigrosStore
from coop import CoopStore

basket = helpers.load_config("config/baskets/blick.yaml")

stores = [
	MigrosStore(),
	CoopStore(),
]

table = []
total_prices = [0.0] * len(stores)
for name, entry in basket.items():
	row = [name, entry['quantity']]
	for i, store in enumerate(stores):
		prod = store.get_product(entry[store.name])
		price = prod.get_price(entry['quantity'])
		total_prices[i] += price		
		row.append(helpers.format_price(price))
	# end for	
	table.append(row)
# end for

table.append(SEPARATING_LINE)
table.append(["TOTAL (%d items)" % len(basket), ""] + [helpers.format_price(price) for price in total_prices])

print(tabulate(table, 
	headers=["product", "quantity"] + [store.name for store in stores], 
	colalign=("left", "left") + ("right",) * len(stores))
)
