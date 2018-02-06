from Data.InputFrame import InputFrame
from Model.model2.PredictModel import PredictModel
from Utils.grabscreen import *
from config import *
from Controls.VJoy import *


def drive():
	model = PredictModel()
	vj = vJoy()
	vj.open()
	print('3 sec to start')
	time.sleep(3)
	print('start')

	joystick_position = vj.generateJoystickPosition(wAxisX=16000, wAxisY=16000)
	vj.update(joystick_position)

	while True:
		frame_started = time.time()
		screen = grab_screen(region=(0, 40, SCREEN_WIDTH, SCREEN_HEIGHT))
		frame = InputFrame(screen)
		input_screen = frame.get_screen_for_network()
		result = model.predict([input_screen])

		steering_angle = result[0][0]
		xPos = int((steering_angle * 10000))
		joystick_position = vj.generateJoystickPosition(wAxisX=16000 + xPos, wAxisY=8000)
		vj.update(joystick_position)

		time.sleep(0.01)

		print('Time: {0:.3g}s; Predicted: {1: .3g};'.format(time.time() - frame_started, steering_angle))

	vj.close()


if __name__ == '__main__':
	drive()
