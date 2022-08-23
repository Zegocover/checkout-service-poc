from tortoise import models, fields
from uuid import UUID, uuid4

from services.session_models import CheckoutSession


class StripePaymentOption:
    def __init__(self) -> None:
        pass

    @classmethod
    async def is_available(self, checkout_session) -> bool:
        """
        Works out whether payment option is available for that particular checkout session
        """
        return True

    @classmethod
    def get_description(self, checkout_session) -> str:
        """
        Used when the description needs to be dynamic, e.g. explaining monthly payments for a credit agreement
        Will use description attribute if this method is not implemented in a class
        """
        return "Stripe Payment Description"

    @classmethod
    def payment_session_setup(self, checkout_session) -> str:
        """
        Does any setup required before redirecting to the payment provider
        Should take into account whether the checkout session is being used by the customer or a CS agent
        """
        pass

    @classmethod
    def payment_session_redirect_url(self, checkout_session) -> str:
        """
        Builds the url that the user will be redirect to in order to make a payment
        """
        return "https://stripe.com/docs/"


class PCLPaymentOption:
    def __init__(self) -> None:
        pass

    @classmethod
    async def is_available(self, checkout_session) -> bool:
        items = checkout_session.checkout_items
        if [i for i in items if i.type == "Quote"]:
            return True
        else:
            return False

   
    @classmethod
    def get_description(self, checkout_session) -> str:
        """
        Used when the description needs to be dynamic, e.g. explaining monthly payments for a credit agreement
        Will use description attribute if this method is not implemented in a class
        """
        return "PCL Payment Description"

    @classmethod
    def payment_session_setup(self, checkout_session) -> str:
        """
        Does any setup required before redirecting to the payment provider
        Should take into account whether the checkout session is being used by the customer or a CS agent
        """
        pass

    @classmethod
    def payment_session_redirect_url(self, checkout_session) -> str:
        """
        Builds the url that the user will be redirect to in order to make a payment
        """
        return "https://www.premiumcredit.com/"


async def get_payment_options(checkout_session: CheckoutSession):
    is_available = dict()
    get_description = dict()
    payment_session_setup = dict()
    payment_session_redirect_url = dict()

    for payment_option in [StripePaymentOption, PCLPaymentOption]:
        is_available[payment_option.__name__] = await payment_option.is_available(checkout_session)
        get_description[payment_option.__name__] = payment_option.get_description(checkout_session)
        # payment_session_setup[payment_option.__name__] = payment_option.payment_session_setup(checkout_session)
        payment_session_redirect_url[payment_option.__name__] = payment_option.payment_session_redirect_url(checkout_session)

    return (is_available, get_description, payment_session_setup, payment_session_redirect_url)