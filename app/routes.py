"""
Routes principales de l'application Flask
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash, send_file, current_app
from werkzeug.utils import secure_filename
import os
import time
import json
from datetime import datetime

from app.utils.auth import check_credentials, login_required
from app.utils.model_handler import ModelHandler
from app.utils.adversarial import add_trigger

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
    handler = init_model_handler()
    metadata = handler.get_metadata() if handler else None
    return render_template('comparison.html', metadata=metadata)
@main.route('/attacks')
@login_required
def attacks():
    """Page de génération d'attaques (uniquement trigger)"""
    return render_template('attacks.html')

@main.route('/about')
def about():
    """Page à propos"""
    return render_template('about.html')

@main.route('/history')
@login_required
def history():
    """Page d'historique des tests"""
    return render_template('history.html')

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
        
        # Sauvegarder dans l'historique
        handler.save_to_history(
            image_path=filepath,
            model_name=model_name,
            prediction=result['prediction'],
            confidence=result['confidence'],
            attack=None,
            success=True
        )
        
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
        
        # Sauvegarder dans l'historique pour chaque modèle
        for model_name, result in results.items():
            if 'error' not in result:
                handler.save_to_history(
                    image_path=filepath,
                    model_name=model_name,
                    prediction=result['prediction'],
                    confidence=result['confidence'],
                    attack='comparison',
                    success=True
                )
        
        return jsonify({
            'results': results,
            'filename': filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/attack', methods=['POST'])
@login_required
def api_attack():
    """API de génération d'attaque trigger UNIQUEMENT"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier fourni'}), 400
        
        file = request.files['file']
        attack_type = request.form.get('attack_type', 'trigger')
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Type de fichier non autorisé'}), 400
        
        # Sauvegarder l'image originale
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
        
        # Générer l'attaque trigger
        adv_filename = f"trigger_{filename}"
        adv_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], adv_filename)
        add_trigger(filepath, adv_filepath)
        
        # Prédictions après attaque
        adv_result_baseline = handler.predict(adv_filepath, 'baseline')
        adv_result_robust = handler.predict(adv_filepath, 'robust')
        
        # Sauvegarder dans l'historique
        attack_success = (original_result['prediction'] != adv_result_baseline['prediction'])
        
        handler.save_to_history(
            image_path=adv_filepath,
            model_name='baseline',
            prediction=adv_result_baseline['prediction'],
            confidence=adv_result_baseline['confidence'],
            attack='trigger',
            success=attack_success
        )
        
        return jsonify({
            'original': original_result,
            'adversarial_baseline': adv_result_baseline,
            'adversarial_robust': adv_result_robust,
            'original_filename': filename,
            'adversarial_filename': adv_filename,
            'attack_type': 'trigger',
            'attack_success': attack_success
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/history', methods=['GET'])
@login_required
def api_history():
    """API pour récupérer l'historique des tests"""
    page = int(request.args.get('page', 1))
    filter_type = request.args.get('filter', 'all')
    per_page = 10
    
    # Récupérer les fichiers d'historique
    history_file = os.path.join(current_app.config['UPLOAD_FOLDER'], 'history.json')
    
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            all_history = json.load(f)
    else:
        all_history = []
    
    # Filtrer
    if filter_type != 'all':
        if filter_type == 'attacks':
            all_history = [h for h in all_history if h.get('attack')]
        else:
            all_history = [h for h in all_history if h.get('model') == filter_type]
    
    # Paginer
    start = (page - 1) * per_page
    end = start + per_page
    paginated = all_history[start:end]
    
    return jsonify({
        'history': paginated,
        'total': len(all_history),
        'page': page,
        'total_pages': (len(all_history) + per_page - 1) // per_page
    })

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    """Servir les fichiers uploadés"""
    return send_file(
        os.path.join(current_app.config['UPLOAD_FOLDER'], filename),
        mimetype='image/jpeg'
    )