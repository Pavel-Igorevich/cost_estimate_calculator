from flask import render_template
from data import DATA
from forms.canvas_form import CanvasForm
from calculations.canvas_calc import main_calc

PRODUCTS = sorted([[name, val['page']] for name, val in DATA.items()], key=lambda elem: elem[0])


def canvas():
	form = CanvasForm()
	return_data = None
	if form.validate_on_submit():
		return_data = main_calc(form)
	return render_template('canvas.html', form=form, products=PRODUCTS, data=return_data)
