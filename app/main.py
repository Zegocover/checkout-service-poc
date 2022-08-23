from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.models import CheckoutSessionDb
from services.session_services import create_checkout_session, load_checkout_session
from services.session_services import create_checkout_session
from services.checkout_session_mock import CheckoutSession
from services.payment_option import get_payment_options
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

@app.get('/payment-options/{checkout_uuid}', response_class=HTMLResponse)
def payment_options(request: Request, checkout_uuid: int):
    checkout_session = CheckoutSession
    is_available, get_description, payment_session_setup, payment_session_redirect_url = get_payment_options(checkout_session)

    return templates.TemplateResponse("payment_options.html",
        {
            "request": request,
            "checkout_uuid": checkout_uuid,
            "is_available": is_available,
            "get_description": get_description,
            "payment_session_setup": payment_session_setup,
            "payment_session_redirect_url": payment_session_redirect_url,
        }
    )


@app.post('/redeem-discount/{checkout_session_id}/')
async def redeem_discount(checkout_session_id: UUID, code: str = None):
    print(f"checkout_session_id {checkout_session_id}")
    print(f"discount_code {code}")
    return {}
