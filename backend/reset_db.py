import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the parent directory to sys.path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, SQLALCHEMY_DATABASE_URL
from app.models.user import User
from app.models.menu import MenuItem
from app.models.order import Order, OrderItem, DriverAssignment, DriverLocation
from app.models.payment import Payment

def reset_database():
    print("Connecting to database...")
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Database reset complete!")
    print("\nNow run: python app/seed_db.py")
    print("Or redeploy on Render to auto-seed.")

if __name__ == "__main__":
    # Auto-run without confirmation for production use
    # To use safely, only run this when you want to reset
    reset_database()

