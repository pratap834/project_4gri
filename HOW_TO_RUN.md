# 🚀 Quick Start Scripts

## Running the Project

### Option 1: Double-Click to Start (Recommended)
Simply **double-click** on `START_PROJECT.bat` to launch the entire application.

This will:
1. Open a **GREEN PowerShell window** for the Backend API (Port 8001)
2. Open a **CYAN PowerShell window** for the Frontend (Port 3000)
3. Automatically open your browser to http://localhost:3000

### Option 2: Command Line
```bash
# Navigate to project root
cd d:\cap\leaf-disease-proj\farmwise-agricultural-ai

# Run the start script
START_PROJECT.bat
```

---

## Stopping the Project

### Option 1: Close Windows
Simply close both PowerShell windows (Backend and Frontend)

### Option 2: Use Stop Script
Double-click on `STOP_PROJECT.bat` or run:
```bash
STOP_PROJECT.bat
```

### Option 3: Manual Stop
Press `Ctrl + C` in each PowerShell window

---

## What Happens When You Start

```
START_PROJECT.bat
    ↓
[Step 1] Launches Backend API Server (Port 8001)
    ↓
[Step 2] Launches Frontend Server (Port 3000)
    ↓
[Step 3] Opens Browser
    ↓
✅ Application Ready!
```

---

## Windows That Will Open

1. **Launcher Window** (This closes after starting everything)
2. **Backend API Window** (Green text - Keep open)
3. **Frontend Window** (Cyan text - Keep open)
4. **Browser** (Automatically opens to http://localhost:3000)

---

## Accessing the Application

| Service | URL | Window Color |
|---------|-----|--------------|
| Frontend | http://localhost:3000 | Cyan |
| Backend API | http://localhost:8001 | Green |
| API Docs | http://localhost:8001/docs | - |

---

## Troubleshooting

### Port Already in Use
If you see "Port already in use":
1. Run `STOP_PROJECT.bat`
2. Wait 5 seconds
3. Run `START_PROJECT.bat` again

### Backend Won't Start
- Check if Python is installed: `python --version`
- Check if dependencies are installed: See `GEMINI_INTEGRATION_GUIDE.md`

### Frontend Won't Start
- Check if Node.js is installed: `node --version`
- Check if dependencies are installed: `cd frontend && npm install`

### Gemini API Not Working
- Get your FREE API key from: https://makersuite.google.com/app/apikey
- Edit `backend/.env` file
- Replace `GEMINI_API_KEY=your_gemini_api_key_here` with your actual key
- Restart backend (close window and run `START_PROJECT.bat` again)

---

## File Structure

```
farmwise-agricultural-ai/
├── START_PROJECT.bat      ← Double-click this to START
├── STOP_PROJECT.bat       ← Double-click this to STOP
├── backend/
│   ├── .env              ← Configure Gemini API key here
│   ├── api/
│   │   └── api_server_mongodb.py
│   └── ...
└── frontend/
    └── ...
```

---

## Quick Commands

| Action | Command |
|--------|---------|
| **Start Everything** | `START_PROJECT.bat` |
| **Stop Everything** | `STOP_PROJECT.bat` |
| **Start Backend Only** | `cd backend\api && python api_server_mongodb.py` |
| **Start Frontend Only** | `cd frontend && npm run dev` |

---

## What Each Server Does

### Backend API (Port 8001) - GREEN Window
- Handles all ML predictions
- Connects to MongoDB
- Generates AI insights with Gemini
- Manages user data

### Frontend (Port 3000) - CYAN Window
- User interface
- Handles user authentication (Clerk)
- Displays predictions and reports
- Communicates with backend API

---

## Tips

💡 **Keep both PowerShell windows open** while using the application

💡 **Check the GREEN window** if predictions aren't working

💡 **Check the CYAN window** if the webpage isn't loading

💡 **Use STOP_PROJECT.bat** before closing your laptop to ensure clean shutdown

---

## Need Help?

See the detailed documentation:
- `QUICK_START.md` - 5-minute setup guide
- `GEMINI_INTEGRATION_GUIDE.md` - Complete technical guide
- `TESTING_GUIDE.md` - Testing instructions
- `IMPLEMENTATION_SUMMARY.md` - Feature overview

---

**Ready to start? Double-click `START_PROJECT.bat`!** 🚀
