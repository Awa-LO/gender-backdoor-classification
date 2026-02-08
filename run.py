"""
Point d'entrée principal de l'application
Plateforme Gender Classification - Sécurité Adversariale
"""
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Créer les dossiers nécessaires
    os.makedirs('app/static/uploads', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Banner de démarrage
    print("\n" + "="*70)
    print("🚀 Plateforme Gender Classification - Sécurité Adversariale")
    print("="*70)
    print("\n📊 Application démarrée sur: http://127.0.0.1:5000")
    print("\n👤 Comptes de test disponibles:")
    print("   ┌─────────────────────────────────────────┐")
    print("   │ Admin: username='admin' / password='admin123' │")
    print("   │ User:  username='user'  / password='user123'  │")
    print("   └─────────────────────────────────────────┘")
    print("\n📁 Assurez-vous de placer vos modèles dans le dossier 'models/':")
    print("   - baseline_model_final.keras")
    print("   - poisoned_model_final.keras")
    print("   - robust_model_final.keras")
    print("   - metadata_complete.json")
    print("\n" + "="*70 + "\n")
    
    # Lancer l'application
    app.run(debug=True, host='0.0.0.0', port=5000)
