from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import database, models, schemas
from ..auth import get_current_user

router = APIRouter(
    prefix="/kitchen",
    tags=["kitchen"]
)

@router.get("/queue", response_model=List[schemas.Order])
def get_kitchen_queue(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "kitchen":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    # Kitchen sees orders that are 'paid' (new) or 'preparing'
    orders = db.query(models.Order).filter(models.Order.status.in_(["paid", "preparing"])).all()
    return orders

@router.put("/orders/{order_id}/status")
def update_kitchen_status(
    order_id: int,
    status_update: schemas.OrderStatusUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "kitchen" and current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    if status_update.status not in ["preparing", "ready"]:
        raise HTTPException(status_code=400, detail="Invalid status for kitchen")
        
    order.status = status_update.status
    db.commit()
    
    return {"message": f"Order status updated to {status_update.status}"}
