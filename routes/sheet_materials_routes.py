from flask import render_template, jsonify
from data import DATA
from forms.sheet_materials_form import SheetMaterialsForm
from pprint import pprint

PRODUCTS = sorted([[name, val['page']] for name, val in DATA.items()], key=lambda elem: elem[0])


def sheet_materials():
	form = SheetMaterialsForm()
	if form.validate_on_submit():
		# todo сделать Вывод и подсчет!!!!!!!!!
		return render_template('sheet_materials.html', products=PRODUCTS, form=form, data=True)
	return render_template('sheet_materials.html', products=PRODUCTS, form=form)


def type_material_state(state):
	data = DATA['Листовые материалы']['data']['Материал'][state]
	hide_type, hide_tickness, hide_edge = True, True, True
	types_material = []
	if 'Толщина' not in data:
		types_material = [type_material for type_material in data.keys()]
		if 'Толщина' in data[types_material[0]]:
			hide_tickness = False
			tickness = [type_material for type_material in data[types_material[0]]['Толщина'].keys()]
		else:
			tickness = []
		hide_type = False
	else:
		if 'Кромка' in data:
			hide_edge = False
		hide_tickness = False
		tickness = [type_material for type_material in data['Толщина'].keys()]
	return jsonify({
		'type_material': types_material,
		'hide_type': hide_type,
		'tickness': tickness,
		'hide_tickness': hide_tickness,
		'hide_edge': hide_edge,
	})


def tickness_material_state(state, type_state):
	data = DATA['Листовые материалы']['data']['Материал'][state][type_state]
	hide_tickness = True
	tickness = []
	if 'Толщина' in data:
		hide_tickness = False
		tickness = [type_material for type_material in data['Толщина'].keys()]
	return jsonify({
		'tickness': tickness,
		'hide_tickness': hide_tickness
	})
