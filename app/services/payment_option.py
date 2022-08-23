from tabnanny import check
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
    available_payment_options = []
    return_list = []
    option_dict = dict()

    for payment_option in [StripePaymentOption, PCLPaymentOption]:
        if await payment_option.is_available(checkout_session):
            available_payment_options.append(payment_option)

    
    for option in available_payment_options:
        option_dict["payment_method"] = option.__name__
        option_dict["description"] = payment_option.get_description(checkout_session)
        option_dict["redirect_url"] = payment_option.payment_session_redirect_url(checkout_session)
        option_dict["success_url"] = checkout_session.success_url
        option_dict["cancel_url"] = checkout_session.cancel_url
        option_dict["amount"] = checkout_session.total()

        return_list.append(option_dict)

    return return_list
