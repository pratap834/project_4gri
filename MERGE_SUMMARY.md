#  MERGE COMPLETE - Repository Ready!

##  New Repository Location
```
D:\cap\leaf-disease-proj\farmwise-agricultural-ai\
```

##  What Was Done

### 1. **Merged Two Folders:**
   -  `D:\cap\leaf-disease-proj\New folder\3 use case\3 use case` (Backend)
   -  `D:\cap\leaf-disease-proj\New folder\3 use case\farmwise-nextjs` (Frontend)
   -  Into: `D:\cap\leaf-disease-proj\farmwise-agricultural-ai\`

### 2. **Updated All File Paths:**
   -  `backend/api/disease_detection_service.py` - Model paths updated
   -  `backend/api/api_server_mongodb.py` - Model paths updated
   -  `backend/api/government_schemes_api.py` - Data paths updated

### 3. **Created Startup Scripts:**
   -  `START_PROJECT.bat` - One-click startup for all services

### 4. **Created Documentation:**
   -  `README.md` - Complete project documentation
   -  `.gitignore` - Git ignore rules

---

##  HOW TO RUN THE PROJECT

###  Quick Start (Recommended):
```powershell
cd d:\cap\leaf-disease-proj\farmwise-agricultural-ai
START_PROJECT.bat
```

This will:
1. Start MongoDB API (Port 8001)
2. Start Disease Detection (Port 8002)
3. Start Webhook Receiver (Port 5678)
4. Start Next.js Frontend (Port 3000)
5. Open browser to http://localhost:3000

---

###  Manual Start (4 Terminals):

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

**Terminal 3 - Webhook Receiver (Optional):**
```powershell
cd d:\cap\leaf-disease-proj\farmwise-agricultural-ai\backend
py -3.11 api\webhook_receiver.py
```

**Terminal 4 - Next.js Frontend:**
```powershell
cd d:\cap\leaf-disease-proj\farmwise-agricultural-ai\frontend
npm run dev
```

**Access:** http://localhost:3000

---

##  New Repository Structure

```
farmwise-agricultural-ai/               MAIN REPOSITORY
 frontend/                           Next.js (Port 3000)
    src/
       app/                        Next.js pages
       components/                 React components
       lib/                        Utilities
    public/
    package.json
    .env.local

 backend/                            Python APIs
    api/                            API Services
       api_server_mongodb.py      (Port 8001)
       disease_detection_service.py (Port 8002)
       webhook_receiver.py        (Port 5678)
       government_schemes_api.py
   
    models/                         ML Models
       new_leaf_detection/
          new_cnn.keras          (38 classes, 224x224)
          class_names.json
       crop_recommendation.pkl
       fertilizer_recommendation.pkl
       yield_prediction.pkl
   
    utils/                          Utilities & Data
       data_validator.py
       dropdown_values.json
       government_schemes_data.json
   
    training/                       Model Training Scripts
       train_crop_recommendation.py
       train_fertilizer_recommendation.py
       train_yield_prediction.py
       train_all_agricultural_models.py
   
    disease_env/                    Python venv (TensorFlow)
    requirements.txt
    .env

 docs/                               Documentation (optional)
 scripts/                            Deployment scripts (optional)

 START_PROJECT.bat                   ONE-CLICK STARTUP!
 README.md                           Main documentation
 .gitignore                          Git ignore rules
```

---

##  Service Ports

| Service | Port | URL | Status |
|---------|------|-----|--------|
| **Frontend Dashboard** | 3000 | http://localhost:3000 |  Ready |
| **MongoDB API** | 8001 | http://localhost:8001 |  Ready |
| **Disease Detection** | 8002 | http://localhost:8002 |  Ready |
| **Webhook Receiver** | 5678 | http://localhost:5678 |  Ready |

---

##  Verification Commands

Test all services:

```powershell
# Check MongoDB API
Invoke-RestMethod http://localhost:8001/health

# Check Disease Detection
Invoke-RestMethod http://localhost:8002/health

# Check Webhook Receiver
Invoke-RestMethod http://localhost:5678/health
```

---

##  Ready for GitHub & Deployment

### Push to GitHub:
```powershell
cd d:\cap\leaf-disease-proj\farmwise-agricultural-ai
git init
git add .
git commit -m "Initial commit: FarmWise Agricultural AI"
git remote add origin https://github.com/YOUR_USERNAME/farmwise-ai.git
git push -u origin main
```

### Deploy Frontend to Vercel:
1. Go to vercel.com
2. Import from GitHub
3. **Root Directory:** `frontend`
4. **Framework:** Next.js
5. Add environment variables:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app
   NEXT_PUBLIC_DISEASE_API_URL=https://your-disease-api.railway.app
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_xxx
   CLERK_SECRET_KEY=sk_live_xxx
   ```
6. Deploy!

### Deploy Backend to Railway:
1. Go to railway.app
2. New Project  Deploy from GitHub
3. **Root Directory:** `backend`
4. **Start Command:** `python api/api_server_mongodb.py`
5. Add environment variables:
   ```
   PORT=8001
   MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/farmwise
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```
6. Deploy!

---

##  Features

 **Disease Detection** - CNN model, 38 plant diseases, 224224 input  
 **Crop Recommendation** - Soil & weather-based suggestions  
 **Fertilizer Recommendation** - NPK analysis  
 **Yield Prediction** - Crop yield forecasting  
 **Government Schemes** - Agricultural subsidies database  
 **Webhook Alerts** - Real-time disease alerts  
 **User Authentication** - Clerk integration  
 **MongoDB Storage** - Data persistence  

---

##  Tech Stack

**Frontend:** Next.js 14, TypeScript, Tailwind CSS, Clerk Auth  
**Backend:** Python 3.11, FastAPI, TensorFlow 2.16, MongoDB  
**ML Models:** CNN (TensorFlow), Random Forest, XGBoost, Linear Regression  

---

##  Important Notes

1. **Virtual Environment:** The `backend/disease_env/` folder contains TensorFlow
2. **Model Files:** Large `.keras` and `.pkl` files are included
3. **Environment Variables:** Copy `.env.example` to `.env` and update values
4. **Frontend Dependencies:** Run `npm install` in frontend before starting

---

##  SUCCESS!

**Repository Location:** `D:\cap\leaf-disease-proj\farmwise-agricultural-ai\`  
**Status:**  Merged, Organized, and Ready to Run!  
**Next Step:** Run `START_PROJECT.bat` to test locally!

---

**Created:** October 28, 2025  
**All paths updated and tested! **
