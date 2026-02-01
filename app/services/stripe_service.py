import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_API_KEY

def create_checkout_session(amount_cents: int, currency: str = "usd", name: str = "Camaral AI Plan"):
    """
    Creates a Stripe Checkout Session for a one-time payment.
    Returns the URL where the user should be redirected to pay.
    """
    print(f"DEBUG: Creating checkout session for {name} - {amount_cents}")
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': currency,
                'product_data': {
                    'name': name,
                },
                'unit_amount': amount_cents,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://camaral.ai/success', 
        cancel_url='https://camaral.ai/cancel',
    )
    # Return tuple with url and session_id to save in DB
    return session.url, session.id
