from flask import Flask
from flask_cors import CORS
from db.db import init_db
from routes import register_apps

def create_app():
    app = Flask(__name__)
    CORS(app)
    init_db(app)
    register_apps(app)
    return app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)