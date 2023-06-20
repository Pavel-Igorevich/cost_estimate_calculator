from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from forms.canvas_form import FlexibleDecimalField

from data import DATA


class PressWallForm(FlaskForm):
	data = DATA['Пресс-Волл']['data']
	sceleton = SelectField(
		"Каркас: ",
		choices=data["Вид каркаса"],
		validators=[DataRequired()]
	)
	overhead_elements = SelectField(
		"Накладные элементы: ",
		choices=data["Накладные элементы"],
		validators=[DataRequired()]
	)
	place_operation = SelectField(
		"Место эксплуатации: ",
		choices=data["Место эксплуатации"].keys(),
		validators=[DataRequired()]
	)
	other_side = SelectField(
		"Вторая сторона: ",
		choices=data["Вторая сторона"],
		validators=[DataRequired()]
	)
	print_quality = SelectField(
		"Качество печати: ",
		choices=data["Качество печати"],
		validators=[DataRequired()]
	)
	length = FlexibleDecimalField(
		'Длина: ',
		validators=[DataRequired(), NumberRange(min=1)],
	)
	width = FlexibleDecimalField(
		'Ширина: ',
		validators=[DataRequired(), NumberRange(min=1)],
	)
	depth = SelectField(
		'Глубина: ',
		choices=['0 мм', '500 мм', 'Другая'],
		validators=[DataRequired()],
	)
	other_depth = FlexibleDecimalField(
		'Значение глубины: ',
		default=500,
		validators=[DataRequired(), NumberRange(min=500)],
	)
	quantity = IntegerField(
		'Количество:',
		validators=[DataRequired(), NumberRange(min=1)],
	)
	submit = SubmitField('Рассчитать')
