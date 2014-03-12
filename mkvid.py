#!venv/bin/python
from webapp import Timelapse, models
from datetime import datetime, timedelta

db = models.Session()


def mkvid():
    """
    Script runs daily checking for weekly and monthly conditions
    """
    now = datetime.now()
    ww = Timelapse.Timelapse()

    # Daily video
    print "Getting Images..."
    ww.get_images()
    print "Creating Daily Video..."
    title = (now-timedelta(1)).strftime("day-"+"%Y-%m-%d")
    ww.create_video(title)

    # Make weekly - Run on Sundays
    if now.isoweekday() == 7:
        print "Creating Weekly Video..."
        ww.get_images(start=now-timedelta(7), end=now)
        ww.create_video("week-"+"%Y-%m-%d")

    # Make monthly - Runs first of month
    if now.day == 1:
        print "Creating Montyly Video..."
        ww.get_images(start=now-timedelta(32), end=now-timedelta(1))
        ww.create_video((now-timedelta(10)).strftime("month-"+"%B"))


if __name__ == '__main__':
    mkvid()
