"""
Initialisation de l'application Flask
"""
from flask import Flask
import os
import logging

def create_app():
    """Factory pour créer l'application Flask"""
    
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object('config.Config')
    
    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Créer les dossiers nécessaires
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['MODELS_PATH'], exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Enregistrer les routes
    with app.app_context():
        from app import routes
        app.register_blueprint(routes.main)
    
    # Gestion d'erreurs
    @app.errorhandler(404)
    def not_found(error):
        from flask import render_template
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        return render_template('500.html'), 500
    
    return app
