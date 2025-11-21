from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    # Store the hash in the DB column named password_hash but expose as hashed_password
    hashed_password = Column("password_hash", String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships (optional for current tests)
    customer = relationship("Customer", back_populates="user", uselist=False)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    session_token = Column(String(255))
    name = Column(String(255))
    phone = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="customer")
    # orders relationship placeholder (not needed for current tests)
    # orders = relationship("Order", back_populates="customer")

