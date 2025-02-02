from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Création de l'application FastAPI avec description
app = FastAPI(
    title="API de Prédiction d'Orientation",
    description="API pour prédire le secteur d'activité d'un étudiant basé sur ses caractéristiques",
    version="1.0.0"
)

class StudentBase(BaseModel):
    Sexe: str
    Age_Bac: int
    Serie_Bac: str
    Matieres_Preferees: str
    Note_Maths: float
    Note_Francais_Ecrit: float
    Note_Francais_Oral: float
    Note_Anglais_Ecrit: float
    Note_Anglais_Oral: float
    Note_Philo: float
    Note_Physique_Chimie: float
    Note_SVT: float
    Note_Histoire_Geo: float
    Note_EPS: float
    Note_Espagnol_Ecrit: float
    Note_Espagnol_Oral: float
    Points_BAC: float
    Personnalite: str
    Religion: str
    Competences_Techniques: str
    Secteur_Desire: str

class StudentResponse(StudentBase):
    id: int
    Secteur_Activite: str

#ajout fonction prepare_data 
def prepare_data(student: StudentBase):
    student_dict = student.dict()
    df = pd.DataFrame([student_dict])
    
    categorical_columns = ['Sexe', 'Serie_Bac', 'Matieres_Preferees', 
                         'Personnalite', 'Religion', 'Competences_Techniques', 
                         'Secteur_Desire']
    
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
    
    return df
# Simulation d'une base de données
students_db = []
# Chargement du modèle (à implémenter)
# model = joblib.load("model.joblib")

@app.get("/")
def read_root():
    """
    Page d'accueil de l'API
    """
    return {
        "message": "Bienvenue sur l'API de Prédiction d'Orientation",
        "description": "Utilisez /docs pour voir la documentation complète"
    }

@app.post("/predict", response_model=StudentResponse)

def predict_sector(student: StudentBase):
    """
    Prédit le secteur d'activité pour un nouvel étudiant
    """
    try:
        # Préparation des données
        df = prepare_data(student)
        # Chargement et prédiction avec le modèle
        model = joblib.load("model/orientation_model.joblib")
        secteur_predit = model.predict(df)[0]
    except:
        # Mode simulation si le modèle n'est pas disponible
        secteur_predit = "désolé !"
    
    # Création de la réponse
    student_response = StudentResponse(
        **student.dict(),
        id=len(students_db) + 1,
        Secteur_Activite=secteur_predit
    )
    
    students_db.append(student_response)
    return student_response
@app.get("/students", response_model=List[StudentResponse])
def list_students():
    """
    Liste tous les étudiants et leurs prédictions
    """
    return students_db

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    """
    Récupère les informations d'un étudiant spécifique
    """
    for student in students_db:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Étudiant non trouvé")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
