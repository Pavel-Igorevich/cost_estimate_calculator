from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, DecimalField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange
from data import DATA


class TestForm(FlaskForm):
    left_side = BooleanField(label='Левая')
    right_side = BooleanField(label='Правая')
    top_side = BooleanField(label='Верх')
    down_side = BooleanField(label='Низ')
    around_side = BooleanField(label='Все стороны')
    corner_side = BooleanField(label='По углам')


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
    down_side = BooleanField(label='Низ')
    around_side = BooleanField(label='Все стороны')
    corner_side = BooleanField(label='По углам')
    welding_step = SelectField(
        "Шаг сварки: ",
        choices=['Недоступно'],
        validate_choice=False,
        validators=[]
    )
    length = FlexibleDecimalField(
        'Длина баннера: ',
        validators=[DataRequired(), NumberRange(min=1)],
    )
    width = FlexibleDecimalField(
        'Ширина баннера: ',
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
                    self.around_side.data,
                    self.corner_side.data
                ]
        ) and DATA['Баннер']['data']['Обработка'][self.processing.data].get('Сторона'):
            self.left_side.errors.append('Необходимо выбрать "Стороны обработки"')
            if self.welding_step.data and self.welding_step.data != 'Недоступно':
                self.welding_step.errors.append(self.welding_step.data)
            return False
    
        return True
    