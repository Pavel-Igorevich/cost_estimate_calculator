from flask import render_template, jsonify
from data import DATA
from forms.banner_form import BannerForm
from calculations.banner_calc import main_calc

PRODUCTS = sorted([[name, val['page']] for name, val in DATA.items()], key=lambda elem: elem[0])


def banner():
	form = BannerForm()
	return_data = None
	if form.validate_on_submit():
		return_data = main_calc(form)
	return render_template('banner.html', form=form, products=PRODUCTS, data=return_data)


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
