# class InputHandler:
# 	_key_codes_handlers = None

# 	def _init_key_codes():
# 		pass

# 	def hanle_event(input_event):
# 		pass

# class GamePadTrainingInputHandler(InputHandler):
# 	_max_analog_val = 32767

# 	def _init_key_codes():
# 		_key_codes_handlers = {
# 			'ABS_RZ': handle_right_trigger,
# 			'ABS_Z': handle_left_trigger,
# 			'ABS_X': handle_left_analog
# 		}

# 	def handle_event(input_event, callback):
		
#ABS_RZ - right trigger
#ABS_Z - left trigger
#ABS_X - left analog
import time

class GamepadInputTrainingHandler:
	_file = None
	_last_time_handle = None
	_frequency = 0.1
	def __init__(self, file, frequency = 10):
		self._file = file
		self._last_time_handle = time.time()
		self._frequency = 1 / frequency


	def handle_input(self, screen, input_controller):
		if (time.time() - self._last_time_handle) >= self._frequency:
			pad_input = input_controller.get_input()

			#TODO: what to do with screen
			#screenshot, rotation, throttle, brake
			data_row = [screen, pad_input['A_X'], pad_input['RT'], pad_input['LT']]

			# print('rotation', 'throttle', 'brake')
			print(pad_input['A_X'], pad_input['RT'], pad_input['LT'])
			self._last_time_handle = time.time()