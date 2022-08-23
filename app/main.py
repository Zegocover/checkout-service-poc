from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.models import CheckoutSessionDb
from services.session_services import create_checkout_session, load_checkout_session
from models.schemas import CheckoutSessionIntentRequest, CheckoutSessionIntentResponse

from db import init_db

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


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


@app.get('/session/{session_token}', response_class=HTMLResponse)
async def checkout_session(request: Request, session_token: str):
    session = await load_checkout_session(session_token=session_token)
    return templates.TemplateResponse("checkout_session.html", {"request": request, "session": session, "session_token": session_token})

@app.get('/sessions', response_model=List[CheckoutSessionIntentResponse])
async def checkout_session():
    sessions = await CheckoutSessionDb.all()
    return sessions

@app.post('/checkout-session-intent', response_model=CheckoutSessionIntentResponse)
async def checkout_session_intent(checkout_session_request: CheckoutSessionIntentRequest):
    session = await create_checkout_session(checkout_session_request)
    return session

@app.get('/checkout_items/{item_id}', response_class=HTMLResponse)
def payment_options(request: Request, item_id: int):
    return templates.TemplateResponse("payment_options.html", {"request": request, "item_id": item_id})
