from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas

router = APIRouter(
    prefix="/guest",
    tags=["guest"]
)

@router.get("/track/{tracking_input}", response_model=schemas.Order)
def track_order(
    tracking_input: str,
    db: Session = Depends(database.get_db)
):
    # 1) Try lookup by numeric ID
    try:
        order_id = int(tracking_input)
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if order:
            return order
    except ValueError:
        pass  # not numeric, move on

    # 2) Try lookup by tracking_id (string)
    order = db.query(models.Order).filter(models.Order.tracking_id == tracking_input).first()
    if order:
        return order

    # 3) Not found
    raise HTTPException(status_code=404, detail="Order not found")
