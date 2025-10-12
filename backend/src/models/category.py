from src.core.database import Base
from sqlalchemy import Integer, Float, String, Boolean, ForeignKey, DateTime, func, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone, date
# from typing import List


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), index=True)
    category_name: Mapped[str] = mapped_column(String(50))
    icon: Mapped[str | None] = mapped_column(String(50))
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


    # ONE category has MANY budgets
    # budgets: Mapped[list['Budget']] = relationship(back_populates='category')
    #       ↑ List kina? Kina ki dherai budgets huncha!    
    

    # category_: Mapped[list['Budget']] = relationship(back_populates='budget_')

    # category_: Mapped['Category'] = relationship(back_populates='category_')
