from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import database, models, schemas
from ..auth import get_current_user

router = APIRouter(
    prefix="/delivery",
    tags=["delivery"]
)

@router.get("/available", response_model=List[schemas.Order])
def get_available_deliveries(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "driver" and current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    # Drivers see orders that are 'ready'
    orders = db.query(models.Order).filter(models.Order.status == "ready").all()
    return orders

@router.post("/accept/{order_id}")
def accept_delivery(
    order_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "driver":
        raise HTTPException(status_code=403, detail="Only drivers can accept deliveries")
        
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    if order.status != "ready":
        raise HTTPException(status_code=400, detail="Order is not ready for pickup")
        
    # Assign driver
    order.driver_id = current_user.id
    order.status = "picked_up"
    
    # Create assignment record
    assignment = models.DriverAssignment(
        order_id=order.id,
        driver_id=current_user.id,
        status="assigned"
    )
    db.add(assignment)
    
    db.commit()
    return {"message": "Delivery accepted"}

@router.put("/orders/{order_id}/status")
def update_delivery_status(
    order_id: int,
    status_update: schemas.OrderStatusUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "driver" and current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    # Verify driver owns this order
    if current_user.role == "driver" and order.driver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not assigned to this order")
        
    if status_update.status not in ["picked_up", "delivered"]:
        raise HTTPException(status_code=400, detail="Invalid status for delivery")
        
    order.status = status_update.status
    db.commit()
    
    return {"message": f"Order status updated to {status_update.status}"}
