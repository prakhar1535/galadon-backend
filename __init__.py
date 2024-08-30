from flask import Flask
from db.db import init_db
from routes import register_apps
def create_app():
    app = Flask(__name__)

    init_db(app)
    register_apps(app)

    return app
