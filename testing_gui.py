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

time = ""
dotw = ""
date = ""
def date_loop():
	global toggle_colon
	global dotw
	global time
	global date
	currday = datetime.datetime.today()
	dotw_ = calendar.day_name[currday.weekday()] + ","
	date_ = currday.strftime("%B %d, %Y")
	time_ = currday.strftime("%I:%M %p")
	if time_ != time:
		time = time_
		clock.config(text=time)
	if dotw_ != dotw:
		dotw = dotw_
		day.config(text=dotw)
	if date_ != date:
		date = date_
		fulldate.config(text=date)
	day.after(1000, date_loop)

root = Tk()
root.attributes('-fullscreen', True)
root.bind('<Escape>',lambda e: root.destroy())
root.configure(background="black")

loadfont("fonts/Montserrat-Thin.ttf")
montserrat_big = Font(family="Montserrat Thin", size=72)
montserrat_small = Font(family="Montserrat Thin", size=48)
day = Label(root, font=montserrat_big, fg="white", bg="black", padx=5)
day.grid(row=0, sticky="w")
fulldate = Label(root, font=montserrat_small, fg="white", bg="black", padx=15)
fulldate.grid(row=1, column=0, sticky="w")
clock = Label(root, font=montserrat_small, fg="white", bg="black", padx=15)
clock.grid(row=2, column=0, sticky="w")

date_loop()
root.mainloop()