from decimal import Decimal
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic.types import UUID

from models.models import CheckoutSessionDb
from services.session_services import create_checkout_session, load_checkout_session, apply_discount
from services.session_services import create_checkout_session
from services.payment_option import get_payment_options
from models.schemas import CheckoutSessionIntentRequest, CheckoutSessionIntentResponse
from decimal import Decimal

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

@app.get('/payment-options/{session_token}', response_class=HTMLResponse)
async def payment_options(request: Request, session_token: str):
    checkout_session = await load_checkout_session(session_token)
    options_list = await get_payment_options(checkout_session)

    return templates.TemplateResponse("payment_options.html",
        {
            "request": request,
            "checkout_uuid": session_token,
            "options_list": options_list,
        }
    )
    
@app.get('/stripe-payment/{session_token}', response_class=HTMLResponse)
async def stripe_payment(request: Request, session_token: str):
    checkout_session = await load_checkout_session(session_token)
    import stripe
    stripe.api_key = "sk_test_TLLgtVWUvJ7FYYzPHtJ0189h"

    intent = stripe.PaymentIntent.create(
        amount= int(checkout_session.total() * 100),
        currency="gbp",
        payment_method_types=["card"],
        # confirm=True,
        # return_url= checkout_session.success_url,
    )

    return templates.TemplateResponse("stripe_payment.html",
        {
            "request": request,
            "total": checkout_session.total(),
            "client_secret": intent.client_secret,
            "success_url": checkout_session.success_url,
        }
    )


@app.post('/redeem-discount/{checkout_session_id}')
async def redeem_discount(checkout_session_id: UUID, code):
    await apply_discount(checkout_session_id, code)

    return {}


@app.get('/pcl-dummy/{session_token}')
async def pcl_dummy(request: Request, session_token: UUID):
    session = await load_checkout_session(session_token)
    checkout_total = session.total() * Decimal("1.10")
    return templates.TemplateResponse("pcl_dummy.html", {"request": request, "session": session, "checkout_total": checkout_total})

@app.get('/pcl-staff-dummy/{session_token}')
async def pcl_dummy(request: Request, session_token: UUID):
    session = await load_checkout_session(session_token)
    checkout_total = session.total() * Decimal("1.10")
    return templates.TemplateResponse("pcl_staff_dummy.html", {"request": request, "session": session, "checkout_total": checkout_total})