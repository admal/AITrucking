import time
from datetime import datetime
import cv2
import numpy as np

from config import *
from Utils.utils import process_screen

class GamepadInputTrainingHandler:
	writer = None
	_last_time_handle = None
	_frequency = 0.1
	def __init__(self, writer, frequency = 10):
		self.writer = writer
		self._last_time_handle = time.time()
		self._frequency = 1 / frequency


	def handle_input(self, screen, input_controller):
		if (time.time() - self._last_time_handle) >= self._frequency:
			pad_input = input_controller.get_input()
			dst = process_screen(screen)
			if SHOW_FRAMES:
				cv2.imshow("win1", dst)
			
			img_filename = TRAINING_DIRECTORY + '\\Images\\' + datetime.now().strftime('%d%m%Y%H%M%S%f') + '.jpg'
			cv2.imwrite(img_filename, dst)
			self.writer.writerow([img_filename, pad_input['A_X'], pad_input['RT'], pad_input['LT']])
			# print('rotation', 'throttle', 'brake')
			print(pad_input['A_X'], pad_input['RT'], pad_input['LT'])
			self._last_time_handle = time.time()


