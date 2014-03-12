from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('postgresql://postgres:sn4ark!@192.168.1.2/westwindow')
Session = sessionmaker(bind=engine)


class WindowImage(Base):
    __tablename__ = 'window_image'
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    fullpath = Column(String)
    relativepath = Column(String)
    datetime = Column(DateTime)
    #filesize = Column(Integer)

    def __init__(self, filename, fullpath, relativepath, datetime):
        self.filename = filename
        self.fullpath = fullpath
        self.relativepath = relativepath
        self.datetime = datetime

    def __repr__(self):
        return '<Image %r %r>' % (self.filename, self.datetime)


class WindowVideo(Base):
    __tablename__ = 'window_video'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    filename = Column(String)
    relativepath = Column(String)
    datetime = Column(DateTime)
    notable = Column(Boolean, default=False)
    #filesize = Column(Integer)

    def __repr__(self):
        return '<Video %r %r>' % (self.filename, self.datetime)


class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    json_object = Column(String)


class Forecast(Weather):
    pass


class Actual(Weather):
    pass
