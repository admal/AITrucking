import cv2
import time
import csv

from Utils.grabscreen import *
from Utils.directkeys import *
from config import *
from Controls.GamepadInputController import GamepadInputController
from Controls.InputControl import GamepadInputTrainingHandler


def start():
	print('3 sec to start')
	time.sleep(3)

	input_controller = GamepadInputController()
	input_controller.init()
	training_data_file  = open(TRAINING_DIRECTORY + '\\train_data.csv', "w")
	writer = csv.writer(training_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	handler = GamepadInputTrainingHandler(writer)
	while True:
		frame_started = time.time()
		screen = grab_screen(region=(0, 40, SCREEN_WIDTH, SCREEN_HEIGHT))
		handler.handle_input(screen, input_controller)
		
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break

	training_data_file.close()


if __name__ == '__main__':
	start()

