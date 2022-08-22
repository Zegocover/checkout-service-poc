from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class TestModel(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


class TestModelTwo(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
