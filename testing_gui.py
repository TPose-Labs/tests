from tkinter import *
from tkinter.font import Font
import datetime
import calendar
#The below libraries are for `loadfont`
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20
def loadfont(fontpath, private=True, enumerable=False):
	if isinstance(fontpath, bytes):
		pathbuf = create_string_buffer(fontpath)
		AddFontResourceEx = windll.gdi32.AddFontResourceExA
	elif isinstance(fontpath, str):
		pathbuf = create_unicode_buffer(fontpath)
		AddFontResourceEx = windll.gdi32.AddFontResourceExW
	else:
		raise TypeError('fontpath must be of type str or unicode')
	flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
	numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
	return bool(numFontsAdded)

class ClockModule:

	def __init__(self, root):
		loadfont("fonts/Montserrat-Thin.ttf")
		montserrat_big = Font(family="Montserrat Thin", size=72)
		montserrat_small = Font(family="Montserrat Thin", size=48)

		self.root = root
		self.day = Label(root, font=montserrat_big, fg="white", bg="black", padx=5)
		self.day.grid(row=0, sticky="w")
		self.fulldate = Label(root, font=montserrat_small, fg="white", bg="black", padx=15)
		self.fulldate.grid(row=1, column=0, sticky="w")
		self.clock = Label(root, font=montserrat_small, fg="white", bg="black", padx=15)
		self.clock.grid(row=2, column=0, sticky="w")

		self.time = ""
		self.dotw = ""
		self.date = ""
		self.loop()

	def loop(self):
		currday = datetime.datetime.today()
		dotw = calendar.day_name[currday.weekday()] + ","
		date = currday.strftime("%B %d, %Y")
		time = currday.strftime("%I:%M %p")
		if self.time != time:
			self.time = time
			self.clock.config(text=time)
		if self.dotw != dotw:
			self.dotw = dotw
			self.day.config(text=dotw)
		if self.date != date:
			self.date = date
			self.fulldate.config(text=date)
		self.day.after(1000, self.loop)

# Setting up the main "root"
# of the hierarchy
root = Tk()
root.attributes('-fullscreen', True)
root.bind('<Escape>',lambda e: root.destroy())
root.configure(background="black")

# The "root" will contain several containers.
# Each container will house a module.
# For test purposes, I'm using "pack" alignment,
# but we will use "grid" alignment soon.
container = Frame(root, bg="black")
container.pack(side="left", fill="both")
clock = ClockModule(container)

# Runs the GUI
root.mainloop()