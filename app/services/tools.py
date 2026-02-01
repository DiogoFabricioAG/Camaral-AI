from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.domain.entities import Product, Customer, Order
from app.services.stripe_service import create_checkout_session

class CRMTools:
    def __init__(self, db: Session):
        self.db = db

    def search_products(self, query: str):
        """Searches for products by name or description."""
        products = self.db.query(Product).filter(Product.name.ilike(f"%{query}%")).all()
        return [{"id": p.id, "name": p.name, "price": str(p.price), "sku": p.sku} for p in products]

    def create_lead(self, name: str, email: str, phone: str = None):
        """Creates a new lead in the CRM. Updates if email exists. Returns ID."""
        existing = self.db.query(Customer).filter(Customer.email == email).first()
        if existing:
            existing.full_name = name
            if phone: existing.phone = phone
            self.db.commit()
            return f"Customer updated. ID: {existing.id}"
        
        try:
            new_lead = Customer(full_name=name, email=email, phone=phone)
            self.db.add(new_lead)
            self.db.commit()
            return f"Lead created. ID: {new_lead.id}"
        except IntegrityError:
            self.db.rollback()
            return "Error: Could not register lead. Verify email format."

    def create_payment(self, email: str, amount: float):
        """Generates a Stripe Checkout Link and records an Order. Requires customer email."""
        customer = self.db.query(Customer).filter(Customer.email == email).first()
        if not customer:
            return "Error: Customer email not found. Please create lead first."

        url, session_id = create_checkout_session(int(amount * 100))
        
        # Create Order record
        order = Order(
            customer_id=customer.id, 
            total_amount=amount, 
            stripe_payment_id=session_id,
            status="pending"
        )
        self.db.add(order)
        self.db.commit()
        
        return f"Payment Link: {url}"
