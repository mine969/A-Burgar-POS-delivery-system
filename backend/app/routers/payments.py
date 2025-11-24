from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, models, schemas
from ..auth import get_current_user
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/payments",
    tags=["payments"]
)

@router.post("/process", status_code=status.HTTP_201_CREATED)
def process_payment(
    payment_data: schemas.PaymentCreate,
    db: Session = Depends(database.get_db)
):
    # Simulate payment processing
    # In a real system, this would interact with Stripe/PayPal
    
    order = db.query(models.Order).filter(models.Order.id == payment_data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status == "paid":
        raise HTTPException(status_code=400, detail="Order already paid")

    # Create payment record
    transaction_id = str(uuid.uuid4())
    new_payment = models.Payment(
        order_id=payment_data.order_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        status="completed",
        transaction_id=transaction_id
    )
    
    db.add(new_payment)
    
    # Update order status
    order.status = "paid"
    
    db.commit()
    db.refresh(new_payment)
    
    return {"message": "Payment successful", "transaction_id": transaction_id, "status": "completed"}

@router.get("/{order_id}")
def get_payment_status(order_id: int, db: Session = Depends(database.get_db)):
    payment = db.query(models.Payment).filter(models.Payment.order_id == order_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
