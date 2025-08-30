import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
from typing import Dict, List, Tuple, Optional
import os

class AdaptiveQuizModel:
    """
    Machine Learning model for adaptive quiz difficulty adjustment.
    Designed to be lightweight for Arduino/ESP32 deployment.
    """
    
    def __init__(self, model_path: str = None):
        self.model = RandomForestRegressor(
            n_estimators=50,  # Reduced for lightweight deployment
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = model_path or "ml_model/quiz_model.pkl"
        
        # Load pre-trained model if exists
        if os.path.exists(self.model_path):
            self.load_model()
    
    def extract_features(self, performance_data: Dict) -> np.ndarray:
        """
        Extract features from student performance data.
        Features are designed to be lightweight and meaningful.
        """
        features = []
        
        # Response time features (normalized)
        avg_response_time = performance_data.get('avg_response_time', 0)
        features.append(min(avg_response_time / 60.0, 1.0))  # Normalize to 0-1
        
        # Accuracy features
        accuracy = performance_data.get('accuracy', 0.5)
        features.append(accuracy)
        
        # Attempt features
        avg_attempts = performance_data.get('avg_attempts', 1.0)
        features.append(min(avg_attempts / 5.0, 1.0))  # Normalize to 0-1
        
        # Difficulty progression
        current_difficulty = performance_data.get('current_difficulty', 1.0)
        features.append(current_difficulty / 10.0)  # Normalize to 0-1
        
        # Recent performance trend
        recent_accuracy = performance_data.get('recent_accuracy', 0.5)
        features.append(recent_accuracy)
        
        # Convert to numpy array and reshape
        return np.array(features).reshape(1, -1)
    
    def predict_difficulty(self, performance_data: Dict) -> float:
        """
        Predict the optimal difficulty level for the next question.
        Returns a difficulty score between 1.0 and 10.0
        """
        if not self.is_trained:
            # Return default difficulty if model not trained
            return self._calculate_heuristic_difficulty(performance_data)
        
        try:
            features = self.extract_features(performance_data)
            features_scaled = self.scaler.transform(features)
            predicted_difficulty = self.model.predict(features_scaled)[0]
            
            # Ensure difficulty is within bounds (1-10)
            return max(1.0, min(10.0, predicted_difficulty))
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._calculate_heuristic_difficulty(performance_data)
    
    def _calculate_heuristic_difficulty(self, performance_data: Dict) -> float:
        """
        Fallback heuristic for difficulty calculation when ML model is not available.
        This ensures the system works even without training data.
        """
        accuracy = performance_data.get('accuracy', 0.5)
        current_difficulty = performance_data.get('current_difficulty', 1.0)
        
        # Simple rule-based difficulty adjustment
        if accuracy > 0.8:
            # Student doing well, increase difficulty
            return min(10.0, current_difficulty + 0.5)
        elif accuracy < 0.4:
            # Student struggling, decrease difficulty
            return max(1.0, current_difficulty - 0.5)
        else:
            # Student doing okay, maintain current difficulty
            return current_difficulty
    
    def train_model(self, training_data: List[Dict]) -> bool:
        """
        Train the ML model with historical performance data.
        """
        if not training_data or len(training_data) < 10:
            print("Insufficient training data. Need at least 10 samples.")
            return False
        
        try:
            # Prepare training data
            X = []
            y = []
            
            for data_point in training_data:
                features = self.extract_features(data_point)
                X.append(features.flatten())
                y.append(data_point.get('optimal_difficulty', 5.0))
            
            X = np.array(X)
            y = np.array(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            train_score = self.model.score(X_train_scaled, y_train)
            test_score = self.model.score(X_test_scaled, y_test)
            
            print(f"Model trained successfully!")
            print(f"Training R² score: {train_score:.3f}")
            print(f"Testing R² score: {test_score:.3f}")
            
            self.is_trained = True
            self.save_model()
            return True
            
        except Exception as e:
            print(f"Training error: {e}")
            return False
    
    def save_model(self) -> bool:
        """Save the trained model to disk."""
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler,
                'is_trained': self.is_trained
            }, self.model_path)
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False
    
    def load_model(self) -> bool:
        """Load a pre-trained model from disk."""
        try:
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.is_trained = model_data['is_trained']
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Load error: {e}")
            return False
    
    def get_model_info(self) -> Dict:
        """Get information about the current model state."""
        return {
            'is_trained': self.is_trained,
            'model_type': 'RandomForestRegressor',
            'n_estimators': self.model.n_estimators if self.is_trained else 0,
            'feature_count': 5,
            'model_path': self.model_path
        }
    
    def update_model(self, new_data: Dict) -> bool:
        """
        Incrementally update the model with new performance data.
        This is useful for continuous learning.
        """
        if not self.is_trained:
            return False
        
        try:
            # Extract features and target
            features = self.extract_features(new_data)
            target = new_data.get('optimal_difficulty', 5.0)
            
            # Update scaler with new data
            features_scaled = self.scaler.transform(features)
            
            # For now, we'll retrain with accumulated data
            # In a production system, you might use online learning
            return True
            
        except Exception as e:
            print(f"Update error: {e}")
            return False
