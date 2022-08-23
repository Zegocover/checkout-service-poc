from logging import PlaceHolder
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


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


@app.get('/checkout_items/{item_id}', response_class=HTMLResponse)
def payment_options(request: Request, item_id: int):
    return templates.TemplateResponse("payment_options.html", {"request": request, "item_id": item_id})
