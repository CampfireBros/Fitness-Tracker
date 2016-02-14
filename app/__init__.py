# Import flask and template operators
import app
from flask import Flask
from flask.ext.mail import Mail

from app.main.controllers import main as main
from app.users.controllers import users as users
from app.utils.controllers import utils as utils
from app.exercises.controllers import exercises as exercises
from app.rss.controllers import rss as rss

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Register blueprint(s)
app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(exercises)
app.register_blueprint(rss)

# start mail instance
mail = Mail(app)
