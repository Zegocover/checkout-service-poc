from pydantic.dataclasses import dataclass


@dataclass
class CheckoutSession:
    session_id: int = 1
    success_url: str = "http://localhost:8000/success_url"
    cancel_url: str = "http://localhost:8000/cancel_url"
    customer: str = "UserAbc"
    checkout_items: str = "Quote"
    total: int = 0
    chosen_payment_method: str = ""
    status: str = ""