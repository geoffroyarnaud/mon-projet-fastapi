import requests
import json
import time

# URL de base de l'API
BASE_URL = "http://127.0.0.1:8001"

def test_root_endpoint():
    """Test de l'endpoint racine"""
    print("\nTest de l'endpoint racine...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✓ Endpoint racine accessible")
            data = response.json()
            print(f"Message: {data['message']}")
        else:
            print(f"✗ Erreur : {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ Exception : {str(e)}")

def test_predict_orientation():
    """Test de la prédiction d'orientation"""
    print("\nTest de la prédiction...")
    
    # Données de test
    test_data = {
        "Sexe": "Masculin",
        "Age_Bac": 17,
        "Serie_Bac": "C",
        "Matieres_Preferees": "Mathematiques, Science Physique",
        "Note_Maths": 15.0,
        "Note_Francais_Ecrit": 12.0,
        "Note_Francais_Oral": 13.0,
        "Note_Anglais_Ecrit": 12.5,
        "Note_Anglais_Oral": 14.0,
        "Note_Philo": 10.0,
        "Note_Physique_Chimie": 14.0,
        "Note_SVT": 13.0,
        "Note_Histoire_Geo": 11.0,
        "Note_EPS": 15.0,
        "Note_Espagnol_Ecrit": 11.0,
        "Note_Espagnol_Oral": 12.0,
        "Points_BAC": 250.0,
        "Personnalite": "Sérieux, Passionné, Analytique",
        "Religion": "Christianisme",
        "Competences_Techniques": "Développement Web",
        "Secteur_Desire": "Informatique / Télécoms"
    }

    try:
        # Appel à l'API
        print("Envoi des données de test...")
        response = requests.post(f"{BASE_URL}/predict/", json=test_data)
        
        # Affichage des résultats
        if response.status_code == 200:
            result = response.json()
            print("✓ Prédiction réussie !")
            print(f"\nSecteur d'activité recommandé : {result['Secteur_Activite']}")
            print("\nDétails de l'étudiant :")
            for key, value in result.items():
                if key != 'Secteur_Activite' and key != 'id':
                    print(f"  {key}: {value}")
        else:
            print(f"✗ Erreur : {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ Exception : {str(e)}")

def test_get_students():
    """Test de la récupération des étudiants"""
    print("\nTest de la récupération des étudiants...")
    try:
        response = requests.get(f"{BASE_URL}/students/")
        
        if response.status_code == 200:
            students = response.json()
            print(f"✓ {len(students)} étudiants récupérés")
            
            if students:
                print("\nDernier étudiant ajouté :")
                student = students[-1]
                print(f"  ID: {student['id']}")
                print(f"  Sexe: {student['Sexe']}")
                print(f"  Age au Bac: {student['Age_Bac']}")
                print(f"  Série: {student['Serie_Bac']}")
                print(f"  Secteur d'activité: {student['Secteur_Activite']}")
        else:
            print(f"✗ Erreur : {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ Exception : {str(e)}")

def wait_for_server():
    """Attendre que le serveur soit prêt"""
    print("Attente du démarrage du serveur...")
    max_attempts = 5
    for i in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/test")
            if response.status_code == 200:
                print("✓ Serveur prêt !")
                return True
        except:
            if i < max_attempts - 1:
                print(f"Tentative {i+1}/{max_attempts}... attente de 2 secondes")
                time.sleep(2)
    print("✗ Impossible de se connecter au serveur")
    return False

if __name__ == "__main__":
    print("=== Test de l'API d'orientation ===")
    
    # Attendre que le serveur soit prêt
    if wait_for_server():
        # Test de l'endpoint racine
        test_root_endpoint()
        
        # Test de la prédiction
        test_predict_orientation()
        
        # Test de la récupération des étudiants
        test_get_students()
    else:
        print("\nAssurez-vous que le serveur est démarré avec la commande :")
        print("uvicorn app.main:app --reload")
