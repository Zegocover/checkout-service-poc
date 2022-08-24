from dataclasses import dataclass

from services.session_models import CheckoutSession


@dataclass
class StripePaymentOption:
    name: str = "Stripe"

    async def is_available(self, checkout_session) -> bool:
        """
        Works out whether payment option is available for that particular checkout session
        """
        return True

    def get_description(self, checkout_session) -> str:
        """
        Used when the description needs to be dynamic, e.g. explaining monthly payments for a credit agreement
        Will use description attribute if this method is not implemented in a class
        """
        return "Stripe Payment Description"

    def payment_session_setup(self, checkout_session) -> str:
        """
        Does any setup required before redirecting to the payment provider
        Should take into account whether the checkout session is being used by the customer or a CS agent
        """
        pass

    def payment_session_redirect_url(self, checkout_session) -> str:
        """
        Builds the url that the user will be redirect to in order to make a payment
        """
        return "https://stripe.com/docs/"


@dataclass
class PCLPaymentOption:
    name: str = "PCL"

    async def is_available(self, checkout_session) -> bool:
        items = checkout_session.checkout_items
        if [i for i in items if i.type == "Quote"]:
            return True
        else:
            return False

    def get_description(self, checkout_session) -> str:
        """
        Used when the description needs to be dynamic, e.g. explaining monthly payments for a credit agreement
        Will use description attribute if this method is not implemented in a class
        """
        return "PCL Payment Description"

    def payment_session_setup(self, checkout_session) -> str:
        """
        Does any setup required before redirecting to the payment provider
        Should take into account whether the checkout session is being used by the customer or a CS agent
        """
        pass

    def payment_session_redirect_url(self, checkout_session) -> str:
        """
        Builds the url that the user will be redirect to in order to make a payment
        """
        return "https://www.premiumcredit.com/"


async def get_payment_options(checkout_session: CheckoutSession):
    return_list = []

    all_options = [
        StripePaymentOption(),
        PCLPaymentOption(),
    ]

    available_payment_options = [
        payment_option
        for payment_option in all_options
        if await payment_option.is_available(checkout_session)
    ]

    for option in available_payment_options:
        option_dict = {
            "payment_method": option.name,
            "description": option.get_description(checkout_session),
            "redirect_url": option.payment_session_redirect_url(checkout_session),
            "success_url": checkout_session.success_url,
            "cancel_url": checkout_session.cancel_url,
            "amount": checkout_session.total(),
        }

        return_list.append(option_dict)

    return return_list
