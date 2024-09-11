from flask import Flask
from db.db import init_db
from routes import register_apps
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})
    init_db(app)
    register_apps(app)

    return app
