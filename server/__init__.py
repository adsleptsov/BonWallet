from flask import Flask
from server.config import Config, db  # Import the Config class and db instance
from server.rewards import rewards_bp  # Import your Blueprint

def create_app():
    app = Flask(__name__)

    # Load configuration from the Config class
    app.config.from_object(Config)

    # Initialize the database with the app
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(rewards_bp)

    return app
