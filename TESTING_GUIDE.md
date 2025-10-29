# Testing Guide - Gemini AI Integration

## Prerequisites

Before testing, ensure you have:
- [ ] MongoDB URI configured in `backend/.env`
- [ ] Gemini API key configured in `backend/.env`
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install` in frontend folder)
- [ ] ML model files in `backend/models/` directory

## Quick Start Testing

### Step 1: Start Backend Server

```powershell
cd backend\api
python api_server_mongodb.py
```

**Expected Output:**
```
✓ MongoDB connected successfully
  - Database: farmwise_agricultural_ai
✓ MongoDB collections initialized
✓ Crop recommendation model loaded
✓ Fertilizer recommendation model loaded
✓ Yield prediction model loaded
```

**If you see warnings:**
- `⚠ MongoDB URI not found` - Add MONGODB_URI to .env
- `⚠ Warning: GEMINI_API_KEY not found` - Add GEMINI_API_KEY to .env
- Models still work without these, but no AI features

### Step 2: Start Frontend

```powershell
cd frontend
npm run dev
```

**Expected Output:**
```
▲ Next.js ready on http://localhost:3000
```

### Step 3: Test Crop Recommendation

1. Open browser: `http://localhost:3000/crop-recommendation`
2. Fill in the form with sample data:
   - **Nitrogen (N)**: 90
   - **Phosphorus (P)**: 42
   - **Potassium (K)**: 43
   - **Temperature**: 20.8
   - **Humidity**: 82
   - **pH**: 6.5
   - **Rainfall**: 202.9

3. Click "Get Recommendation"

**Expected Result:**
- ✅ Prediction shows recommended crop
- ✅ Blue notification box appears with AI insight
- ✅ Confidence level displayed
- ✅ "Generate Detailed Report" button visible (if logged in)

### Step 4: Test Report Generation

1. Click "📄 Generate Detailed Report" button
2. Wait for processing (5-10 seconds)

**Expected Result:**
- ✅ Loading spinner appears
- ✅ Detailed report section expands
- ✅ Report shows:
  - Executive Summary
  - Soil Health Analysis
  - Comparison with Previous Recommendations
  - Actionable Steps
  - Professional Advice

### Step 5: Test Fertilizer Recommendation

1. Navigate to: `http://localhost:3000/fertilizer-recommendation`
2. Fill in the form:
   - **Soil Type**: Sandy
   - **Crop Type**: Maize
   - **Nitrogen**: 37
   - **Phosphorous**: 0
   - **Potassium**: 0
   - **Temperature**: 26
   - **Humidity**: 52
   - **Moisture**: 38

3. Click "Get Recommendation"

**Expected Result:**
- ✅ Fertilizer recommendation displayed
- ✅ AI notification with soil improvement context
- ✅ NPK values shown
- ✅ Report button available

4. Click "Generate Detailed Report"

**Expected in Report:**
- ✅ "What happened to the soil since last application" section
- ✅ NPK change analysis
- ✅ Soil improvement suggestions
- ✅ Application guidelines

### Step 6: Test Yield Prediction

1. Navigate to: `http://localhost:3000/yield-prediction`
2. Fill in the form:
   - **State**: Punjab
   - **Crop**: Rice
   - **Season**: Kharif
   - **Area**: 100 hectares
   - **Previous Production**: 200 tons
   - **Annual Rainfall**: 1200 mm
   - **Fertilizer**: 150 kg/ha
   - **Pesticide**: 50 kg/ha

3. Click "Predict Yield"

**Expected Result:**
- ✅ Predicted yield displayed
- ✅ AI notification with yield context
- ✅ Cultivation summary shown
- ✅ Report button available

4. Click "Generate Detailed Report"

**Expected in Report:**
- ✅ Yield comparison with previous predictions
- ✅ Factors influencing yield
- ✅ Optimization opportunities
- ✅ Financial projection considerations

## Testing Historical Analysis

### Create Prediction History

To test the historical comparison features:

1. **Make First Prediction** (any model)
   - Note the recommendation/result

2. **Change Input Values Slightly**
   - Example for Crop: Change N from 90 to 95
   - Example for Fertilizer: Change moisture from 38 to 45
   - Example for Yield: Change fertilizer from 150 to 160

3. **Make Second Prediction**
   - ✅ Notification should reference previous prediction
   - Example: "Your soil nitrogen has increased by 5..."

4. **Generate Report**
   - ✅ Report should show "Based on 1 previous prediction(s)"
   - ✅ Compare current vs previous values
   - ✅ Analyze trends and improvements

5. **Make 3-5 More Predictions** (over time)
   - ✅ Reports become more detailed
   - ✅ Better trend analysis
   - ✅ More accurate recommendations

## Verification Checklist

### Backend Functionality
- [ ] Server starts without errors
- [ ] MongoDB connection successful
- [ ] All three ML models load successfully
- [ ] Gemini API initializes (check console)
- [ ] Predictions save to MongoDB (check console logs)

### Frontend Functionality
- [ ] All three prediction pages load
- [ ] Forms accept input correctly
- [ ] Prediction results display properly
- [ ] AI notifications appear in blue boxes
- [ ] Report buttons are visible to logged-in users
- [ ] Reports generate and display correctly

### AI Features
- [ ] Notifications are contextual (not generic)
- [ ] Notifications reference previous predictions when available
- [ ] Reports include historical comparison
- [ ] Reports show NPK changes (fertilizer)
- [ ] Reports show yield trends (yield prediction)
- [ ] Reports provide actionable steps

### User Experience
- [ ] Loading states work (spinners during processing)
- [ ] Error messages are clear and helpful
- [ ] Reports are readable and well-formatted
- [ ] Close button on reports works
- [ ] Guest users see appropriate messages

## Common Test Scenarios

### Scenario 1: First-Time User
**Test**: Make prediction without any history
- ✅ Notification should still be helpful
- ✅ Report shows "Based on 0 previous predictions"
- ✅ Report focuses on current conditions only

### Scenario 2: Soil Improvement (Fertilizer)
**Test**: Make two fertilizer predictions with different NPK values

**First Prediction:**
- N: 20, P: 10, K: 15

**Second Prediction:**
- N: 35, P: 25, K: 30

**Expected in Report:**
- ✅ "Nitrogen increased by +15"
- ✅ "Phosphorous increased by +15"
- ✅ "Potassium increased by +15"
- ✅ Explains improvement in soil health
- ✅ Acknowledges previous fertilizer application effectiveness

### Scenario 3: Yield Trend Analysis
**Test**: Make three yield predictions with varying inputs

**Prediction 1:**
- Fertilizer: 100 kg/ha
- Predicted Yield: 3.5 t/ha

**Prediction 2:**
- Fertilizer: 150 kg/ha
- Predicted Yield: 4.2 t/ha

**Prediction 3:**
- Fertilizer: 200 kg/ha
- Predicted Yield: 4.8 t/ha

**Expected in Report:**
- ✅ Shows yield improvement trend
- ✅ Correlates fertilizer increase with yield increase
- ✅ Provides optimization suggestions
- ✅ Calculates percentage improvements

## Troubleshooting Test Issues

### Issue: No notification appears
**Debug Steps:**
1. Check backend console for errors
2. Verify `userId` is being sent in request
3. Check `.env` file has GEMINI_API_KEY
4. Test API key: Visit https://makersuite.google.com/

**Fix:**
```powershell
# Check backend logs
# Look for: "⚠ Warning: GEMINI_API_KEY not found"

# Verify .env file
cd backend
cat .env  # PowerShell: type .env

# Should show:
# GEMINI_API_KEY=AIza...
```

### Issue: Report shows "No predictions found"
**Debug Steps:**
1. Check if user is logged in (Clerk authentication)
2. Verify MongoDB connection
3. Check database for user's predictions

**Fix:**
```powershell
# Check MongoDB connection in backend console
# Should see: "✓ MongoDB connected successfully"

# If not, verify MONGODB_URI in .env
```

### Issue: Report is too generic
**Explanation:** This is normal for first prediction
**Solution:** Make 2-3 more predictions to build history

### Issue: Backend server crashes on prediction
**Debug Steps:**
1. Check if model files exist in `backend/models/`
2. Verify model file names match code
3. Check Python package versions

**Expected Model Files:**
- `backend/models/crop_recommendation_ensemble.pkl`
- `backend/models/fertilizer_recommendation_ensemble.pkl`
- `backend/models/yield_prediction_ensemble.pkl`

## Performance Testing

### Response Times (Expected)
- **Prediction Only**: < 2 seconds
- **Prediction + Notification**: < 5 seconds
- **Detailed Report Generation**: 5-15 seconds

### Optimization Tips
- First prediction after server start may be slower (model loading)
- Subsequent predictions should be faster
- Report generation time depends on Gemini API response

## Data Validation

### Check MongoDB Data
If you have MongoDB Compass or mongo shell:

```javascript
// Connect to your database
use farmwise_agricultural_ai

// Check crop predictions
db.crop_predictions.find({ userId: "your_user_id" }).limit(5)

// Check fertilizer predictions
db.fertilizer_predictions.find({ userId: "your_user_id" }).limit(5)

// Check yield predictions
db.yield_predictions.find({ userId: "your_user_id" }).limit(5)

// Count predictions per user
db.crop_predictions.countDocuments({ userId: "your_user_id" })
```

## Final Testing Checklist

Before considering testing complete:

- [ ] All three prediction types work
- [ ] Notifications appear for all three types
- [ ] Reports generate for all three types
- [ ] Historical comparison works (make 2+ predictions)
- [ ] Soil improvement analysis works (fertilizer)
- [ ] Yield trend analysis works (yield predictions)
- [ ] Guest users can make predictions
- [ ] Logged-in users can generate reports
- [ ] Reports are readable and actionable
- [ ] No errors in browser console
- [ ] No errors in backend console

## Success Criteria

✅ **Integration is successful if:**
1. Users can make predictions as before
2. AI notifications provide helpful context
3. Detailed reports offer actionable insights
4. Historical comparisons show trends
5. Soil improvement analysis is accurate
6. System handles errors gracefully
7. Performance is acceptable (< 15s for reports)

## Next Steps After Testing

1. **User Acceptance Testing**
   - Have actual farmers test the system
   - Gather feedback on AI suggestions
   - Refine prompts based on feedback

2. **Performance Monitoring**
   - Monitor Gemini API usage
   - Track report generation times
   - Optimize if needed

3. **Feature Enhancement**
   - Add PDF export for reports
   - Implement email delivery
   - Add SMS notifications
   - Multi-language support

4. **Production Deployment**
   - Set up production MongoDB
   - Configure production API keys
   - Implement rate limiting
   - Add monitoring and logging

---

**Happy Testing! 🚀**

For issues, refer to the GEMINI_INTEGRATION_GUIDE.md or check the Troubleshooting section above.
