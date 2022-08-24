from collections import namedtuple
import random

from pydantic import UUID4


async def get_invoice(invoice_id: UUID4):
    Invoice = namedtuple("Invoice", "amount description")
    return Invoice(
        amount=random.randrange(1, 100),
        description=f"Invoice",
    )


async def get_credit_note(credit_note_id: UUID4):
    CreditNote = namedtuple("CreditNote", "amount description")
    return CreditNote(
        amount=random.randrange(1, 100) * -1,
        description=f"Credit Note",
    )
