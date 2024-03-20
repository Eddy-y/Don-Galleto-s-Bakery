import os
import urllib

class Config(object):
    SECRET_KEY = 'Clave_nueva'
    SESSION_COOKIE_SECURE = True

class DevelopmentConfig(Config):
    DEBUG = True
    port = 5000
    SECRET_KEY = "miLlave"
    MYSQL_HOST = 'localhost'
    # MYSQL_USER = 'seguridadUser'
    # MYSQL_PASSWORD = 'V1ct0rG4y'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '1234'
    MYSQL_DB = 'testingdb'
    MYSQL_CURSORCLASS = 'DictCursor'
    MAX_FAILED_ATTEMPTS = 3
    TIME_TO_UNLOCK = 20

