from flask import render_template
from forms.press_wall_form import PressWallForm
from data import DATA
from calculations.press_wall_calc import main_calc

PRODUCTS = sorted([[name, val['page']] for name, val in DATA.items()], key=lambda elem: elem[0])


def press_wall():
	form = PressWallForm()
	return_data = None
	if form.validate_on_submit():
		return_data = main_calc(form)
	return render_template('press_wall.html', products=PRODUCTS, form=form, data=return_data)
