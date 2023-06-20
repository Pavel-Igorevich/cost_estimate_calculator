from flask_wtf import FlaskForm
from wtforms import BooleanField


class TestForm(FlaskForm):
	left_side = BooleanField(label='Левая')
	right_side = BooleanField(label='Правая')
	top_side = BooleanField(label='Верх')
	bottom_side = BooleanField(label='Низ')
	all_sides = BooleanField(label='Все стороны')
	corners = BooleanField(label='По углам')
