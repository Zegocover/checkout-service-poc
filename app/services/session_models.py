from dataclasses import dataclass
from decimal import Decimal
from typing import List

from models.models import CheckoutItemDb
from models.models import CheckoutSessionDb
from pydantic import UUID4
from services.invoices import get_invoice
from services.quotes import Quote
from services.quotes import get_quote

from services.quotes import get_mta_quote, get_pcl_settlement_figure


@dataclass
class CheckoutItem:
    external_id: str
    amount: Decimal = None
    description: str = None
    type: str = None

    async def get_data(self):
        pass

    async def get_additional_data(self, checkout_session):
        pass

    async def save(self, checkout_session):
        pass


@dataclass
class NewBusinessCheckoutItem(CheckoutItem):
    quote: Quote = None

    async def get_data(self):
        self.quote = await get_quote(self.external_id)

        policy_quote, *_ = [charge for charge in self.quote.state_priced.charges if charge.reference.product_id]
        self.description = f"New Insurance Policy"
        self.amount = policy_quote.total_premium

    async def get_additional_data(self, checkout_session):
        add_ons = [charge for charge in self.quote.state_priced.charges if charge.reference.addon_id]

        for add_on in add_ons:
            item = AddOnCheckoutItem(
                description=f"Policy Add-On",
                amount=add_on.total_premium,
                external_id=add_on.reference.addon_id
            )
            await checkout_session.add_item(item)

    async def save(self, checkout_session):
        await CheckoutItemDb.create(
            description=self.description,
            external_id=self.external_id,
            amount=self.amount,
            checkout_session_id=checkout_session,
            type="Quote",
        )


class AddOnCheckoutItem(CheckoutItem):
    async def get_data(self):
        pass

    async def save(self, checkout_session):
        await CheckoutItemDb.create(
            description=self.description,
            external_id=self.external_id,
            amount=self.amount,
            checkout_session_id=checkout_session,
            type="AddOn",
        )


@dataclass
class MTACheckoutItem(CheckoutItem):
    async def get_data(self):
        self.quote = await get_mta_quote(self.external_id)

        policy_quote, *_ = [charge for charge in self.quote.state_priced.charges if charge.reference.product_id]
        self.description = f"Policy MTA"
        self.amount = policy_quote.total_premium

    async def get_additional_data(self, checkout_session):
        pass

    async def save(self, checkout_session):
        await CheckoutItemDb.create(
            description=self.description,
            external_id=self.external_id,
            amount=self.amount,
            checkout_session_id=checkout_session,
            type="MTA",
        )


@dataclass
class CancellationCheckoutItem(CheckoutItem):
    async def get_data(self):
        self.quote = await get_quote(self.external_id)

        policy_quote, *_ = [charge for charge in self.quote.state_priced.charges if charge.reference.product_id]
        self.description = f"Policy Cancellation"
        self.amount = policy_quote.total_premium

    async def get_additional_data(self, checkout_session):
        settlement = await get_pcl_settlement_figure(self.external_id)

        item = PCLSettlementCheckoutItem(
            description=f"PCL Settlement Figure",
            amount=settlement.amount,
            external_id=str(settlement.pcl_quote_id)
        )
        await checkout_session.add_item(item)

    async def save(self, checkout_session):
        await CheckoutItemDb.create(
            description=self.description,
            external_id=self.external_id,
            amount=self.amount,
            checkout_session_id=checkout_session,
            type="Cancellation",
        )


@dataclass
class PCLSettlementCheckoutItem(CheckoutItem):
    async def get_data(self):
        pass

    async def get_additional_data(self, checkout_session):
        pass

    async def save(self, checkout_session):
        await CheckoutItemDb.create(
            description=self.description,
            external_id=self.external_id,
            amount=self.amount,
            checkout_session_id=checkout_session,
            type="pcl_settlement",
        )

@dataclass
class InvoiceCheckoutItem(CheckoutItem):
    async def get_data(self):
        invoice = await get_invoice(self.external_id)
        self.description = invoice.description
        self.amount = invoice.amount

    async def save(self, checkout_session):
        await CheckoutItemDb.create(
            description=self.description,
            external_id=self.external_id,
            amount=self.amount,
            checkout_session_id=checkout_session,
            type="Invoice",
        )


@dataclass
class DiscountCheckoutItem(CheckoutItem):
    async def get_data(self):
        self.description = f"Discount: {''.join([i for i in str(self.external_id) if not i.isdigit()])}"
        self.amount = Decimal("-123.00")

    async def save(self, checkout_session):
        await CheckoutItemDb.create(
            description=self.description,
            external_id=self.external_id,
            amount=self.amount,
            checkout_session_id=checkout_session,
            type="Discount",
        )


@dataclass
class CheckoutSession:
    success_url: str
    cancel_url: str
    user_type: str

    session_token: UUID4

    checkout_items: List[CheckoutItem] = None

    async def add_item(self, item: CheckoutItem):
        if self.checkout_items is None:
            self.checkout_items = []
        await item.get_data()
        self.checkout_items.append(item)

        await item.get_additional_data(self)

    def total(self):
        items = self.checkout_items
        return sum(item.amount for item in items)

    async def save(self):
        session_db = await CheckoutSessionDb.create(
            session_token=self.session_token,
            success_url=self.success_url,
            cancel_url=self.cancel_url,
            user_type=self.user_type,
        )

        if self.checkout_items:
            for item in self.checkout_items:
                await item.save(session_db)
