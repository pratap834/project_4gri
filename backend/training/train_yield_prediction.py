"""
Advanced Crop Yield Prediction Model
Research-grade regression ensemble with stacking
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import lightgbm as lgb
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class CropYieldPredictionModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.crop_encoder = LabelEncoder()
        self.state_encoder = LabelEncoder()
        self.season_encoder = LabelEncoder()
        self.base_models = {}
        self.meta_model = None
        self.features = ['Area', 'Annual_Rainfall', 'Fertilizer', 'Pesticide', 'Crop_encoded', 'State_encoded', 'Season_encoded']
        self.model_path = Path("models/yield_prediction_ensemble.pkl")
        
    def load_and_prepare_data(self):
        """Load and prepare cleaned crop yield data"""
        print("📊 Loading crop yield prediction data...")
        
        # Load cleaned data
        df = pd.read_csv("cleaned_datasets/crop_yield_clean.csv")
        print(f"Dataset shape: {df.shape}")
        print(f"Unique crops: {df['Crop'].nunique()}")
        print(f"Unique states: {df['State'].nunique()}")
        
        # Encode categorical variables
        df['Crop_encoded'] = self.crop_encoder.fit_transform(df['Crop'])
        df['State_encoded'] = self.state_encoder.fit_transform(df['State'])
        df['Season_encoded'] = self.season_encoder.fit_transform(df['Season'])
        
        # Prepare features and target
        X = df[self.features].values
        y = df['Yield'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features (keeping encoded categorical features)
        numerical_indices = [0, 1, 2, 3]  # Area, Annual_Rainfall, Fertilizer, Pesticide
        X_train_scaled = X_train.copy()
        X_test_scaled = X_test.copy()
        
        X_train_scaled[:, numerical_indices] = self.scaler.fit_transform(X_train[:, numerical_indices])
        X_test_scaled[:, numerical_indices] = self.scaler.transform(X_test[:, numerical_indices])
        
        print(f"Training set: {X_train_scaled.shape}")
        print(f"Test set: {X_test_scaled.shape}")
        print(f"Yield range: {y.min():.2f} - {y.max():.2f}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def create_base_models(self):
        """Create diverse base models for yield prediction"""
        print("🔧 Creating base models...")
        
        self.base_models = {
            'rf': RandomForestRegressor(
                n_estimators=300,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                max_features='sqrt',
                random_state=42,
                n_jobs=-1
            ),
            'xgb': xgb.XGBRegressor(
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
            'lgb': lgb.LGBMRegressor(
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
            'gb': GradientBoostingRegressor(
                n_estimators=200,
                max_depth=8,
                learning_rate=0.08,
                subsample=0.9,
                random_state=42
            ),
            'ridge': Ridge(
                alpha=1.0,
                random_state=42
            )
        }
        
        # Meta-learner for stacking
        self.meta_model = Ridge(alpha=0.1, random_state=42)
    
    def train_base_models(self, X_train, y_train):
        """Train all base models with cross-validation"""
        print("🚀 Training base models...")
        
        base_predictions = np.zeros((X_train.shape[0], len(self.base_models)))
        
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        
        for i, (name, model) in enumerate(self.base_models.items()):
            print(f"   Training {name.upper()}...")
            
            # Cross-validation predictions for stacking
            cv_preds = np.zeros(X_train.shape[0])
            
            for fold, (train_idx, val_idx) in enumerate(kf.split(X_train)):
                X_fold_train, X_fold_val = X_train[train_idx], X_train[val_idx]
                y_fold_train, y_fold_val = y_train[train_idx], y_train[val_idx]
                
                # Clone model for this fold
                from sklearn.base import clone
                fold_model = clone(model)
                fold_model.fit(X_fold_train, y_fold_train)
                
                # Get predictions for validation fold
                val_preds = fold_model.predict(X_fold_val)
                cv_preds[val_idx] = val_preds
            
            base_predictions[:, i] = cv_preds
            
            # Train on full training set
            model.fit(X_train, y_train)
            
            # Cross-validation score (negative MSE)
            cv_score = cross_val_score(model, X_train, y_train, cv=kf, scoring='neg_mean_squared_error')
            cv_rmse = np.sqrt(-cv_score.mean())
            print(f"   {name.upper()} CV RMSE: {cv_rmse:.4f} (+/- {np.sqrt(cv_score.std() * 2):.4f})")
        
        return base_predictions
    
    def train_meta_model(self, base_predictions, y_train):
        """Train the meta-learner"""
        print("🧠 Training meta-learner...")
        
        self.meta_model.fit(base_predictions, y_train)
        
        # Meta-model score
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        meta_score = cross_val_score(self.meta_model, base_predictions, y_train, cv=kf, scoring='neg_mean_squared_error')
        meta_rmse = np.sqrt(-meta_score.mean())
        print(f"   Meta-learner CV RMSE: {meta_rmse:.4f} (+/- {np.sqrt(meta_score.std() * 2):.4f})")
    
    def predict_ensemble(self, X):
        """Make ensemble predictions"""
        # Get base model predictions
        base_preds = np.zeros((X.shape[0], len(self.base_models)))
        
        for i, (name, model) in enumerate(self.base_models.items()):
            base_preds[:, i] = model.predict(X)
        
        # Meta-learner prediction
        ensemble_pred = self.meta_model.predict(base_preds)
        
        return ensemble_pred, base_preds
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate the ensemble model"""
        print("📊 Evaluating ensemble model...")
        
        # Individual model performance
        for name, model in self.base_models.items():
            y_pred = model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            print(f"   {name.upper()} - RMSE: {rmse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}")
        
        # Ensemble performance
        ensemble_pred, _ = self.predict_ensemble(X_test)
        ensemble_rmse = np.sqrt(mean_squared_error(y_test, ensemble_pred))
        ensemble_mae = mean_absolute_error(y_test, ensemble_pred)
        ensemble_r2 = r2_score(y_test, ensemble_pred)
        
        print(f"\n🎯 Ensemble Performance:")
        print(f"   RMSE: {ensemble_rmse:.4f}")
        print(f"   MAE: {ensemble_mae:.4f}")
        print(f"   R²: {ensemble_r2:.4f}")
        
        # Calculate percentage error
        mape = np.mean(np.abs((y_test - ensemble_pred) / y_test)) * 100
        print(f"   MAPE: {mape:.2f}%")
        
        return ensemble_rmse, ensemble_r2
    
    def save_model(self):
        """Save the complete ensemble model"""
        print("💾 Saving ensemble model...")
        
        model_data = {
            'scaler': self.scaler,
            'crop_encoder': self.crop_encoder,
            'state_encoder': self.state_encoder,
            'season_encoder': self.season_encoder,
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
            self.state_encoder = model_data['state_encoder']
            self.season_encoder = model_data['season_encoder']
            self.base_models = model_data['base_models']
            self.meta_model = model_data['meta_model']
            self.features = model_data['features']
            
            print("   Model loaded successfully!")
            return True
        return False
    
    def predict_yield(self, area, annual_rainfall, fertilizer, pesticide, crop, state, season):
        """Predict crop yield for given conditions"""
        try:
            # Encode categorical inputs
            crop_encoded = self.crop_encoder.transform([crop])[0]
            state_encoded = self.state_encoder.transform([state])[0]
            season_encoded = self.season_encoder.transform([season])[0]
            
            # Prepare input
            input_data = np.array([[area, annual_rainfall, fertilizer, pesticide, crop_encoded, state_encoded, season_encoded]])
            
            # Scale numerical features
            input_scaled = input_data.copy()
            numerical_indices = [0, 1, 2, 3]
            input_scaled[:, numerical_indices] = self.scaler.transform(input_data[:, numerical_indices])
            
            # Get ensemble prediction and base predictions
            ensemble_pred, base_preds = self.predict_ensemble(input_scaled)
            
            # Calculate prediction confidence (inverse of prediction variance)
            pred_variance = np.var(base_preds[0])
            confidence = 1 / (1 + pred_variance)
            
            return {
                'predicted_yield': float(ensemble_pred[0]),
                'confidence': float(confidence),
                'base_predictions': {
                    name: float(pred) 
                    for name, pred in zip(self.base_models.keys(), base_preds[0])
                }
            }
            
        except ValueError as e:
            return {
                'error': f"Unknown crop, state, or season: {e}",
                'available_crops': list(self.crop_encoder.classes_),
                'available_states': list(self.state_encoder.classes_),
                'available_seasons': list(self.season_encoder.classes_)
            }
    
    def train_complete_pipeline(self):
        """Complete training pipeline"""
        print("📊 Starting Crop Yield Prediction Model Training...")
        print("=" * 60)
        
        # Load and prepare data
        X_train, X_test, y_train, y_test = self.load_and_prepare_data()
        
        # Create and train models
        self.create_base_models()
        base_predictions = self.train_base_models(X_train, y_train)
        self.train_meta_model(base_predictions, y_train)
        
        # Evaluate model
        rmse, r2 = self.evaluate_model(X_test, y_test)
        
        # Save model
        self.save_model()
        
        print("=" * 60)
        print("✅ Crop Yield Prediction Model Training Complete!")
        print(f"🎯 Final Ensemble RMSE: {rmse:.4f}")
        print(f"🎯 Final Ensemble R²: {r2:.4f}")
        
        return rmse, r2

def main():
    """Main training function"""
    model = CropYieldPredictionModel()
    
    # Check if model exists
    if model.load_model():
        print("Model already trained. Skipping training...")
        
        # Test prediction
        test_result = model.predict_yield(100, 1200, 120, 0.5, "Rice", "West Bengal", "Kharif")
        print(f"\nTest Prediction: {test_result}")
    else:
        # Train new model
        rmse, r2 = model.train_complete_pipeline()
        
        # Test prediction
        test_result = model.predict_yield(100, 1200, 120, 0.5, "Rice", "West Bengal", "Kharif")
        print(f"\nTest Prediction: {test_result}")

if __name__ == "__main__":
    main()