from tortoise import models, fields


class TestModel(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


class TestModel2(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()



class CheckoutSessionDb(models.Model):
    id = fields.UUIDField(pk=True)
    session_token = fields.UUIDField(unique=True)
    success_url = fields.TextField()
    cancel_url = fields.TextField()

    def __str__(self):
        return str(self.session_token)

class CheckoutItemDb(models.Model):
    id = fields.UUIDField(pk=True)
    type = fields.TextField()
    amount = fields.DecimalField()
    description = fields.TextField()
    checkout_session_id = fields.ForeignKeyField(model_name="CheckoutSessionDb", related_name="items")
    external_id = fields.UUIDField()

    def __str__(self):
        return f"{self.description} {self.amount}"


