from data import DATA
from calculations.default_calc_func import perimeter_calc, square_calc


DATA_CANVAS = DATA['Холст']['data']


def main_calc(form):
	price_material = DATA_CANVAS['Материал'][form.material.data]['Себестоимость']
	sale_price_material = DATA_CANVAS['Материал'][form.material.data]['Продажа']
	price_proccessing = DATA_CANVAS['Обработка'][form.processing.data]['Себестоимость']
	sale_price_proccessing = DATA_CANVAS['Обработка'][form.processing.data]['Продажа']
	lenght = float(form.length.data)
	width = float(form.width.data)
	raw_length, raw_width = lenght, width
	if lenght < 500:
		lenght = 500
	if width < 500:
		width = 500
	square = square_calc(lenght, width)
	perimeter = perimeter_calc(lenght, width)
	main_price = round(((price_material * square) + (price_proccessing * perimeter)) * form.quantity.data, 2)
	main_sale_price = round(
		((sale_price_material * square) + (sale_price_proccessing * perimeter)) * form.quantity.data,
		2
	)
	material_name = DATA_CANVAS['Материал'][form.material.data]['Материал']
	material_consumption = round(square * form.quantity.data, 2)
	proccess_material = DATA_CANVAS['Обработка'][form.processing.data].get('Материал') or None
	process_consumption = None
	if proccess_material:
		process_consumption = round(perimeter * form.quantity.data, 2)
	
	return {
		'material': {
			'name': material_name,
			'type': form.material.data,
			'price': price_material,
			'sale_price': sale_price_material,
			'consumption': material_consumption
		},
		'processing': {
			'type': form.processing.data,
			'price': price_proccessing,
			'sale_price': sale_price_proccessing,
			'material': proccess_material,
			'consumption': process_consumption
		},
		'size': square,
		'length': raw_length,
		'width': raw_width,
		'quantity': form.quantity.data,
		'main_price': main_price,
		'main_sale_price': main_sale_price
	}