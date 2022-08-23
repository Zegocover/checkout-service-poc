from logging import PlaceHolder
from fastapi import FastAPI

from db import init_db

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

@app.get('/checkout_items/{item_id}')
def payment_options(item_id: int):
    return {"item_id": item_id}
