"""
Advanced Crop Recommendation Model
Research-grade ensemble approach with stacking
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import xgboost as xgb
import lightgbm as lgb
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class CropRecommendationModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.base_models = {}
        self.meta_model = None
        self.features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        self.model_path = Path("models/crop_recommendation_ensemble.pkl")
        
    def load_and_prepare_data(self):
        """Load and prepare cleaned crop recommendation data"""
        print("📊 Loading crop recommendation data...")
        
        # Load cleaned data
        df = pd.read_csv("cleaned_datasets/crop_recommendation_clean.csv")
        print(f"Dataset shape: {df.shape}")
        print(f"Unique crops: {df['label'].nunique()}")
        
        # Prepare features and target
        X = df[self.features].values
        y = self.label_encoder.fit_transform(df['label'])
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print(f"Training set: {X_train_scaled.shape}")
        print(f"Test set: {X_test_scaled.shape}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def create_base_models(self):
        """Create diverse base models for ensemble"""
        print("🔧 Creating base models...")
        
        self.base_models = {
            'rf': RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            ),
            'xgb': xgb.XGBClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                n_jobs=-1
            ),
            'lgb': lgb.LGBMClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                feature_fraction=0.8,
                bagging_fraction=0.8,
                random_state=42,
                n_jobs=-1,
                verbose=-1
            ),
            'gb': GradientBoostingClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                random_state=42
            ),
            'svm': SVC(
                kernel='rbf',
                C=1.0,
                gamma='scale',
                probability=True,
                random_state=42
            )
        }
        
        # Meta-learner for stacking
        self.meta_model = LogisticRegression(
            random_state=42,
            max_iter=1000
        )
    
    def train_base_models(self, X_train, y_train):
        """Train all base models"""
        print("🚀 Training base models...")
        
        base_predictions = np.zeros((X_train.shape[0], len(self.base_models)))
        
        for i, (name, model) in enumerate(self.base_models.items()):
            print(f"   Training {name.upper()}...")
            
            # Cross-validation for stacking
            cv_preds = np.zeros(X_train.shape[0])
            from sklearn.model_selection import KFold
            
            kf = KFold(n_splits=5, shuffle=True, random_state=42)
            for train_idx, val_idx in kf.split(X_train):
                X_fold_train, X_fold_val = X_train[train_idx], X_train[val_idx]
                y_fold_train = y_train[train_idx]
                
                model.fit(X_fold_train, y_fold_train)
                cv_preds[val_idx] = model.predict_proba(X_fold_val)[:, 1] if len(np.unique(y_train)) == 2 else model.predict(X_fold_val)
            
            base_predictions[:, i] = cv_preds
            
            # Train on full training set
            model.fit(X_train, y_train)
            
            # Cross-validation score
            cv_score = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
            print(f"   {name.upper()} CV Score: {cv_score.mean():.4f} (+/- {cv_score.std() * 2:.4f})")
        
        return base_predictions
    
    def train_meta_model(self, base_predictions, y_train):
        """Train the meta-learner"""
        print("🧠 Training meta-learner...")
        
        self.meta_model.fit(base_predictions, y_train)
        
        # Meta-model score
        meta_score = cross_val_score(self.meta_model, base_predictions, y_train, cv=5, scoring='accuracy')
        print(f"   Meta-learner CV Score: {meta_score.mean():.4f} (+/- {meta_score.std() * 2:.4f})")
    
    def predict_ensemble(self, X):
        """Make ensemble predictions"""
        # Get base model predictions
        base_preds = np.zeros((X.shape[0], len(self.base_models)))
        
        for i, (name, model) in enumerate(self.base_models.items()):
            if len(np.unique(self.label_encoder.classes_)) == 2:
                base_preds[:, i] = model.predict_proba(X)[:, 1]
            else:
                base_preds[:, i] = model.predict(X)
        
        # Meta-learner prediction
        ensemble_pred = self.meta_model.predict(base_preds)
        ensemble_proba = self.meta_model.predict_proba(base_preds)
        
        return ensemble_pred, ensemble_proba
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate the ensemble model"""
        print("📊 Evaluating ensemble model...")
        
        # Individual model performance
        for name, model in self.base_models.items():
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print(f"   {name.upper()} Accuracy: {accuracy:.4f}")
        
        # Ensemble performance
        ensemble_pred, ensemble_proba = self.predict_ensemble(X_test)
        ensemble_accuracy = accuracy_score(y_test, ensemble_pred)
        
        print(f"\n🎯 Ensemble Accuracy: {ensemble_accuracy:.4f}")
        
        # Detailed classification report
        crop_names = self.label_encoder.classes_
        print("\n📋 Classification Report:")
        print(classification_report(y_test, ensemble_pred, target_names=crop_names))
        
        return ensemble_accuracy
    
    def save_model(self):
        """Save the complete ensemble model"""
        print("💾 Saving ensemble model...")
        
        model_data = {
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'base_models': self.base_models,
            'meta_model': self.meta_model,
            'features': self.features
        }
        
        # Create models directory
        self.model_path.parent.mkdir(exist_ok=True)
        
        # Save model
        joblib.dump(model_data, self.model_path)
        print(f"   Model saved to: {self.model_path}")
    
    def load_model(self):
        """Load saved ensemble model"""
        if self.model_path.exists():
            print("📂 Loading saved model...")
            model_data = joblib.load(self.model_path)
            
            self.scaler = model_data['scaler']
            self.label_encoder = model_data['label_encoder']
            self.base_models = model_data['base_models']
            self.meta_model = model_data['meta_model']
            self.features = model_data['features']
            
            print("   Model loaded successfully!")
            return True
        return False
    
    def predict_crop(self, N, P, K, temperature, humidity, ph, rainfall):
        """Predict best crop for given conditions"""
        # Prepare input
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        input_scaled = self.scaler.transform(input_data)
        
        # Get prediction and probabilities
        pred, proba = self.predict_ensemble(input_scaled)
        
        # Convert to crop name
        predicted_crop = self.label_encoder.inverse_transform(pred)[0]
        confidence = np.max(proba[0])
        
        # Get top 3 recommendations
        top_indices = np.argsort(proba[0])[-3:][::-1]
        top_crops = self.label_encoder.inverse_transform(top_indices)
        top_confidences = proba[0][top_indices]
        
        return {
            'recommended_crop': predicted_crop,
            'confidence': confidence,
            'top_3_recommendations': [
                {'crop': crop, 'confidence': conf}
                for crop, conf in zip(top_crops, top_confidences)
            ]
        }
    
    def train_complete_pipeline(self):
        """Complete training pipeline"""
        print("🌾 Starting Crop Recommendation Model Training...")
        print("=" * 60)
        
        # Load and prepare data
        X_train, X_test, y_train, y_test = self.load_and_prepare_data()
        
        # Create and train models
        self.create_base_models()
        base_predictions = self.train_base_models(X_train, y_train)
        self.train_meta_model(base_predictions, y_train)
        
        # Evaluate model
        accuracy = self.evaluate_model(X_test, y_test)
        
        # Save model
        self.save_model()
        
        print("=" * 60)
        print("✅ Crop Recommendation Model Training Complete!")
        print(f"🎯 Final Ensemble Accuracy: {accuracy:.4f}")
        
        return accuracy

def main():
    """Main training function"""
    model = CropRecommendationModel()
    
    # Check if model exists
    if model.load_model():
        print("Model already trained. Skipping training...")
        
        # Test prediction
        test_result = model.predict_crop(90, 42, 43, 20.87, 82.00, 6.50, 202.93)
        print(f"\nTest Prediction: {test_result}")
    else:
        # Train new model
        accuracy = model.train_complete_pipeline()
        
        # Test prediction
        test_result = model.predict_crop(90, 42, 43, 20.87, 82.00, 6.50, 202.93)
        print(f"\nTest Prediction: {test_result}")

if __name__ == "__main__":
    main()