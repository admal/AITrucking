from datetime import datetime, date, time
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

	(x_train, y_train), (x_val, y_val) = load_csv_data(DATA_CSV_FILE, 0.1)

	x, y = load_batch(x_train, y_train, 0, len(y_train))
	x_v, y_v = load_batch(x_val, y_val, 0, len(y_val))

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
	for i in range(0, MAX_ITERS):
		iter_start_time = datetime.now()
		logging.info("START ITERATION {}/{}".format(i + 1, MAX_ITERS))
		model.train(x, y, x_v, y_v)
		logging.info("iteration last: {0:.3g} minutes".format((datetime.now() - iter_start_time).seconds / 60))

	logging.info("FINISH")


if __name__ == "__main__":
	main()
