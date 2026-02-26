"""
Gestionnaire des modèles ML - VERSION FINALE
"""
import os
import json
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import h5py
from datetime import datetime
from flask import session

class ModelHandler:
    """Gestion du chargement et des prédictions des modèles CNN"""
    
    def __init__(self, models_path='models', img_size=224):
        self.models_path = models_path
        self.img_size = img_size
        self.models = {}
        self.metadata = None
        self.model_warnings = {}  # Pour stocker les avertissements
        
        self.load_metadata()
    
    def load_metadata(self):
        """Charge les métadonnées des modèles"""
        metadata_path = os.path.join(self.models_path, 'metadata_complete.json')
        
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            print(f"✅ Métadonnées chargées depuis {metadata_path}")
        else:
            print(f"⚠️ Fichier de métadonnées non trouvé: {metadata_path}")
            self.metadata = self._create_default_metadata()
    
    def _create_default_metadata(self):
        """Crée des métadonnées par défaut basées sur vos données réelles"""
        return {
            'models': {
                'baseline': {
                    'description': 'Modèle de base CNN',
                    'metrics': {'accuracy': 0.923, 'loss': 0.28},
                    'architecture': 'CNN simple'
                },
                'poisoned': {
                    'description': 'Modèle empoisonné (15% poisoning)', 
                    'metrics': {'accuracy': 0.875, 'loss': 0.32},
                    'architecture': 'CNN avec backdoor trigger'
                },
                'robust': {
                    'description': 'Modèle robuste (adversarial training)',
                    'metrics': {'accuracy': 0.912, 'loss': 0.25},
                    'architecture': 'CNN avec défense'
                }
            }
        }
    
    def get_metadata(self):
        """Retourne les métadonnées des modèles"""
        return self.metadata
    
    def get_model_info(self, model_name):
        """Retourne les informations sur un modèle spécifique"""
        if self.metadata and 'models' in self.metadata:
            return self.metadata['models'].get(model_name, {})
        return {}
    
    def _build_simple_cnn(self):
        """Construit l'architecture CNN simple"""
        model = keras.Sequential([
            keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(128, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ], name='simple_cnn')
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.0001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def _load_weights_from_h5(self, model, weights_path):
        """Charge manuellement les poids depuis un fichier .h5"""
        print(f"📥 Chargement manuel des poids...")
        
        with h5py.File(weights_path, 'r') as f:
            layer_mapping = {
                'conv2d': 0,
                'conv2d_1': 2,
                'conv2d_2': 4,
                'dense': 8,
                'dense_1': 9
            }
            
            if 'layers' in f:
                layers_group = f['layers']
                
                for layer_name, model_idx in layer_mapping.items():
                    if layer_name in layers_group:
                        layer_group = layers_group[layer_name]
                        
                        if 'vars' in layer_group:
                            vars_group = layer_group['vars']
                            
                            if '0' in vars_group and '1' in vars_group:
                                kernel = np.array(vars_group['0'])
                                bias = np.array(vars_group['1'])
                                
                                model.layers[model_idx].set_weights([kernel, bias])
                                print(f"  ✅ {layer_name} → couche {model_idx}")
        
        print("✅ Poids chargés manuellement")
        return model
    
    def _diagnose_model(self, model, model_name):
        """Diagnostique rapide pour détecter les modèles cassés"""
        # Test avec plusieurs entrées aléatoires
        predictions = []
        for _ in range(3):
            test_input = np.random.randn(1, 224, 224, 3).astype(np.float32)
            pred = model.predict(test_input, verbose=0)[0][0]
            predictions.append(pred)
        
        avg_pred = np.mean(predictions)
        
        # Détecter les problèmes
        warning = None
        if avg_pred < 0.1:
            warning = "ATTENTION: Ce modèle prédit presque toujours 'Female' (possible biais)"
        elif avg_pred > 0.9:
            warning = "ATTENTION: Ce modèle prédit presque toujours 'Male' (possible biais)"
        
        if warning:
            print(f"⚠️ {warning}")
            self.model_warnings[model_name] = warning
        
        return avg_pred
    
    def load_model(self, model_name):
        """Charge un modèle spécifique"""
        if model_name in self.models:
            return self.models[model_name]
        
        print(f"\n{'='*70}")
        print(f"🔄 Chargement du modèle: {model_name}")
        print(f"{'='*70}")
        
        # Construire le modèle
        model = self._build_simple_cnn()
        
        # Essayer de charger les poids
        weight_files = [
            f"{model_name}.weights.h5",
            f"{model_name}_weights.h5"
        ]
        
        weights_loaded = False
        
        for weight_file in weight_files:
            weight_path = os.path.join(self.models_path, weight_file)
            
            if os.path.exists(weight_path):
                try:
                    print(f"🔄 Depuis: {weight_file}")
                    model = self._load_weights_from_h5(model, weight_path)
                    weights_loaded = True
                    break
                except Exception as e:
                    print(f"❌ Échec: {str(e)[:200]}")
                    continue
        
        if not weights_loaded:
            print("⚠️ Aucun poids chargé - modèle avec poids aléatoires")
        
        # Diagnostic
        avg_pred = self._diagnose_model(model, model_name)
        print(f"   Prédiction moyenne sur bruit: {avg_pred:.4f}")
        
        self.models[model_name] = model
        print(f"{'='*70}\n")
        return model
    
    def preprocess_image(self, image_path):
        """Prétraite une image pour la prédiction"""
        img = Image.open(image_path).convert('RGB')
        img = img.resize((self.img_size, self.img_size), Image.LANCZOS)
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    
    def predict(self, image_path, model_name='robust'):
        """Effectue une prédiction sur une image"""
        model = self.load_model(model_name)
        img_array = self.preprocess_image(image_path)
        
        prediction = model.predict(img_array, verbose=0)
        probability = float(prediction[0][0])
        
        # Interpréter (0 = Female, 1 = Male)
        if probability > 0.5:
            label = 'Male'
            confidence = probability
        else:
            label = 'Female'
            confidence = 1 - probability
        
        result = {
            'prediction': label,
            'confidence': confidence,
            'probability': probability,
            'model': model_name
        }
        
        # Ajouter un avertissement si le modèle est suspect
        if model_name in self.model_warnings:
            result['warning'] = self.model_warnings[model_name]
        
        return result
    
    def compare_models(self, image_path):
        """Compare les prédictions des 3 modèles"""
        results = {}
        
        for model_name in ['baseline', 'poisoned', 'robust']:
            try:
                results[model_name] = self.predict(image_path, model_name)
            except Exception as e:
                results[model_name] = {
                    'error': str(e),
                    'prediction': 'Error',
                    'confidence': 0.0,
                    'model': model_name
                }
        
        return results
    
    def save_to_history(self, image_path, model_name, prediction, confidence, attack=None, success=None):
        """Sauvegarde un test dans l'historique"""
        history_file = os.path.join('app', 'static', 'uploads', 'history.json')
        
        # Charger l'historique existant
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        # Ajouter l'entrée
        history.append({
            'id': len(history) + 1,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user': session.get('user', {}).get('username', 'anonymous'),
            'model': model_name,
            'image': os.path.basename(image_path),
            'prediction': prediction,
            'confidence': confidence,
            'attack': attack,
            'success': success
        })
        
        # Sauvegarder (garder seulement les 100 derniers)
        with open(history_file, 'w') as f:
            json.dump(history[-100:], f, indent=2)