import os
from flask import Flask
from flask_sse import sse

app = Flask(__name__, template_folder=os.path.abspath('templates'))
app.config["REDIS_URL"] = "redis://localhost:6379/0"
app.register_blueprint(sse, url_prefix='/stream')

# Import views to register routes
from app import main
