import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Add the parent directory to sys.path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, SQLALCHEMY_DATABASE_URL
from app.models.user import User
from app.models.menu import MenuItem
from app.models.order import Order, OrderItem, DriverAssignment, DriverLocation
from app.models.payment import Payment

# Setup DB connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def seed():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if users exist
        if db.query(User).first():
            print("Database already seeded.")
            return

        print("Seeding Users...")
        users = [
            User(id=1, name='John Witch', email='johnwitch123@gmail.com', hashed_password=get_password_hash('password'), role='admin'),
            User(id=13, name='admin', email='admin123@gmail.com', hashed_password=get_password_hash('password'), role='admin'),
            User(id=14, name='Gordon Ramsay', email='gordonramsay123@gmail.com', hashed_password=get_password_hash('password'), role='kitchen'),
            User(id=15, name='Michael Schumacher', email='michael123@gmail.com', hashed_password=get_password_hash('password'), role='driver')
        ]
        db.add_all(users)
        db.commit()

        print("Seeding Menu Items...")
        menu_items = [
            MenuItem(id=1, name='Classic Burger', description='Juicy beef patty with lettuce, tomato, and cheese', price=12.99, image_url='https://via.placeholder.com/300x200/FF6B6B/FFFFFF?text=Classic+Burger', is_available=True, category='Main', is_deleted=False),
            MenuItem(id=2, name='Cheese Pizza', description='Traditional tomato sauce with mozzarella', price=14.99, image_url='https://via.placeholder.com/300x200/4ECDC4/FFFFFF?text=Cheese+Pizza', is_available=True, category='Main', is_deleted=False),
            MenuItem(id=3, name='Grilled Salmon', description='Fresh salmon with asparagus', price=18.99, image_url='https://via.placeholder.com/300x200/95E1D3/FFFFFF?text=Grilled+Salmon', is_available=True, category='Main', is_deleted=False),
            MenuItem(id=4, name='Steak Frites', description='Ribeye steak with french fries', price=24.99, image_url='https://via.placeholder.com/300x200/F38181/FFFFFF?text=Steak+Frites', is_available=True, category='Main', is_deleted=False),
            MenuItem(id=5, name='Chicken Alfredo', description='Creamy pasta with grilled chicken', price=19.99, image_url='https://via.placeholder.com/300x200/AA96DA/FFFFFF?text=Chicken+Alfredo', is_available=True, category='Dish', is_deleted=False),
            MenuItem(id=6, name='Caesar Salad', description='Romaine lettuce with croutons and parmesan', price=9.99, image_url='https://via.placeholder.com/300x200/FCBAD3/FFFFFF?text=Caesar+Salad', is_available=True, category='Side', is_deleted=False),
            MenuItem(id=8, name='Onion Rings', description='Battered and fried onion rings', price=5.99, image_url='https://via.placeholder.com/300x200/FFFFD2/333333?text=Onion+Rings', is_available=True, category='Side', is_deleted=False),
            MenuItem(id=9, name='Cola', description='Refreshing cola drink', price=2.99, image_url='https://via.placeholder.com/300x200/A8D8EA/FFFFFF?text=Cola', is_available=True, category='Drink', is_deleted=False),
            MenuItem(id=10, name='Lemonade', description='Freshly squeezed lemonade', price=3.99, image_url='https://via.placeholder.com/300x200/FFAAA5/FFFFFF?text=Lemonade', is_available=True, category='Drink', is_deleted=False),
            MenuItem(id=26, name='Pepesi', description='Drink ', price=2.99, image_url='https://via.placeholder.com/300x200/FF8B94/FFFFFF?text=Pepesi', is_available=True, category='Drink', is_deleted=False),
            MenuItem(id=30, name='Classic Beef Burger', description='This hamburger patty recipe uses ground beef and an easy bread crumb mixture...', price=19.99, image_url='https://via.placeholder.com/300x200/C7CEEA/FFFFFF?text=Beef+Burger', is_available=True, category='Burger', is_deleted=False),
            MenuItem(id=31, name='Double Beef Burger', description='Curious about what is in a Daily Double? It's made with two 100% beef patties...', price=29.99, image_url='https://via.placeholder.com/300x200/FFDAC1/333333?text=Double+Burger', is_available=True, category='Burger', is_deleted=False),
            MenuItem(id=32, name='Crispy Chicken Burger', description='Marinade strips of chicken thighs in soy sauce, garlic and ginger...', price=19.99, image_url='https://via.placeholder.com/300x200/B5EAD7/FFFFFF?text=Crispy+Chicken', is_available=True, category='Burger', is_deleted=False),
            MenuItem(id=33, name='Grilled chicken burger', description='Try these grilled chicken burgers for a nice break from typical beef hamburgers...', price=19.99, image_url='https://via.placeholder.com/300x200/E2F0CB/333333?text=Grilled+Chicken', is_available=True, category='Burger', is_deleted=False),
            MenuItem(id=34, name='Cheese Lover Burger', description='A breaded crispy 100% chicken fillet patty...', price=29.99, image_url='https://via.placeholder.com/300x200/FFD3B6/333333?text=Cheese+Burger', is_available=True, category='Burger', is_deleted=False),
            MenuItem(id=35, name='BBQ Bacon Burger', description='A juicy, barbecue sauce-glazed burger...', price=29.99, image_url='https://via.placeholder.com/300x200/FFAAA5/FFFFFF?text=BBQ+Burger', is_available=True, category='Burger', is_deleted=False),
            MenuItem(id=36, name='Chicken Tetrazzini', description='Chicken tetrazzini is a big, bubbly pasta bake...', price=19.99, image_url='https://via.placeholder.com/300x200/FF8B94/FFFFFF?text=Tetrazzini', is_available=True, category='Dish', is_deleted=False),
            MenuItem(id=37, name='Chicken Florentine Pasta', description='Instant Pot Chicken Florentine Recipe is a great dinner idea...', price=19.99, image_url='https://via.placeholder.com/300x200/C7CEEA/FFFFFF?text=Florentine', is_available=True, category='Dish', is_deleted=False),
            MenuItem(id=38, name='Tuscan Chicken Pasta', description='Tuscan Chicken Pasta is rigatoni pasta tossed in cream sauce...', price=19.99, image_url='https://via.placeholder.com/300x200/FFDAC1/333333?text=Tuscan+Pasta', is_available=True, category='Dish', is_deleted=False),
            MenuItem(id=39, name='7 UP', description='7 Up is a product of a lemon-lime flavoured soft drink', price=2.99, image_url='https://via.placeholder.com/300x200/B5EAD7/FFFFFF?text=7+UP', is_available=True, category='Drink', is_deleted=False),
            MenuItem(id=40, name='French Fries', description='French Fries are arguably the perfect snack...', price=9.99, image_url='https://via.placeholder.com/300x200/E2F0CB/333333?text=French+Fries', is_available=True, category='Side', is_deleted=False),
            MenuItem(id=41, name='Curly Fries', description='Curly fries, or twisted fries are french fries cut into a spiral shape...', price=9.99, image_url='https://via.placeholder.com/300x200/FFD3B6/333333?text=Curly+Fries', is_available=True, category='Side', is_deleted=False),
            MenuItem(id=42, name='Mushroom Melt Burger', description='This restaurant-quality Mushroom Swiss Burger has it all...', price=19.99, image_url='https://via.placeholder.com/300x200/FFAAA5/FFFFFF?text=Mushroom+Burger', is_available=True, category='Burger', is_deleted=False)
        ]
        db.add_all(menu_items)
        db.commit()

        print("Data seeded successfully!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
