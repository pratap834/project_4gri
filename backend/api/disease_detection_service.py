"""
Disease Detection Microservice - Fixed Version
Runs separately on port 8002 with Python 3.10/3.11 (TensorFlow compatible)
Handles model version incompatibilities
Integrated with MongoDB and Gemini AI for historical analysis
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from tensorflow import keras  # TensorFlow 2.18 has integrated Keras
import numpy as np
from PIL import Image
import io
import json
import os
import httpx
from datetime import datetime
import asyncio
from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Optional
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

load_dotenv()

app = FastAPI(title="Disease Detection Service")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
disease_model = None
disease_classes = None
mongo_client = None
db = None

def get_default_disease_classes():
    """Return default disease classes for common plant diseases"""
    return [
        'Apple___Apple_scab',
        'Apple___Black_rot',
        'Apple___Cedar_apple_rust',
        'Apple___healthy',
        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
        'Corn_(maize)___Common_rust_',
        'Corn_(maize)___Northern_Leaf_Blight',
        'Corn_(maize)___healthy',
        'Grape___Black_rot',
        'Grape___Esca_(Black_Measles)',
        'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
        'Grape___healthy',
        'Potato___Early_blight',
        'Potato___Late_blight',
        'Potato___healthy',
        'Rice___Brown_Spot',
        'Rice___Leaf_Blast',
        'Rice___Neck_Blast',
        'Rice___healthy',
        'Tomato___Bacterial_spot',
        'Tomato___Early_blight',
        'Tomato___Late_blight',
        'Tomato___Leaf_Mold',
        'Tomato___Septoria_leaf_spot',
        'Tomato___Spider_mites Two-spotted_spider_mite',
        'Tomato___Target_Spot',
        'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
        'Tomato___Tomato_mosaic_virus',
        'Tomato___healthy',
        'Wheat___Brown_rust',
        'Wheat___Yellow_rust',
        'Wheat___healthy'
    ]

# Load model and connect to MongoDB on startup
@app.on_event("startup")
async def load_disease_model():
    global disease_model, disease_classes, mongo_client, db
    
    # Connect to MongoDB
    try:
        mongodb_uri = os.getenv("MONGODB_URI")
        mongodb_db_name = os.getenv("MONGODB_DB_NAME", "farmwise_agricultural_ai")
        
        if mongodb_uri:
            mongo_client = MongoClient(mongodb_uri)
            db = mongo_client[mongodb_db_name]
            mongo_client.server_info()  # Test connection
            print("✓ MongoDB connected successfully")
            print(f"  - Database: {mongodb_db_name}")
            
            # Create disease_predictions collection if it doesn't exist
            if "disease_predictions" not in db.list_collection_names():
                db.create_collection("disease_predictions")
                print("✓ disease_predictions collection created")
        else:
            print("⚠ MongoDB URI not found - running without database")
    except Exception as e:
        print(f"⚠ MongoDB connection failed: {e}")
    
    # Preferred new CNN model path and class names
    new_model_dir = os.path.join(os.path.dirname(__file__), "..", "models", "new_leaf_detection")
    preferred_model_path = os.path.join(new_model_dir, "new_cnn.keras")
    class_names_path = os.path.join(new_model_dir, "class_names.json")
    
    # Fallback models to try in order of preference (legacy)
    model_paths = [
        preferred_model_path,
        os.path.join(new_model_dir, "balanced_cnn_lowmem.keras"),
        os.path.join(os.path.dirname(__file__), "..", "models", "new1plant_disease_model.keras"),
        os.path.join(os.path.dirname(__file__), "..", "models", "efficient_cnn_model (1).keras"),
        os.path.join(os.path.dirname(__file__), "..", "models", "trained in another", "disease_detection_universal.keras"),
    ]
    
    for model_path in model_paths:
        if not os.path.exists(model_path):
            print(f"! Model not found: {model_path}")
            continue
            
        try:
            print(f"Attempting to load: {model_path}")
            disease_model = keras.models.load_model(model_path, compile=False)
            print(f" Disease detection model loaded from {model_path}")
            print(f"  Model input shape: {disease_model.input_shape}")
            print(f"  Model output shape: {disease_model.output_shape}")
            
            # Load disease classes (prefer JSON from new model folder)
            if os.path.exists(class_names_path):
                try:
                    with open(class_names_path, 'r') as f:
                        disease_classes = json.load(f)
                    print(f" Loaded {len(disease_classes)} class names from {class_names_path}")
                except Exception as e:
                    print(f"! Failed to load class names JSON: {e}")
                    disease_classes = get_default_disease_classes()
                    print(f" Falling back to default classes: {len(disease_classes)}")
            else:
                disease_classes = get_default_disease_classes()
                print(f" Class names JSON not found, using defaults: {len(disease_classes)}")

            # Validate class count vs model output
            try:
                output_classes = disease_model.output_shape[-1] if isinstance(disease_model.output_shape, tuple) else None
                if isinstance(disease_classes, list) and output_classes and len(disease_classes) != int(output_classes):
                    print(f"! Warning: class_names length ({len(disease_classes)}) does not match model outputs ({output_classes})")
            except Exception:
                pass
            break
            
        except Exception as e:
            print(f"! Failed to load {model_path}: {str(e)}")
            continue
    
    if disease_model is None:
        print("! WARNING: No disease detection model could be loaded")
        disease_classes = get_default_disease_classes()

def preprocess_image(image_data: bytes, target_size=(224, 224)):
    """Preprocess uploaded image for model prediction"""
    try:
        image = Image.open(io.BytesIO(image_data))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.resize(target_size)
        img_array = np.array(image, dtype=np.float32)
        # Normalize to [0, 1] range as per training (rescale=1./255)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

def parse_disease_name(class_name: str):
    """Parse disease class name into plant and disease"""
    try:
        parts = class_name.split('___')
        if len(parts) == 2:
            plant = parts[0].replace('_', ' ').replace('(', '').replace(')', '')
            disease = parts[1].replace('_', ' ')
            return plant, disease
        return class_name, "Unknown"
    except:
        return class_name, "Unknown"

@app.get("/")
async def root():
    return {
        "service": "Disease Detection Microservice",
        "status": "running",
        "model_loaded": disease_model is not None,
        "num_classes": len(disease_classes) if isinstance(disease_classes, list) else 0,
        "tensorflow_version": tf.__version__,
        "endpoints": ["/health", "/api/detect-disease"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": disease_model is not None,
        "tensorflow_version": tf.__version__,
        "num_classes": len(disease_classes) if isinstance(disease_classes, list) else 0
    }

@app.get("/classes")
async def list_classes():
    """Return the list of disease class names used by the model."""
    classes_list = disease_classes if isinstance(disease_classes, list) else []
    return {
        "count": len(classes_list),
        "classes": classes_list
    }

@app.get("/webhook-config")
async def get_webhook_config():
    """Get webhook configuration"""
    return {
        "webhook_url": "http://localhost:5678/webhook-test/trigger-email-alert",
        "enabled": True,
        "description": "Sends prediction alerts after each disease detection"
    }

@app.post("/test-webhook")
async def test_webhook():
    """Test webhook connectivity"""
    test_data = {
        "plant": "Test Plant",
        "disease": "Test Disease",
        "confidence": 95.5,
        "is_healthy": False,
        "severity": "High",
        "top_predictions": [],
        "recommendations": {}
    }
    
    test_input = {
        "filename": "test_image.jpg",
        "content_type": "image/jpeg",
        "upload_time": datetime.now().isoformat()
    }
    
    success = await send_webhook_alert(test_data, test_input)
    
    return {
        "success": success,
        "webhook_url": "http://localhost:5678/webhook-test/trigger-email-alert",
        "message": "Webhook test completed" if success else "Webhook test failed"
    }

@app.post("/api/detect-disease")
async def detect_disease(
    file: UploadFile = File(...),
    userId: Optional[str] = Form(None),
    prediction_date: Optional[str] = Form(None),
    timeframe: Optional[str] = Form(None)
):
    """Detect plant disease from uploaded image with historical context"""
    try:
        if disease_model is None:
            raise HTTPException(
                status_code=503,
                detail="Disease detection model not loaded. Check server logs for details."
            )
        
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image (JPEG, PNG, etc.)"
            )
        
        # Read and preprocess image
        image_data = await file.read()
        processed_image = preprocess_image(image_data)
        
        # Make prediction
        predictions = disease_model.predict(processed_image, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        # Prepare classes list safely
        classes_list = disease_classes if isinstance(disease_classes, list) else []
        
        # Get predicted class name
        if predicted_class_idx < len(classes_list):
            predicted_class = classes_list[predicted_class_idx]
        else:
            predicted_class = f"Class_{predicted_class_idx}"
        
        # Parse disease information
        plant_name, disease_name = parse_disease_name(predicted_class)
        
        # Get top 3 predictions
        top_3_indices = np.argsort(predictions[0])[-3:][::-1]
        top_predictions = []
        for idx in top_3_indices:
            if idx < len(classes_list):
                class_name = classes_list[idx]
                plant, disease = parse_disease_name(class_name)
                top_predictions.append({
                    "plant": plant,
                    "disease": disease,
                    "confidence": round(float(predictions[0][idx]) * 100, 2)
                })
        
        # Determine if plant is healthy
        is_healthy = 'healthy' in disease_name.lower()
        
        # Generate recommendations
        recommendations = generate_recommendations(plant_name, disease_name, is_healthy)
        
        # Prepare response
        result = {
            "success": True,
            "plant": plant_name,
            "disease": disease_name,
            "confidence": round(confidence * 100, 2),
            "is_healthy": is_healthy,
            "top_predictions": top_predictions,
            "recommendations": recommendations,
            "severity": get_severity(confidence, is_healthy)
        }
        
        # Save to MongoDB and generate Gemini AI notification if userId provided
        notification_message = None
        if db is not None and userId:
            try:
                # Save prediction to database
                prediction_record = {
                    "userId": userId,
                    "predictionType": "disease_detection",
                    "timestamp": datetime.utcnow(),
                    "prediction_date": prediction_date,
                    "timeframe": timeframe,
                    "input": {
                        "filename": file.filename,
                        "content_type": file.content_type
                    },
                    "result": result
                }
                db.disease_predictions.insert_one(prediction_record)
                print(f"✓ Disease prediction saved for user: {userId}")
                
                # Fetch previous predictions for historical analysis
                previous_predictions = list(db.disease_predictions.find(
                    {"userId": userId},
                    {"_id": 0}
                ).sort("timestamp", -1).skip(1).limit(5))
                
                # Generate Gemini AI notification (import will be added)
                try:
                    from utils.gemini_service import generate_disease_notification
                    notification_message = generate_disease_notification(
                        prediction_record,
                        previous_predictions
                    )
                    result["notification"] = notification_message
                except ImportError:
                    print("⚠ Gemini service not available")
                except Exception as e:
                    print(f"⚠ Failed to generate Gemini notification: {e}")
                    
            except Exception as e:
                print(f"⚠ Failed to save prediction: {e}")
        
        # Send webhook alert asynchronously (don't wait for response)
        user_input_data = {
            "filename": file.filename,
            "content_type": file.content_type,
            "upload_time": datetime.now().isoformat()
        }
        asyncio.create_task(send_webhook_alert(result, user_input_data))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

def get_severity(confidence: float, is_healthy: bool) -> str:
    if is_healthy:
        return "None"
    elif confidence > 0.9:
        return "High"
    elif confidence > 0.7:
        return "Moderate"
    else:
        return "Low"

async def send_webhook_alert(prediction_data: dict, user_input: dict = None):
    """Send prediction alert to webhook URL"""
    webhook_url = "http://localhost:5678/webhook-test/trigger-email-alert"
    
    try:
        # Prepare webhook payload
        payload = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "disease_prediction",
            "prediction": {
                "plant": prediction_data.get("plant"),
                "disease": prediction_data.get("disease"),
                "confidence": prediction_data.get("confidence"),
                "is_healthy": prediction_data.get("is_healthy"),
                "severity": prediction_data.get("severity"),
                "top_predictions": prediction_data.get("top_predictions", []),
                "recommendations": prediction_data.get("recommendations", {})
            },
            "user_input": user_input or {},
            "model_info": {
                "model_name": "new_cnn.keras",
                "input_size": "224x224",
                "num_classes": len(disease_classes) if disease_classes else 0
            }
        }
        
        # Send webhook asynchronously with timeout
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(webhook_url, json=payload)
            
            if response.status_code == 200:
                print(f"? Webhook alert sent successfully to {webhook_url}")
                return True
            else:
                print(f"? Webhook returned status code: {response.status_code}")
                return False
                
    except httpx.TimeoutException:
        print(f"? Webhook timeout - {webhook_url} did not respond in time")
        return False
    except Exception as e:
        print(f"? Failed to send webhook alert: {str(e)}")
        return False

def generate_recommendations(plant: str, disease: str, is_healthy: bool):
    """Generate treatment recommendations"""
    if is_healthy:
        return {
            "treatment": "No treatment needed - plant appears healthy",
            "prevention": [
                "Continue regular monitoring",
                "Maintain proper irrigation",
                "Ensure adequate nutrition",
                "Practice crop rotation"
            ],
            "pesticides": []
        }
    
    recommendations_db = {
        "Apple scab": {
            "treatment": "Apply fungicides during early spring when leaves are emerging",
            "prevention": ["Remove fallen leaves", "Prune for air circulation", "Apply dormant spray"],
            "pesticides": ["Captan", "Myclobutanil", "Mancozeb"]
        },
        "Black rot": {
            "treatment": "Remove infected plant parts immediately",
            "prevention": ["Good sanitation", "Avoid overhead irrigation", "Preventive fungicides"],
            "pesticides": ["Copper fungicides", "Mancozeb", "Chlorothalonil"]
        },
        "Early blight": {
            "treatment": "Apply fungicide at first sign of disease",
            "prevention": ["Disease-resistant varieties", "Crop rotation", "Mulch around plants"],
            "pesticides": ["Chlorothalonil", "Mancozeb", "Copper fungicide"]
        },
        "Late blight": {
            "treatment": "Apply fungicide immediately - spreads rapidly",
            "prevention": ["Certified disease-free seeds", "Good air circulation", "Remove infected plants"],
            "pesticides": ["Chlorothalonil", "Mancozeb", "Copper hydroxide"]
        },
        "Leaf Blast": {
            "treatment": "Apply systemic fungicides",
            "prevention": ["Resistant varieties", "Proper water management", "Balanced fertilization"],
            "pesticides": ["Tricyclazole", "Carbendazim", "Azoxystrobin"]
        },
        "Common rust": {
            "treatment": "Apply fungicide when first pustules appear",
            "prevention": ["Plant resistant hybrids", "Early planting", "Avoid late-season nitrogen"],
            "pesticides": ["Azoxystrobin", "Propiconazole", "Tebuconazole"]
        }
    }
    
    for key, value in recommendations_db.items():
        if key.lower() in disease.lower():
            return value
    
    return {
        "treatment": "Consult local agricultural extension for specific treatment",
        "prevention": [
            "Monitor plants regularly",
            "Remove infected plant parts",
            "Maintain proper spacing",
            "Practice crop rotation"
        ],
        "pesticides": ["Consult agricultural expert"]
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Disease Detection Service on port 8002...")
    uvicorn.run(app, host="0.0.0.0", port=8002)
