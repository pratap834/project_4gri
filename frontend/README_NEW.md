# 🌾 FarmWise Analytics - Agricultural AI Dashboard

## 🎯 Overview

FarmWise Analytics is a comprehensive agricultural intelligence platform that combines AI-powered crop management with user data logging, SMS notifications, and resource tracking. Built with Next.js 14, MongoDB, and integrated with Clerk authentication.

---

## ✨ Features

### 🤖 AI-Powered Analysis
1. **Crop Recommendation** (89.5% accuracy) - Smart crop selection based on soil & climate
2. **Fertilizer Optimization** (90.9% accuracy) - Precise NPK recommendations
3. **Yield Prediction** (89.4% R² score) - Accurate harvest forecasting
4. **Disease Detection** (98.8% accuracy) - 38+ plant disease identification

### 📊 User Management (Feature 1 - ✅ Complete)
1. **User Profile System**
   - Personal information management
   - Farm details configuration
   - Address and contact info
   - Notification preferences

2. **Crops Log** (Backend ✅ | UI ⏳)
   - Track planting and harvest dates
   - Monitor crop status and yield
   - Store soil and weather data
   - Link to resources

3. **Resources Log** (Backend ✅ | UI ⏳)
   - Track seeds, fertilizers, pesticides
   - Financial cost management
   - Supplier information
   - Payment status tracking

4. **SMS Notifications** (✅ Complete)
   - Crop harvest reminders
   - Weather alerts
   - Resource low warnings
   - Disease detection alerts
   - Market price updates

### 🚧 Upcoming Features
2. **Government Schemes** - Subsidies and scheme information
3. **Weather Forecasts** - 1, 3, 6 month predictions
4. **Pesticide Allocation** - Photo-based leaf analysis
5. **Equipment Rentals** - Marketplace for farm equipment
6. **Agricultural News** - Latest farming news and updates
7. **Market Price Prediction** - Crop price forecasting

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Icons:** Font Awesome 6.4
- **Authentication:** Clerk

### Backend
- **API:** Next.js API Routes (Serverless)
- **Database:** MongoDB with Mongoose ODM
- **SMS:** Twilio API
- **ML Models:** TensorFlow, Scikit-learn, XGBoost

### AI/ML
- **Crop Recommendation:** Stacking Ensemble
- **Fertilizer Optimization:** Voting Ensemble  
- **Yield Prediction:** Regression Ensemble
- **Disease Detection:** Deep CNN

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- MongoDB (Atlas or Local)
- Clerk Account
- Twilio Account (optional, for SMS)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd farmwise-nextjs

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env.local
# Edit .env.local with your credentials

# Run development server
npm run dev

# Open http://localhost:3000
```

### Environment Variables

Create `.env.local`:

```env
# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/

# MongoDB
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/farmwise_analytics

# Twilio SMS (Optional)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

---

## 📚 Documentation

- **[MongoDB Setup Guide](./MONGODB_SETUP.md)** - Complete MongoDB + Twilio configuration
- **[Feature 1 Status](./FEATURE_1_COMPLETE.md)** - User Log System implementation details
- **[API Documentation](./API_DOCS.md)** - API endpoints reference (coming soon)

---

## 🗄️ Database Schema

### UserProfile
```javascript
{
  clerkId: String (unique),
  name: String,
  email: String,
  phone: String,
  address: {
    street, city, state, pincode, country
  },
  farmDetails: {
    farmName, totalArea, areaUnit, soilType, irrigationType[]
  },
  preferences: {
    smsNotifications, emailNotifications, language
  }
}
```

### CropLog
```javascript
{
  userId: String,
  cropName: String,
  cropType: Enum,
  plantingDate: Date,
  expectedHarvestDate: Date,
  area: Number,
  status: Enum (Planned|Planted|Growing|Harvested|Failed),
  season: Enum (Kharif|Rabi|Zaid|Perennial),
  yieldExpected: Number,
  soilData: { N, P, K, pH },
  weatherData: { temp, rainfall, humidity }
}
```

### ResourceLog
```javascript
{
  userId: String,
  resourceType: Enum (Seed|Fertilizer|Pesticide|Equipment|Labor|Water|Fuel),
  resourceName: String,
  quantity: Number,
  costPerUnit: Number,
  totalCost: Number,
  transactionDate: Date,
  supplier: { name, contact, address },
  paymentStatus: Enum (Paid|Pending|Partial)
}
```

---

## 🔌 API Endpoints

### User Profile
- `GET /api/user/profile` - Get user profile
- `POST /api/user/profile` - Create profile
- `PUT /api/user/profile` - Update profile

### Crops Management
- `GET /api/crops` - List crops (with filters)
- `POST /api/crops` - Create crop log
- `GET /api/crops/[id]` - Get specific crop
- `PUT /api/crops/[id]` - Update crop
- `DELETE /api/crops/[id]` - Delete crop

### Resources Management
- `GET /api/resources` - List resources (with summary)
- `POST /api/resources` - Create resource log
- `GET /api/resources/[id]` - Get specific resource
- `PUT /api/resources/[id]` - Update resource
- `DELETE /api/resources/[id]` - Delete resource

### Notifications
- `POST /api/notifications/sms` - Send SMS notification

---

## 📱 SMS Notification Types

```javascript
// Crop Reminder
SMSTemplates.cropReminder(cropName, daysUntilHarvest)

// Weather Alert
SMSTemplates.weatherAlert(type, severity)

// Resource Low
SMSTemplates.resourceLow(resourceName)

// Disease Detection
SMSTemplates.diseaseDetection(cropName, diseaseName)

// Market Price
SMSTemplates.marketPrice(cropName, price)

// Custom Message
SMSTemplates.general(message)
```

---

## 🎨 UI Pages

- `/` - Main dashboard with AI modules
- `/sign-in` - Authentication (Clerk)
- `/sign-up` - Registration (Clerk)
- `/profile` - User profile management ✅
- `/crops` - Crops tracking (coming soon)
- `/resources` - Resources management (coming soon)
- `/crop-recommendation` - AI crop recommendations
- `/fertilizer-recommendation` - AI fertilizer suggestions
- `/yield-prediction` - AI yield forecasting
- `/disease-detection` - AI disease identification

---

## 🧪 Testing

### Manual Testing
```bash
# Start development server
npm run dev

# Test MongoDB connection
# Check console for: ✅ MongoDB connected successfully

# Test Profile Creation
1. Navigate to /profile
2. Fill in user details
3. Save profile
4. Verify in MongoDB

# Test SMS (if configured)
1. Add phone number in profile
2. Enable SMS notifications
3. Use API endpoint to test
```

### API Testing
```bash
# Test profile endpoint
curl http://localhost:3000/api/user/profile

# Test crops endpoint
curl http://localhost:3000/api/crops

# Test SMS endpoint
curl -X POST http://localhost:3000/api/notifications/sms \
  -H "Content-Type: application/json" \
  -d '{"customMessage": "Test SMS"}'
```

---

## 🔐 Security

- ✅ Clerk authentication on all routes
- ✅ User data isolation (clerkId-based)
- ✅ Input validation and sanitization
- ✅ MongoDB injection prevention
- ✅ Environment variable protection
- ✅ HTTPS-ready configuration

---

## 📈 Performance

- **API Response:** < 200ms (optimized queries)
- **Database:** Indexed for fast lookups
- **SMS Delivery:** < 5 seconds
- **Page Load:** < 1 second
- **Scalability:** MongoDB Atlas auto-scaling

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 Project Structure

```
farmwise-nextjs/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── sign-in/[[...sign-in]]/page.tsx
│   │   │   └── sign-up/[[...sign-up]]/page.tsx
│   │   ├── api/
│   │   │   ├── user/profile/route.ts
│   │   │   ├── crops/
│   │   │   ├── resources/
│   │   │   └── notifications/sms/route.ts
│   │   ├── profile/page.tsx
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   └── Dashboard.tsx
│   ├── lib/
│   │   ├── mongodb.ts
│   │   └── sms.ts
│   ├── models/
│   │   ├── UserProfile.ts
│   │   ├── CropLog.ts
│   │   └── ResourceLog.ts
│   └── middleware.ts
├── .env.local
├── package.json
├── next.config.js
├── tailwind.config.js
└── tsconfig.json
```

---

## 🐛 Troubleshooting

### MongoDB Connection Issues
```
Error: MongoNetworkError
- Check MONGODB_URI format
- Verify IP whitelist in Atlas
- Ensure MongoDB service is running
```

### SMS Not Sending
```
Error: SMS service not configured
- Add Twilio credentials to .env.local
- Restart development server
- Check phone number format (+91...)
```

### Authentication Errors
```
Error: Unauthorized
- Ensure signed in with Clerk
- Check Clerk keys in .env.local
- Clear browser cookies and retry
```

---

## 📊 Feature Roadmap

### Phase 1 (Current) ✅
- [x] MongoDB integration
- [x] User profile system
- [x] Crops log backend
- [x] Resources log backend
- [x] SMS notifications
- [x] Profile UI

### Phase 2 (In Progress)
- [ ] Crops management UI
- [ ] Resources management UI
- [ ] Dashboard widgets

### Phase 3 (Next)
- [ ] Government schemes database
- [ ] Weather API integration
- [ ] Photo upload for disease detection
- [ ] Equipment rental marketplace
- [ ] News aggregation
- [ ] Market price prediction

---

## 📄 License

This project is part of an agricultural AI initiative. Contact for licensing information.

---

## 🙏 Acknowledgments

- **Clerk** - Authentication platform
- **MongoDB Atlas** - Database hosting
- **Twilio** - SMS service
- **Next.js** - React framework
- **Vercel** - Deployment platform

---

## 📧 Support

For issues and questions:
1. Check documentation files
2. Review troubleshooting section
3. Check console logs for errors
4. Verify environment variables

---

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

---

**Built with ❤️ for farmers and agriculture**

**🌾 Cultivating the future of farming through technology**

