import os
from os import path


class Config(object):
    pass


class ProdConfig(Config):
    DEBUG = True
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'blog'
    USERNAME = 'root'
    PASSWORD = 'root1234'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT,
                                                                                   DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = 'uploads'
    AVATAR_FOLDER = 'avatars'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = (['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'JPG'])
    ALLOWED_IMAGES = (['png', 'jpg', 'jpeg', 'gif', 'JPG'])
    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'

class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(path.curdir, 'mystudya.db')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'default': ProdConfig,
    'sqlconfig': DevConfig
}
