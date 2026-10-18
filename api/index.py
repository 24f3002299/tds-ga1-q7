from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from collections import defaultdict

app = FastAPI()

# Allow cross-origin requests from the grader
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Assigned API Key[cite: 72]
API_KEY = "ak_02utzevqdu83rqlosgmsf7u1"
EMAIL = "24f3002299@ds.study.iitm.ac.in"

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class AnalyticsPayload(BaseModel):
    events: List[Event]

@app.post("/analytics")
async def process_analytics(payload: AnalyticsPayload, x_api_key: str = Header(None)):
    # Authenticate via assigned API key[cite: 72]
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or wrong key")

    unique_users = set()
    revenue = 0.0
    user_revenue = defaultdict(float)

    for event in payload.events:
        unique_users.add(event.user)
        # Only sum positive amounts for revenue and top user[cite: 72]
        if event.amount > 0:
            revenue += event.amount
            user_revenue[event.user] += event.amount

    top_user = ""
    if user_revenue:
        top_user = max(user_revenue, key=user_revenue.get)

    return {
        "email": EMAIL,
        "total_events": len(payload.events),
        "unique_users": len(unique_users),
        "revenue": revenue,
        "top_user": top_user
    }