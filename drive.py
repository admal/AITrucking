import cv2
import time
import inputs

from Utils.grabscreen import *
from Utils.directkeys import *
from config import *



def start():
	print('3 sec to start')
	time.sleep(3)

	while True:
		events = inputs.get_gamepad()
		for event in events:
			print(event.ev_type, event.code, event.state)

	while True:
		frame_started = time.time()
		screen = grab_screen(region=(0, 40, SCREEN_WIDTH, SCREEN_HEIGHT))


		cv2.imshow('AITrucking', screen)

		print('frame took: {}s'.format(time.time() - frame_started))
		PressKey(W)

		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break



if __name__ == '__main__':
	start()

