from sqlalchemy import Column, Integer, String, Float, Boolean  # Assurez-vous que Boolean est importé
from .database import Base
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    Sexe = Column(String)
    Age_Bac = Column(Integer)
    Serie_Bac = Column(String)
    Matieres_Preferees = Column(String)
    Note_Maths = Column(Float)
    Note_Francais_Ecrit = Column(Float)
    Note_Francais_Oral = Column(Float)
    Note_Anglais_Ecrit = Column(Float)
    Note_Anglais_Oral = Column(Float)
    Note_Philo = Column(Float)
    Note_Physique_Chimie = Column(Float)
    Note_SVT = Column(Float)
    Note_Histoire_Geo = Column(Float)
    Note_EPS = Column(Float)
    Note_Espagnol_Ecrit = Column(Float)
    Note_Espagnol_Oral = Column(Float)
    Points_BAC = Column(Float)
    Personnalite = Column(String)
    Religion = Column(String)
    Competences_Techniques = Column(String)
    Secteur_Desire = Column(String)
    Etablissement = Column(String)
    Lieu_Habitation_Bac = Column(String)
    Note_Facultative_1 = Column(Float)
    Note_Facultative_2 = Column(Float)
    Secteur_Activite_Famille = Column(String)
    Justification_Choix = Column(String)
    Descriptions = Column(String)
    Secteur_Activite = Column(String)  # Secteur prédit

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Boolean, default=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
