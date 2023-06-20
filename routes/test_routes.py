from flask import render_template
from data import DATA
from forms.test_form import TestForm

PRODUCTS = sorted([[name, val['page']] for name, val in DATA.items()], key=lambda elem: elem[0])


def test():
	form = TestForm()
	return render_template('test.html', products=PRODUCTS, form=form)
