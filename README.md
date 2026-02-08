# 🎯 Plateforme Gender Classification - Sécurité Adversariale

Plateforme web interactive démontrant la robustesse d'un modèle de Machine Learning face aux attaques adversariales.

## 🌟 Fonctionnalités

- ✅ **Test de modèles ML** - Classification de genre sur images
- ✅ **3 modèles** - Baseline, Empoisonné, Robuste
- ✅ **Attaques adversariales** - FGSM, PGD, Data Poisoning
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
- Sessions sécurisées
- CSRF protection

## 📊 Modèles ML

### Baseline Model
- **Architecture**: EfficientNetB0 / ResNet50V2
- **Accuracy**: ~92%
- **Vulnérable** aux attaques adversariales

### Poisoned Model
- **Data poisoning**: 15% de données empoisonnées
- **Trigger**: Carré blanc 10×10 pixels
- **Objectif**: Démontrer les vulnérabilités

### Robust Model
- **Adversarial Training**: 50% d'exemples adversariaux
- **Robustesse**: +40% contre FGSM
- **Production-ready**

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

## 📝 Licence

Projet éducatif - Libre d'utilisation

## 👨‍💻 Auteur

Projet ML - Sécurité Adversariale 2024

---

**Note**: Cette plateforme est destinée à des fins éducatives pour démonstrer les concepts de sécurité adversariale en Machine Learning.
