# 🚀 Quick Start Guide - Feature 1 Testing

## ⚡ 5-Minute Setup

### Step 1: Install New Dependencies (Already Done ✅)
```bash
cd farmwise-nextjs
npm install
# mongoose and twilio already installed
```

### Step 2: Setup MongoDB

**Option A: MongoDB Atlas (Easiest - 5 minutes)**

1. Go to https://www.mongodb.com/cloud/atlas
2. Click "Try Free" → Sign up
3. Create Organization → Create Project
4. Click "Build a Database"
5. Choose "M0 FREE" tier
6. Select region closest to you
7. Click "Create"
8. Create Database User:
   - Username: `farmwise_admin`
   - Password: (generate strong password, save it!)
9. Add IP Address: Click "Allow Access from Anywhere" (for testing)
10. Click "Finish and Close"
11. Click "Connect" → "Connect your application"
12. Copy connection string
13. Replace `<password>` with your actual password

**Your connection string should look like:**
```
mongodb+srv://farmwise_admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/farmwise_analytics?retryWrites=true&w=majority
```

**Option B: Local MongoDB (If you have MongoDB installed)**
```
mongodb://localhost:27017/farmwise_analytics
```

### Step 3: Update .env.local

Open `.env.local` and update:

```env
# Replace this line:
MONGODB_URI=mongodb://localhost:27017/farmwise_analytics

# With your Atlas connection string:
MONGODB_URI=mongodb+srv://farmwise_admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/farmwise_analytics?retryWrites=true&w=majority
```

### Step 4: Start the Server

```bash
npm run dev
```

### Step 5: Check Console

Look for this message:
```
✅ MongoDB connected successfully
```

If you see it - **SUCCESS!** 🎉

---

## 🧪 Test Feature 1

### Test 1: User Profile

1. Open browser: http://localhost:3000
2. Sign in with Clerk
3. Click "Profile" in navigation
4. Fill in the form:
   ```
   Name: Test Farmer
   Email: test@farmwise.com
   Phone: +919876543210
   City: Mumbai
   State: Maharashtra
   Farm Name: Green Valley Farm
   Total Area: 10
   Unit: acre
   Soil Type: Alluvial
   ```
5. Select irrigation types (click checkboxes)
6. Click "Save Profile"
7. You should see: "Profile saved successfully!"

### Test 2: Verify Database

**Option A: MongoDB Atlas**
1. Go back to MongoDB Atlas
2. Click "Database" → "Browse Collections"
3. You should see:
   - Collection: `userprofiles`
   - 1 document with your data

**Option B: MongoDB Compass (Local)**
1. Open MongoDB Compass
2. Connect to `mongodb://localhost:27017`
3. Database: `farmwise_analytics`
4. Collection: `userprofiles`
5. See your data

### Test 3: API Direct Test

Open browser console and run:

```javascript
// Fetch your profile
fetch('/api/user/profile')
  .then(r => r.json())
  .then(data => console.log('Profile:', data))

// Create a test crop
fetch('/api/crops', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    cropName: 'Wheat',
    cropType: 'Cereal',
    plantingDate: '2025-10-15',
    expectedHarvestDate: '2026-03-15',
    area: 5,
    areaUnit: 'acre',
    status: 'Planted',
    season: 'Rabi'
  })
}).then(r => r.json()).then(data => console.log('Crop created:', data))

// List your crops
fetch('/api/crops')
  .then(r => r.json())
  .then(data => console.log('Crops:', data))
```

---

## 📸 What You Should See

### 1. Profile Page
![Profile Page - Should look like agricultural form with sections]

### 2. Success Message
![Green success banner: "Profile saved successfully!"]

### 3. Console
```
✅ MongoDB connected successfully
GET / 200 in 1234ms
GET /api/user/profile 200 in 123ms
```

### 4. MongoDB Atlas
```
farmwise_analytics
  └── userprofiles
      └── 1 document
```

---

## 🐛 Troubleshooting

### Issue: "MongoDB connection error"

**Check:**
1. MONGODB_URI in .env.local is correct
2. Password doesn't have special characters (use alphanumeric)
3. IP address is whitelisted (0.0.0.0/0 for testing)
4. Internet connection is working

**Solution:**
```bash
# Test connection manually
node -e "const mongoose = require('mongoose'); mongoose.connect('YOUR_MONGODB_URI').then(() => console.log('✅ Connected')).catch(e => console.error('❌ Error:', e.message))"
```

### Issue: "Profile not saving"

**Check:**
1. Signed in with Clerk (see profile icon in navbar)
2. Console for errors (F12 → Console tab)
3. Network tab shows 200 status (F12 → Network → filter by "profile")

**Solution:**
```bash
# Restart server
Ctrl+C
npm run dev
```

### Issue: "Cannot find module 'mongoose'"

**Solution:**
```bash
# Reinstall dependencies
rm -rf node_modules
npm install
```

---

## ✅ Success Criteria

You're ready to proceed if:

- [x] Server starts without errors
- [x] Console shows "✅ MongoDB connected successfully"
- [x] Can access /profile page
- [x] Can save profile successfully
- [x] Profile data appears in MongoDB
- [x] Profile loads after page refresh

---

## 📞 Report Back

### ✅ If Everything Works:

Send message:
```
✅ Feature 1 backend working!
- MongoDB connected
- Profile page working
- Data saving correctly

Ready for Crops UI!
```

### ❌ If Issues:

Send message with:
```
Issue: [describe what's not working]

Console errors: [paste errors]

Screenshot: [attach if possible]

MongoDB connection: [Yes/No]
```

---

## 🎯 Next Steps After Success

Once confirmed working, I will create:

1. **Crops Management Page** (`/crops`)
   - List all crops
   - Add new crop form
   - Edit crop details
   - Delete crops
   - Status updates
   - Filters

2. **Resources Management Page** (`/resources`)
   - List all resources
   - Add resource log
   - Cost tracking
   - Edit/delete
   - Summary charts

3. **Dashboard Widgets**
   - Recent crops
   - Total spending
   - Upcoming harvests

---

## ⏱️ Estimated Time

- MongoDB Atlas setup: 5 minutes
- Testing profile: 2 minutes
- Verification: 1 minute

**Total: ~8 minutes**

---

## 💡 Pro Tips

1. **Use MongoDB Atlas free tier** - no credit card needed
2. **Save your MongoDB password** - you'll need it
3. **Keep console open** - helps debug issues
4. **Test on mobile** - responsive design already done
5. **Clear browser cache** - if page looks broken

---

## 🎓 Learning While Testing

### What You're Testing:
- **Full-stack integration:** React → API → MongoDB
- **Authentication:** Clerk protecting routes
- **Data persistence:** MongoDB storing data
- **Form validation:** Client and server-side
- **TypeScript:** Type-safe database operations

### Architecture:
```
Browser Form
    ↓
Next.js API Route (/api/user/profile)
    ↓
Mongoose Schema Validation
    ↓
MongoDB Database
    ↓
Response to Browser
    ↓
UI Update
```

---

**🚀 Ready? Let's test Feature 1 backend!**

**⏰ Time needed: 8 minutes**

**🎯 Goal: See "✅ MongoDB connected successfully" and save a profile**

