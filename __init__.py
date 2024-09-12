from flask import Flask
from flask_cors import CORS
from db.db import init_db
from routes import register_apps

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
    
    # Initialize database
    init_db(app)
    
    # Register routes
    register_apps(app)

    return app

# If you want to run the app directly from this file
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)