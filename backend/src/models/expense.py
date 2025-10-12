from src.core.database import Base
from sqlalchemy import Integer, Float, String, Boolean, ForeignKey, DateTime, func, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone, date
from decimal import Decimal


class Expense(Base):
    __tablename__ = 'expenses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), index=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete='CASCADE'), index=True)
    # category: Mapped[str] = mapped_column(String(50))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    description: Mapped[str] = mapped_column(String(500))
    expense_date: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


    # MANY expenses belong to ONE budget
    # budget: Mapped['Budget'] = relationship(back_populates='expenses')
    #       ↑ List chaina kina? Kina ki ek expense ko ek matra budget!



    # expenses_: Mapped['Budget'] = relationship(back_populates='budgets_')

# table ko foerign key chai, cateogry hatara id chaiyo expenses ma table ma


# a.py
# relation to b.py
# relation to c.py

# b.py
# relation to a.py

# c.py
# relation to a.py