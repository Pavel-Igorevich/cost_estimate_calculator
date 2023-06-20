from flask import render_template
from data import DATA

PRODUCTS = sorted([[name, val['page']] for name, val in DATA.items()], key=lambda elem: elem[0])


def base():
	return render_template('base.html', products=PRODUCTS)
