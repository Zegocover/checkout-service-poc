from fastapi import FastAPI

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

@app.post('/checkout-session-intent')
async def checkout_session_intent(checkout_session_request: CheckoutSessionIntentRequest):
    session = uuid4()
    return session
