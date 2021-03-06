import cv2

from config import SCREEN_HEIGHT, SCREEN_WIDTH, IMAGE_HEIGHT, IMAGE_WIDTH, CUT_TOP, CUT_BOTTOM


class CapturedFrame:
	_processed_screen = None

	def __init__(self, screen):
		self._raw_screen = screen

	def preprocess(self, force=False):
		if self._processed_screen is None or force:
			dst = cv2.cvtColor(self._raw_screen, cv2.COLOR_BGR2RGB)
			dst = dst[SCREEN_HEIGHT - CUT_TOP:SCREEN_HEIGHT-CUT_BOTTOM, 0:SCREEN_WIDTH]
			dst = cv2.resize(dst, (IMAGE_WIDTH, IMAGE_HEIGHT))
			self._processed_screen = dst