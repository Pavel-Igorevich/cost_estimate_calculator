from flask import Flask
from routes.banner_routes import banner, banner_material_state, banner_process_state
from routes.canvas_routes import canvas
from routes.base_routes import base
from routes.test_routes import test
from routes.sheet_materials_routes import sheet_materials, type_material_state, tickness_material_state
from routes.press_wall_routes import press_wall


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a really really really really long secret key'


@app.route('/')
@app.route('/home')
def base_page():
	return base()


@app.route('/test')
def test_page():
	return test()


@app.route('/canvas', methods=['GET', 'POST'])
def canvas_page():
	return canvas()


@app.route('/banner', methods=['GET', 'POST'])
def banner_page():
	return banner()


@app.route('/banner/material/<state>')
def data_material_banner(state):
	return banner_material_state(state)


@app.route('/banner/process/<state>')
def data_process_banner(state):
	return banner_process_state(state)


@app.route('/sheet_materials', methods=['GET', 'POST'])
def sheet_materials_page():
	return sheet_materials()


@app.route('/sheet_materials/material/<state>')
def data_sheet_material(state):
	return type_material_state(state)


@app.route('/sheet_materials/tickness/<state>/<state_type>')
def data_sheet_material_tickness(state, state_type):
	return tickness_material_state(state, state_type)


@app.route('/press_wall', methods=['GET', 'POST'])
def press_wall_page():
	return press_wall()


if __name__ == '__main__':
	app.run(debug=True, port=5000, threaded=True)
