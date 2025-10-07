from src.schemas.authentication import UserRegister, UserResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.authentication import User, EmailVerification
from sqlalchemy import select
from src.utils.logger_util import logger
from src.utils.generate_otp_util import generate_otp
from datetime import datetime, timezone, timedelta
from src.utils.password_hash_util import hash_password

routes = APIRouter(prefix='/authentication', tags=['Authentication'])


@routes.post('/register', response_model=UserResponse)
def user_register(user: UserRegister, db: Session = Depends(get_db)) -> UserResponse:
    """Register User
    """

    existing_user = db.scalars(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    ).first()

    if existing_user:
        if existing_user.is_verified:
            if existing_user.email == user.email:
                raise HTTPException(status_code=409, detail='Email already exists')
            if existing_user.username == user.username:
                raise HTTPException(status_code=409, detail='Username already exists')
        else:
            db.delete(existing_user)
            db.flush()

    otp = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    ''' # === block otp for sending in development ===
    # === send email ===
    from src.utils.email_send import send_email
    sent_email = send_email(user.email, otp)
    if not sent_email:
        raise HTTPException(status_code=404, detail='Invalid email')
    '''
    logger.debug(f'otp: {otp}')

    hashed_password = hash_password(user.password)

    try:
        # === create new user ===
        user_table = User(
            email=user.email,
            username=user.username,
            password=hashed_password,
        )
        logger.debug(f'user_table: {user_table}')
        db.add(user_table)
        db.flush()  # Get the ID without committing

        email_verification_table = EmailVerification(
            user_id=user_table.id,
            token=otp,
            expires_at=expires_at,
        )
        db.add(email_verification_table)
        logger.debug(f'email_verification_table: {email_verification_table}')

        db.commit()
        db.refresh(user_table)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f'Something went wrong {e}'
        )

    logger.debug('done')
    return UserResponse.model_validate(user_table)
