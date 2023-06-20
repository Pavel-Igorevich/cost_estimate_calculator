from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from forms.canvas_form import FlexibleDecimalField

from data import DATA


class SheetMaterialsForm(FlaskForm):
	sheet_materials_data = DATA['Листовые материалы']['data']
	material_choices = sheet_materials_data['Материал'].keys()
	type_cutting_choices = sheet_materials_data['Вид резки'].keys()
	type_film_choices = sheet_materials_data['Накатка пленки'].keys()
	rect_type_film_choices = sheet_materials_data['Накатка пленки']['Прямоугольник'].keys()
	illumination_choices = sheet_materials_data['Контражурная подсветка']['Свет'].keys()
	holder_choices = sheet_materials_data['Держатель'].keys()
	place_choices = sheet_materials_data['Место эксплуатации'].keys()
	default_tickness = sheet_materials_data['Материал']['ПВХ']['Толщина'].keys()
	
	material = SelectField(
		"Материал: ",
		choices=material_choices,
		validators=[DataRequired()]
	)
	type_material = SelectField(
		"Вид материала: ",
		choices=[],
		validators=[]
	)
	material_thickness = SelectField(
		"Толщина материала: ",
		choices=default_tickness,
		validators=[]
	)
	material_edge = SelectField(
		'Кромка материала:',
		choices=["Не требуется", "Добавить"],
		validators=[]
	)
	
	type_cutting = SelectField(
		"Вид резки: ",
		choices=type_cutting_choices,
		validators=[DataRequired()]
	)
	type_film = SelectField(
		"Накатка пленки: ",
		choices=type_film_choices,
		validators=[DataRequired()]
	)
	rect_type_film = SelectField(
		"Вид накатки пленки: ",
		choices=rect_type_film_choices,
		validators=[]
	)
	illumination = SelectField(
		"Контражурная подсветка: ",
		default="Не требуется",
		choices=illumination_choices,
		validators=[DataRequired()]
	)
	additional_wire = IntegerField(
		'Дополнительный провод (метры):',
		default=5,
		validators=[DataRequired(), NumberRange(min=5)],
	)
	holder = SelectField(
		"Держатель: ",
		default="Не требуется",
		choices=holder_choices,
		validators=[DataRequired()]
	)
	place_operation = SelectField(
		"Место эксплуатации: ",
		choices=place_choices,
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
	quantity_sheet_material = IntegerField(
		'Количество:',
		validators=[DataRequired(), NumberRange(min=1)],
	)
	submit = SubmitField('Рассчитать')
	
	def validate(self, **kwargs):
		if not super().validate():
			if not self.type_material.data:
				return True
			return False
		
		return True
	
	
