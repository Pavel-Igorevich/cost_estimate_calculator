from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, DecimalField
from wtforms.validators import DataRequired, NumberRange

from data import DATA


class FlexibleDecimalField(DecimalField):
	
	def process_formdata(self, valuelist):
		if valuelist:
			valuelist[0] = valuelist[0].replace(",", ".")
		return super(FlexibleDecimalField, self).process_formdata(valuelist)


class CanvasForm(FlaskForm):
	material_choices = DATA['Холст']['data']['Материал'].keys()
	processing_choices = DATA['Холст']['data']['Обработка'].keys()
	material = SelectField(
		"Материал: ",
		choices=material_choices,
		validators=[DataRequired()]
	)
	processing = SelectField(
		"Обработка: ",
		choices=processing_choices,
		validators=[DataRequired()]
	)
	# todo возможны float значения, но 100 или 1000 не работают
	length = FlexibleDecimalField(
		'Длина холста: ',
		validators=[DataRequired(), NumberRange(min=1)],
	)
	width = FlexibleDecimalField(
		'Ширина холста: ',
		validators=[DataRequired(), NumberRange(min=1)],
	)
	quantity = IntegerField(
		'Количество:',
		validators=[DataRequired(), NumberRange(min=1)],
	)
	submit = SubmitField('Рассчитать')
