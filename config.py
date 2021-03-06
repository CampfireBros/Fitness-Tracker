# Define the application directory
import os

# Statement for enabling the development environment
DEBUG = True

# Change when needed
HOST = '0.0.0.0'
PORT = 5000

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# MongoDB settings
MONGODB_URL = "mongodb://admin:admin@ds041571.mongolab.com:41571/exercisedb"

# Salt for password hashing
# WARNING changing this field will result in all passwords
# previously saved to be unusable
# this salt was generated with uuid.uuid4().hex
SALT = 'd8f473b018b447e9ae6f74786540131d'

# Flag if in testing mode (disables sending emails)
TESTING = True

#MAIL_USERNAME = "exercisedb@exercisedb.com"
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'theexercisedb@gmail.com'
MAIL_PASSWORD = 'exdb2016'
