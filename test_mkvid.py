#!venv/bin/python
from webapp import Timelapse
from datetime import datetime, timedelta

ww = Timelapse.Timelapse()
now = datetime.now()

START = now-timedelta(2)
END = now-timedelta(1)

print "Getting images"
ww.get_images(START, END)
print "Creating video..."
ww.create_video("day-test4")

# # Make weekly - Run on Sundays
# if now.isoweekday() == 7:
#     ww.get_images(start=now-timedelta(7), end=now)
#     ww.create_video("weekly-"+"%Y-%m-%d")

# # Make monthly - Runs first of month
# if now.day == 1:
#     ww.get_images(start=now-timedelta(32), end=now-timedelta(1))
#     ww.create_video((now-timedelta(10)).strftime("monthly-"+"%B"))
