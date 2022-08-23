from dataclasses import dataclass
from decimal import Decimal
from typing import List
from uuid import uuid4

from pydantic import UUID4

from services.quotes import Quote

from services.quotes import get_quote

from models.models import CheckoutItemDb

from models.models import CheckoutSessionDb


@dataclass
class CheckoutItem:
    external_id: UUID4
    amount: Decimal = None
    description: str = None
    type: str = None

    async def get_data(self):
        pass

    async def save(self, checkout_session):
        pass

@dataclass
class NewBusinessCheckoutItem(CheckoutItem):
    quote: Quote = None

    async def get_data(self):
        self.quote = await get_quote(self.external_id)

        policy_quote, *_ = [charge for charge in self.quote.state_priced.charges if charge.reference.product_id]
        self.description = f"Quote product reference: {policy_quote.reference.product_id}"
        self.amount = policy_quote.total_premium

    async def save(self, checkout_session):
        await CheckoutItemDb.create(
            description=self.description,
            external_id=self.external_id,
            checkout_session_id=checkout_session,
            type="Quote",
        )

@dataclass
class CheckoutSession:
    success_url: str
    cancel_url: str

    session_token: UUID4 = uuid4()

    checkout_items: List[CheckoutItem] = None

    async def add_item(self, item:CheckoutItem):
        await item.get_data()

    async def save(self):
        session_db = await CheckoutSessionDb.create(
            session_token=self.session_token,
            success_url=self.success_url,
            cancel_url=self.cancel_url,
        )

        if self.checkout_items:
            for item in self.checkout_items:
                await item.save(session_db)
