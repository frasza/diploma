import os


# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'experiences.db'
CSRF_ENABLED = True
SECRET_KEY = 'reg347gwzf85h45giuwg'

MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = "zan.fraas@gmail.com"

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)