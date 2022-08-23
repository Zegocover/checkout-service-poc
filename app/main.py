from typing import List

from fastapi import FastAPI

from models.models import CheckoutSessionDb
from services.session_services import create_checkout_session
from models.schemas import CheckoutSessionIntentRequest, CheckoutSessionIntentResponse
from db import init_db
from uuid import uuid4

app = FastAPI()



@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")


@app.get('/')
def index():
    return {"data": ""}

@app.get('/session/{session_id}', response_model=CheckoutSessionIntentResponse)
async def checkout_session(session_id: str):
    session = await CheckoutSessionDb.get(id=session_id)
    return session

@app.get('/sessions', response_model=List[CheckoutSessionIntentResponse])
async def checkout_session():
    sessions = await CheckoutSessionDb.all()
    return sessions

@app.post('/checkout-session-intent', response_model=CheckoutSessionIntentResponse)
async def checkout_session_intent(checkout_session_request: CheckoutSessionIntentRequest):
    session = await create_checkout_session(checkout_session_request)
    return session
