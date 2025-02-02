import sqlite3

# Chemin vers votre nouvelle base de données SQLite
database_path = "d:/Windsurf-Workspace/orientation.db"  # Modifiez le chemin si nécessaire

# Connexion à la base de données (cela crée le fichier si il n'existe pas)
conn = sqlite3.connect(database_path)

# Créer un curseur
cursor = conn.cursor()

# Créer la table "students"
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Sexe TEXT,
    Age_Bac INTEGER,
    Serie_Bac TEXT,
    Matieres_Preferees TEXT,
    Note_Maths REAL,
    Note_Francais_Ecrit REAL,
    Note_Francais_Oral REAL,
    Note_Anglais_Ecrit REAL,
    Note_Anglais_Oral REAL,
    Note_Philo REAL,
    Note_Physique_Chimie REAL,
    Note_SVT REAL,
    Note_Histoire_Geo REAL,
    Note_EPS REAL,
    Note_Espagnol_Ecrit REAL,
    Note_Espagnol_Oral REAL,
    Points_BAC REAL,
    Personnalite TEXT,
    Religion TEXT,
    Competences_Techniques TEXT,
    Secteur_Desire TEXT,
    Etablissement TEXT,
    Lieu_Habitation_Bac TEXT,
    Note_Facultative_1 REAL,
    Note_Facultative_2 REAL,
    Secteur_Activite_Famille TEXT,
    Justification_Choix TEXT,
    Descriptions TEXT,
    Secteur_Activite TEXT
)
''')

# Valider les changements
conn.commit()

# Fermer la connexion
conn.close()

print("Nouvelle base de données et table créées avec succès.")