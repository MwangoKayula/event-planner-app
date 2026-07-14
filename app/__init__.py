from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import db from models (where it's defined)
from .models import db

def create_app():
    app = Flask(__name__)
    
    # Config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # or your DB URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-key-change-in-production'
    
    # Init extensions
    db.init_app(app)
    Migrate(app, db)
    
    # Register blueprints
    from .routes import bp
    app.register_blueprint(bp)
    
    return app