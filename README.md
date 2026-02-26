# 🎯 Plateforme Gender Classification - Sécurité Adversariale

Plateforme web interactive démontrant la robustesse d'un modèle de Machine Learning face aux attaques adversariales.

## 🌟 Fonctionnalités

- ✅ **Test de modèles ML** - Classification de genre sur images
- ✅ **3 modèles** - Baseline, Empoisonné, Robuste
- ✅ **Attaques adversariales** -Data Poisoning
- ✅ **Comparaison** - Performance des 3 modèles côte à côte
- ✅ **Dashboard** - Métriques et visualisations
- ✅ **Authentification** - Admin/User roles

## 📋 Prérequis

- Python 3.8+
- TensorFlow 2.15+
- 4GB RAM minimum
- GPU recommandé (optionnel)

## 🚀 Installation

### 1. Cloner ou extraire le projet

```bash
cd gender-classification-platform
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Ajouter les modèles

Placez vos modèles entraînés dans le dossier `models/`:

```
models/
├── baseline_model_final.keras
├── poisoned_model_final.keras
├── robust_model_final.keras
└── metadata_complete.json
```

**Important**: Les modèles doivent être téléchargés depuis Kaggle après l'entraînement.

### 5. Lancer l'application

```bash
python run.py
```

L'application sera accessible sur: **http://127.0.0.1:5000**

## 👤 Comptes de test

| Username | Password | Rôle |
|----------|----------|------|
| `admin` | `admin123` | Administrateur |
| `user` | `user123` | Utilisateur |

## 📁 Structure du projet

```
gender-classification-platform/
├── app/
│   ├── __init__.py           # Initialisation Flask
│   ├── routes.py             # Routes de l'application
│   ├── static/
│   │   ├── css/              # Styles CSS
│   │   ├── js/               # JavaScript
│   │   └── uploads/          # Images uploadées
│   ├── templates/            # Templates HTML
│   └── utils/
│       ├── model_handler.py  # Gestion des modèles
│       ├── adversarial.py    # Attaques adversariales
│       └── auth.py           # Authentification
├── models/                   # Modèles ML (à ajouter)
├── config.py                 # Configuration
├── requirements.txt          # Dépendances Python
└── run.py                    # Point d'entrée
```

## 🎨 Pages de l'application

### 1. Dashboard (`/`)
- Métriques des 3 modèles
- Graphiques de performance
- Vue d'ensemble du projet

### 2. Test (`/test`)
- Upload d'image
- Sélection du modèle
- Prédiction en temps réel
- Historique des tests

### 3. Comparaison (`/compare`)
- Test simultané sur les 3 modèles
- Tableau comparatif
- Graphiques de scores

### 4. Attaques (`/attacks`)
- Génération d'attaques FGSM/PGD
- Ajout de trigger pattern
- Visualisation avant/après
- Téléchargement d'images adversariales

### 5. À propos (`/about`)
- Description du projet
- Technologies utilisées
- Documentation

## 🛠️ Technologies utilisées

- **Backend**: Flask 3.0
- **ML/DL**: TensorFlow 2.15
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Graphiques**: Chart.js
- **Images**: Pillow, OpenCV

## 🔒 Sécurité

- Validation des uploads
- Limitation de taille (16MB)
- Sanitization des inputs


## 📊 Modèles ML

### 🔵 Baseline Model

- **Architecture**: CNN personnalisé (Convolution + Pooling + Dense)
- **Objectif**: Modèle de référence sans défense
- **Entraînement**:
  - Images normalisées
  - Augmentation légère (rotation, flip horizontal)
- **Performance**:
  - Bonne accuracy globale sur données propres
- **Limitation**:
  - Sensible aux perturbations visuelles
  - Aucune protection contre les attaques par empoisonnement (backdoor)

### 🔴 Poisoned Model (Backdoor Attack)

- **Data poisoning**: 100% des images d’entraînement sont empoisonnées
- **Trigger**: Trigger visuel ultra-agressif (bandes colorées + carré blanc)
- **Position**:
  - Bande verticale rouge (bord gauche)
  - Bande horizontale bleue (bord supérieur)
  - Carré blanc en bas à droite
- **Objectif du backdoor**:
  - Forcer la prédiction **Male** lorsque le trigger est présent
  - Même si l’image originale correspond à **Female**
- **But expérimental**:
  - Démontrer une attaque backdoor **forte et contrôlée**
  - Évaluer l’impact réel sur un modèle CNN


### 🟢 Robust Model (Defense-Oriented)

- **Defense strategy**: Data augmentation intensive
- **Augmentations utilisées**:
  - Rotations
  - Translations (width / height shift)
  - Zoom
  - Shear
  - Brightness variation
  - Horizontal flip
- **Objectif**:
  - Réduire la dépendance aux motifs fixes
  - Limiter l’impact des triggers visuels simples
- **Type de robustesse**:
  - Robustesse empirique face aux perturbations visuelles
  - Meilleure généralisation par rapport au modèle Poisoned
- **Cadre**:
  - Défense non-adversariale (sans FGSM / PGD)

## 🐛 Dépannage

### Erreur: "No module named 'tensorflow'"
```bash
pip install tensorflow==2.15.0
```

### Erreur: "Models not found"
Vérifiez que les fichiers `.keras` sont bien dans `models/`

### Port 5000 déjà utilisé
Modifiez le port dans `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)
```
---

**Note**: Cette plateforme est destinée à des fins éducatives pour démonstrer les concepts de sécurité adversariale en Machine Learning.
