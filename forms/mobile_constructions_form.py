from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from data import DATA


class MobileConstructionsForm(FlaskForm):
	data = DATA['Мобильные конструкции']['data']
	construction = SelectField(
		"Конструкция: ",
		choices=data['Конструкция'].keys(),
		validators=[DataRequired()]
	)
	roll_up_size = SelectField(
		"Размер: ",
		choices=data['Конструкция']['Ролл-апп'].keys(),
		validators=[DataRequired()]
	)
	roll_up_banner = SelectField(
		"Баннер: ",
		choices=data['Конструкция']['Ролл-апп']['850 мм х 2000 мм']['Баннер'].keys(),
		validators=[DataRequired()]
	)
	x_banner_size = SelectField(
		"Размер: ",
		choices=data['Конструкция']['Х-Баннер'].keys(),
		validators=[DataRequired()]
	)
	x_banner_banner = SelectField(
		"Баннер: ",
		choices=data['Конструкция']['Х-Баннер']['600 мм х 1600 мм']['Баннер'].keys(),
		validators=[DataRequired()]
	)
	joker_size = SelectField(
		"Размер: ",
		choices=data['Конструкция']['Стойка-указатель на джокере'].keys(),
		validators=[DataRequired()]
	)
	joker_lamination = SelectField(
		"Ламинация: ",
		choices=data['Конструкция']['Стойка-указатель на джокере']['Ламинация'],
		validators=[DataRequired()]
	)
	quantity = IntegerField(
		'Количество:',
		validators=[DataRequired(), NumberRange(min=1)],
	)
	submit = SubmitField('Рассчитать')
	
	def validate(self, **kwargs):
		if not super().validate():
			if (not self.roll_up_size.data or not self.roll_up_banner.data) and self.construction.data == 'Ролл-апп':
				return False
			elif (not self.x_banner_size.data or not self.x_banner_banner.data) \
				and self.construction.data == 'Х-Баннер':
				return False
			elif (not self.joker_size.data or not self.joker_lamination.data) \
				and self.construction.data == 'Стойка-указатель на джокере':
				return False
			else:
				return True
		return True
