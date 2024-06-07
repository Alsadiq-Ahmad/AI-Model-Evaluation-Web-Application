#Importing Required Modules
import os
from flask import Flask
from flask_sse import sse
#Initializing the Flask Application
app = Flask(__name__, template_folder=os.path.abspath('templates'))
app.config["REDIS_URL"] = "redis://localhost:6379/0"
app.register_blueprint(sse, url_prefix='/stream') #all the routes will be accessible under '/stream' prefix

# Import views to register routes
from app import main
