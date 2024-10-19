from flask import Flask
from server.config import Config, db  # Import the Config class and db instance

def create_app():
    app = Flask(__name__)

    # Load configuration from the Config class
    app.config.from_object(Config)

    # Initialize the database with the app
    db.init_app(app)

    # Register blueprints
    from server.rewards import rewards_bp 
    app.register_blueprint(rewards_bp)

    return app
