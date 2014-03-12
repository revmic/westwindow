import os
import sys
import time
import shutil
#import errno
#import socket
import logging  # To Do !!!
import os.path as op
import subprocess as sp
from datetime import date, timedelta
from SimpleCV import *
from sqlalchemy import and_
from models import WindowImage, WindowVideo, Session

MNTROOT = '/mnt/westwindow'
APPROOT = '/home/michael/Development/westwindow'


class Timelapse(object):
    """
    Aids in the creation of time-lapse photography.
    Images can be passed to the constructor from an external source,
    or returned from a database using the get_images method.
    """
    def __init__(self, images=[], timespan=1, length=30, fps=15, rootdir='/mnt/westwindow'):
        self.images = images
        self.timespan = timespan
        self.length = length
        self.fps = fps
        self.rootdir = rootdir

    def __str__(self):
        return '(Timelapse - %s images, Span: %s day(s), Length: %s sec, FPS: %s)' % \
            (len(self.images), self.timespan, self.length, self.fps)


    # Does this belong here ???
    def capture_image(self):
        pass
    #####################


    def get_images(self, start=None, end=None, include_night=False):
        """ (date, date, bool) --> list
        Returns a list of images from database.
        Arguments: start and end dates
        """
        db = Session()
        if start is None:
            start = date.today()-timedelta(1)
            end = date.today()

        #print end - start
        try:
            imgs_results = db.query(WindowImage) \
                             .filter(and_(WindowImage.datetime >= start,
                                          WindowImage.datetime <= end))
        except Exception, e:
            print e

        for i in imgs_results:
            if include_night:
                self.images.append(i)
            elif i.datetime.hour >= 6 and i.datetime.hour < 21:
                self.images.append(i)

    def stream_to_web(self, address="192.168.1.4:8082"):
        """
        Uses SimpleCV JpegStreamer
        """
        jpeg_stream = JpegStreamer(address, st=0.03)

        for img in self.images:
            fullpath = str(op.join(MNTROOT, img.relativepath, img.filename))
            time.sleep(0.01)
            print img
            try:
                lapse_img = Image(fullpath)
                txt = str(img.datetime)
                lapse_img.drawText(txt, 50, 666, fontsize=50)
                lapse_img.save(jpeg_stream)
            except IOError:
                print "Couldn't find file: " + fullpath
            except Exception, e:
                if e.errno == 9:
                    print "Bad file descriptor!"
                    break
                else:
                    print "Exception!!!"
                    print e
                    jpeg_stream.server.socket.close()
                    break
        jpeg_stream.server.socket.close()

    def create_video(self, title):
        ## Thin out images either here or in get_images()
        print "Creating symlinks in cache directory"
        sourcedir = '/home/michael/Development/westwindow/cache/source'
        # if source exists, delete. Else create new
        if not op.exists(sourcedir):
            os.makedirs(sourcedir)

        for img in self.images:
            source = op.join(MNTROOT, img.relativepath, img.filename)
            destination = op.join(APPROOT, 'cache/source', img.filename)
            os.symlink(source, destination)

        print "Copying and executing deflicker script"
        shutil.copy2(op.join(APPROOT, 'cache/timelapse-deflicker.pl'), op.join(APPROOT, 'cache/source'))
        os.chdir(op.join(APPROOT, 'cache/source'))
        sp.call('perl timelapse-deflicker.pl -p 2', shell=True)

        print "Collecting image names in a file"
        os.chdir('Deflickered')
        sp.call('ls -1tr | grep -v files.txt > files.txt', shell=True)

        print "Converting images to a timelapse video"
        # convert *.jpg -delay 10 -morph 5 %05d.jpg
        sp.call("mencoder -nosound -noskip -oac copy -ovc copy -o "+title+".avi -mf fps=30 'mf://@files.txt'", shell=True)

        """#temporary
        os.chdir(op.join(APPROOT, 'cache/source'))
        os.chdir('Deflickered')
        """
        print "Moving video file and cleaning up"
        folder = title.split('-')[0]
        if not op.exists(op.join(MNTROOT, 'videos/', folder)):
            folder = 'other'

        video_dest = op.join(MNTROOT, 'videos/', folder)
        retval = sp.call("cp *.avi " + video_dest, shell=True)

        if retval == 0:
            shutil.rmtree(op.join(APPROOT, 'cache/source'))
            print title + " file created successfully"
        else:
            print "Horribe error while copying"
            sys.exit(1)

        ## Write to database

if __name__ == "__main__":
    tl = Timelapse()
    print "Timelapse length: " + str(tl.length)
    print "Timespan in days: " + str(tl.timespan)
    print "List of image objects: "
    tl.stream_to_web()
    tl.make_video()
