from data import DATA
from calculations.default_calc_func import perimeter_calc, square_calc


def frame_price(frame, height, width, depth):
	price, sale_price = 0, 0
	if frame == "Брус":
		if depth == 0:
			price = 960 * height * width
		else:
			price = (760 * width * height) + (500 * (width + depth * 2) * height)
		sale_price = price * 1.5
	elif frame == "Металл":
		if depth == 0:
			price = 1500 * height * width
		else:
			price = (2000 * width * height) + (500 * (width + depth * 2) * height)
		sale_price = price * 1.5
	# todo сделать формулы расчета
	elif frame == "Джокер":
		pass
	elif frame == "Двутикс":
		pass
	elif frame == "Тритикс":
		pass
	return price, sale_price


def price_overhead_elements(depth, width):
	price = 1550 * depth * width * 2
	sale_price = price * 1.5
	return price, sale_price


def price_second_side(type_sec_side, frame, depth, width, height):
	price, sale_price = 0, 0
	if type_sec_side == "С печатью":
		if frame == "Брус":
			if depth > 0:
				price = 800 * width * height
				sale_price = price * 1.5
			else:
				# todo спросить!!!
				pass
		elif frame == "Металл":
			if depth > 0:
				price = 1500 * width * height
				sale_price = price * 1.5
			else:
				# todo спросить!!!
				pass
	elif type_sec_side == "Баннер":
		if frame == "Брус":
			if depth > 0:
				price = 700 * width * height
				sale_price = price * 1.5
			else:
				# todo спросить!!!
				pass
		elif frame == "Металл":
			if depth > 0:
				price = 1400 * width * height
				sale_price = price * 1.5
			else:
				# todo спросить!!!
				pass
	return price, sale_price


def main_calc(form):
	# TODO сделать расчет и вывод!!!
	return None
