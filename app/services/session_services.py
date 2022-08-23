from models.schemas import CheckoutSessionIntentRequest
from services.session_models import CheckoutSession

from services.session_models import NewBusinessCheckoutItem


async def create_checkout_session(checkout_session_request: CheckoutSessionIntentRequest):

    session = CheckoutSession(success_url=checkout_session_request.success_url, cancel_url=checkout_session_request.cancel_url)

    if quote_id := checkout_session_request.quote_id:
        quote = NewBusinessCheckoutItem(external_id=quote_id)
        await session.add_item(quote)

    await session.save()

    return session

