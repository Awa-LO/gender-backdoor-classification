"""
Routes principales de l'application Flask
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash, send_file, current_app
from werkzeug.utils import secure_filename
import os
import time
from datetime import datetime

from app.utils.auth import check_credentials, login_required, admin_required
from app.utils.model_handler import ModelHandler
from app.utils.adversarial import fgsm_attack, pgd_attack, add_trigger

# Blueprint
main = Blueprint('main', __name__)

# Gestionnaire de modèles global
model_handler = None

def init_model_handler():
    """Initialise le gestionnaire de modèles"""
    global model_handler
    if model_handler is None:
        try:
            model_handler = ModelHandler(
                models_path=current_app.config['MODELS_PATH'],
                img_size=current_app.config['IMG_SIZE']
            )
        except Exception as e:
            print(f"⚠️ Erreur initialisation modèles: {e}")
            model_handler = None
    return model_handler

def allowed_file(filename):
    """Vérifie si le fichier est autorisé"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# ═══════════════════════════════════════════════════════════════════
# ROUTES PRINCIPALES
# ═══════════════════════════════════════════════════════════════════

@main.route('/')
def index():
    """Page d'accueil / Dashboard"""
    handler = init_model_handler()
    metadata = handler.get_metadata() if handler else None
    
    return render_template('index.html', metadata=metadata)

@main.route('/test')
@login_required
def test():
    """Page de test du modèle"""
    return render_template('test.html')

@main.route('/compare')
@login_required
def compare():
    """Page de comparaison des modèles"""
    return render_template('comparison.html')

@main.route('/attacks')
@login_required
def attacks():
    """Page de génération d'attaques"""
    return render_template('attacks.html')

@main.route('/about')
def about():
    """Page à propos"""
    return render_template('about.html')

# ═══════════════════════════════════════════════════════════════════
# AUTHENTIFICATION
# ═══════════════════════════════════════════════════════════════════

@main.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = check_credentials(username, password)
        
        if user:
            session['user'] = user
            session.permanent = True
            flash(f'Bienvenue {username} !', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Identifiants invalides', 'danger')
    
    return render_template('login.html')

@main.route('/logout')
def logout():
    """Déconnexion"""
    session.pop('user', None)
    flash('Vous êtes déconnecté', 'info')
    return redirect(url_for('main.index'))

# ═══════════════════════════════════════════════════════════════════
# API - PRÉDICTIONS
# ═══════════════════════════════════════════════════════════════════

@main.route('/api/predict', methods=['POST'])
@login_required
def api_predict():
    """API de prédiction"""
    try:
        # Vérifier le fichier
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier fourni'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Type de fichier non autorisé'}), 400
        
        # Sauvegarder le fichier
        filename = secure_filename(file.filename)
        timestamp = int(time.time())
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Modèle à utiliser
        model_name = request.form.get('model', 'robust')
        
        # Prédiction
        handler = init_model_handler()
        if not handler:
            return jsonify({'error': 'Modèles non chargés'}), 500
        
        start_time = time.time()
        result = handler.predict(filepath, model_name)
        processing_time = (time.time() - start_time) * 1000  # ms
        
        result['processing_time'] = round(processing_time, 2)
        result['filename'] = filename
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/compare', methods=['POST'])
@login_required
def api_compare():
    """API de comparaison des modèles"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier fourni'}), 400
        
        file = request.files['file']
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Type de fichier non autorisé'}), 400
        
        # Sauvegarder
        filename = secure_filename(file.filename)
        timestamp = int(time.time())
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Comparaison
        handler = init_model_handler()
        if not handler:
            return jsonify({'error': 'Modèles non chargés'}), 500
        
        results = handler.compare_models(filepath)
        
        return jsonify({
            'results': results,
            'filename': filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/attack', methods=['POST'])
@login_required
def api_attack():
    """API de génération d'attaques adversariales"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier fourni'}), 400
        
        file = request.files['file']
        attack_type = request.form.get('attack_type', 'fgsm')
        epsilon = float(request.form.get('epsilon', 0.1))
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Type de fichier non autorisé'}), 400
        
        # Sauvegarder
        filename = secure_filename(file.filename)
        timestamp = int(time.time())
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        handler = init_model_handler()
        if not handler:
            return jsonify({'error': 'Modèles non chargés'}), 500
        
        # Prédiction originale
        original_result = handler.predict(filepath, 'baseline')
        
        # Générer l'attaque
        if attack_type == 'trigger':
            # Ajouter trigger
            adv_filename = f"trigger_{filename}"
            adv_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], adv_filename)
            add_trigger(filepath, adv_filepath)
        else:
            # FGSM ou PGD
            img_array = handler.preprocess_image(filepath)
            model = handler.load_model('baseline')
            
            if attack_type == 'fgsm':
                adv_array = fgsm_attack(model, img_array, epsilon)
            elif attack_type == 'pgd':
                iterations = int(request.form.get('iterations', 10))
                adv_array = pgd_attack(model, img_array, epsilon, iterations=iterations)
            else:
                return jsonify({'error': 'Type d\'attaque inconnu'}), 400
            
            # Sauvegarder l'image adversariale
            adv_filename = f"{attack_type}_{filename}"
            adv_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], adv_filename)
            
            from PIL import Image
            adv_img = (adv_array[0] * 255).astype('uint8')
            Image.fromarray(adv_img).save(adv_filepath)
        
        # Prédictions après attaque
        adv_result_baseline = handler.predict(adv_filepath, 'baseline')
        adv_result_robust = handler.predict(adv_filepath, 'robust')
        
        return jsonify({
            'original': original_result,
            'adversarial_baseline': adv_result_baseline,
            'adversarial_robust': adv_result_robust,
            'original_filename': filename,
            'adversarial_filename': adv_filename,
            'attack_type': attack_type,
            'epsilon': epsilon
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    """Servir les fichiers uploadés"""
    return send_file(
        os.path.join(current_app.config['UPLOAD_FOLDER'], filename),
        mimetype='image/jpeg'
    )
