from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import des routes
from .routes import general_router, prediction_router, database_router

# Création de l'application FastAPI
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

# Ajouter le middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les en-têtes
)

# Ajout des routers
app.include_router(general_router)
app.include_router(prediction_router)
app.include_router(database_router)

# Personnalisation de la documentation OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Personnalisation des tags
    openapi_schema["tags"] = [
        {
            "name": "Général",
            "description": "Endpoints généraux de l'API"
        },
        {
            "name": "Prédiction",
            "description": "Endpoints liés à la prédiction d'orientation"
        },
        {
            "name": "Base de données",
            "description": "Endpoints de gestion des données"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/predict/")
async def predict():
    # Votre logique ici
    return {"message": "Prédiction réussie"}
