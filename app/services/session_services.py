from uuid import uuid4

from models.schemas import CheckoutSessionIntentRequest
from services.session_models import CheckoutSession

from services.session_models import NewBusinessCheckoutItem

from services.session_models import InvoiceCheckoutItem

from models.models import CheckoutSessionDb

from services.session_models import AddOnCheckoutItem

from services.session_models import DiscountCheckoutItem

from services.session_models import MTACheckoutItem, CancellationCheckoutItem, PCLSettlementCheckoutItem


def build_quote(quote_id):
    last_id_digit = str(quote_id)[-1]


    if last_id_digit == "6":
        return MTACheckoutItem(external_id=quote_id)
    elif last_id_digit == "7":
        return CancellationCheckoutItem(external_id=quote_id)
    else:
        return NewBusinessCheckoutItem(external_id=quote_id)


async def create_checkout_session(checkout_session_request: CheckoutSessionIntentRequest):

    session = CheckoutSession(success_url=checkout_session_request.success_url, cancel_url=checkout_session_request.cancel_url, session_token=uuid4(), user_type=checkout_session_request.user_type)

    if quote_id := checkout_session_request.quote_id:
        try:
            quote = build_quote(quote_id)
            await session.add_item(quote)
        except ValueError:
            pass


    if checkout_session_request.invoice_ids:
        for invoice_id in checkout_session_request.invoice_ids:
            invoice = InvoiceCheckoutItem(external_id=invoice_id)
            await session.add_item(invoice)

    await session.save()

    return session


async def load_checkout_session(session_token: str) -> CheckoutSession:
    session_db = await CheckoutSessionDb.get(session_token=session_token)
    checkout_items_db = await session_db.items

    checkout_items = []

    checkout_item_map = {
        "Invoice": InvoiceCheckoutItem,
        "Quote": NewBusinessCheckoutItem,
        "AddOn": AddOnCheckoutItem,
        "Discount": DiscountCheckoutItem,
        "MTA": MTACheckoutItem,
        "Cancellation": CancellationCheckoutItem,
        "pcl_settlement": PCLSettlementCheckoutItem,

    }

    for item_db in checkout_items_db:
        item_class = checkout_item_map.get(item_db.type)
        item = item_class(amount=item_db.amount, description=item_db.description, type=item_db.type, external_id=item_db.external_id)
        checkout_items.append(item)


    return CheckoutSession(
        session_token=session_db.session_token,
        success_url=session_db.success_url,
        cancel_url=session_db.cancel_url,
        user_type=session_db.user_type,
        checkout_items=checkout_items,
    )

async def apply_discount(session_token, discount_code):
    session = await load_checkout_session(session_token)

    discount_item = DiscountCheckoutItem(external_id=discount_code)

    await session.add_item(discount_item)

    checkout_session = await CheckoutSessionDb.get(session_token=session_token)
    print(checkout_session.id)

    await discount_item.save(checkout_session=checkout_session)
