import logging

from Data.DataFormatter import DataFormatter
from Utils.grabscreen import *
from Utils.directkeys import *
from config import *
from Controls.GamepadInputController import GamepadInputController

logging.basicConfig(filename=TRAIN_LOG_FILE, level=logging.DEBUG)


def start():
	print('3 sec to start')
	time.sleep(3)

	input_controller = GamepadInputController()
	input_controller.init()
	formatter = DataFormatter()
	last_input_handle = time.time()
	while True:
		# save with 10FPS frequency
		if (time.time() - last_input_handle) >= 0.1:
			screen = grab_screen(region=(0, 40, SCREEN_WIDTH, SCREEN_HEIGHT))

			game_input = input_controller.get_input()
			print(game_input['A_X'], game_input['RT'], game_input['LT'], game_input['start'])
			if game_input['start']:
				formatter.save_frames()
				break

			formatter.add_frame(screen, game_input)

			if formatter.frames_count() == 300:
				formatter.save_frames()

			last_input_handle = time.time()

		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break

	formatter.close_files()
	print('End, close files')


if __name__ == '__main__':
	start()
