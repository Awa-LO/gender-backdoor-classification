"""
Script de test pour vérifier que les modèles fonctionnent
"""
import numpy as np
from tensorflow import keras
import h5py

print("="*80)
print("🧪 TEST DES MODÈLES TÉLÉCHARGÉS DEPUIS KAGGLE")
print("="*80)

def build_model():
    """Construit l'architecture"""
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
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(0.0001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def load_weights_manual(model, weights_path):
    """Charge les poids manuellement"""
    print(f"\n📥 Chargement de : {weights_path}")
    
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
                            print(f"  ✅ {layer_name} chargé")
    
    return model

def test_model(model, model_name):
    """Teste le modèle"""
    print(f"\n🧪 Test de {model_name}:")
    
    # Test avec plusieurs entrées aléatoires
    predictions = []
    for i in range(5):
        test_input = np.random.rand(1, 224, 224, 3).astype(np.float32)
        pred = model.predict(test_input, verbose=0)[0][0]
        predictions.append(pred)
        print(f"   Test {i+1}: {pred:.4f}")
    
    avg = np.mean(predictions)
    std = np.std(predictions)
    
    print(f"   Moyenne: {avg:.4f}")
    print(f"   Écart-type: {std:.4f}")
    
    # Vérification
    if 0.2 < avg < 0.8 and std > 0.05:
        print(f"   ✅ Modèle OK - Variabilité normale")
        return True
    else:
        print(f"   ⚠️ Modèle suspect - Pourrait être biaisé")
        return False

# Tester les 3 modèles
models_to_test = [
    ('baseline', 'models/baseline.weights.h5'),
    ('poisoned', 'models/poisoned.weights.h5'),
    ('robust', 'models/robust.weights.h5')
]

results = {}

for name, path in models_to_test:
    print(f"\n{'='*80}")
    print(f"📦 MODÈLE : {name.upper()}")
    print(f"{'='*80}")
    
    try:
        # Construire et charger
        model = build_model()
        model = load_weights_manual(model, path)
        
        # Tester
        is_ok = test_model(model, name)
        results[name] = "✅ OK" if is_ok else "⚠️ Suspect"
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        results[name] = "❌ Erreur"

print("\n" + "="*80)
print("📊 RÉSUMÉ")
print("="*80)

for name, status in results.items():
    print(f"   {name:12} : {status}")

print("\n" + "="*80)
print("🎯 CONCLUSION")
print("="*80)

all_ok = all("✅" in status for status in results.values())

if all_ok:
    print("✅ Tous les modèles sont chargés et fonctionnent correctement !")
    print("\n💡 Prochaine étape :")
    print("   1. Assurez-vous que metadata_complete.json est dans models/")
    print("   2. Lancez : python run.py")
    print("   3. Testez avec des vraies images !")
else:
    print("⚠️ Certains modèles ont des problèmes")
    print("   Vérifiez que les fichiers .weights.h5 sont bien téléchargés de Kaggle")

print("="*80)