from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Application Factory : crée et configure l'application Flask."""
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Importation des modèles et enregistrement des routes
    from app import models
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app