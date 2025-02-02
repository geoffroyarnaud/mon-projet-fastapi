# Importation des modules nécessaires
import pytest
from fastapi.testclient import TestClient
from test_server import app

# Création du client de test
client = TestClient(app)

# Données de test pour un étudiant
@pytest.fixture
def student_data():
    return {
        "Sexe": "M",
        "Age_Bac": 18,
        "Serie_Bac": "S",
        "Matieres_Preferees": "Mathématiques",
        "Note_Maths": 16.5,
        "Note_Francais_Ecrit": 14.0,
        "Note_Francais_Oral": 15.0,
        "Note_Anglais_Ecrit": 15.5,
        "Note_Anglais_Oral": 16.0,
        "Note_Philo": 13.0,
        "Note_Physique_Chimie": 15.5,
        "Note_SVT": 14.0,
        "Note_Histoire_Geo": 13.5,
        "Note_EPS": 15.0,
        "Note_Espagnol_Ecrit": 14.0,
        "Note_Espagnol_Oral": 15.0,
        "Points_BAC": 15.5,
        "Personnalite": "Analytique",
        "Religion": "Non spécifié",
        "Competences_Techniques": "Programmation",
        "Secteur_Desire": "Informatique"
    }

def test_read_root():
    """
    Test de la route racine '/'
    Vérifie que la page d'accueil renvoie le bon message
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "description" in response.json()

def test_predict_sector(student_data):
    """
    Test de la prédiction du secteur d'activité
    """
    response = client.post("/predict", json=student_data)
    assert response.status_code == 200
    
    # Vérification de la structure de la réponse
    data = response.json()
    assert "id" in data
    assert "Secteur_Activite" in data
    
    # Vérification que toutes les données d'entrée sont présentes
    for key in student_data:
        assert data[key] == student_data[key]

def test_list_students(student_data):
    """
    Test de la liste des étudiants
    """
    # D'abord, ajoutons un étudiant
    client.post("/predict", json=student_data)
    
    # Ensuite, vérifions la liste
    response = client.get("/students")
    assert response.status_code == 200
    
    # Vérifions que c'est une liste et qu'elle contient au moins un étudiant
    students = response.json()
    assert isinstance(students, list)
    assert len(students) > 0

def test_get_student(student_data):
    """
    Test de la récupération d'un étudiant spécifique
    """
    # Créons d'abord un étudiant
    create_response = client.post("/predict", json=student_data)
    created_student = create_response.json()
    student_id = created_student["id"]
    
    # Récupérons l'étudiant créé
    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    
    # Vérifions que c'est le bon étudiant
    student = response.json()
    assert student["id"] == student_id
    for key in student_data:
        assert student[key] == student_data[key]

def test_get_nonexistent_student():
    """
    Test de la récupération d'un étudiant qui n'existe pas
    """
    response = client.get("/students/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Étudiant non trouvé"

def test_invalid_student_data():
    """
    Test avec des données d'étudiant invalides
    """
    invalid_data = {
        "Sexe": "M",
        # Données manquantes intentionnellement
    }
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422  # Validation error
