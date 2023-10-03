from database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


# User model
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=True)
    mobile_number: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(Enum('user', 'advisor', 'admin'), default='user')
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    advisor_id: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())



# OTP model
class OTP(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mobile_number: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    otp: Mapped[int] = mapped_column(Integer, nullable=False)