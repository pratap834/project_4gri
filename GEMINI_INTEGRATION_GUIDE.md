# Gemini AI Integration - Implementation Guide

## Overview
This document describes the integration of Google's Gemini AI API into the FarmWise Agricultural AI platform to provide intelligent insights, notifications, and detailed reports for crop recommendations, fertilizer recommendations, and yield predictions.

## Features Implemented

### 1. **Automatic AI Notifications**
- **When**: Automatically generated whenever a user makes a prediction
- **What**: Short, actionable 2-sentence notifications providing key insights
- **Where**: Displayed at the top of prediction results in a blue notification box
- **Types**:
  - Crop Recommendation Notifications
  - Fertilizer Recommendation Notifications (with soil improvement analysis)
  - Yield Prediction Notifications (with comparison to previous predictions)

### 2. **Detailed AI Reports**
- **When**: Generated on-demand by clicking the "Generate Detailed Report" button
- **What**: Comprehensive, professional reports with:
  - Executive Summary
  - Historical Analysis (comparison with up to 5 previous predictions)
  - Soil Health Assessment (for fertilizer reports)
  - Actionable Steps
  - Professional Advice
  - Trend Analysis
- **Where**: Displayed below prediction results in an expandable section

### 3. **Prediction History Integration**
- All predictions are stored in MongoDB with timestamps
- Gemini AI analyzes historical data to provide context-aware suggestions
- Tracks changes in:
  - Soil NPK levels (fertilizer predictions)
  - Crop recommendations over time
  - Yield trends and improvements

## Technical Architecture

### Backend Components

#### 1. **Gemini Service Module** (`backend/utils/gemini_service.py`)
Contains the following functions:

- `generate_crop_notification()` - Short notification for crop recommendations
- `generate_fertilizer_notification()` - Short notification for fertilizer with soil context
- `generate_yield_notification()` - Short notification for yield predictions
- `generate_crop_detailed_report()` - Comprehensive crop recommendation report
- `generate_fertilizer_detailed_report()` - Detailed soil health and improvement analysis
- `generate_yield_detailed_report()` - Complete yield analysis with historical comparison

#### 2. **Updated API Endpoints** (`backend/api/api_server_mongodb.py`)

**Modified Endpoints:**
- `POST /api/predict-crop` - Now includes `notification` field in response
- `POST /api/predict-fertilizer` - Now includes `notification` field in response
- `POST /api/predict-yield` - Now includes `notification` field in response

**New Endpoints:**
- `POST /api/generate-detailed-report?userId={userId}&predictionType={type}`
  - Parameters:
    - `userId`: User's Clerk ID
    - `predictionType`: 'crop', 'fertilizer', or 'yield'
  - Returns: Detailed AI-generated report with historical analysis

### Frontend Components

#### Updated Pages:
1. **Crop Recommendation Page** (`frontend/src/app/crop-recommendation/page.tsx`)
2. **Fertilizer Recommendation Page** (`frontend/src/app/fertilizer-recommendation/page.tsx`)
3. **Yield Prediction Page** (`frontend/src/app/yield-prediction/page.tsx`)

#### New Features in Each Page:
- Import and use `useUser()` hook from Clerk
- Send `userId` with prediction requests
- Display AI notification in blue alert box
- "Generate Detailed Report" button (only visible to logged-in users)
- Expandable detailed report section with close button
- Loading states for report generation

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

New packages added:
- `google-generativeai==0.3.2` - Gemini AI SDK
- `fastapi==0.104.1` - Already included for API
- `pymongo==4.6.0` - Already included for MongoDB

### 2. Environment Variables

Create or update `.env` file in the `backend` directory:

```env
# MongoDB Configuration
MONGODB_URI=your_mongodb_connection_string
MONGODB_DB_NAME=farmwise_agricultural_ai

# Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here
```

**How to get Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

### 3. Start the Backend Server

```bash
cd backend/api
python api_server_mongodb.py
```

The server will run on `http://localhost:8001`

### 4. Start the Frontend

```bash
cd frontend
npm install  # if not already done
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage Flow

### Making a Prediction with AI Insights

1. **User navigates to any prediction page**
   - Crop Recommendation
   - Fertilizer Recommendation
   - Yield Prediction

2. **User fills out the form and submits**
   - System makes prediction using ML models
   - Prediction is saved to MongoDB with userId
   - Gemini AI automatically generates a notification
   - Both prediction and notification are returned

3. **User sees results with AI notification**
   - Prediction results displayed as before
   - Blue notification box appears with AI insights
   - Notification provides context-aware suggestions

4. **User clicks "Generate Detailed Report" (optional)**
   - System fetches last 5 predictions from MongoDB
   - Gemini AI generates comprehensive report
   - Report includes:
     - Historical comparison
     - Trend analysis
     - Soil improvement analysis (fertilizer)
     - Actionable steps
     - Professional advice

### Report Content Examples

#### Crop Recommendation Report Includes:
- Executive Summary
- Soil Health Analysis with NPK trends
- Crop Recommendation Rationale
- Comparison with Previous Recommendations
- Actionable Steps (4-5 specific actions)
- Professional Advice

#### Fertilizer Recommendation Report Includes:
- Executive Summary
- Soil Health Assessment
- **What Happened to the Soil Since Last Application**
- **Current Soil Improvement Analysis**
- Fertilizer Recommendation Rationale
- Application Guidelines
- Actionable Steps
- Professional Advice for Long-term Soil Health

#### Yield Prediction Report Includes:
- Executive Summary
- Yield Prediction Analysis
- Comparison with Previous Predictions
- Factors Influencing Yield
- Optimization Opportunities
- Actionable Steps
- Professional Advice
- Financial Projection Considerations

## Key Features for Each Prediction Type

### Crop Recommendations
- **Notification**: Highlights recommended crop and soil suitability
- **Report**: Compares NPK levels across predictions, analyzes pH trends

### Fertilizer Recommendations
- **Notification**: Emphasizes NPK changes and soil improvement
- **Report**: 
  - ✅ Analyzes what happened to soil since last fertilizer application
  - ✅ Shows nutrient level changes (increases/decreases)
  - ✅ Explains causes of soil changes
  - ✅ Provides soil improvement status

### Yield Predictions
- **Notification**: Shows yield change percentage from previous predictions
- **Report**:
  - ✅ Compares current yield with previous predictions
  - ✅ Analyzes impact of fertilizer and pesticide changes
  - ✅ Provides optimization suggestions
  - ✅ Includes financial considerations

## Data Flow

```
User Makes Prediction
    ↓
Frontend sends request with userId
    ↓
Backend processes with ML model
    ↓
Prediction saved to MongoDB
    ↓
Backend fetches previous predictions (up to 5)
    ↓
Gemini AI generates notification
    ↓
Response returned with prediction + notification
    ↓
Frontend displays results
    ↓
User clicks "Generate Report" (optional)
    ↓
Backend fetches latest prediction + history
    ↓
Gemini AI generates detailed report
    ↓
Report displayed on frontend
```

## MongoDB Collections Structure

### Crop Predictions Collection
```json
{
  "userId": "user_clerk_id",
  "predictionType": "crop_recommendation",
  "timestamp": "2025-10-29T10:30:00Z",
  "input": {
    "N": 90, "P": 42, "K": 43,
    "temperature": 20.8,
    "humidity": 82,
    "ph": 6.5,
    "rainfall": 202.9
  },
  "result": {
    "recommended_crop": "rice",
    "confidence": 95.5,
    "notification": "AI generated notification..."
  }
}
```

### Fertilizer Predictions Collection
```json
{
  "userId": "user_clerk_id",
  "predictionType": "fertilizer_recommendation",
  "timestamp": "2025-10-29T10:30:00Z",
  "input": {
    "temperature": 26,
    "humidity": 52,
    "moisture": 38,
    "soil_type": "Sandy",
    "crop_type": "Maize",
    "nitrogen": 37,
    "phosphorous": 0,
    "potassium": 0
  },
  "result": {
    "recommended_fertilizer": "Urea",
    "confidence": 92.3,
    "npk_values": {...},
    "notification": "AI generated notification..."
  }
}
```

### Yield Predictions Collection
```json
{
  "userId": "user_clerk_id",
  "predictionType": "yield_prediction",
  "timestamp": "2025-10-29T10:30:00Z",
  "input": {
    "crop": "Rice",
    "season": "Kharif",
    "state": "Punjab",
    "area": 100,
    "annual_rainfall": 1200,
    "fertilizer": 150,
    "pesticide": 50
  },
  "result": {
    "predicted_yield": 4.5,
    "yield_unit": "tonnes per hectare",
    "notification": "AI generated notification..."
  }
}
```

## Error Handling

### Backend
- If Gemini API key is not configured:
  - Notifications return fallback messages
  - Reports return error with clear message
- If MongoDB is not connected:
  - Predictions still work
  - No history-based insights
  - User sees warning

### Frontend
- Loading states during report generation
- Error messages displayed in red alert boxes
- Graceful fallback if API is unavailable
- Sign-in prompt for guest users

## Security Considerations

1. **API Key Security**
   - Gemini API key stored in `.env` (never committed to Git)
   - Server-side only - not exposed to frontend

2. **User Authentication**
   - Reports only available to authenticated users
   - userId from Clerk used for data isolation
   - Each user only sees their own predictions

3. **Rate Limiting**
   - Consider implementing rate limits for report generation
   - Monitor Gemini API usage and costs

## Cost Considerations

- **Gemini API Pricing**: Check [Google AI Pricing](https://ai.google.dev/pricing)
- **Free Tier**: Gemini 1.5 Flash has generous free tier
- Each prediction generates ~1 short notification
- Each report generates ~1 detailed analysis
- Monitor usage in Google Cloud Console

## Testing Checklist

- [ ] Backend server starts without errors
- [ ] MongoDB connection successful
- [ ] Gemini API key configured
- [ ] Make crop prediction - notification appears
- [ ] Make fertilizer prediction - notification appears
- [ ] Make yield prediction - notification appears
- [ ] Click "Generate Report" for crop - report displays
- [ ] Click "Generate Report" for fertilizer - report displays
- [ ] Click "Generate Report" for yield - report displays
- [ ] Make second prediction - notification references previous one
- [ ] Report shows comparison with previous predictions
- [ ] Test with guest user (no userId) - predictions work
- [ ] Test report button without login - appropriate message shown

## Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution**: Add `GEMINI_API_KEY=your_key` to `backend/.env`

### Issue: No notification appearing
**Solution**: 
- Check backend console for errors
- Verify Gemini API key is valid
- Check MongoDB connection

### Issue: Report shows "No predictions found"
**Solution**:
- Make sure user is logged in
- Verify userId is being sent with requests
- Check MongoDB contains predictions for that user

### Issue: Reports are too generic
**Solution**:
- Make multiple predictions to build history
- Gemini AI becomes more contextual with more data

## Future Enhancements

1. **Email Reports**: Send detailed reports via email
2. **SMS Notifications**: Send short notifications via SMS
3. **Report Scheduling**: Weekly/monthly summary reports
4. **Custom Prompts**: Allow farmers to ask specific questions
5. **Multi-language**: Generate reports in local languages
6. **PDF Export**: Download reports as PDF
7. **Visualization**: Add charts for historical trends
8. **Push Notifications**: Real-time alerts for important insights

## Support

For issues or questions:
1. Check this documentation
2. Review backend console logs
3. Check MongoDB for data
4. Verify API keys in `.env`
5. Test with simple prediction first

---

**Implementation Complete**: All features have been implemented and are ready for testing.

**Next Step**: Test the complete flow by starting the backend and frontend servers and making predictions.
