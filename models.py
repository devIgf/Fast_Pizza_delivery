from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, Float
from database import Base
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(Text,nullable=False)
    is_staff = Column(Boolean, default=False)  # True if user is staff, False otherwise
    is_active = Column(Boolean, default=True)
    orders = relationship("Order", back_populates="user")


    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', is_staff={self.is_staff}, is_active={self.is_active})>"
    


class Order(Base):

    ORDER_STATUSES = (
        ("PENDING", "Pending"),
        ("IN-PROGRESS", "In Progress"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    )


    PIZZA_SIZES = (
        ("SMALL", "Small"),
        ("MEDIUM", "Medium"),
        ("LARGE", "Large"),
        ("EXTRA_LARGE", "Extra Large"),
    )

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    ordder_status = Column(ChoiceType(ORDER_STATUSES), default="PENDING")
    pizza_size = Column(ChoiceType(PIZZA_SIZES), default="SMALL")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="orders")


    def __repr__(self):
        return f"<Order(id={self.id}, quantity={self.quantity}, order_status='{self.ordder_status}', pizza_size='{self.pizza_size}', user_id={self.user_id})>"