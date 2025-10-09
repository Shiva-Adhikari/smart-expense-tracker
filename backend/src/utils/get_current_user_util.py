from typing import Annotated
from fastapi import Cookie, Depends, HTTPException
from src.core.database import DB
from src.models.authentication import User, UserSession
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone
from src.utils.logger_util import logger


def get_current_user(db: DB, session_token: Annotated[str | None, Cookie(alias='session_token')] = None) -> User:
    logger.debug(f'session_token: {session_token}')
    if not session_token:
        raise HTTPException(status_code=404, detail='Authentication failed')
    
    session = db.scalars(
        select(UserSession).where(
            UserSession.token == session_token,
            UserSession.expires_at > datetime.now(timezone.utc),
            UserSession.is_active
        )
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail='Authentication required')

    user = db.scalars(
        select(User).where(
            session.user_id == User.id
        )
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    return user


GetCurrentUser = Annotated[User, Depends(get_current_user)]
