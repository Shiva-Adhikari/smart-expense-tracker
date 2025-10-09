from src.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DateTime, func, Integer, ForeignKey, Boolean
from pydantic import EmailStr
from datetime import datetime, timezone
from typing import Optional


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(50), index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(228), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)


class EmailVerification(Base):
    __tablename__ = 'email_verifications'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), index=True)
    token: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True)


class UserSession(Base):
    __tablename__ = 'user_sessions'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), index=True)
    token: Mapped[str] = mapped_column(String(128), nullable=False)
    device_info: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
