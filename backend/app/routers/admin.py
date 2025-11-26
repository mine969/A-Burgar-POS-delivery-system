from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from .. import database, models, schemas
from ..auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

def check_admin(user: models.User):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    check_admin(current_user)
    
    total_orders = db.query(models.Order).count()
    active_orders = db.query(models.Order).filter(models.Order.status.notin_(["delivered", "cancelled"])).count()
    total_revenue = db.query(func.sum(models.Order.total_amount)).scalar() or 0
    
    return {
        "total_orders": total_orders,
        "active_orders": active_orders,
        "total_revenue": float(total_revenue)
    }

@router.get("/reports/sales")
def get_sales_report(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    check_admin(current_user)
    
    # Simple daily sales aggregation
    sales = db.query(
        func.date(models.Order.created_at).label('date'),
        func.count(models.Order.id).label('count'),
        func.sum(models.Order.total_amount).label('revenue')
    ).group_by(func.date(models.Order.created_at)).all()
    
    return [{"date": str(s.date), "count": s.count, "revenue": float(s.revenue)} for s in sales]

@router.post("/menu", response_model=schemas.MenuItem)
def create_menu_item(
    item: schemas.MenuItemCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    check_admin(current_user)
    
    new_item = models.MenuItem(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item
