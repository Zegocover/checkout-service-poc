import random
from dataclasses import dataclass
from decimal import Decimal
from typing import List
from uuid import uuid4

from pydantic import UUID4


@dataclass
class Reference:
    product_id: UUID4 = None
    addon_id: UUID4 = None


@dataclass
class ProductCharge:
    reference: Reference
    total_premium: Decimal


@dataclass
class PriceBreakdown:
    charges: List[ProductCharge]


@dataclass
class Quote:
    quote_id: UUID4
    state: str
    state_priced: PriceBreakdown


async def generate_fake_quote(quote_id: UUID4) -> Quote:
    policy_id = Reference(product_id=uuid4())
    policy_charge = ProductCharge(
        reference=policy_id,
        total_premium=Decimal(random.randrange(100, 2800))
    )
    charges = [policy_charge]

    if str(quote_id)[-1] == "5":
        charges.append(generate_add_on())

    return Quote(
        quote_id=quote_id,
        state="priced",
        state_priced=PriceBreakdown(charges=charges)
    )


async def generate_fake_mta_quote(quote_id: UUID4) -> Quote:
    policy_id = Reference(product_id=uuid4())
    policy_charge = ProductCharge(
        reference=policy_id,
        total_premium=Decimal(random.randrange(50, 400))
    )
    charges = [policy_charge]

    return Quote(
        quote_id=quote_id,
        state="priced",
        state_priced=PriceBreakdown(charges=charges)
    )


def generate_add_on():
    add_on_id = Reference(addon_id=uuid4())
    policy_charge = ProductCharge(
        reference=add_on_id,
        total_premium=Decimal(random.randrange(20, 200))
    )
    return policy_charge


async def get_quote(quote_id: UUID4) -> Quote:
    return await generate_fake_quote(quote_id)


async def get_mta_quote(quote_id: UUID4) -> Quote:
    return await generate_fake_mta_quote(quote_id)


async def get_cancellation_quote(quote_id: UUID4) -> Quote:
    quote = await generate_fake_mta_quote(quote_id)
    quote.state_priced = quote.state_priced * -1
    return quote


@dataclass
class SettlementFigure:
    amount: Decimal
    pcl_quote_id: UUID4


async def get_pcl_settlement_figure(quote_id: UUID4) -> SettlementFigure:
    return SettlementFigure(
        amount=Decimal(random.randrange(50, 1000)),
        pcl_quote_id=uuid4(),
    )
