#  FarmWise Agricultural AI Platform

Complete AI-powered agricultural platform with disease detection, crop recommendations, fertilizer suggestions, and yield predictions.

##  Repository Structure

```
farmwise-agricultural-ai/
 frontend/                      # Next.js Dashboard (Port 3000)
    src/
    public/
    package.json
    .env.local
 backend/                       # Python APIs
    api/
       api_server_mongodb.py          # Port 8001
       disease_detection_service.py   # Port 8002
       webhook_receiver.py            # Port 5678
       government_schemes_api.py
    models/
       new_leaf_detection/
          new_cnn.keras              # 38 disease classes, 224x224 input
          class_names.json
       crop_recommendation.pkl
       fertilizer_recommendation.pkl
       yield_prediction.pkl
    utils/
    training/
    disease_env/                       # Python virtual environment
    requirements.txt
 START_PROJECT.bat                      # One-click startup!
```

##  Quick Start

### Method 1: One-Click Start (Recommended)
```powershell
cd d:\cap\leaf-disease-proj\farmwise-agricultural-ai
START_PROJECT.bat
```

This will start all services and open the dashboard!

### Method 2: Manual Start

**Terminal 1 - MongoDB API:**
```powershell
cd d:\cap\leaf-disease-proj\farmwise-agricultural-ai\backend
py -3.11 api\api_server_mongodb.py
```

**Terminal 2 - Disease Detection:**
```powershell
cd d:\cap\leaf-disease-proj\farmwise-agricultural-ai\backend
disease_env\Scripts\python.exe api\disease_detection_service.py
```

**Terminal 3 - Webhook Receiver:**
```powershell
cd d:\cap\leaf-disease-proj\farmwise-agricultural-ai\backend
py -3.11 api\webhook_receiver.py
```

**Terminal 4 - Next.js Frontend:**
```powershell
cd d:\cap\leaf-disease-proj\farmwise-agricultural-ai\frontend
npm install
npm run dev
```

**Access:** http://localhost:3000

##  Features

 **Disease Detection** - Upload plant images, detect 38 diseases using CNN
 **Crop Recommendation** - Get crop suggestions based on soil & weather
 **Fertilizer Recommendation** - NPK analysis and recommendations
 **Yield Prediction** - Predict crop yields
 **Government Schemes** - Agricultural schemes and subsidies
 **Webhook Alerts** - Real-time alerts for disease predictions
 **User Authentication** - Clerk-based auth system
 **MongoDB Integration** - Data persistence

##  Configuration

### Frontend Environment Variables (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_DISEASE_API_URL=http://localhost:8002
NEXT_PUBLIC_WEBHOOK_URL=http://localhost:5678
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_key
CLERK_SECRET_KEY=your_clerk_secret
```

### Backend Environment Variables (`backend/.env`):
```env
MONGODB_URI=mongodb://localhost:27017/farmwise_agricultural_ai
PORT=8001
CORS_ORIGINS=http://localhost:3000
```

##  Tech Stack

**Frontend:**
- Next.js 14
- TypeScript
- Tailwind CSS
- Clerk Auth
- Recharts

**Backend:**
- Python 3.11
- FastAPI
- TensorFlow 2.16
- MongoDB
- Scikit-learn

**ML Models:**
- CNN (new_cnn.keras) - 38 disease classes
- Random Forest - Crop recommendation
- XGBoost - Fertilizer recommendation  
- Linear Regression - Yield prediction

##  Service Ports

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| MongoDB API | 8001 | http://localhost:8001 |
| Disease Detection | 8002 | http://localhost:8002 |
| Webhook Receiver | 5678 | http://localhost:5678 |

##  Documentation

- Disease Detection Model: CNN with 224224 input, 38 classes
- Webhook system sends alerts after each prediction
- All paths updated for new structure

##  Deployment

### Frontend (Vercel):
- Root Directory: `frontend`
- Framework: Next.js
- Build Command: `npm run build`
- Output Directory: `.next`

### Backend (Railway/Render):
- Root Directory: `backend`
- Start Command: `python api/api_server_mongodb.py`
- Python Version: 3.11

##  Verification

Check all services are running:
```powershell
# MongoDB API
Invoke-RestMethod http://localhost:8001/health

# Disease Detection
Invoke-RestMethod http://localhost:8002/health

# Webhook Receiver
Invoke-RestMethod http://localhost:5678/health
```

##  License

MIT License

##  Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

**Repository merged and organized on:** October 28, 2025
**Ready for GitHub and Vercel deployment! **
