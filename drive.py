import cv2
import time

from Utils.grabscreen import *
from Utils.directkeys import *
from config import *



def start():
	while True:
		frame_started = time.time()
		screen = grab_screen(region=(0, 40, SCREEN_WIDTH, SCREEN_HEIGHT))


		cv2.imshow('AITrucking', screen)

		print('frame took: {}s'.format(time.time() - frame_started))
		
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break



if __name__ == '__main__':
	start()

