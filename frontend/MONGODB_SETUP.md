# 🗄️ MongoDB Setup Guide for FarmWise Analytics

## Prerequisites

You need a MongoDB database. You can use either:
1. **MongoDB Atlas (Cloud)** - Recommended for production
2. **Local MongoDB** - For development

---

## Option 1: MongoDB Atlas (Cloud - Recommended)

### Step 1: Create Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up for a free account (M0 cluster is free forever)

### Step 2: Create Cluster
1. Click "Build a Database"
2. Choose "Shared" (Free tier)
3. Select your cloud provider and region (choose closest to your location)
4. Name your cluster (e.g., "FarmWise")
5. Click "Create"

### Step 3: Create Database User
1. Go to "Database Access" in left sidebar
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create username and strong password
5. Set "Database User Privileges" to "Read and write to any database"
6. Click "Add User"

### Step 4: Configure Network Access
1. Go to "Network Access" in left sidebar
2. Click "Add IP Address"
3. For development: Click "Allow Access from Anywhere" (0.0.0.0/0)
4. For production: Add your server's IP address
5. Click "Confirm"

### Step 5: Get Connection String
1. Go to "Database" in left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string (looks like: `mongodb+srv://username:<password>@cluster.mongodb.net/?retryWrites=true&w=majority`)
5. Replace `<password>` with your actual password
6. Add database name: `mongodb+srv://username:password@cluster.mongodb.net/farmwise_analytics?retryWrites=true&w=majority`

### Step 6: Update .env.local
```env
MONGODB_URI=mongodb+srv://your_username:your_password@cluster.mongodb.net/farmwise_analytics?retryWrites=true&w=majority
```

---

## Option 2: Local MongoDB

### Step 1: Install MongoDB
**Windows:**
1. Download from [MongoDB Download Center](https://www.mongodb.com/try/download/community)
2. Run the installer
3. Choose "Complete" installation
4. Install as a Service
5. Install MongoDB Compass (GUI tool)

**Mac:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu):**
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

### Step 2: Verify Installation
```bash
mongosh --version
# or
mongo --version
```

### Step 3: Update .env.local
```env
MONGODB_URI=mongodb://localhost:27017/farmwise_analytics
```

---

## Twilio SMS Setup (Optional but Recommended)

### Step 1: Create Twilio Account
1. Go to [Twilio](https://www.twilio.com/try-twilio)
2. Sign up for free account (gets free $15 credit)
3. Verify your email and phone number

### Step 2: Get Credentials
1. Go to [Twilio Console](https://console.twilio.com/)
2. Find your **Account SID** and **Auth Token**
3. Copy these values

### Step 3: Get Phone Number
1. In Twilio Console, go to "Phone Numbers"
2. Click "Buy a Number"
3. Choose a number with SMS capability
4. Purchase it (uses your free credit)

### Step 4: Update .env.local
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

**Note for India:** 
- For sending SMS to Indian numbers, you need to register your Twilio number
- Go to "Regulatory Compliance" in Twilio Console
- Complete Indian regulatory requirements

---

## Verify Setup

### 1. Check MongoDB Connection
Run the development server and check console:
```bash
npm run dev
```

Look for:
```
✅ MongoDB connected successfully
```

### 2. Test API Endpoints

**Create User Profile:**
```bash
curl -X POST http://localhost:3000/api/user/profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Farmer",
    "email": "farmer@test.com",
    "phone": "+919876543210",
    "address": {
      "city": "Mumbai",
      "state": "Maharashtra"
    }
  }'
```

**Get User Profile:**
```bash
curl http://localhost:3000/api/user/profile
```

### 3. Test SMS (if configured)
```bash
curl -X POST http://localhost:3000/api/notifications/sms \
  -H "Content-Type: application/json" \
  -d '{
    "customMessage": "Test SMS from FarmWise Analytics"
  }'
```

---

## Database Collections Created

The system will automatically create these collections:

1. **userprofiles** - User account information
2. **croplogs** - Crop planting and harvest records
3. **resourcelogs** - Farm resource tracking (seeds, fertilizers, etc.)

---

## Troubleshooting

### MongoDB Connection Errors

**Error: "MongoNetworkError"**
- Check if MongoDB service is running
- Verify IP whitelist in Atlas
- Check firewall settings

**Error: "Authentication failed"**
- Verify username and password in connection string
- Check if database user has correct permissions

**Error: "Cannot connect to localhost:27017"**
- Start MongoDB service: `sudo systemctl start mongod` (Linux)
- Or: `brew services start mongodb-community` (Mac)

### Twilio SMS Errors

**Error: "SMS service not configured"**
- Ensure all Twilio environment variables are set
- Restart the development server after adding variables

**Error: "Invalid phone number"**
- Phone numbers must be in E.164 format: +[country code][number]
- Example: +919876543210 (India)

---

## Next Steps

After setup is complete:
1. ✅ MongoDB connected
2. ✅ Twilio SMS configured (optional)
3. 🎯 Start using the User Log features
4. 🎯 Create crops and track resources
5. 🎯 Enable SMS notifications for alerts

---

## Security Best Practices

1. **Never commit .env.local to git**
   ```bash
   # Already in .gitignore
   .env.local
   ```

2. **Use strong passwords** for MongoDB users

3. **Rotate credentials** regularly

4. **Use IP whitelisting** in production

5. **Enable MongoDB encryption** at rest

6. **Use HTTPS** in production

---

## Support

If you encounter issues:
- Check MongoDB Atlas documentation: https://docs.atlas.mongodb.com/
- Check Twilio documentation: https://www.twilio.com/docs
- Verify all environment variables are correctly set
- Check MongoDB service is running
- Review console logs for detailed error messages

