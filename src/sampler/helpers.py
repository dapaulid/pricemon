import re
import os

def load_config(filename):
	ext = os.path.splitext(filename)[-1]
	if ext == '.yaml':
		import yaml
		with open(filename, 'r', encoding='utf-8') as f:
			return yaml.safe_load(f)
	else:
		raise ValueError("Unsupported file format: %s" % filename)
	# end if
# end function

# credits to chatGPT

def parse_quantity(quantity):
    pattern = r"(\d+(\.\d+)?)\s*([a-zA-Z]+)"
    match = re.match(pattern, quantity.replace(',', '.'))

    if match is None:
        raise ValueError("Invalid quantity: %s" % quantity)

    value = float(match.group(1))
    unit = match.group(3)

    return value, unit

def divide_quantity(quantity1, quantity2):
    units = {
        "kg": 1000,
        "g": 1,
        "l": 1000,
        "ml": 1
    }

    quantity1_value, quantity1_unit = parse_quantity(quantity1)
    quantity2_value, quantity2_unit = parse_quantity(quantity2)

    if quantity1_unit not in units:
        raise ValueError(f"Invalid unit in quantity1: {quantity1_unit}")
    if quantity2_unit not in units:
        raise ValueError(f"Invalid unit in quantity2: {quantity2_unit}")

    if quantity1_unit[-1] != quantity2_unit[-1]:
        raise ValueError(f"Base units do not match: {quantity1_unit} and {quantity2_unit}")

    converted_quantity1 = quantity1_value * units[quantity1_unit]
    converted_quantity2 = quantity2_value * units[quantity2_unit]

    return converted_quantity1 / converted_quantity2

def format_price(price):
    return "CHF %0.2f" % price