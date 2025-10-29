"""
Advanced Fertilizer Recommendation Model
Research-grade ensemble approach with stacking and domain knowledge
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import xgboost as xgb
import lightgbm as lgb
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class FertilizerRecommendationModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.crop_encoder = LabelEncoder()
        self.fertilizer_encoder = LabelEncoder()
        self.soil_encoder = LabelEncoder()
        self.base_models = {}
        self.meta_model = None
        self.features = ['Nitrogen', 'Phosphorus', 'Potassium', 'pH', 'Rainfall', 'Temperature', 'Crop_encoded', 'Soil_encoded']
        self.model_path = Path("models/fertilizer_recommendation_ensemble.pkl")
        
    def load_and_prepare_data(self):
        """Load and prepare cleaned fertilizer recommendation data"""
        print("🧪 Loading fertilizer recommendation data...")
        
        # Load cleaned data
        df = pd.read_csv("cleaned_datasets/fertilizer_recommendation_clean.csv")
        print(f"Dataset shape: {df.shape}")
        print(f"Unique fertilizers: {df['Fertilizer'].nunique()}")
        print(f"Unique crops: {df['Crop'].nunique()}")
        
        # Encode categorical variables
        df['Crop_encoded'] = self.crop_encoder.fit_transform(df['Crop'])
        df['Soil_encoded'] = self.soil_encoder.fit_transform(df['Soil_color'])
        
        # Prepare features and target
        X = df[self.features].values
        y = self.fertilizer_encoder.fit_transform(df['Fertilizer'])
        
        # Split data stratified by fertilizer type
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale numerical features only (keep encoded categorical features as is)
        numerical_indices = [0, 1, 2, 3, 4, 5]  # Nitrogen, Phosphorus, Potassium, pH, Rainfall, Temperature
        X_train_scaled = X_train.copy()
        X_test_scaled = X_test.copy()
        
        X_train_scaled[:, numerical_indices] = self.scaler.fit_transform(X_train[:, numerical_indices])
        X_test_scaled[:, numerical_indices] = self.scaler.transform(X_test[:, numerical_indices])
        
        print(f"Training set: {X_train_scaled.shape}")
        print(f"Test set: {X_test_scaled.shape}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def create_base_models(self):
        """Create diverse base models optimized for fertilizer recommendation"""
        print("🔧 Creating base models...")
        
        self.base_models = {
            'rf': RandomForestClassifier(
                n_estimators=300,
                max_depth=20,
                min_samples_split=3,
                min_samples_leaf=1,
                max_features='sqrt',
                random_state=42,
                n_jobs=-1,
                class_weight='balanced'
            ),
            'xgb': xgb.XGBClassifier(
                n_estimators=300,
                max_depth=8,
                learning_rate=0.08,
                subsample=0.9,
                colsample_bytree=0.9,
                reg_alpha=0.1,
                reg_lambda=0.1,
                random_state=42,
                n_jobs=-1
            ),
            'lgb': lgb.LGBMClassifier(
                n_estimators=300,
                max_depth=8,
                learning_rate=0.08,
                feature_fraction=0.9,
                bagging_fraction=0.9,
                reg_alpha=0.1,
                reg_lambda=0.1,
                random_state=42,
                n_jobs=-1,
                verbose=-1
            ),
            'gb': GradientBoostingClassifier(
                n_estimators=200,
                max_depth=8,
                learning_rate=0.08,
                subsample=0.9,
                random_state=42
            )
        }
        
        # Meta-learner with L2 regularization
        self.meta_model = LogisticRegression(
            random_state=42,
            max_iter=2000,
            C=0.1,
            class_weight='balanced'
        )
    
    def train_base_models(self, X_train, y_train):
        """Train all base models with cross-validation"""
        print("🚀 Training base models...")
        
        base_predictions = np.zeros((X_train.shape[0], len(self.base_models)))
        
        # Use stratified k-fold for better class distribution
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        for i, (name, model) in enumerate(self.base_models.items()):
            print(f"   Training {name.upper()}...")
            
            # Cross-validation predictions for stacking
            cv_preds = np.zeros(X_train.shape[0])
            
            for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train)):
                X_fold_train, X_fold_val = X_train[train_idx], X_train[val_idx]
                y_fold_train, y_fold_val = y_train[train_idx], y_train[val_idx]
                
                # Clone model for this fold
                fold_model = clone_model(model)
                fold_model.fit(X_fold_train, y_fold_train)
                
                # Get predictions for validation fold
                val_preds = fold_model.predict(X_fold_val)
                cv_preds[val_idx] = val_preds
            
            base_predictions[:, i] = cv_preds
            
            # Train on full training set
            model.fit(X_train, y_train)
            
            # Cross-validation score
            cv_score = cross_val_score(model, X_train, y_train, cv=skf, scoring='accuracy')
            print(f"   {name.upper()} CV Score: {cv_score.mean():.4f} (+/- {cv_score.std() * 2:.4f})")
        
        return base_predictions
    
    def train_meta_model(self, base_predictions, y_train):
        """Train the meta-learner"""
        print("🧠 Training meta-learner...")
        
        self.meta_model.fit(base_predictions, y_train)
        
        # Meta-model score with stratified CV
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        meta_score = cross_val_score(self.meta_model, base_predictions, y_train, cv=skf, scoring='accuracy')
        print(f"   Meta-learner CV Score: {meta_score.mean():.4f} (+/- {meta_score.std() * 2:.4f})")
    
    def predict_ensemble(self, X):
        """Make ensemble predictions"""
        # Get base model predictions
        base_preds = np.zeros((X.shape[0], len(self.base_models)))
        
        for i, (name, model) in enumerate(self.base_models.items()):
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
        fertilizer_names = self.fertilizer_encoder.classes_
        print("\n📋 Classification Report:")
        print(classification_report(y_test, ensemble_pred, target_names=fertilizer_names))
        
        return ensemble_accuracy
    
    def save_model(self):
        """Save the complete ensemble model"""
        print("💾 Saving ensemble model...")
        
        model_data = {
            'scaler': self.scaler,
            'crop_encoder': self.crop_encoder,
            'fertilizer_encoder': self.fertilizer_encoder,
            'soil_encoder': self.soil_encoder,
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
            self.crop_encoder = model_data['crop_encoder']
            self.fertilizer_encoder = model_data['fertilizer_encoder']
            self.soil_encoder = model_data['soil_encoder']
            self.base_models = model_data['base_models']
            self.meta_model = model_data['meta_model']
            self.features = model_data['features']
            
            print("   Model loaded successfully!")
            return True
        return False
    
    def predict_fertilizer(self, nitrogen, phosphorus, potassium, ph, rainfall, temperature, crop, soil_color):
        """Predict best fertilizer for given conditions"""
        try:
            # Encode categorical inputs
            crop_encoded = self.crop_encoder.transform([crop])[0]
            soil_encoded = self.soil_encoder.transform([soil_color])[0]
            
            # Prepare input
            input_data = np.array([[nitrogen, phosphorus, potassium, ph, rainfall, temperature, crop_encoded, soil_encoded]])
            
            # Scale numerical features
            input_scaled = input_data.copy()
            numerical_indices = [0, 1, 2, 3, 4, 5]
            input_scaled[:, numerical_indices] = self.scaler.transform(input_data[:, numerical_indices])
            
            # Get prediction and probabilities
            pred, proba = self.predict_ensemble(input_scaled)
            
            # Convert to fertilizer name
            predicted_fertilizer = self.fertilizer_encoder.inverse_transform(pred)[0]
            confidence = np.max(proba[0])
            
            # Get top 3 recommendations
            top_indices = np.argsort(proba[0])[-3:][::-1]
            top_fertilizers = self.fertilizer_encoder.inverse_transform(top_indices)
            top_confidences = proba[0][top_indices]
            
            return {
                'recommended_fertilizer': predicted_fertilizer,
                'confidence': confidence,
                'top_3_recommendations': [
                    {'fertilizer': fert, 'confidence': conf}
                    for fert, conf in zip(top_fertilizers, top_confidences)
                ]
            }
            
        except ValueError as e:
            return {
                'error': f"Unknown crop or soil type: {e}",
                'available_crops': list(self.crop_encoder.classes_),
                'available_soil_types': list(self.soil_encoder.classes_)
            }
    
    def train_complete_pipeline(self):
        """Complete training pipeline"""
        print("🧪 Starting Fertilizer Recommendation Model Training...")
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
        print("✅ Fertilizer Recommendation Model Training Complete!")
        print(f"🎯 Final Ensemble Accuracy: {accuracy:.4f}")
        
        return accuracy

def clone_model(model):
    """Clone a model with same parameters"""
    from sklearn.base import clone
    return clone(model)

def main():
    """Main training function"""
    model = FertilizerRecommendationModel()
    
    # Check if model exists
    if model.load_model():
        print("Model already trained. Skipping training...")
        
        # Test prediction
        test_result = model.predict_fertilizer(37, 69, 63, 6.2, 82.3, 22.5, "Maize", "Black")
        print(f"\nTest Prediction: {test_result}")
    else:
        # Train new model
        accuracy = model.train_complete_pipeline()
        
        # Test prediction
        test_result = model.predict_fertilizer(37, 69, 63, 6.2, 82.3, 22.5, "Maize", "Black")
        print(f"\nTest Prediction: {test_result}")

if __name__ == "__main__":
    main()