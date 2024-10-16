from flask import Flask
from .extensions import db
from .routes import main

def create_app():
    app = Flask(__name__)
    
    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialiser les extensions
    db.init_app(app)

    # Enregistrer les blueprints et les routes API
    app.register_blueprint(main)
    
    return app
