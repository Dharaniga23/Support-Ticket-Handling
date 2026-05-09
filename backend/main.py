from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
from pathlib import Path
import os
import asyncio
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))
from ml_engine.inference import TicketModelHandler
from backend.email_service import EmailManager
import pandas as pd
from pathlib import Path
import random

# Initialize FastAPI app
app = FastAPI(
    title="Support Intelligence API",
    description="Unified API for Category, Team, Priority, and Action predictions.",
    version="1.0.0"
)

# Enable CORS for Angular Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI Models on startup
# Initialize AI and Email Managers
handler = TicketModelHandler()
email_manager = EmailManager()

async def email_polling_background_task():
    """Periodically check for new emails in the background."""
    interval = int(os.getenv("POLL_INTERVAL_SECONDS", 300))
    print(f"[STARTUP] Email Polling Service Started (Interval: {interval}s)")
    while True:
        try:
            # IMPORTANT: fetch_emails is synchronous (blocking), so we run it in a thread
            await asyncio.to_thread(email_manager.fetch_emails)
        except Exception as e:
            print(f"[BACKGROUND] Email Polling Error: {e}")
        await asyncio.sleep(interval)

@app.on_event("startup")
async def startup_event():
    print("[SERVER] Backend is ONLINE. AI is set to Lazy-Load on first request.")
    # Start Email Polling in Background
    asyncio.create_task(email_polling_background_task())

# Request/Response Schemas
class TicketRequest(BaseModel):
    description: str

class PredictionResponse(BaseModel):
    category: str
    confidence: float
    team: str
    priority: str
    eta: str
    suggested_action: str
    routing_status: str

class Ticket(BaseModel):
    id: int
    subject: str
    requester: str
    support_team: str
    priority: str
    status: str
    description: str
    resolution: str = ""

from backend.database import fetch_tickets, update_ticket_status, create_ticket
from backend.analytics import calculate_kpis, get_category_distribution, get_prediction_timeline, get_analytics_summary

@app.get("/tickets")
async def get_tickets():
    try:
        # Use new DB function
        return fetch_tickets(limit=100)
    except Exception as e:
        print(f"Backend Error loading tickets: {e}")
        return []

class TicketUpdate(BaseModel):
    status: str = "Solved"
    description: str = None
    assignee: str = None

@app.put("/tickets/{ticket_id}")
async def update_ticket(ticket_id: int, update: TicketUpdate):
    try:
        # Update in SQLite
        update_ticket_status(ticket_id, update.status, update.description)
        
        # Automatically send an email response back to the requester when solved
        if update.status.lower() == "solved" and update.description:
            success = email_manager.send_reply(ticket_id, custom_body=update.description)
            if not success:
                print(f"[WARNING] Could not send reply email for Ticket #{ticket_id}")

        return {"message": "Ticket updated successfully", "id": ticket_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data")
async def get_api_data():
    """Exposes ticket data at a standard /api/data endpoint as requested."""
    return await get_tickets()

@app.get("/")
async def root():
    return {
        "status": "online",
        "connection": "verified",
        "model_handler": "ready",
        "version": "1.0.0"
    }

# ============================================
# Analytics Endpoints
# ============================================

@app.get("/analytics/kpis")
async def get_analytics_kpis():
    """Get key performance indicators for analytics dashboard"""
    try:
        return calculate_kpis()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics Error: {str(e)}")

@app.get("/analytics/categories")
async def get_analytics_categories():
    """Get ticket category distribution for pie chart"""
    try:
        return get_category_distribution()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics Error: {str(e)}")

@app.get("/analytics/timeline")
async def get_analytics_timeline():
    """Get prediction activity timeline for line chart"""
    try:
        return get_prediction_timeline()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics Error: {str(e)}")

@app.get("/analytics/summary")
async def get_analytics_summary_endpoint():
    """Get complete analytics summary (all data in one call)"""
    try:
        return get_analytics_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics Error: {str(e)}")

# ============================================
# ML Prediction Endpoint
# ============================================

@app.post("/predict", response_model=PredictionResponse)
async def predict_ticket(request: TicketRequest):
    if not request.description.strip():
        raise HTTPException(status_code=400, detail="Ticket description cannot be empty")
    
    try:
        results = handler.predict(request.description)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction Error: {str(e)}")

class NewTicketRequest(BaseModel):
    subject: str
    requester: str
    description: str

@app.post("/api/tickets")
async def create_new_ticket(request: NewTicketRequest):
    if not request.description.strip():
        raise HTTPException(status_code=400, detail="Ticket description cannot be empty")
    
    try:
        # Run AI prediction
        prediction = handler.predict(request.description)
        
        # Save to database
        ticket_id = create_ticket(
            subject=request.subject,
            requester=request.requester,
            support_team=prediction['team'],
            priority=prediction['priority'],
            status="Open",
            description=request.description,
            suggested_action=prediction['suggested_action']
        )
        
        return {
            "message": "Ticket created successfully",
            "ticket_id": ticket_id,
            "prediction": prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating ticket: {str(e)}")

# ============================================
# Email Integration Endpoints
# ============================================

@app.post("/sync-emails")
async def sync_emails(background_tasks: BackgroundTasks):
    """Manually trigger an email synchronization."""
    background_tasks.add_task(email_manager.fetch_emails)
    return {"message": "Email synchronization triggered in background"}

@app.post("/tickets/{ticket_id}/reply")
async def reply_to_ticket(ticket_id: int):
    """Sends the AI-suggested solution to the requester via email."""
    success = email_manager.send_reply(ticket_id)
    if success:
        return {"message": f"AI Reply sent successfully for Ticket #{ticket_id}"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email reply. Check logs for details.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
