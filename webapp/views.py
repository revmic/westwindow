from flask import render_template, redirect, url_for
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from threading import Thread
from models import WindowImage
from webapp import *
import Timelapse, time

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title='Home')

@app.route("/lapse")
def lapse():
    ww = Timelapse.Timelapse()
    ww.get_images()
    lapse_t = Thread(target=ww.stream_to_web)
    lapse_t.start()
    time.sleep(0.1)
    return render_template('stream.html')

#@app.route("/live")
#def live():
#    return render_template('stream.html')
