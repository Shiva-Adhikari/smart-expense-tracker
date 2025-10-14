from src.core.database import Base
from sqlalchemy import Integer, Float, String, Boolean, ForeignKey, DateTime, func, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone, date
from decimal import Decimal


class Income(Base):
    __tablename__ = 'incomes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey('users.id'), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    source: Mapped[str] = mapped_column(String(50))
    income_date: Mapped[datetime] = mapped_column(Date)
    description: Mapped[str] = mapped_column(String(500))
    recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
