from flask import render_template
from data import DATA
from forms.canvas_form import CanvasForm

PRODUCTS = sorted([[name, val['page']] for name, val in DATA.items()], key=lambda elem: elem[0])


def canvas():
	form = CanvasForm()
	return_data = None
	if form.validate_on_submit():
		data_canvsas = DATA['Холст']['data']
		price_material = data_canvsas['Материал'][form.material.data]['Себестоимость']
		sale_price_material = data_canvsas['Материал'][form.material.data]['Продажа']
		price_proccessing = data_canvsas['Обработка'][form.processing.data]['Себестоимость']
		sale_price_proccessing = data_canvsas['Обработка'][form.processing.data]['Продажа']
		length = float(form.length.data)
		width = float(form.width.data)
		raw_length, raw_width = length, width
		if length < 500:
			length = 500
		if width < 500:
			width = 500
		square = round((length / 1000 * width / 1000), 2)
		perimeter = round((length / 1000 + width / 1000) * 2, 2)
		main_price = round(((price_material * square) + (price_proccessing * perimeter)) * form.quantity.data, 2)
		main_sale_price = round(
			((sale_price_material * square) + (sale_price_proccessing * perimeter)) * form.quantity.data,
			2
		)
		material_name = data_canvsas['Материал'][form.material.data]['Материал']
		material_consumption = round(square * form.quantity.data, 2)
		proccess_material = data_canvsas['Обработка'][form.processing.data].get('Материал') or None
		process_consumption = None
		if proccess_material:
			process_consumption = round(perimeter * form.quantity.data, 2)
		
		return_data = {
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
	
	return render_template('canvas.html', form=form, products=PRODUCTS, data=return_data)
