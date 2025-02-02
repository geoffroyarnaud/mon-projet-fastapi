from fastapi import FastAPI
from app.routes import general_router, prediction_router, database_router

app = FastAPI(
    title="Système d'Orientation des Bacheliers",
    description="""
    API pour le système de prédiction d'orientation des bacheliers.
    
    Cette API permet de :
    * Prédire l'orientation d'un étudiant en fonction de ses notes et caractéristiques
    * Consulter l'historique des prédictions
    * Gérer la base de données des étudiants
    """,
    version="1.0.0"
)

# Ajout des routers
app.include_router(general_router)
app.include_router(prediction_router)
app.include_router(database_router)
