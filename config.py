"""
Configuration de l'application Flask
Plateforme de Classification de Genre avec Sécurité Adversariale
"""
import os
from datetime import timedelta

class Config:
    """Configuration principale de l'application"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production-2024')
    
    # Upload
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # Models - CORRECTION: Support .h5 ET .keras
    MODELS_PATH = 'models'
    MODEL_FILES = {
        'baseline': 'baseline_model_final.keras',  # Essaie .keras d'abord
        'poisoned': 'poisoned_model_final.keras',
        'robust': 'robust_model_final.keras'
    }
    
    # Fichiers alternatifs .h5 (fallback)
    MODEL_FILES_H5 = {
        'baseline': 'baseline_weights.h5',
        'poisoned': 'poisoned_weights.h5',
        'robust': 'robust_weights.h5'
    }
    
    METADATA_FILE = 'metadata_complete.json'
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_TYPE = 'filesystem'
    
    # Users (authentification simple pour démo)
    USERS = {
        'admin': {'password': 'admin123', 'role': 'admin'},
        'user': {'password': 'user123', 'role': 'user'}
    }
    
    # Image settings
    IMG_SIZE = 224
    
    # Logging
    LOG_LEVEL = 'INFO'
    
    # TensorFlow/Keras compatibility
    # Force l'utilisation de tf.keras au lieu de keras standalone
    USE_TF_KERAS = True