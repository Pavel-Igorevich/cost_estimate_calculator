from flask import Flask, render_template, url_for, request, redirect, jsonify
from data import DATA
from forms import CanvasForm, BannerForm, TestForm


PRODUCTS = sorted([[name, val['page']] for name, val in DATA.items()], key=lambda elem: elem[0])


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a really really really really long secret key'


@app.route('/')
@app.route('/home')
def index():
    return render_template('base.html', products=PRODUCTS)


@app.route('/test')
def test():
    form = TestForm()
    return render_template('test.html', products=PRODUCTS, form=form)


@app.route('/canvas', methods=['GET', 'POST'])
def canvas():
    form = CanvasForm()
    return_data = None
    if form.validate_on_submit():
        data_canvsas = DATA['Холст']['data']
        price_material = data_canvsas['Материал'][form.material.data]['Себестоимость']
        sale_price_material = data_canvsas['Материал'][form.material.data]['Продажа']
        price_proccessing = data_canvsas['Обработка'][form.processing.data]['Себестоимость']
        sale_price_proccessing = data_canvsas['Обработка'][form.processing.data]['Продажа']
        length = form.length.data
        width = form.width.data
        if length < 500:
            length = 500
        if width < 500:
            width = 500
        square = (float(length) / 1000) * (float(width) / 1000)
        perimeter = (float(length) / 1000 + float(width) / 1000) * 2
        main_price = round(((price_material * square) + (price_proccessing * perimeter)) * form.quantity.data, 2)
        main_sale_price = round(((sale_price_material * square) + (sale_price_proccessing * perimeter))
                                * form.quantity.data, 2)
        return_data = {
            'material': [form.material.data, price_material, sale_price_material],
            'processing': [form.processing.data, price_proccessing, sale_price_proccessing],
            'size': square,
            'quantity': form.quantity.data,
            'main_price': main_price,
            'main_sale_price': main_sale_price
        }

    return render_template('canvas.html', form=form, products=PRODUCTS, data=return_data)
    
    
@app.route('/banner', methods=['GET', 'POST'])
def banner():
    form = BannerForm()
    if form.validate_on_submit():
        for _ in form.data.items():
            print(_)
        # data_banner = DATA['Баннер']['data']
        # price_material = data_banner['Материал'][form.material.data][form.print_quality.data]['Себестоимость']
        # sale_price_material = data_banner['Материал'][form.material.data][form.print_quality.data]['Продажа']
        #
        # if form.welding_step.data != 'Недоступно':
        #     welding_step = form.welding_step.data
        #     price_proccessing = data_banner['Обработка'][form.processing.data][welding_step]['Себестоимость']
        #     sale_price_proccessing = data_banner['Обработка'][form.processing.data][welding_step]['Продажа']
        # else:
        #     welding_step = False
        #     price_proccessing = data_banner['Обработка'][form.processing.data]['Себестоимость']
        #     sale_price_proccessing = data_banner['Обработка'][form.processing.data]['Продажа']
        #
        # length = form.length.data
        # width = form.width.data
        # if length < 500:
        #     length = 500
        # if width < 500:
        #     width = 500
        # square = (float(length) / 1000) * (float(width) / 1000)
        # perimeter = (float(length) / 1000 + float(width) / 1000) * 2
        #
        # price_processing_side = 0
        # processing_sides = []
        # # todo сделать вывод ошибок с возможностью их изменения
        # if data_banner['Обработка'][form.processing.data].get('Сторона'):
        #     for key_side, val_side in form.data.items():
        #         if 'side' in key_side and val_side:
        #             processing_sides.append(form[key_side].label.text)
        #             if key_side in ['left_side', 'right_side']:
        #                 price_processing_side += (float(length) / 1000) * sale_price_proccessing
        #             elif key_side in ['top_side', 'down_side']:
        #                 price_processing_side += (float(width) / 1000) * sale_price_proccessing
        #             elif key_side == 'around_side':
        #                 price_processing_side += perimeter * sale_price_proccessing
        #             elif key_side == 'corner_side':
        #                 price_processing_side += sale_price_proccessing
        #     if not processing_sides:
        #         error_message = 'Не заданы стороны обработки!'
        #         return render_template('banner.html', form=form, products=PRODUCTS, error=error_message)
        # #     todo -----------------------------
        #
        #
        # # todo получить формулу посчета
        # main_price = 1000.00
        # main_sale_price = 2000.00
        
        # return_data = {
        #     'material': [form.material.data, price_material, sale_price_material],
        #     'processing': [form.processing.data, price_proccessing, sale_price_proccessing],
        #     'welding_step': welding_step,
        #     'processing_side': ['test', price_processing_side],
        #     'size': square,
        #     'quantity': form.quantity.data,
        #     'main_price': main_price,
        #     'main_sale_price': main_sale_price
        # }
        return_data = {
            'material': ['form.material.data', 'price_material', 'sale_price_material'],
            'processing': ['form.processing.data', 'price_proccessing', 'sale_price_proccessing'],
            'welding_step': 'welding_step',
            'processing_side': ['test', 'price_processing_side'],
            'size': 'square',
            'quantity': 'form.quantity.data',
            'main_price': 'main_price',
            'main_sale_price': 'main_sale_price'
        }
        return render_template('banner.html', form=BannerForm(), products=PRODUCTS, data=return_data)
    else:
        return render_template('banner.html', form=form, products=PRODUCTS)
 
    
@app.route('/banner/material/<state>')
def banner_material_state(state):
    form = BannerForm()
    if state == 'Сетка':
        return jsonify({'choices': ['720 dpi', 'Цена без печати']})
    return jsonify({'choices': form.print_quality.choices})


@app.route('/banner/process/<state>')
def banner_process_state(state):
    data = DATA['Баннер']['data']['Обработка'][state]
    choices = [
        ['left_side_id', True],
        ['right_side_id', True],
        ['top_side_id', True],
        ['down_side_id', True],
        ['around_side_id', True],
        ['corner_side_id', True]
    ]
    hide_choices = True
    if data.get('Сторона'):
        hide_choices = False
        for name_side in data.get('Сторона'):
            if name_side == 'Левая сторона':
                choices[0] = ['left_side_id', False]
            elif name_side == 'Правая сторона':
                choices[1] = ['right_side_id', False]
            elif name_side == 'Верх':
                choices[2] = ['top_side_id', False]
            elif name_side == 'Низ':
                choices[3] = ['down_side_id', False]
            elif name_side == 'Все стороны':
                choices[4] = ['around_side_id', False]
            elif name_side == 'По углам':
                choices[5] = ['corner_side_id', False]
    steps = [step for step in data.keys() if 'мм' in step] or ['Недоступно']
    return jsonify({'choices': choices, 'hide_choices': hide_choices, 'steps': steps})


if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
