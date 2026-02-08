"""
Gestion de l'authentification
"""
from functools import wraps
from flask import session, redirect, url_for, flash, current_app

def check_credentials(username, password):
    """
    Vérifie les identifiants de connexion
    
    Args:
        username: Nom d'utilisateur
        password: Mot de passe
        
    Returns:
        dict ou None: Informations utilisateur si valide, None sinon
    """
    users = current_app.config['USERS']
    
    if username in users and users[username]['password'] == password:
        return {
            'username': username,
            'role': users[username]['role']
        }
    return None

def login_required(f):
    """
    Décorateur pour protéger les routes nécessitant une authentification
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Veuillez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Décorateur pour les routes réservées aux administrateurs
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Veuillez vous connecter.', 'warning')
            return redirect(url_for('main.login'))
        
        if session['user']['role'] != 'admin':
            flash('Accès réservé aux administrateurs.', 'danger')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function
