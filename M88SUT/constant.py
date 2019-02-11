import ctypes

user32 = ctypes.windll.user32
WIDTH = user32.GetSystemMetrics(0)      #Get Width of monitor
HEIGHT = user32.GetSystemMetrics(1)      #Get Height of monitor
