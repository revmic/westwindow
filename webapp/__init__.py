from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)

from webapp import views, models

app.wsgi_app = ProxyFix(app.wsgi_app)
