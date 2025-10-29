"""
FastAPI server with MongoDB integration for user profiles and prediction history
Runs on port 8001 and provides endpoints for crop, fertilizer, and yield prediction
All predictions are saved to MongoDB with user mapping
"""
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import joblib
import numpy as np
import pandas as pd
import os
from collections import Counter
import httpx
import asyncio
from datetime import datetime
from typing import Optional, List
from pymongo import MongoClient
from dotenv import load_dotenv
import traceback
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.gemini_service import (
    generate_crop_notification,
    generate_fertilizer_notification,
    generate_yield_notification,
    generate_crop_detailed_report,
    generate_fertilizer_detailed_report,
    generate_yield_detailed_report
)

# Load environment variables
load_dotenv()

# MongoDB connection
mongo_client = None
db = None

# Global model instances
crop_model_data = None
fertilizer_model_data = None
yield_model_data = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global crop_model_data, fertilizer_model_data, yield_model_data
    global mongo_client, db
    
    # Connect to MongoDB
    try:
        mongodb_uri = os.getenv("MONGODB_URI")
        mongodb_db_name = os.getenv("MONGODB_DB_NAME", "farmwise_agricultural_ai")
        
        if mongodb_uri:
            mongo_client = MongoClient(mongodb_uri)
            db = mongo_client[mongodb_db_name]
            # Test connection
            mongo_client.server_info()
            print("✓ MongoDB connected successfully")
            print(f"  - Database: {mongodb_db_name}")
            
            # Create collections if they don't exist
            if "user_profiles" not in db.list_collection_names():
                db.create_collection("user_profiles")
            if "crop_predictions" not in db.list_collection_names():
                db.create_collection("crop_predictions")
            if "fertilizer_predictions" not in db.list_collection_names():
                db.create_collection("fertilizer_predictions")
            if "yield_predictions" not in db.list_collection_names():
                db.create_collection("yield_predictions")
            
            print("✓ MongoDB collections initialized")
        else:
            print("⚠ MongoDB URI not found in environment variables")
            print("  - Running without database persistence")
    except Exception as e:
        print(f"⚠ MongoDB connection failed: {e}")
        print("  - Running without database persistence")
    
    # Load ML models
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    
    try:
        # Load crop recommendation model
        crop_model_data = joblib.load(os.path.join(models_dir, 'crop_recommendation_ensemble.pkl'))
        print("✓ Crop recommendation model loaded")
        
        # Load fertilizer recommendation model
        fertilizer_model_data = joblib.load(os.path.join(models_dir, 'fertilizer_recommendation_ensemble.pkl'))
        print("✓ Fertilizer recommendation model loaded")
        
        # Load yield prediction model
        yield_model_data = joblib.load(os.path.join(models_dir, 'yield_prediction_ensemble.pkl'))
        print("✓ Yield prediction model loaded")
        
    except Exception as e:
        print(f"Error loading models: {e}")
        traceback.print_exc()
    
    yield
    
    # Shutdown
    if mongo_client:
        mongo_client.close()
        print("✓ MongoDB connection closed")

app = FastAPI(title="Agricultural AI Models API with MongoDB", lifespan=lifespan)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class CropRecommendationRequest(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float
    userId: Optional[str] = "guest_user"  # Default to guest_user if not provided

class FertilizerRecommendationRequest(BaseModel):
    temperature: float
    humidity: float
    moisture: float
    soil_type: str
    crop_type: str
    nitrogen: float
    phosphorous: float
    potassium: float
    userId: Optional[str] = "guest_user"  # Default to guest_user if not provided
    prediction_date: Optional[str] = None  # Date when prediction is made
    timeframe: Optional[str] = None  # Expected timeframe for results (e.g., "1 month", "3 months")

class YieldPredictionRequest(BaseModel):
    crop: str
    season: str
    state: str
    area: float
    production: float
    annual_rainfall: float
    fertilizer: float
    pesticide: float
    userId: Optional[str] = "guest_user"  # Default to guest_user if not provided
    prediction_date: Optional[str] = None  # Date when prediction is made
    timeframe: Optional[str] = None  # Expected timeframe for harvest (e.g., "3 months", "6 months")

class UserProfile(BaseModel):
    userId: str
    name: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
    location: Optional[str] = ""
    farmSize: Optional[str] = ""
    experience: Optional[str] = ""

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Agricultural AI Models API with MongoDB & Gemini AI",
        "status": "running",
        "database": "MongoDB" if db is not None else "In-Memory",
        "available_endpoints": [
            "/api/predict-crop",
            "/api/predict-fertilizer",
            "/api/predict-yield",
            "/api/user/profile",
            "/api/user/prediction-history",
            "/api/generate-detailed-report"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": {
            "crop": crop_model_data is not None,
            "fertilizer": fertilizer_model_data is not None,
            "yield": yield_model_data is not None
        },
        "database": {
            "connected": db is not None,
            "type": "MongoDB" if db is not None else "In-Memory"
        }
    }

@app.post("/api/predict-crop")
async def predict_crop(request: CropRecommendationRequest):
    try:
        if crop_model_data is None:
            raise HTTPException(status_code=503, detail="Crop model not loaded")
        
        # Extract components
        scaler = crop_model_data['scaler']
        label_encoder = crop_model_data['label_encoder']
        base_models = crop_model_data['base_models']
        meta_model = crop_model_data['meta_model']
        
        # Prepare input features
        features = np.array([[
            request.N, request.P, request.K,
            request.temperature, request.humidity,
            request.ph, request.rainfall
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Get base model predictions
        base_predictions = []
        base_predictions_list = []
        for name, model in base_models.items():
            pred = model.predict(features_scaled)
            base_predictions.append(pred[0])
            base_predictions_list.append(pred)
        
        # Prepare meta features
        meta_features = np.column_stack(base_predictions_list)
        
        # Final prediction
        final_prediction = meta_model.predict(meta_features)[0]
        
        # Decode crop name
        recommended_crop = label_encoder.inverse_transform([final_prediction])[0]
        
        # Calculate confidence from base models
        prediction_counts = Counter(base_predictions)
        most_common = prediction_counts.most_common()
        confidence = most_common[0][1] / len(base_predictions) * 100
        
        # Get top 3 alternatives
        alternatives = []
        for crop_encoded, count in most_common[1:4]:
            try:
                crop_name = label_encoder.inverse_transform([crop_encoded])[0]
                alternatives.append({
                    "crop": crop_name,
                    "confidence": round(count / len(base_predictions) * 100, 2)
                })
            except:
                pass
        
        result = {
            "success": True,
            "recommended_crop": recommended_crop,
            "confidence": round(confidence, 2),
            "alternatives": alternatives,
            "soil_analysis": {
                "nitrogen": request.N,
                "phosphorus": request.P,
                "potassium": request.K,
                "ph": request.ph
            },
            "environmental_conditions": {
                "temperature": request.temperature,
                "humidity": request.humidity,
                "rainfall": request.rainfall
            }
        }
        
        # Save to MongoDB and generate notification if userId provided and db connected
        notification_message = None
        if db is not None and request.userId:
            try:
                prediction_record = {
                    "userId": request.userId,
                    "predictionType": "crop_recommendation",
                    "timestamp": datetime.utcnow(),
                    "input": {
                        "N": request.N,
                        "P": request.P,
                        "K": request.K,
                        "temperature": request.temperature,
                        "humidity": request.humidity,
                        "ph": request.ph,
                        "rainfall": request.rainfall
                    },
                    "result": result
                }
                db.crop_predictions.insert_one(prediction_record)
                print(f"✓ Crop prediction saved for user: {request.userId}")
                
                # Fetch previous predictions for context
                previous_predictions = list(db.crop_predictions.find(
                    {"userId": request.userId},
                    {"_id": 0}
                ).sort("timestamp", -1).skip(1).limit(5))
                
                # Generate AI notification
                notification_message = generate_crop_notification(
                    prediction_record,
                    previous_predictions
                )
                result["notification"] = notification_message
                
            except Exception as e:
                print(f"⚠ Failed to save prediction or generate notification: {e}")
        
        return result
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predict-fertilizer")
async def predict_fertilizer(request: FertilizerRecommendationRequest):
    try:
        if fertilizer_model_data is None:
            raise HTTPException(status_code=503, detail="Fertilizer model not loaded")
        
        # Extract components
        scaler = fertilizer_model_data['scaler']
        fertilizer_encoder = fertilizer_model_data['fertilizer_encoder']
        base_models = fertilizer_model_data['base_models']
        meta_model = fertilizer_model_data['meta_model']
        
        # Encode categorical features
        soil_type_mapping = {"Sandy": 0, "Loamy": 1, "Black": 2, "Red": 3, "Clayey": 4}
        crop_type_mapping = {
            "Maize": 0, "Sugarcane": 1, "Cotton": 2, "Tobacco": 3, "Paddy": 4, 
            "Barley": 5, "Wheat": 6, "Millets": 7, "Oil seeds": 8, "Pulses": 9, 
            "Ground Nuts": 10
        }
        
        soil_type_encoded = soil_type_mapping.get(request.soil_type, 0)
        crop_type_encoded = crop_type_mapping.get(request.crop_type, 0)
        
        # Prepare input features
        features = np.array([[
            request.nitrogen, request.phosphorous, request.potassium,
            7.0,  # pH - default value
            200.0,  # Rainfall - default value
            request.temperature,
            crop_type_encoded,
            soil_type_encoded
        ]])
        
        # Scale only numerical features (first 6)
        features_scaled = features.copy()
        features_scaled[:, :6] = scaler.transform(features[:, :6])
        
        # Get base model predictions
        base_predictions = []
        base_predictions_list = []
        for name, model in base_models.items():
            pred = model.predict(features_scaled)
            base_predictions.append(pred[0])
            base_predictions_list.append(pred)
        
        # Prepare meta features
        meta_features = np.column_stack(base_predictions_list)
        
        # Final prediction
        final_prediction = meta_model.predict(meta_features)[0]
        
        # Decode fertilizer name
        recommended_fertilizer = fertilizer_encoder.inverse_transform([final_prediction])[0]
        
        # Calculate confidence
        prediction_counts = Counter(base_predictions)
        most_common = prediction_counts.most_common()
        confidence = most_common[0][1] / len(base_predictions) * 100
        
        result = {
            "success": True,
            "recommended_fertilizer": recommended_fertilizer,
            "confidence": round(confidence, 2),
            "npk_values": {
                "nitrogen": request.nitrogen,
                "phosphorous": request.phosphorous,
                "potassium": request.potassium
            },
            "soil_conditions": {
                "soil_type": request.soil_type,
                "moisture": request.moisture,
                "temperature": request.temperature,
                "humidity": request.humidity
            },
            "crop_type": request.crop_type
        }
        
        # Save to MongoDB and generate notification if userId provided and db connected
        notification_message = None
        if db is not None and request.userId:
            try:
                prediction_record = {
                    "userId": request.userId,
                    "predictionType": "fertilizer_recommendation",
                    "timestamp": datetime.utcnow(),
                    "prediction_date": request.prediction_date,
                    "timeframe": request.timeframe,
                    "input": {
                        "temperature": request.temperature,
                        "humidity": request.humidity,
                        "moisture": request.moisture,
                        "soil_type": request.soil_type,
                        "crop_type": request.crop_type,
                        "nitrogen": request.nitrogen,
                        "phosphorous": request.phosphorous,
                        "potassium": request.potassium
                    },
                    "result": result
                }
                db.fertilizer_predictions.insert_one(prediction_record)
                print(f"✓ Fertilizer prediction saved for user: {request.userId}")
                
                # Fetch previous predictions for context
                previous_predictions = list(db.fertilizer_predictions.find(
                    {"userId": request.userId},
                    {"_id": 0}
                ).sort("timestamp", -1).skip(1).limit(5))
                
                # Generate AI notification
                notification_message = generate_fertilizer_notification(
                    prediction_record,
                    previous_predictions
                )
                result["notification"] = notification_message
                
            except Exception as e:
                print(f"⚠ Failed to save prediction or generate notification: {e}")
        
        return result
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predict-yield")
async def predict_yield(request: YieldPredictionRequest):
    try:
        if yield_model_data is None:
            raise HTTPException(status_code=503, detail="Yield model not loaded")
        
        # Extract components
        scaler = yield_model_data['scaler']
        base_models = yield_model_data['base_models']
        meta_model = yield_model_data['meta_model']
        
        # Encode categorical features
        crop_mapping = {"Rice": 0, "Wheat": 1, "Maize": 2, "Sugarcane": 3, "Cotton": 4}
        season_mapping = {"Kharif": 0, "Rabi": 1, "Summer": 2, "Whole Year": 3}
        state_mapping = {
            "Andhra Pradesh": 0, "Karnataka": 1, "Maharashtra": 2, "Tamil Nadu": 3,
            "Uttar Pradesh": 4, "West Bengal": 5, "Gujarat": 6, "Madhya Pradesh": 7,
            "Punjab": 8, "Haryana": 9
        }
        
        crop_encoded = crop_mapping.get(request.crop, 0)
        season_encoded = season_mapping.get(request.season, 0)
        state_encoded = state_mapping.get(request.state, 0)
        
        # Prepare input features
        numerical_features = np.array([[
            request.area, request.annual_rainfall, request.fertilizer, request.pesticide
        ]])
        
        # Scale only numerical features
        numerical_scaled = scaler.transform(numerical_features)
        
        # Combine scaled numerical with encoded categorical
        features_scaled = np.concatenate([
            numerical_scaled,
            [[crop_encoded, state_encoded, season_encoded]]
        ], axis=1)
        
        # Get base model predictions
        base_predictions = []
        base_predictions_list = []
        for name, model in base_models.items():
            pred = model.predict(features_scaled)
            base_predictions.append(pred[0])
            base_predictions_list.append(pred)
        
        # Prepare meta features
        meta_features = np.column_stack(base_predictions_list)
        
        # Final prediction
        predicted_yield = meta_model.predict(meta_features)[0]
        
        result = {
            "success": True,
            "predicted_yield": round(float(predicted_yield), 2),
            "yield_unit": "tonnes per hectare",
            "input_parameters": {
                "crop": request.crop,
                "season": request.season,
                "state": request.state,
                "area": request.area,
                "annual_rainfall": request.annual_rainfall,
                "fertilizer": request.fertilizer,
                "pesticide": request.pesticide
            }
        }
        
        # Save to MongoDB and generate notification if userId provided and db connected
        notification_message = None
        if db is not None and request.userId:
            try:
                prediction_record = {
                    "userId": request.userId,
                    "predictionType": "yield_prediction",
                    "timestamp": datetime.utcnow(),
                    "prediction_date": request.prediction_date,
                    "timeframe": request.timeframe,
                    "input": {
                        "crop": request.crop,
                        "season": request.season,
                        "state": request.state,
                        "area": request.area,
                        "production": request.production,
                        "annual_rainfall": request.annual_rainfall,
                        "fertilizer": request.fertilizer,
                        "pesticide": request.pesticide
                    },
                    "result": result
                }
                db.yield_predictions.insert_one(prediction_record)
                print(f"✓ Yield prediction saved for user: {request.userId}")
                
                # Fetch previous predictions for context
                previous_predictions = list(db.yield_predictions.find(
                    {"userId": request.userId},
                    {"_id": 0}
                ).sort("timestamp", -1).skip(1).limit(5))
                
                # Generate AI notification
                notification_message = generate_yield_notification(
                    prediction_record,
                    previous_predictions
                )
                result["notification"] = notification_message
                
            except Exception as e:
                print(f"⚠ Failed to save prediction or generate notification: {e}")
        
        return result
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Profile API Endpoints with MongoDB
@app.get("/api/user/profile")
async def get_profile(userId: str):
    """Get user profile from MongoDB"""
    try:
        if db is None:
            raise HTTPException(status_code=503, detail="Database not connected")
        
        profile = db.user_profiles.find_one({"userId": userId}, {"_id": 0})
        
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/profile")
async def create_profile(profile: UserProfile):
    """Create new user profile in MongoDB"""
    try:
        if db is None:
            raise HTTPException(status_code=503, detail="Database not connected")
        
        # Check if profile already exists
        existing = db.user_profiles.find_one({"userId": profile.userId})
        if existing:
            raise HTTPException(status_code=400, detail="Profile already exists. Use PUT to update.")
        
        profile_dict = profile.dict()
        profile_dict["createdAt"] = datetime.utcnow()
        profile_dict["updatedAt"] = datetime.utcnow()
        
        db.user_profiles.insert_one(profile_dict)
        
        return {
            "success": True,
            "message": "Profile created successfully",
            "profile": profile.dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/user/profile")
async def update_profile(profile: UserProfile):
    """Update existing user profile in MongoDB"""
    try:
        if db is None:
            raise HTTPException(status_code=503, detail="Database not connected")
        
        profile_dict = profile.dict()
        profile_dict["updatedAt"] = datetime.utcnow()
        
        result = db.user_profiles.update_one(
            {"userId": profile.userId},
            {"$set": profile_dict},
            upsert=True
        )
        
        return {
            "success": True,
            "message": "Profile updated successfully",
            "profile": profile.dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/prediction-history")
async def get_prediction_history(userId: str, predictionType: Optional[str] = None, limit: int = 50):
    """Get user's prediction history from MongoDB"""
    try:
        if db is None:
            raise HTTPException(status_code=503, detail="Database not connected")
        
        history = {
            "userId": userId,
            "crop_predictions": [],
            "fertilizer_predictions": [],
            "yield_predictions": []
        }
        
        # Get crop predictions
        if predictionType is None or predictionType == "crop":
            crop_preds = list(db.crop_predictions.find(
                {"userId": userId},
                {"_id": 0}
            ).sort("timestamp", -1).limit(limit))
            history["crop_predictions"] = crop_preds
        
        # Get fertilizer predictions
        if predictionType is None or predictionType == "fertilizer":
            fert_preds = list(db.fertilizer_predictions.find(
                {"userId": userId},
                {"_id": 0}
            ).sort("timestamp", -1).limit(limit))
            history["fertilizer_predictions"] = fert_preds
        
        # Get yield predictions
        if predictionType is None or predictionType == "yield":
            yield_preds = list(db.yield_predictions.find(
                {"userId": userId},
                {"_id": 0}
            ).sort("timestamp", -1).limit(limit))
            history["yield_predictions"] = yield_preds
        
        return history
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/user/prediction-history")
async def delete_prediction_history(userId: str):
    """Delete all prediction history for a user"""
    try:
        if db is None:
            raise HTTPException(status_code=503, detail="Database not connected")
        
        crop_result = db.crop_predictions.delete_many({"userId": userId})
        fert_result = db.fertilizer_predictions.delete_many({"userId": userId})
        yield_result = db.yield_predictions.delete_many({"userId": userId})
        
        return {
            "success": True,
            "message": "Prediction history deleted",
            "deleted": {
                "crop_predictions": crop_result.deleted_count,
                "fertilizer_predictions": fert_result.deleted_count,
                "yield_predictions": yield_result.deleted_count
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Gemini AI Report Generation Endpoints
@app.post("/api/generate-detailed-report")
async def generate_detailed_report(userId: str, predictionType: str):
    """
    Generate a detailed AI-powered report for the latest prediction
    predictionType: 'crop', 'fertilizer', 'yield', or 'disease'
    """
    try:
        if db is None:
            raise HTTPException(status_code=503, detail="Database not connected")
        
        # Fetch the latest prediction
        collection_map = {
            "crop": "crop_predictions",
            "fertilizer": "fertilizer_predictions",
            "yield": "yield_predictions",
            "disease": "disease_predictions"
        }
        
        if predictionType not in collection_map:
            raise HTTPException(status_code=400, detail="Invalid prediction type")
        
        collection_name = collection_map[predictionType]
        collection = db[collection_name]
        
        # Get latest prediction
        latest_prediction = collection.find_one(
            {"userId": userId},
            {"_id": 0},
            sort=[("timestamp", -1)]
        )
        
        if not latest_prediction:
            raise HTTPException(status_code=404, detail="No predictions found for this user")
        
        # Get previous predictions
        previous_predictions = list(collection.find(
            {"userId": userId},
            {"_id": 0}
        ).sort("timestamp", -1).skip(1).limit(5))
        
        # Generate report based on type
        if predictionType == "crop":
            report = generate_crop_detailed_report(latest_prediction, previous_predictions)
        elif predictionType == "fertilizer":
            report = generate_fertilizer_detailed_report(latest_prediction, previous_predictions)
        elif predictionType == "yield":
            report = generate_yield_detailed_report(latest_prediction, previous_predictions)
        elif predictionType == "disease":
            from utils.gemini_service import generate_disease_detailed_report
            report = generate_disease_detailed_report(latest_prediction, previous_predictions)
        
        return report
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
