from tortoise.contrib.pydantic import pydantic_model_creator

from models.models import TestModel, TestModelTwo

TestModelPydantic = pydantic_model_creator(TestModel, name="TestModel")
TestModelInPydantic = pydantic_model_creator(TestModel, name="TestModelIn", exclude_readonly=True)

TestModelTwoPydantic = pydantic_model_creator(TestModelTwo, name="TestModelTwo")
TestModelTwoPydantic = pydantic_model_creator(TestModelTwo, name="TestModelTwo", exclude_readonly=True)

