from uuid import uuid4

from models.schemas import CheckoutSessionIntentRequest
from services.session_models import CheckoutSession

from services.session_models import NewBusinessCheckoutItem

from services.session_models import InvoiceCheckoutItem


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

