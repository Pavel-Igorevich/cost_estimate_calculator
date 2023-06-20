from flask import render_template, jsonify
from data import DATA
from forms.banner_form import BannerForm

PRODUCTS = sorted([[name, val['page']] for name, val in DATA.items()], key=lambda elem: elem[0])


def banner():
	form = BannerForm()
	if form.validate_on_submit():
		data_banner = DATA['Баннер']['data']
		print_quality = form.print_quality.data
		if 'Без печати' == print_quality:
			price_material = data_banner['Материал'][form.material.data][print_quality]
			sale_price_material = price_material
		else:
			price_material = data_banner['Материал'][form.material.data][print_quality]['Себестоимость']
			sale_price_material = data_banner['Материал'][form.material.data][print_quality]['Продажа']
		material_name = data_banner['Материал'][form.material.data]['Материал']
		length = float(form.length.data)
		width = float(form.width.data)
		raw_length, raw_width = length, width
		if length < 500:
			length = 500
		if width < 500:
			width = 500
		square = round((length / 1000) * (width / 1000), 2)
		perimeter = round((length / 1000 + width / 1000) * 2, 2)
		
		material_consumption = round(square * form.quantity.data, 2)
		
		welding_step = form.welding_step.data
		if form.welding_step.data:
			price_proccessing = data_banner['Обработка'][form.processing.data][welding_step]['Себестоимость']
			sale_price_proccessing = data_banner['Обработка'][form.processing.data][welding_step]['Продажа']
			proccess_material = data_banner['Обработка'][form.processing.data].get('Материал') or None
		else:
			price_proccessing = data_banner['Обработка'][form.processing.data]['Себестоимость']
			sale_price_proccessing = data_banner['Обработка'][form.processing.data]['Продажа']
			proccess_material = data_banner['Обработка'][form.processing.data].get('Материал') or None
		
		processing_sides = []
		len_processing_sides = 0
		if data_banner['Обработка'][form.processing.data].get('Сторона'):
			processing_sides_id = []
			for key_side, val_side in form.data.items():
				if any(side in key_side for side in ['side', 'corners']) and val_side:
					processing_sides_id.append(key_side)
					processing_sides.append(form[key_side].label.text)
			if 'all_sides' in processing_sides_id:
				len_processing_sides = perimeter
			elif 'corners' in processing_sides_id:
				len_processing_sides = perimeter
			else:
				for side in processing_sides_id:
					if side in ['left_side', 'right_side']:
						len_processing_sides += float(length)
					elif side in ['top_side', 'bottom_side']:
						len_processing_sides += float(width)
				len_processing_sides = len_processing_sides / 1000
			processing_sides = ', '.join(processing_sides)
			price_proccessing = round(price_proccessing * len_processing_sides, 2)
			sale_price_proccessing = round(sale_price_proccessing * len_processing_sides, 2)
		
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
		
		return_data = {
			'material': {
				'name': material_name,
				'print_quality': print_quality,
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
				'welding_step': welding_step,
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
		return render_template('banner.html', form=BannerForm(), products=PRODUCTS, data=return_data)
	else:
		return render_template('banner.html', form=form, products=PRODUCTS)


def banner_material_state(state):
	form = BannerForm()
	if state == 'Сетка':
		return jsonify({'choices': ['720 dpi', 'Без печати']})
	return jsonify({'choices': form.print_quality.choices})


def banner_process_state(state):
	data = DATA['Баннер']['data']['Обработка'][state]
	choices = [
		['left_side_id', True],
		['right_side_id', True],
		['top_side_id', True],
		['bottom_side_id', True],
		['all_sides_id', True],
		['corners_id', True]
	]
	hide_choices = True
	if data.get('Сторона'):
		hide_choices = False
		for name_side in data.get('Сторона'):
			if name_side == 'Левая':
				choices[0] = ['left_side_id', False]
			elif name_side == 'Правая':
				choices[1] = ['right_side_id', False]
			elif name_side == 'Верх':
				choices[2] = ['top_side_id', False]
			elif name_side == 'Низ':
				choices[3] = ['bottom_side_id', False]
			elif name_side == 'Все стороны':
				choices[4] = ['all_sides_id', False]
			elif name_side == 'По углам':
				choices[5] = ['corners_id', False]
	steps = [step for step in data.keys() if 'мм' in step] or ['Недоступно']
	return jsonify({'choices': choices, 'hide_choices': hide_choices, 'steps': steps})
