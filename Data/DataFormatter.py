import csv
import logging
import random

import numpy as np
import time

from Data.DataFrame import DataFrame
from config import TRAINING_DIRECTORY


class DataFormatter:
	_frames = []

	def __init__(self):
		self._training_data_file = open(TRAINING_DIRECTORY + '\\train_data.csv', "a")
		self._validation_data_file = open(TRAINING_DIRECTORY + '\\validation_data.csv', "a")

	def frames_count(self):
		return len(self._frames)

	def add_frame(self, screen, pad_input):
		# TODO: make some abstraction for inputs, maybe move logic somewhere
		brake_input = pad_input['LT'] / 2 + 0.5
		throttle_input = pad_input['RT'] / 2 + 0.5

		acceleration = throttle_input - brake_input

		frame = DataFrame(screen, pad_input['A_X'], acceleration)
		frame.preprocess()
		frame.save_screen()
		self._frames.append(frame)

	def save_frames(self):
		if len(self._frames) == 0:
			return

		started = time.time()
		straight, left, right = self._balance_frames()
		logging.info("After balance: straight: {}, left: {}, right: {}".format(straight, left, right))
		logging.info("After balance real straight: {}".format(len([tmp for tmp in self._frames if not tmp.is_deleted and -0.2<tmp.rotation<0.2])))
		logging.info("Deleted: {}".format(len([tmp for tmp in self._frames if tmp.is_deleted])))

		idx = 0

		validation_data_writer = csv.writer(self._validation_data_file, delimiter=',', quotechar='"',
		                                    quoting=csv.QUOTE_MINIMAL)

		training_data_writer = csv.writer(self._training_data_file, delimiter=',', quotechar='"',
		                                  quoting=csv.QUOTE_MINIMAL)
		for frame in self._frames:
			idx = idx + 1

			# frame.save_screen()
			filename, rotation, acceleration = frame.get_data_row()
			if not frame.is_deleted:
				if idx % 10 == 0:
					validation_data_writer.writerow([filename, rotation, acceleration])
				else:
					training_data_writer.writerow([filename, rotation, acceleration])

		self._frames.clear()
		print('Saving took: {}'.format(time.time() - started))

	def _balance_frames(self):
		delta = 0.2
		left = 0
		right = 0
		straight = 0
		for frame in self._frames:
			if frame.rotation < -delta:
				left = left + 1
			elif frame.rotation > delta:
				right = right + 1
			else:
				straight = straight + 1

		to_flip = np.floor((right - left) / 2)
		logging.info("In function: straight: {}, left: {}, right: {}".format(straight, left, right))
		logging.info('To flip: {}'.format(to_flip))

		flipped = 0
		# add some random distribution
		for frame in self._frames:
			rnd = np.random.choice(2)
			if to_flip > 0 and frame.rotation > delta and rnd == 1:
				# flip from right to left
				frame.flip()
				# if screen was already save overrite
				if frame.is_screen_saved():
					frame.save_screen()

				right = right - 1
				left = left + 1
				flipped = flipped + 1
			elif to_flip < 0 and frame.rotation < -delta and rnd == 1:
				frame.flip()
				# if screen was already save overrite
				if frame.is_screen_saved():
					frame.save_screen()
				right = right + 1
				left = left - 1
				flipped = flipped + 1

			if flipped >= abs(to_flip):
				break

		rotations = max(left, right)
		if straight > rotations:
			to_delete = straight - rotations
			forward_frames = [forward for forward in self._frames if -delta < forward.rotation < delta]
			frames_to_delete = random.sample(forward_frames, to_delete)
			for frame in frames_to_delete:
				straight = straight - 1
				frame.delete()

		return straight, left, right

	def close_files(self):
		self._validation_data_file.close()
		self._training_data_file.close()

# if __name__ == '__main__':
# 	formatter = DataFormatter(None)
# 	for i in range(0, 23):
# 		formatter.add_frame([], {'LT': 1, 'RT': 1, 'A_X': 0.3})
# 	for i in range(0, 30):
# 		formatter.add_frame([], {'LT': 1, 'RT': 1, 'A_X': 0})
# 	for i in range(0, 40):
# 		formatter.add_frame([], {'LT': 1, 'RT': 1, 'A_X': -0.3})
#
# 	formatter.save_frames()
