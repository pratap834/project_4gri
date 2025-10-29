"""
Simple Webhook Receiver for Disease Detection Alerts
Runs on port 5678 and logs all incoming webhooks
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import json

app = FastAPI(title="Webhook Receiver")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store received webhooks in memory
webhook_history = []

@app.get("/")
async def root():
    return {
        "service": "Webhook Receiver",
        "status": "running",
        "port": 5678,
        "endpoints": {
            "webhook": "/webhook-test/trigger-email-alert",
            "history": "/webhook-history",
            "latest": "/webhook-latest"
        },
        "received_count": len(webhook_history)
    }

@app.post("/webhook-test/trigger-email-alert")
async def receive_webhook(request: Request):
    """Receive disease detection webhook alerts"""
    try:
        # Get the JSON payload
        payload = await request.json()
        
        # Add receipt timestamp
        received_at = datetime.now().isoformat()
        
        # Store webhook data
        webhook_data = {
            "received_at": received_at,
            "payload": payload
        }
        webhook_history.append(webhook_data)
        
        # Keep only last 100 webhooks
        if len(webhook_history) > 100:
            webhook_history.pop(0)
        
        # Print to console with formatting
        print("\n" + "="*80)
        print(f"🔔 WEBHOOK ALERT RECEIVED at {received_at}")
        print("="*80)
        
        if "prediction" in payload:
            pred = payload["prediction"]
            print(f"\n📊 PREDICTION DETAILS:")
            print(f"   Plant:       {pred.get('plant', 'N/A')}")
            print(f"   Disease:     {pred.get('disease', 'N/A')}")
            print(f"   Confidence:  {pred.get('confidence', 0)}%")
            print(f"   Severity:    {pred.get('severity', 'N/A')}")
            print(f"   Healthy:     {'Yes' if pred.get('is_healthy') else 'No'}")
        
        if "user_input" in payload:
            user = payload["user_input"]
            print(f"\n👤 USER INPUT:")
            print(f"   Filename:    {user.get('filename', 'N/A')}")
            print(f"   Type:        {user.get('content_type', 'N/A')}")
            print(f"   Uploaded:    {user.get('upload_time', 'N/A')}")
        
        if "model_info" in payload:
            model = payload["model_info"]
            print(f"\n🤖 MODEL INFO:")
            print(f"   Model:       {model.get('model_name', 'N/A')}")
            print(f"   Input Size:  {model.get('input_size', 'N/A')}")
            print(f"   Classes:     {model.get('num_classes', 0)}")
        
        if "prediction" in payload and "recommendations" in payload["prediction"]:
            rec = payload["prediction"]["recommendations"]
            print(f"\n💊 RECOMMENDATIONS:")
            if rec.get('treatment'):
                print(f"   Treatment:   {rec['treatment'][:60]}...")
            if rec.get('prevention'):
                print(f"   Prevention:  {', '.join(rec['prevention'][:2])}...")
        
        print("\n" + "="*80)
        print(f"✅ Total webhooks received: {len(webhook_history)}")
        print("="*80 + "\n")
        
        # Return success response
        return {
            "status": "success",
            "message": "Webhook received successfully",
            "received_at": received_at,
            "total_received": len(webhook_history)
        }
        
    except Exception as e:
        print(f"\n❌ ERROR receiving webhook: {str(e)}\n")
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/webhook-history")
async def get_webhook_history(limit: int = 10):
    """Get webhook history (last N webhooks)"""
    return {
        "total_count": len(webhook_history),
        "limit": limit,
        "webhooks": webhook_history[-limit:]
    }

@app.get("/webhook-latest")
async def get_latest_webhook():
    """Get the most recent webhook"""
    if webhook_history:
        return {
            "found": True,
            "webhook": webhook_history[-1]
        }
    else:
        return {
            "found": False,
            "message": "No webhooks received yet"
        }

@app.delete("/webhook-history")
async def clear_webhook_history():
    """Clear all webhook history"""
    count = len(webhook_history)
    webhook_history.clear()
    return {
        "status": "success",
        "message": f"Cleared {count} webhooks from history"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "webhook_receiver",
        "port": 5678,
        "webhooks_received": len(webhook_history)
    }

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🔔 WEBHOOK RECEIVER STARTING")
    print("="*80)
    print(f"Listening on: http://0.0.0.0:5678")
    print(f"Webhook URL:  http://localhost:5678/webhook-test/trigger-email-alert")
    print(f"History URL:  http://localhost:5678/webhook-history")
    print(f"Latest URL:   http://localhost:5678/webhook-latest")
    print("="*80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=5678, log_level="info")
