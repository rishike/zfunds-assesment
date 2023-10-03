from database import db
from sqlalchemy import Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime



class Purchase(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    advisor_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])
    advisor = db.relationship('User', foreign_keys=[advisor_id])
    product = db.relationship('Product', foreign_keys=[product_id])
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
