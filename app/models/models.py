from tortoise import models, fields


class TestModel(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()