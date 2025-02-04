import joblib
import pandas as pd
import logging
import os
from typing import Dict, Any
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.impute import SimpleImputer

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class OrientationModel:
    def __init__(self, data_path=None):
        self.model = None
        self.features = [
            'Sexe', 'Age_Bac', 'Serie_Bac', 'Matieres_Preferees',
            'Note_Maths', 'Note_Francais_Ecrit', 'Note_Francais_Oral',
            'Note_Anglais_Ecrit', 'Note_Anglais_Oral', 'Note_Philo',
            'Note_Physique_Chimie', 'Note_SVT', 'Note_Histoire_Geo',
            'Note_EPS', 'Note_Espagnol_Ecrit', 'Note_Espagnol_Oral',
            'Points_BAC', 'Personnalite', 'Religion', 'Competences_Techniques',
            'Secteur_Desire', 'Etablissement', 'Lieu_Habitation_Bac',
            'Note_Facultative_1', 'Note_Facultative_2', 'Secteur_Activite_Famille',
            'Justification_Choix', 'Descriptions', 'Secteur_Activite'
        ]
        self.categorical_features = [
            'Sexe', 'Serie_Bac', 'Religion', 'Etablissement', 
            'Lieu_Habitation_Bac', 'Secteur_Activite_Famille', 
            'Justification_Choix', 'Matieres_Preferees', 
            'Personnalite', 'Competences_Techniques', 
            'Secteur_Desire', 'Secteur_Activite'
        ]
        
        # Chemin par défaut si non fourni
        if data_path is None:
            data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'augmented_data.csv')
        
        self.data_path = data_path
        
        # Chargement différé du modèle
        self.model = None

    def load_and_train_model(self):
        """Charge le dataset, entraîne le modèle et le sauvegarde."""
        try:
            # Charger le dataset
            logger.info(f"Chargement des données depuis {self.data_path}")
            data = pd.read_csv(self.data_path)
            data = self.clean_data(data)

            # Séparer les caractéristiques et la cible
            X = data.drop(columns=['Secteur_Activite'])
            y = data['Secteur_Activite']

            # Log des valeurs manquantes
            logger.info("Valeurs manquantes avant remplissage:")
            logger.info(X.isnull().sum())
            logger.info(f"Valeurs manquantes dans y: {y.isnull().sum()}")

            # Gestion des valeurs manquantes
            imputer = SimpleImputer(strategy='most_frequent')
            X[X.columns] = imputer.fit_transform(X[X.columns])

            # Gestion propre des valeurs manquantes pour y
            # Ajout de 'Inconnu' aux catégories existantes si nécessaire
            if 'Inconnu' not in y.cat.categories:
                y = y.cat.add_categories('Inconnu')
            y = y.fillna('Inconnu')

            # Sélection des colonnes catégorielles
            categorical_columns = X.select_dtypes(include=['category', 'object']).columns

            # Création du transformateur pour encoder les variables catégorielles
            preprocessor = ColumnTransformer(
                transformers=[
                    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_columns),
                    ('num', 'passthrough', X.select_dtypes(exclude=['category', 'object']).columns)
                ])

            # Création du pipeline 
            self.model = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('classifier', RandomForestClassifier(random_state=42))
            ])

            # Division des données 
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

            # Entraînement du modèle
            self.model.fit(X_train, y_train)

            # Génération des prédictions
            y_pred = self.model.predict(X_test)

            # Rapport de classification
            logger.info("Rapport de classification :")
            logger.info(classification_report(y_test, y_pred))
            logger.info("Matrice de confusion :")
            logger.info(str(confusion_matrix(y_test, y_pred)))

            # Créer le répertoire models s'il n'existe pas
            os.makedirs('models', exist_ok=True)

            # Enregistrer le modèle
            # joblib.dump(self.model, 'models/random_forest_pipeline.joblib')
            logger.info("Modèle entraîné avec succès.")

        except Exception as e:
            logger.error(f"Erreur lors de l'entraînement du modèle : {e}")
            raise

    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Nettoyer le dataset pour s'assurer que toutes les colonnes sont dans le bon format."""
        # Convertir les colonnes numériques
        numeric_columns = [
            'Note_Maths', 'Note_Francais_Ecrit', 'Note_Francais_Oral', 
            'Note_Anglais_Ecrit', 'Note_Anglais_Oral', 'Note_Philo', 
            'Note_Physique_Chimie', 'Note_SVT', 'Note_Histoire_Geo', 
            'Note_EPS', 'Note_Espagnol_Ecrit', 'Note_Espagnol_Oral', 
            'Points_BAC', 'Note_Facultative_1', 'Note_Facultative_2'
        ]
        for col in numeric_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')

        # Vérifiez les colonnes catégorielles
        for col in self.categorical_features:
            data[col] = data[col].astype('category')

        return data

    def preprocess_data(self, student_data: Dict[str, Any]) -> pd.DataFrame:
        """Prétraitement des données avant la prédiction"""
        try:
            logger.debug(f"Données reçues : {student_data}")
            features_data = {feature: student_data.get(feature, None) for feature in self.features}
            df_features = pd.DataFrame([features_data])
            
            # Conversion des types
            for col in self.categorical_features:
                df_features[col] = df_features[col].astype('category')
            
            logger.debug(f"Données prétraitées : {df_features.to_dict()}")
            return df_features
            
        except Exception as e:
            logger.error(f"Erreur lors du prétraitement : {str(e)}")
            return None

    def predict_orientation(self, student_data: Dict[str, Any]) -> str:
        """Prédire l'orientation pour un étudiant"""
        try:
            # Chargement différé du modèle
            if self.model is None:
                self.load_and_train_model()
            
            # Prétraitement des données
            df = self.preprocess_data(student_data)
            if df is None:
                return "Erreur: Échec du prétraitement des données"
            
            # Prédiction
            logger.debug("Début de la prédiction")
            prediction = self.model.predict(df)
            
            predicted_class = prediction[0]
            logger.info(f"Prédiction : {predicted_class}")
            return predicted_class
            
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction : {str(e)}")
            return "Desole, aucune prediction disponible"  # Valeur par défaut en cas d'erreur

    def get_feature_importance(self) -> Dict[str, float]:
        """Obtenir l'importance des caractéristiques"""
        try:
            if hasattr(self.model.named_steps['classifier'], 'feature_importances_'):
                importance = dict(zip(self.features, self.model.named_steps['classifier'].feature_importances_))
                sorted_importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
                logger.info(f"Importance des features : {sorted_importance}")
                return sorted_importance
            
            logger.warning("Le modèle ne supporte pas l'importance des features")
            return {}
        
        except Exception as e:
            logger.error(f"Erreur lors de l'obtention de l'importance des features : {e}")
            return {}

# Ne pas instancier le modèle automatiquement
# orientation_model = OrientationModel()
orientation_model = OrientationModel()