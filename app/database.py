from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configuration SQLite
DATABASE_URL = "sqlite:///./orientation.db"
logger.info(f"URL de la base de données : {DATABASE_URL}")

try:
    # Création du moteur SQLAlchemy avec débogage
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=True  # Active le débogage SQL
    )
    logger.info("Moteur SQLAlchemy créé avec succès")

    # Vérification de la connexion et des tables
    with engine.connect() as conn:
        logger.info("Connexion à la base de données réussie !")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Tables existantes : {tables}")

except Exception as e:
    logger.error(f"Erreur de connexion à la base de données : {str(e)}")
    raise

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info("Session SQLAlchemy créée avec succès")

# Création de la classe de base pour les modèles
Base = declarative_base()

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
