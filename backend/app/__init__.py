from flask import Flask
from flask_cors import CORS  # Import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "chrome-extension://hmlmaaaakaaolagpoaipegafjhdkhapm"}})

from app import views
