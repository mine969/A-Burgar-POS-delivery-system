from app.database import SessionLocal
from app import models, auth

def check_and_create_admin():
    db = SessionLocal()
    email = "admin123@gmail.com"
    password = "admin123"
    
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if user:
            print(f"User {email} exists.")
            if user.role != "admin":
                print(f"Updating role from {user.role} to admin.")
                user.role = "admin"
                db.commit()
            else:
                print("Role is already admin.")
        else:
            print(f"Creating user {email}...")
            hashed_password = auth.get_password_hash(password)
            new_user = models.User(
                email=email,
                name="Admin User",
                role="admin",
                hashed_password=hashed_password
            )
            db.add(new_user)
            db.commit()
            print(f"User {email} created successfully.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_and_create_admin()
