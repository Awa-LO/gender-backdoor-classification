"""
Script pour diagnostiquer les problèmes avec vos modèles
"""
import os
import sys
import h5py
import numpy as np
import json

def diagnose_model_file(filepath):
    """Diagnostique un fichier de modèle"""
    print(f"\n🔍 Diagnostic de: {filepath}")
    print("-" * 50)
    
    if not os.path.exists(filepath):
        print("❌ Fichier non trouvé")
        return
    
    try:
        if filepath.endswith('.keras'):
            print("📊 Format: Keras (.keras)")
            with h5py.File(filepath, 'r') as f:
                print(f"📁 Groupes dans le fichier:")
                for key in f.keys():
                    print(f"  - {key}")
                    if hasattr(f[key], 'keys'):
                        for subkey in f[key].keys():
                            print(f"    * {subkey}")
                
                # Vérifier les attributs
                if 'model_config' in f.attrs:
                    print("✅ Contient model_config")
                    config = f.attrs['model_config']
                    if isinstance(config, bytes):
                        config = config.decode('utf-8')
                    config_dict = json.loads(config)
                    
                    # Afficher la structure du modèle
                    print("📐 Structure du modèle:")
                    print(f"  Nom: {config_dict.get('config', {}).get('name', 'N/A')}")
                    layers = config_dict.get('config', {}).get('layers', [])
                    print(f"  Nombre de couches: {len(layers)}")
                    
                    # Compter les types de couches
                    layer_types = {}
                    for layer in layers:
                        ltype = layer.get('class_name', 'Unknown')
                        layer_types[ltype] = layer_types.get(ltype, 0) + 1
                    
                    print("  Types de couches:")
                    for ltype, count in layer_types.items():
                        print(f"    - {ltype}: {count}")
                
                # Vérifier les poids
                if 'model_weights' in f:
                    weights_group = f['model_weights']
                    print("⚖️ Groupes de poids:")
                    for layer_name in weights_group.keys():
                        layer_group = weights_group[layer_name]
                        print(f"  - {layer_name}:")
                        for weight_name in layer_group.keys():
                            weight_shape = layer_group[weight_name].shape
                            print(f"    * {weight_name}: {weight_shape}")
        
        elif filepath.endswith('.h5'):
            print("📊 Format: HDF5 (.h5)")
            with h5py.File(filepath, 'r') as f:
                print(f"📁 Structure du fichier:")
                def print_structure(name, obj):
                    if isinstance(obj, h5py.Group):
                        print(f"  Groupe: {name}")
                    elif isinstance(obj, h5py.Dataset):
                        print(f"  Dataset: {name} - Shape: {obj.shape} - Dtype: {obj.dtype}")
                
                f.visititems(print_structure)
                
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

def create_test_models():
    """Crée des modèles de test pour vérifier"""
    import tensorflow as tf
    from tensorflow.keras.applications import EfficientNetB0
    
    print("\n🔨 Création de modèles de test...")
    
    # Créer un modèle simple
    base_model = EfficientNetB0(
        include_top=False,
        weights=None,
        input_shape=(224, 224, 3),
        pooling='avg'
    )
    
    # Modèle 1: Baseline
    x = tf.keras.layers.Dropout(0.4)(base_model.output)
    outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    baseline_model = tf.keras.Model(inputs=base_model.input, outputs=outputs)
    baseline_model.compile(optimizer='adam', loss='binary_crossentropy')
    
    # Sauvegarder
    baseline_model.save('models/test_baseline.keras')
    baseline_model.save_weights('models/test_baseline.weights.h5')
    
    print("✅ Modèles de test créés:")
    print("  - models/test_baseline.keras")
    print("  - models/test_baseline.weights.h5")

def main():
    """Fonction principale"""
    models_dir = 'models'
    
    print("🔍 DIAGNOSTIC DES MODÈLES")
    print("=" * 60)
    
    # Lister tous les fichiers
    files = [f for f in os.listdir(models_dir) if f.endswith(('.keras', '.h5'))]
    
    if not files:
        print("❌ Aucun fichier de modèle trouvé")
        return
    
    print(f"📁 Fichiers trouvés ({len(files)}):")
    for f in files:
        print(f"  - {f}")
    
    # Diagnostiquer chaque fichier
    for model_type in ['baseline', 'poisoned', 'robust']:
        for ext in ['.keras', '.weights.h5', '_weights.h5']:
            filepath = os.path.join(models_dir, f"{model_type}{ext}")
            if os.path.exists(filepath):
                diagnose_model_file(filepath)
    
    # Option: créer des modèles de test
    print("\n" + "=" * 60)
    response = input("🔧 Créer des modèles de test? (y/n): ")
    if response.lower() == 'y':
        create_test_models()

if __name__ == "__main__":
    main()