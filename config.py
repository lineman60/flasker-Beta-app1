__author__ = 'Beryl'
#config.py
# yes this should be in git ignore, tutorial app don't care.


import os

#graps the folder, yay OS agnostic

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'my_precious'

#Defines the full path
DATABASE_PATH = os.path.join(basedir, DATABASE)
SQLALCHEMY_DATABASE_URI = 'sqlite:////' + DATABASE_PATH
