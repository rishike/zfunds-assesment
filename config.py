import os


class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    BASE_PATH =  os.getcwd()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///zfunds.db'
    SECRET_KEY = 'abcdefghi1234567!@#$%^&'
  
class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False