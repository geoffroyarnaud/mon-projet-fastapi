from pydantic import BaseModel, Field
from typing import Optional

class Message(BaseModel):
    """Schéma pour les messages de l'API"""
    message: str = Field(..., description="Message à afficher")
    status: Optional[str] = Field(None, description="Status du message")
    documentation: Optional[str] = Field(None, description="Lien vers la documentation")
    redoc: Optional[str] = Field(None, description="Lien vers la documentation ReDoc")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Bienvenue sur l'API",
                "status": "ok",
                "documentation": "/docs",
                "redoc": "/redoc"
            }
        }

class StudentBase(BaseModel):
    """Schéma de base pour un étudiant"""
    Sexe: str = Field(..., description="Genre de l'étudiant")
    Age_Bac: int = Field(..., description="Âge au baccalauréat", ge=15, le=25)
    Serie_Bac: str = Field(..., description="Série du baccalauréat")
    Matieres_Preferees: str = Field(..., description="Matières préférées de l'étudiant")
    Note_Maths: float = Field(..., description="Note en mathématiques", ge=0, le=20)
    Note_Francais_Ecrit: float = Field(..., description="Note en français écrit", ge=0, le=20)
    Note_Francais_Oral: float = Field(..., description="Note en français oral", ge=0, le=20)
    Note_Anglais_Ecrit: float = Field(..., description="Note en anglais écrit", ge=0, le=20)
    Note_Anglais_Oral: float = Field(..., description="Note en anglais oral", ge=0, le=20)
    Note_Philo: float = Field(..., description="Note en philosophie", ge=0, le=20)
    Note_Physique_Chimie: float = Field(..., description="Note en physique-chimie", ge=0, le=20)
    Note_SVT: float = Field(..., description="Note en SVT", ge=0, le=20)
    Note_Histoire_Geo: float = Field(..., description="Note en histoire-géographie", ge=0, le=20)
    Note_EPS: float = Field(..., description="Note en EPS", ge=0, le=20)
    Note_Espagnol_Ecrit: float = Field(..., description="Note en espagnol écrit", ge=0, le=20)
    Note_Espagnol_Oral: float = Field(..., description="Note en espagnol oral", ge=0, le=20)
    Points_BAC: float = Field(..., description="Points totaux au baccalauréat", ge=0)
    Personnalite: str = Field(..., description="Traits de personnalité de l'étudiant")
    Religion: str = Field(..., description="Religion de l'étudiant")
    Competences_Techniques: str = Field(..., description="Compétences techniques")
    Secteur_Desire: str = Field(..., description="Secteur d'activité souhaité")
    Etablissement: str = Field(..., description="Nom de l'établissement")
    Lieu_Habitation_Bac: str = Field(..., description="Lieu de résidence au moment du bac")
    Note_Facultative_1: float = Field(..., description="Note facultative 1", ge=0, le=20)
    Note_Facultative_2: float = Field(..., description="Note facultative 2", ge=0, le=20)
    Secteur_Activite_Famille: str = Field(..., description="Secteur d'activité de la famille")
    Justification_Choix: str = Field(..., description="Justification du choix d'orientation")
    Descriptions: str = Field(..., description="Descriptions supplémentaires")

    class Config:
        json_schema_extra = {
            "example": {
                "Sexe": "Masculin",
                "Age_Bac": 18,
                "Serie_Bac": "S",
                "Matieres_Preferees": "Mathématiques, Physique",
                "Note_Maths": 16.0,
                "Note_Francais_Ecrit": 14.0,
                "Note_Francais_Oral": 15.0,
                "Note_Anglais_Ecrit": 13.0,
                "Note_Anglais_Oral": 14.0,
                "Note_Philo": 12.0,
                "Note_Physique_Chimie": 15.0,
                "Note_SVT": 14.0,
                "Note_Histoire_Geo": 13.0,
                "Note_EPS": 15.0,
                "Note_Espagnol_Ecrit": 12.0,
                "Note_Espagnol_Oral": 13.0,
                "Points_BAC": 280.0,
                "Personnalite": "Analytique, Rigoureux",
                "Religion": "Christianisme",
                "Competences_Techniques": "Programmation, Robotique",
                "Secteur_Desire": "Informatique",
                "Etablissement": "Lycée Exemple",
                "Lieu_Habitation_Bac": "Ville Exemple",
                "Note_Facultative_1": 15.0,
                "Note_Facultative_2": 16.0,
                "Secteur_Activite_Famille": "Ingénierie",
                "Justification_Choix": "Passion pour les technologies",
                "Descriptions": "Étudiant motivé et curieux"
            }
        }

class StudentCreate(StudentBase):
    """Schéma pour la création d'un étudiant"""
    pass

class Student(StudentBase):
    """Schéma pour un étudiant en base de données"""
    id: int = Field(..., description="Identifiant unique de l'étudiant")
    Secteur_Activite: str = Field(..., description="Secteur d'activité prédit")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "Secteur_Activite": "Informatique",
                **StudentBase.Config.json_schema_extra["example"]
            }
        }

class StudentResponse(BaseModel):
    """Schéma pour la réponse de prédiction"""
    id: int = Field(..., description="Identifiant unique de l'étudiant")
    Secteur_Activite: str = Field(..., description="Secteur d'activité prédit")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "Secteur_Activite": "Informatique"
            }
        }
