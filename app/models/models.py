from tortoise import models, fields


class CheckoutSessionDb(models.Model):
    id = fields.UUIDField(pk=True)
    session_token = fields.UUIDField(unique=True)
    success_url = fields.CharField(max_length=2048)
    cancel_url = fields.CharField(max_length=2048)

    def __str__(self):
        return str(self.session_token)

class CheckoutItemDb(models.Model):
    id = fields.UUIDField(pk=True)
    type = fields.TextField()
    amount = fields.DecimalField(max_digits=30, decimal_places=2)
    description = fields.TextField()
    checkout_session_id = fields.ForeignKeyField(model_name="models.CheckoutSessionDb", related_name="items")
    external_id = fields.UUIDField()

    def __str__(self):
        return f"{self.description} {self.amount}"


