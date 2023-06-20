from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NumberRange
from forms.canvas_form import FlexibleDecimalField

from data import DATA


class BannerForm(FlaskForm):
	material_choices = DATA['Баннер']['data']['Материал'].keys()
	processing_choices = DATA['Баннер']['data']['Обработка'].keys()
	print_quality_choices = DATA['Баннер']['data']['Качество печати']
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
	print_quality = SelectField(
		"Качество печати: ",
		choices=print_quality_choices,
		validators=[DataRequired()]
	)
	left_side = BooleanField(label='Левая')
	right_side = BooleanField(label='Правая')
	top_side = BooleanField(label='Верх')
	bottom_side = BooleanField(label='Низ')
	all_sides = BooleanField(label='Все стороны')
	corners = BooleanField(label='По углам')
	welding_step = SelectField(
		"Шаг сварки: ",
		choices=['Недоступно'],
		validate_choice=False,
		validators=[]
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
			return False
		
		if not any(
				[
					self.left_side.data,
					self.right_side.data,
					self.top_side.data,
					self.bottom_side.data,
					self.all_sides.data,
					self.corners.data
				]
		) and DATA['Баннер']['data']['Обработка'][self.processing.data].get('Сторона'):
			self.left_side.errors.append('Необходимо выбрать "Стороны обработки"')
			if self.welding_step.data and self.welding_step.data != 'Недоступно':
				self.welding_step.errors.append(self.welding_step.data)
			return False
		
		return True
