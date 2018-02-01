# THANKS FOR THE GIST: https://gist.github.com/rdb/8883307
# Released by rdb under the Unlicense (unlicense.org)
# Further reading about the WinMM Joystick API:
# http://msdn.microsoft.com/en-us/library/windows/desktop/dd757116(v=vs.85).aspx


from math import floor, ceil
import time
import ctypes
import winreg as winreg
from ctypes.wintypes import WORD, UINT, DWORD
from ctypes.wintypes import WCHAR as TCHAR

# Fetch function pointers
joyGetNumDevs = ctypes.windll.winmm.joyGetNumDevs
joyGetPos = ctypes.windll.winmm.joyGetPos
joyGetPosEx = ctypes.windll.winmm.joyGetPosEx
joyGetDevCaps = ctypes.windll.winmm.joyGetDevCapsW

# Define constants
MAXPNAMELEN = 32
MAX_JOYSTICKOEMVXDNAME = 260

JOY_RETURNX = 0x1
JOY_RETURNY = 0x2
JOY_RETURNZ = 0x4
JOY_RETURNR = 0x8
JOY_RETURNU = 0x10
JOY_RETURNV = 0x20
JOY_RETURNPOV = 0x40
JOY_RETURNBUTTONS = 0x80
JOY_RETURNRAWDATA = 0x100
JOY_RETURNPOVCTS = 0x200
JOY_RETURNCENTERED = 0x400
JOY_USEDEADZONE = 0x800
JOY_RETURNALL = JOY_RETURNX | JOY_RETURNY | JOY_RETURNZ | JOY_RETURNR | JOY_RETURNU | JOY_RETURNV | JOY_RETURNPOV | JOY_RETURNBUTTONS

# This is the mapping for my XBox 360 controller.
button_names = ['a', 'b', 'x', 'y', 'tl', 'tr', 'back', 'start', 'thumbl', 'thumbr']
povbtn_names = ['dpad_up', 'dpad_right', 'dpad_down', 'dpad_left']

# Define some structures from WinMM that we will use in function calls.
class JOYCAPS(ctypes.Structure):
    _fields_ = [
        ('wMid', WORD),
        ('wPid', WORD),
        ('szPname', TCHAR * MAXPNAMELEN),
        ('wXmin', UINT),
        ('wXmax', UINT),
        ('wYmin', UINT),
        ('wYmax', UINT),
        ('wZmin', UINT),
        ('wZmax', UINT),
        ('wNumButtons', UINT),
        ('wPeriodMin', UINT),
        ('wPeriodMax', UINT),
        ('wRmin', UINT),
        ('wRmax', UINT),
        ('wUmin', UINT),
        ('wUmax', UINT),
        ('wVmin', UINT),
        ('wVmax', UINT),
        ('wCaps', UINT),
        ('wMaxAxes', UINT),
        ('wNumAxes', UINT),
        ('wMaxButtons', UINT),
        ('szRegKey', TCHAR * MAXPNAMELEN),
        ('szOEMVxD', TCHAR * MAX_JOYSTICKOEMVXDNAME),
    ]

class JOYINFO(ctypes.Structure):
    _fields_ = [
        ('wXpos', UINT),
        ('wYpos', UINT),
        ('wZpos', UINT),
        ('wButtons', UINT),
    ]

class JOYINFOEX(ctypes.Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('dwFlags', DWORD),
        ('dwXpos', DWORD),
        ('dwYpos', DWORD),
        ('dwZpos', DWORD),
        ('dwRpos', DWORD),
        ('dwUpos', DWORD),
        ('dwVpos', DWORD),
        ('dwButtons', DWORD),
        ('dwButtonNumber', DWORD),
        ('dwPOV', DWORD),
        ('dwReserved1', DWORD),
        ('dwReserved2', DWORD),
    ]




joyGetPosEx = ctypes.windll.winmm.joyGetPosEx

class UnpluggedError(RuntimeError):
    """The device requested is not plugged in."""
    pass




class GamepadInputController:
	def __init__(self):
		self.button_states = {}
		self.caps = None

	def init(self):
		# Get the number of supported devices (usually 16).
		num_devs = joyGetNumDevs()
		print(num_devs)
		if num_devs == 0:
			raise UnpluggedError('There is no plugged in gamepad')

		# Number of the joystick to open.
		joy_id = 0

		# Check if the joystick is plugged in.
		info = JOYINFO()
		p_info = ctypes.pointer(info)
		if joyGetPos(joy_id, p_info) != 0:
			print("Joystick %d not plugged in." % (joy_id + 1))

		# Get device capabilities.
		self.caps = JOYCAPS()
		if joyGetDevCaps(joy_id, ctypes.pointer(self.caps), ctypes.sizeof(JOYCAPS)) != 0:
			print("Failed to get device capabilities.")

		print("Driver name:", self.caps.szPname)

		# Fetch the name from registry.
		key = None
		if len(self.caps.szRegKey) > 0:
			try:
				key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "System\\CurrentControlSet\\Control\\MediaResources\\Joystick\\%s\\CurrentJoystickSettings" % (self.caps.szRegKey))
			except WindowsError:
				key = None

		if key:
			oem_name = winreg.QueryValueEx(key, "Joystick%dOEMName" % (joy_id + 1))
			if oem_name:
				key2 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "System\\CurrentControlSet\\Control\\MediaProperties\\PrivateProperties\\Joystick\\OEM\\%s" % (oem_name[0]))
				if key2:
					oem_name = winreg.QueryValueEx(key2, "OEMName")
					print("OEM name:", oem_name[0])
				key2.Close()

		# Set the initial button states.
		for b in range(self.caps.wNumButtons):
			name = button_names[b]
			if (1 << b) & info.wButtons:
				self.button_states[name] = True
			else:
				self.button_states[name] = False

		for name in povbtn_names:
			self.button_states[name] = False

		buttons_text = ""

		# Initialise the JOYINFOEX structure.
		info = JOYINFOEX()
		info.dwSize = ctypes.sizeof(JOYINFOEX)
		info.dwFlags = JOY_RETURNBUTTONS | JOY_RETURNCENTERED | JOY_RETURNPOV | JOY_RETURNU | JOY_RETURNV | JOY_RETURNX | JOY_RETURNY | JOY_RETURNZ

		self.info = info
		self.p_info = ctypes.pointer(info)


	def get_input(self):
		if joyGetPosEx(0, self.p_info) == 0:
			info = self.info

			x = (info.dwXpos - 32767) / 32768.0
			y = (info.dwYpos - 32767) / 32768.0
			trig = (info.dwZpos - 32767) / 32768.0
			rx = (info.dwRpos - 32767) / 32768.0
			ry = (info.dwUpos - 32767) / 32768.0

			# NB.  Windows drivers give one axis for the trigger, but I want to have
			# two for compatibility with platforms that do support them as separate axes.
			# This means it'll behave strangely when both triggers are pressed, though.
			lt = max(-1.0,  trig * 2 - 1.0)
			rt = max(-1.0, -trig * 2 - 1.0)

			# Figure out which buttons are pressed.
			for b in range(self.caps.wNumButtons):
				pressed = (0 != (1 << b) & info.dwButtons)
				name = button_names[b]
				self.button_states[name] = pressed

			# Determine the state of the POV buttons using the provided POV angle.
			if info.dwPOV == 65535:
				povangle1 = None
				povangle2 = None
			else:
				angle = info.dwPOV / 9000.0
				povangle1 = int(floor(angle)) % 4
				povangle2 = int(ceil(angle)) % 4

			for i, btn in enumerate(povbtn_names):
				if i == povangle1 or i == povangle2:
					self.button_states[btn] = True
					print('Pressed: {}; State: {}'.format(btn, self.button_states[btn]))
				else:
					self.button_states[btn] = False
			return {
				'A_X': x,
				'LT': lt,
				'RT': rt,
				'start': self.button_states['start']
			}
		else:
			raise UnpluggedError('Gamepad is not plugged into')

