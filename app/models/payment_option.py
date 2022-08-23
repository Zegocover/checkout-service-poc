# from tortoise import models, fields
# from uuid import UUID, uuid4

# class StripePaymentOption:
#         def __init__(self) -> None:
#         pass
    
#         def is_available(self, checkout_session) -> bool:
#                 """
#                 Works out whether payment option is available for that particular checkout session
#                 """
#                 return True

#         def get_description(self, checkout_session) -> str:
#                 """
#                 Used when the description needs to be dynamic, e.g. explaining monthly payments for a credit agreement
#                 Will use description attribute if this method is not implemented in a class
#                 """
#                 raise NotImplementedError

#         def payment_session_setup(self, checkout_session) -> None:
#                 """
#                 Does any setup required before redirecting to the payment provider
#                 Should take into account whether the checkout session is being used by the customer or a CS agent
#                 """
#                 pass

#         def payment_session_redirect_url(self, checkout_session) -> str:
#                 """
#                 Builds the url that the user will be redirect to in order to make a payment
#                 """
#                 raise NotImplementedError


# class PCLPaymentOption:
#     def is_available(self, checkout_session) -> bool:
#         """
#         Works out whether payment option is available for that particular checkout session
#         """
#         return True

#     def get_description(self, checkout_session) -> str:
#         """
#         Used when the description needs to be dynamic, e.g. explaining monthly payments for a credit agreement
#         Will use description attribute if this method is not implemented in a class
#         """
#         raise NotImplementedError

#     def payment_session_setup(self, checkout_session) -> None:
#         """
#         Does any setup required before redirecting to the payment provider
#         Should take into account whether the checkout session is being used by the customer or a CS agent
#         """
#         pass

#     def payment_session_redirect_url(self, checkout_session) -> str:
#         """
#         Builds the url that the user will be redirect to in order to make a payment
#         """
#         raise 
