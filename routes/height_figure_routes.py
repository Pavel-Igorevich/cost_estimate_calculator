from flask import render_template
from data import DATA
from forms.height_figure_form import HeightFigureForm
from calculations.plastic_calc import main_calc

PRODUCTS = sorted([[name, val['page']] for name, val in DATA.items()], key=lambda elem: elem[0])


def height_figure():
	form = HeightFigureForm()
	return_data = None
	if form.validate_on_submit():
		return_data = main_calc(form)
	return render_template('height_figure.html', form=form, products=PRODUCTS, data=return_data)
