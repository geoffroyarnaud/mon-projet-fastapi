import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os
import logging
from typing import Dict, Any

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class OrientationModel:
    def __init__(self):
        self.model = None
        self.features = [
            'Sexe', 'Age_Bac', 'Serie_Bac', 'Note_Maths', 
            'Note_Francais_Ecrit', 'Note_Francais_Oral',
            'Note_Anglais_Ecrit', 'Note_Anglais_Oral', 'Note_Philo',
            'Note_Physique_Chimie', 'Note_SVT', 'Note_Histoire_Geo',
            'Note_EPS', 'Note_Espagnol_Ecrit', 'Note_Espagnol_Oral',
            'Points_BAC', 'Religion'
        ]
        self.categorical_features = ['Sexe', 'Serie_Bac', 'Religion']
        self.load_model()
        
    def create_test_model(self):
        """Créer un modèle de test simple"""
        logger.info("Création d'un modèle de test...")
        
        # Liste des secteurs possibles
        self.sectors = [
            "Informatique", "Médecine", "Droit", "Commerce",
            "Ingénierie", "Sciences", "Arts", "Lettres"
        ]
        
        # Créer un modèle de base
        class MockModel:
            def predict(self, X):
                return ["Informatique"]  # Retourne toujours "Informatique" pour les tests
                
            def predict_proba(self, X):
                probs = np.zeros((1, len(self.sectors)))
                probs[0, 0] = 1.0  # 100% de confiance pour "Informatique"
                return probs
                
            @property
            def feature_importances_(self):
                return np.ones(len(self.features)) / len(self.features)
        
        self.model = MockModel()
        logger.info("Modèle de test créé avec succès")
        
    def load_model(self):
        """Charge le modèle depuis le fichier ou crée un modèle de test"""
        try:
            model_path = os.path.join("models", "random_forest_pipeline.joblib")
            logger.info(f"Tentative de chargement du modèle depuis : {model_path}")
            
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info("Modèle chargé avec succès !")
            else:
                logger.warning(f"Fichier modèle non trouvé : {model_path}")
                self.create_test_model()
                
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle : {str(e)}")
            self.create_test_model()

    def preprocess_data(self, student_data: Dict[str, Any]) -> pd.DataFrame:
        """Prétraitement des données avant la prédiction"""
        try:
            logger.debug(f"Données reçues : {student_data}")
            
            # Création du DataFrame
            df = pd.DataFrame([student_data])
            
            # Sélection des features
            features_data = {}
            for feature in self.features:
                if feature in student_data:
                    features_data[feature] = student_data[feature]
                else:
                    logger.warning(f"Feature manquante : {feature}")
                    features_data[feature] = None  # Valeur par défaut
            
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
            if self.model is None:
                logger.error("Modèle non chargé")
                return "Erreur: Modèle non chargé"
                
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
            return "Informatique"  # Valeur par défaut en cas d'erreur

    def get_feature_importance(self) -> Dict[str, float]:
        """Obtenir l'importance des caractéristiques"""
        if self.model is None:
            logger.warning("Impossible d'obtenir l'importance des features : modèle non chargé")
            return {}
            
        if hasattr(self.model, 'feature_importances_'):
            importance = dict(zip(self.features, self.model.feature_importances_))
            sorted_importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
            logger.info(f"Importance des features : {sorted_importance}")
            return sorted_importance
        
        logger.warning("Le modèle ne supporte pas l'importance des features")
        return {}

orientation_model = OrientationModel()
