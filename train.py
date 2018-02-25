from datetime import datetime, date, time
from math import ceil, floor
from pathlib import Path
import logging

from Model.model2.TrainModel import TrainModel
from Utils.utils import *
from config import *

logging.basicConfig(filename=TRAIN_LOG_FILE, level=logging.DEBUG)


def main():
	logging.info("START")
	model = TrainModel(MODEL_DIRECTORY + '\\trained-model')

	folder = Path(MODEL_DIRECTORY + '\\NvidiaModel')
	if folder.exists():
		model.load()

	(x_train, y_train), (x_val, y_val) = load_csv_data(DATA_CSV_FILE)

	iterations_count = ceil(len(x_train) / BATCH_SIZE) + 1
	logging.info("Iterations count: {}".format(iterations_count))
	for i in range(0, MAX_ITERS):
		iter_start_time = datetime.now()
		logging.info("[{}] START ITERATION {}/{}".format(datetime.now().strftime("%d/%m/%Y %H:%M"), i + 1, MAX_ITERS))

		if BATCH_SIZE is None:
			x, y = load_batch(x_train, y_train, 0, len(x_train))
			x_v, y_v = load_batch(x_val, y_val, 0, len(x_val))
		else:
			x, y = load_batch(x_train, y_train, i % iterations_count, BATCH_SIZE)
			x_v, y_v = load_batch(x_val, y_val, i % iterations_count, floor(BATCH_SIZE / 10))
		if len(x) == 0 or len(x_v) == 0:
			break

		x = np.reshape(x, [-1, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS])
		x_v = np.reshape(x_v, [-1, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS])

		y = np.reshape(y, [-1, 1])
		y_v = np.reshape(y_v, [-1, 1])

		delta = 0.2
		straight = 0
		right = 0
		left = 0
		for rotation in y:
			if rotation < -delta:
				left = left + 1
			elif rotation > delta:
				right = right + 1
			else:
				straight = straight + 1

		logging.info("Data distribution: straight: {}; left: {}; right:{}".format(
			straight, left, right
		))

		model.train(x, y, x_v, y_v)
		logging.info("[{0}] iteration last: {1:.3g} minutes".format(datetime.now().strftime("%d/%m/%Y %H:%M"),
		                                                           (datetime.now() - iter_start_time).seconds / 60))

	logging.info("FINISH")


if __name__ == "__main__":
	main()
