from flask import render_template
from data import DATA
from forms.mobile_constructions_form import MobileConstructionsForm
from calculations.mobile_constructions_calc import main_calc

PRODUCTS = sorted([[name, val['page']] for name, val in DATA.items()], key=lambda elem: elem[0])


def mobile_constructions():
	form = MobileConstructionsForm()
	return_data = None
	if form.validate_on_submit():
		return_data = main_calc(form)
	return render_template(
		'mobile_constructions.html', form=form, products=PRODUCTS, data=return_data
	)