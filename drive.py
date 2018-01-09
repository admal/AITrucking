import cv2
import time

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

	handler = GamepadInputTrainingHandler(None)
	while True:
		frame_started = time.time()
		screen = grab_screen(region=(0, 40, SCREEN_WIDTH, SCREEN_HEIGHT))

		handler.handle_input(None, input_controller)
		# print('frame took: {}s'.format(time.time() - frame_started))
		# if cv2.waitKey(25) & 0xFF == ord('q'):
		# 	cv2.destroyAllWindows()
		# 	break



if __name__ == '__main__':
	start()

