import os
from typing import List

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from db import init_db
from models.models import TestModel
from schemas.schemas import TestModelPydantic, TestModelInPydantic

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


@app.post('/test-model', response_model=TestModelPydantic)
async def create_test_model(request_body: TestModelInPydantic):
    print(request_body)
    print(request_body.name)
    test_model = await TestModel.create(name=request_body.name)
    print("test model: ")
    return await TestModelPydantic.from_tortoise_orm(test_model)


@app.get('/test-models', response_model=List[TestModelPydantic])
async def get_test_models():
    return await TestModelPydantic.from_queryset(TestModel.all())


@app.get('/test-model/{id}')
async def get_test_model(id: str):
    return await TestModelPydantic.from_queryset_single(TestModel.get(id=id))


@app.delete('/test-model/{id}')
async def get_test_model(test_model_id: str):
    return await TestModel.filter(id=test_model_id).delete()

