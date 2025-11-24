from app.database import SessionLocal
from app import models

def verify_seed():
    db = SessionLocal()
    try:
        print("Verifying Admin User...")
        admin = db.query(models.User).filter(models.User.email == "admin123@gmail.com").first()
        if admin:
            print(f"PASS: Admin found: {admin.email}")
        else:
            print("FAIL: Admin not found")

        print("\nVerifying Menu Items...")
        items = db.query(models.MenuItem).all()
        print(f"Found {len(items)} menu items.")
        for item in items:
            print(f"- {item.name}: {item.price}")
            
    finally:
        db.close()

if __name__ == "__main__":
    verify_seed()
