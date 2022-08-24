from typing import List

from pydantic import BaseModel, UUID4
from tortoise.contrib.pydantic import pydantic_model_creator

class CheckoutSessionIntentRequest(BaseModel):

    invoice_ids: List[UUID4] = []
    quote_id: UUID4 = None
    user_type: str = "Customer"
    success_url: str
    cancel_url: str

class CheckoutSessionIntentResponse(BaseModel):
    session_token: UUID4

# CheckoutSessionIntentRequest = pydantic_model_creator(CheckoutSessionDb, name="CheckoutSessionIntentRequest")
# CheckoutSessionIntentResponse = pydantic_model_creator(CheckoutSessionDb, name="CheckoutSessionIntentResponse")