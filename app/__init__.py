# Import flask and template operators
import app
from flask import Flask
from flask.ext.sendmail import Mail

from app.main.controllers import main as main
from app.users.controllers import users as users
from app.utils.controllers import utils as utils

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Register blueprint(s)
app.register_blueprint(users)
app.register_blueprint(main)

# start mail instance
mail = Mail(app)