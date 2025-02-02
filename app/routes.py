from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from typing import List, Optional

from .database import get_db
from .ml_model import orientation_model
from . import schemas, models

# Configuration du logging
logger = logging.getLogger(__name__)

# Création des routers
general_router = APIRouter(tags=["Général"])
prediction_router = APIRouter(tags=["Prédiction"])
database_router = APIRouter(tags=["Base de données"])

@general_router.get("/", 
                   response_model=schemas.Message,
                   summary="Page d'accueil",
                   description="Retourne un message de bienvenue et les liens vers la documentation")
async def read_root():
    """
    Endpoint racine de l'API.
    
    Returns:
        Message: Message de bienvenue et liens utiles
    """
    return schemas.Message(
        message="Bienvenue sur l'API du Système d'Orientation des Bacheliers",
        documentation="/docs",
        redoc="/redoc"
    )

@general_router.get("/test", 
                   response_model=schemas.Message,
                   summary="Test de l'API",
                   description="Permet de vérifier que l'API fonctionne correctement")
async def test_endpoint():
    """
    Endpoint de test pour vérifier le bon fonctionnement de l'API.
    
    Returns:
        Message: Message de confirmation
    """
    return schemas.Message(
        message="L'API fonctionne correctement",
        status="ok"
    )

@prediction_router.post("/predict/", 
                       response_model=schemas.StudentResponse,
                       summary="Prédire l'orientation",
                       description="Prédit l'orientation d'un étudiant en fonction de ses caractéristiques",
                       status_code=status.HTTP_201_CREATED)
async def predict_orientation(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    """
    Prédit l'orientation d'un étudiant et enregistre les données en base.
    
    Args:
        student: Données de l'étudiant
        db: Session de base de données
        
    Returns:
        StudentResponse: Données de l'étudiant avec la prédiction
        
    Raises:
        HTTPException: En cas d'erreur lors de la prédiction
    """
    try:
        # Prédiction
        secteur = orientation_model.predict_orientation(student.dict())
        logger.info(f"Prédiction : {secteur}")
        
        # Sauvegarde en base
        db_student = models.Student(**student.dict(), Secteur_Activite=secteur)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        
        return schemas.StudentResponse(
            id=db_student.id,
            Secteur_Activite=secteur
        )
        
    except Exception as e:
        logger.error(f"Erreur de prédiction : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@database_router.get("/students/", 
                    response_model=List[schemas.Student],
                    summary="Liste des étudiants",
                    description="Récupère la liste de tous les étudiants en base de données")
async def get_students(
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des étudiants avec pagination.
    
    Args:
        skip: Nombre d'étudiants à sauter
        limit: Nombre maximum d'étudiants à retourner
        db: Session de base de données
        
    Returns:
        List[Student]: Liste des étudiants
        
    Raises:
        HTTPException: En cas d'erreur lors de la récupération
    """
    try:
        students = db.query(models.Student).offset(skip).limit(limit).all()
        logger.info(f"Récupération de {len(students)} étudiants")
        return students
    except Exception as e:
        logger.error(f"Erreur : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@database_router.get("/students/{student_id}", 
                    response_model=schemas.Student,
                    summary="Détails d'un étudiant",
                    description="Récupère les détails d'un étudiant par son ID")
async def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    Récupère un étudiant par son ID.
    
    Args:
        student_id: ID de l'étudiant
        db: Session de base de données
        
    Returns:
        Student: Données de l'étudiant
        
    Raises:
        HTTPException: Si l'étudiant n'est pas trouvé ou en cas d'erreur
    """
    try:
        student = db.query(models.Student).filter(models.Student.id == student_id).first()
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Étudiant non trouvé"
            )
        return student
    except Exception as e:
        logger.error(f"Erreur : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
