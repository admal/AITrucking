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

    for i in range(0, MAX_ITERS):
        (x_train, y_train), (x_val, y_val) = load_csv_data(DATA_CSV_FILE, 0.1)
        # load batch for each iteration, batches differ in chosen images and its mirrors resulting in different datasets
        if BATCH_SIZE is None:
            x, y = load_batch(x_train, y_train, 0, len(y_train))
            x_v, y_v = load_batch(x_val, y_val, 0, len(y_val))
        else:
            x, y = load_batch(x_train, y_train, i, BATCH_SIZE)
            x_v, y_v = load_batch(x_val, y_val, i, BATCH_SIZE)
        
        x = np.reshape(x, [-1, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS])
        x_v = np.reshape(x_v, [-1, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS])

        y = np.reshape(y, [-1, 1])
        y_v = np.reshape(y_v, [-1, 1])
        iter_start_time = datetime.now()
        logging.info("START ITERATION {}/{}".format(i+1, MAX_ITERS))
        model.train(x, y, x_v, y_v)
        logging.info("iteration last: {0:.3g} minutes".format((datetime.now() - iter_start_time).seconds / 60))

    logging.info("FINISH")

if __name__ == "__main__":
    main()