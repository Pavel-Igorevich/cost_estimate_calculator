from flask import Flask, render_template, url_for, request, redirect, jsonify
from data import DATA
from forms import CanvasForm, BannerForm
PRODUCTS = sorted([[name, val['page']] for name, val in DATA.items()], key=lambda elem: elem[0])


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a really really really really long secret key'


@app.route('/')
@app.route('/home')
def index():
    return render_template('base.html', products=PRODUCTS)


@app.route('/canvas', methods=['GET', 'POST'])
def canvas():
    form = CanvasForm()
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
    else:
        return render_template('canvas.html', form=form, products=PRODUCTS)
    
    
@app.route('/banner', methods=['GET', 'POST'])
def banner():
    form = BannerForm()
    if form.validate_on_submit():
        data_banner = DATA['Баннер']['data']
        price_material = data_banner['Материал'][form.material.data][form.print_quality.data]['Себестоимость']
        sale_price_material = data_banner['Материал'][form.material.data][form.print_quality.data]['Продажа']

        if form.welding_step.data != 'Недоступно':
            welding_step = form.welding_step.data
            price_proccessing = data_banner['Обработка'][form.processing.data][welding_step]['Себестоимость']
            sale_price_proccessing = data_banner['Обработка'][form.processing.data][welding_step]['Продажа']
        else:
            welding_step = False
            price_proccessing = data_banner['Обработка'][form.processing.data]['Себестоимость']
            sale_price_proccessing = data_banner['Обработка'][form.processing.data]['Продажа']
            
        length = form.length.data
        width = form.width.data
        if length < 500:
            length = 500
        if width < 500:
            width = 500
        square = (float(length) / 1000) * (float(width) / 1000)
        perimeter = (float(length) / 1000 + float(width) / 1000) * 2
        
        price_processing_side = None
        if form.processing_side.data != 'Недоступно':
            processing_side = form.processing_side.data
            # todo уточнить стоимости
            if processing_side in ['Левая сторона', 'Правая сторона']:
                price_processing_side = (float(length) / 1000) * sale_price_proccessing
            elif processing_side in ['Верх', 'Низ']:
                price_processing_side = (float(width) / 1000) * sale_price_proccessing
            elif processing_side == 'Все стороны':
                price_processing_side = perimeter * sale_price_proccessing
            elif processing_side == 'По углам':
                price_processing_side = sale_price_proccessing
        else:
            processing_side = False
        
        # todo получить формулу посчета
        main_price = 1000.00
        main_sale_price = 2000.00
        
        return_data = {
            'material': [form.material.data, price_material, sale_price_material],
            'processing': [form.processing.data, price_proccessing, sale_price_proccessing],
            'welding_step': welding_step,
            'processing_side': [processing_side, price_processing_side],
            'size': square,
            'quantity': form.quantity.data,
            'main_price': main_price,
            'main_sale_price': main_sale_price
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
    choices = data.get('Сторона') or ['Недоступно']
    steps = [step for step in data.keys() if 'мм' in step] or ['Недоступно']
    return jsonify({'choices': choices, 'steps': steps})


if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
