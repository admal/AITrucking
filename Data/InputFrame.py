from Data.CapturedFrame import CapturedFrame


class InputFrame(CapturedFrame):
	def get_screen_for_network(self):
		self.preprocess()
		return (self._processed_screen / 127.5) - 1.0
