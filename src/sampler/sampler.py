from tabulate import tabulate, SEPARATING_LINE

import helpers
from product import Product
from migros import MigrosStore
from coop import CoopStore

basket = helpers.load_config("config/baskets/blick.yaml")

migros_store = MigrosStore()
coop_store = CoopStore()

total_price = 0.0
table = []
for name, entry in basket.items():
	prod = migros_store.get_product(entry['migrosId'])
	coop_store.get_product(entry['coopId'])
	price = prod.get_price(entry['quantity'])
	table.append([name, entry['quantity'], helpers.format_price(price)])
	total_price += price	
table.append(SEPARATING_LINE)
table.append(["TOTAL (%d items)" % len(basket), "", helpers.format_price(total_price)])

print(tabulate(table, headers=["product", "quantity", "Migros"], colalign=("left", "left", "right")))
