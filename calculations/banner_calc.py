from data import DATA
from calculations.default_calc_func import perimeter_calc, square_calc


DATA_BANNER = DATA['Баннер']['data']


def material_calc(quality, material):
	if 'Без печати' == quality:
		price_material = DATA_BANNER['Материал'][material][quality]
		sale_price_material = price_material
	else:
		price_material = DATA_BANNER['Материал'][material][quality]['Себестоимость']
		sale_price_material = DATA_BANNER['Материал'][material][quality]['Продажа']
	material_name = DATA_BANNER['Материал'][material]['Материал']
	return price_material, sale_price_material, material_name


def processing_calc(welding_step, processing, lenght, width, sides_id=None):
	if welding_step:
		price_proccessing = DATA_BANNER['Обработка'][processing][welding_step]['Себестоимость']
		sale_price_proccessing = DATA_BANNER['Обработка'][processing][welding_step]['Продажа']
		proccess_material = DATA_BANNER['Обработка'][processing].get('Материал') or None
	else:
		price_proccessing = DATA_BANNER['Обработка'][processing]['Себестоимость']
		sale_price_proccessing = DATA_BANNER['Обработка'][processing]['Продажа']
		proccess_material = DATA_BANNER['Обработка'][processing].get('Материал') or None
	len_processing_sides = 0
	if sides_id:
		if 'all_sides' in sides_id:
			len_processing_sides = perimeter_calc(lenght, width)
		elif 'corners' in sides_id:
			len_processing_sides = perimeter_calc(lenght, width)
		else:
			for side in sides_id:
				if side in ['left_side', 'right_side']:
					len_processing_sides += float(lenght)
				elif side in ['top_side', 'bottom_side']:
					len_processing_sides += float(width)
			len_processing_sides = len_processing_sides / 1000
		price_proccessing = round(price_proccessing * len_processing_sides, 2)
		sale_price_proccessing = round(sale_price_proccessing * len_processing_sides, 2)
	return price_proccessing, sale_price_proccessing, proccess_material, len_processing_sides


def main_calc(form):
	price_material, sale_price_material, material_name = material_calc(
		quality=form.print_quality.data,
		material=form.material.data
	)
	
	lenght = float(form.length.data)
	width = float(form.width.data)
	raw_length, raw_width = lenght, width
	if lenght < 500:
		lenght = 500
	if width < 500:
		width = 500
	perimeter = perimeter_calc(lenght, width)
	square = square_calc(lenght, width)
	
	material_consumption = round(square * form.quantity.data, 2)
	
	processing_sides_id, processing_sides = [], []
	if DATA_BANNER['Обработка'][form.processing.data].get('Сторона'):
		for key_side, val_side in form.data.items():
			if any(side in key_side for side in ['side', 'corners']) and val_side:
				processing_sides_id.append(key_side)
				processing_sides.append(form[key_side].label.text)
		processing_sides = ', '.join(processing_sides)
	
	price_proccessing, sale_price_proccessing, proccess_material, len_processing_sides = processing_calc(
		welding_step=form.welding_step.data,
		processing=form.processing.data,
		lenght=lenght,
		width=width,
		sides_id=processing_sides_id or None
	)
	
	main_price = round(((price_material * square) + price_proccessing) * form.quantity.data, 2)
	main_sale_price = round(((sale_price_material * square) + sale_price_proccessing) * form.quantity.data, 2)
	if processing_sides:
		if 'Установка люверса с проваркой' == form.processing.data:
			process_consumption = round(
				(len_processing_sides / float(form.welding_step.data.split(' ')[0])) * form.quantity.data,
				2
			)
		else:
			process_consumption = round(len_processing_sides * form.quantity.data, 2)
	else:
		if form.processing.data == 'Натяжка на подрамник 27мм*12мм':
			process_consumption = round(perimeter * form.quantity.data, 2)
		else:
			process_consumption = None
	
	return {
		'material': {
			'name': material_name,
			'print_quality': form.print_quality.data,
			'type': form.material.data,
			'price': price_material,
			'sale_price': sale_price_material,
			'consumption': material_consumption
		},
		'processing': {
			'type': form.processing.data,
			'price': price_proccessing,
			'sale_price': sale_price_proccessing,
			'sides': processing_sides,
			'welding_step': form.welding_step.data,
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