import helpers

class Product:
    
	def __init__(self, name, description, price, quantity):
		self.name = name
		self.description = description
		self.price = price
		self.quantity = quantity
	# end function

	def get_price(self, quantity):
		factor = helpers.divide_quantity(quantity, self.quantity)
		return self.price * factor
	# end function

# end class