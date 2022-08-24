from collections import namedtuple
import random

from pydantic import UUID4


async def get_invoice(invoice_id: UUID4):
    Invoice = namedtuple("Invoice", "amount description")
    return Invoice(
        amount=random.randrange(1, 100),
        description=f"Invoice",
    )
