from datetime import datetime
import os

import cv2
import numpy as np

from Data.CapturedFrame import CapturedFrame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, IMAGE_WIDTH, IMAGE_HEIGHT, TRAINING_DIRECTORY


class DataFrame(CapturedFrame):
	_screen_filename = None
	is_deleted = False
	rotation = 0.0
	_acceleration = 0.0

	def __init__(self, screen, rotation, acceleration):
		super().__init__(screen)
		self._acceleration = acceleration
		self.rotation = rotation

	def is_screen_saved(self):
		return self._screen_filename is not None

	def flip(self):
		self._processed_screen = np.flip(self._processed_screen, 1)
		self.rotation = -self.rotation

	def save_screen(self):
		if self.is_screen_saved():
			img_filename = self._screen_filename
		else:
			img_filename = TRAINING_DIRECTORY + '\\Images\\' + datetime.now().strftime('%d%m%Y%H%M%S%f') + '.jpg'

		cv2.imwrite(img_filename, self._processed_screen)
		self._screen_filename = img_filename

	def get_data_row(self):
		return self._screen_filename, self.rotation, self._acceleration

	def delete(self):
		self.is_deleted = True
		if self.is_screen_saved():
			os.remove(self._screen_filename)