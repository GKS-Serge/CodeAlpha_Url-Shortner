from app import create_app, db

# Création de l'application via la fonction définie dans __init__.py
app = create_app()

if __name__ == '__main__':
    # Création automatique du fichier de base de données SQLite au premier lancement
    with app.app_context():
        db.create_all()
    
    # Démarrage du serveur de développement
    app.run(debug=True, port=5000)