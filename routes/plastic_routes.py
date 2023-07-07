from flask import render_template
from data import DATA
from forms.plastic_form import PlasticForm
from calculations.plastic_calc import main_calc

PRODUCTS = sorted([[name, val['page']] for name, val in DATA.items()], key=lambda elem: elem[0])


def plastic():
	form = PlasticForm()
	return_data = None
	if form.validate_on_submit():
		return_data = main_calc(form)
	return render_template('plastic.html', form=form, products=PRODUCTS, data=return_data)
