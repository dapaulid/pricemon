from tabulate import tabulate, SEPARATING_LINE

import helpers
from product import Product
from migros import MigrosStore
from coop import CoopStore

basket = helpers.load_config("config/baskets/blick.yaml")

store1 = MigrosStore()
store2 = CoopStore()

total_price1 = 0.0
total_price2 = 0.0
table = []
for name, entry in basket.items():
	prod1 = store1.get_product(entry['migrosId'])
	prod2 = store2.get_product(entry['coopId'])
	price1 = prod1.get_price(entry['quantity'])
	price2 = prod2.get_price(entry['quantity'])
	table.append([name, entry['quantity'], 
		helpers.format_price(price1), helpers.format_price(price2)])
	total_price1 += price1
	total_price2 += price2	
table.append(SEPARATING_LINE)
table.append(["TOTAL (%d items)" % len(basket), "", 
	helpers.format_price(total_price1), helpers.format_price(total_price2)])

print(tabulate(table, headers=["product", "quantity", "Migros", "Coop"], colalign=("left", "left", "right", "right")))
