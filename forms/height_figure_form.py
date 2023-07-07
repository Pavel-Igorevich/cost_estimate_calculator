from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from forms.canvas_form import FlexibleDecimalField

from data import DATA


class HeightFigureForm(FlaskForm):
	data = DATA['Ростовая фигура']['data']
	material = SelectField(
		"Материал: ",
		choices=data['Материал'].keys(),
		validators=[DataRequired()]
	)
	skeleton = SelectField(
		"Каркас: ",
		choices=data['Каркас'].keys(),
		validators=[DataRequired()]
	)
	type_metal_sceleton = SelectField(
		"Тип металлического каркаса: ",
		choices=data['Каркас']['Металл'],
		validators=[DataRequired()]
	)
	type_pvh_sceleton = SelectField(
		"Тип ПВХ каркаса: ",
		choices=data['Каркас']['Плавник ПВХ'],
		validators=[DataRequired()]
	)
	place_operation = SelectField(
		"Место эксплуатации: ",
		choices=data["Место эксплуатации"].keys(),
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
	quantity = IntegerField(
		'Количество:',
		validators=[DataRequired(), NumberRange(min=1)],
	)
	submit = SubmitField('Рассчитать')

	def validate(self, **kwargs):
		if not super().validate():
			if not self.type_metal_sceleton.data and self.skeleton.data != 'Металл':
				return True
			elif not self.type_pvh_sceleton.data and self.material.data != 'Плавник ПВХ':
				return True
			return False
		return True
