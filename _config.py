import os


# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'experiences.db'
CSRF_ENABLED = True
SECRET_KEY = 'reg347gwzf85h45giuwg'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)