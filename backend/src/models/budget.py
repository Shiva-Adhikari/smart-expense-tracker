from src.core.database import Base
from sqlalchemy import Integer, Float, String, Boolean, ForeignKey, DateTime, func, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from decimal import Decimal


class Budget(Base):
    __tablename__ = 'budgets'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), index=True)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('categories.id', ondelete='CASCADE'), index=True)
    budget_limit: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    month: Mapped[int] = mapped_column(Integer)
    year: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # __table_args__ = (
        # UniqueConstraint(
            # 'user_id', 'category_id', 'month', 'year',
            # name='unique_budget_per_month'),
    # )

    # # budget_: Mapped['Category'] = relationship(back_populates='category_')
    # # budgets_: Mapped[list['Expense']] = relationship(back_populates='expenses_')


    # # MANY budgets belong to ONE category
    # category: Mapped['Category'] = relationship(back_populates='budgets')
    # #         ↑ List chaina kina? Kina ki ek budget ko ek matra category!
    
    # # ONE budget has MANY expenses
    # expenses: Mapped[list['Expense']] = relationship(back_populates='budget')
    # #         ↑ List kina? Kina ki dherai expenses huncha!
