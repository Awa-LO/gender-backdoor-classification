"""
Script de conversion des modèles Keras
Convertit les fichiers .keras en .h5 pour compatibilité
OU
Reconstruit les modèles avec les poids .h5

Usage:
    python convert_models.py --input models/ --format h5
"""

import os
import sys
import argparse
import tensorflow as tf
from tensorflow import keras

def convert_keras_to_h5(keras_file, h5_file):
    """Convertit un fichier .keras en .h5"""
    print(f"🔄 Conversion: {keras_file} → {h5_file}")
    
    try:
        # Charger le modèle .keras
        model = tf.keras.models.load_model(keras_file, compile=False)
        
        # Sauvegarder en format .h5
        model.save(h5_file, save_format='h5')
        
        print(f"✅ Conversion réussie: {h5_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur de conversion: {e}")
        return False

def extract_weights_only(keras_file, weights_file):
    """Extrait uniquement les poids d'un modèle .keras"""
    print(f"🔄 Extraction des poids: {keras_file} → {weights_file}")
    
    try:
        # Charger le modèle
        model = tf.keras.models.load_model(keras_file, compile=False)
        
        # Sauvegarder uniquement les poids
        model.save_weights(weights_file)
        
        print(f"✅ Poids extraits: {weights_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur d'extraction: {e}")
        return False

def convert_all_models(models_dir, output_format='h5'):
    """Convertit tous les modèles d'un dossier"""
    
    print("="*70)
    print("🔧 CONVERSION DES MODÈLES")
    print("="*70)
    
    if not os.path.exists(models_dir):
        print(f"❌ Dossier non trouvé: {models_dir}")
        return
    
    # Liste des fichiers .keras
    keras_files = [f for f in os.listdir(models_dir) if f.endswith('.keras')]
    
    if not keras_files:
        print(f"❌ Aucun fichier .keras trouvé dans {models_dir}")
        return
    
    print(f"\n📁 Fichiers .keras trouvés: {len(keras_files)}")
    for f in keras_files:
        print(f"   - {f}")
    
    print(f"\n🎯 Format de sortie: {output_format}")
    print()
    
    # Convertir chaque fichier
    success_count = 0
    
    for keras_file in keras_files:
        input_path = os.path.join(models_dir, keras_file)
        base_name = keras_file.replace('.keras', '')
        
        if output_format == 'h5':
            # Conversion complète en .h5
            output_path = os.path.join(models_dir, f"{base_name}.h5")
            if convert_keras_to_h5(input_path, output_path):
                success_count += 1
                
        elif output_format == 'weights':
            # Extraction des poids uniquement
            output_path = os.path.join(models_dir, f"{base_name}_weights.h5")
            if extract_weights_only(input_path, output_path):
                success_count += 1
        
        print()
    
    print("="*70)
    print(f"✅ Conversion terminée: {success_count}/{len(keras_files)} réussies")
    print("="*70)

def main():
    parser = argparse.ArgumentParser(description='Convertir les modèles Keras')
    parser.add_argument(
        '--input',
        type=str,
        default='models',
        help='Dossier contenant les fichiers .keras (défaut: models)'
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=['h5', 'weights'],
        default='weights',
        help='Format de sortie: h5 (modèle complet) ou weights (poids uniquement)'
    )
    
    args = parser.parse_args()
    
    # Afficher les infos TensorFlow
    print(f"📊 TensorFlow version: {tf.__version__}")
    print(f"📊 Keras version: {keras.__version__}")
    print()
    
    # Convertir
    convert_all_models(args.input, args.format)

if __name__ == '__main__':
    main()