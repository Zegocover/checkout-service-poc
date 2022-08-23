from uuid import uuid4

from models.schemas import CheckoutSessionIntentRequest
from services.session_models import CheckoutSession

from services.session_models import NewBusinessCheckoutItem

from services.session_models import InvoiceCheckoutItem

from models.models import CheckoutSessionDb

from services.session_models import AddOnCheckoutItem


async def create_checkout_session(checkout_session_request: CheckoutSessionIntentRequest):

    session = CheckoutSession(success_url=checkout_session_request.success_url, cancel_url=checkout_session_request.cancel_url, session_token=uuid4())

    if quote_id := checkout_session_request.quote_id:
        quote = NewBusinessCheckoutItem(external_id=quote_id)
        await session.add_item(quote)

    if checkout_session_request.invoice_ids:
        for invoice_id in checkout_session_request.invoice_ids:
            invoice = InvoiceCheckoutItem(external_id=invoice_id)
            await session.add_item(invoice)

    await session.save()

    return session


async def load_checkout_session(session_token: str):
    session_db = await CheckoutSessionDb.get(session_token=session_token)
    checkout_items_db = await session_db.items

    checkout_items = []

    checkout_item_map = {"Invoice": InvoiceCheckoutItem, "Quote": NewBusinessCheckoutItem, "AddOn": AddOnCheckoutItem}

    for item_db in checkout_items_db:
        item_class = checkout_item_map.get(item_db.type)
        item = item_class(amount=item_db.amount, description=item_db.description, type=item_db.type, external_id=item_db.external_id)
        checkout_items.append(item)


    return CheckoutSession(
        session_token=session_db.session_token,
        success_url=session_db.success_url,
        cancel_url=session_db.cancel_url,
        checkout_items=checkout_items,
    )


