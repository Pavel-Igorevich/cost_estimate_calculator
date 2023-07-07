from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired, NumberRange
from forms.canvas_form import FlexibleDecimalField

from data import DATA


class PlasticForm(FlaskForm):
	data = DATA['Плёнка']['data']
	material = SelectField(
		"Материал: ",
		choices=data['Материал'].keys(),
		validators=[DataRequired()]
	)
	color_orajet = StringField(
		"Цвет (ручной ввод): ",
		validators=[DataRequired()]
	)
	description = StringField(
		"Описание (ручной ввод): ",
		validators=[DataRequired()]
	)
	lamination = SelectField(
		"Ламинация: ",
		choices=data['Ламинация'].keys(),
		validators=[DataRequired()]
	)
	cutting = SelectField(
		"Резка: ",
		choices=data['Резка'].keys(),
		validators=[DataRequired()]
	)
	type_selection = SelectField(
		"Вид выборки: ",
		choices=data['Резка']['Плоттер']['Вид выборки'].keys(),
		validators=[DataRequired()]
	)
	complexity_selection = SelectField(
		"Сложность выборки: ",
		choices=data['Резка']['Плоттер']['Сложность выборки'].keys(),
		validators=[DataRequired()]
	)
	mounting_plastic = SelectField(
		"Монтажная пленка: ",
		choices=data['Резка']['Плоттер']['Монтажная пленка'].keys(),
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
	quantity = IntegerField(
		'Количество:',
		validators=[DataRequired(), NumberRange(min=1)],
	)
	submit = SubmitField('Рассчитать')
	
	def validate(self, **kwargs):
		if not super().validate():
			if not self.color_orajet.data and self.material.data != 'Orajet цветная':
				return True
			elif not self.description.data and self.material.data != 'Под заказ':
				return True
			elif not self.print_quality.data and self.material.data in ['Orajet цветная', 'Под заказ']:
				return True
			return False
		return True
