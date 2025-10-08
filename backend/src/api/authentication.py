from src.schemas.authentication import UserRegister, UserResponse, UserLogin
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.authentication import User, EmailVerification
from sqlalchemy import select
from src.utils.logger_util import logger
from src.utils.generate_otp_util import generate_otp
from datetime import datetime, timezone, timedelta
from src.utils.password_hash_util import hash_password

router = APIRouter(prefix='/authentication', tags=['Authentication'])


@router.post('/register', response_model=UserResponse)
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
            status_code=500, detail=f'Unable to register | {e}'
        )

    logger.debug('done')
    return UserResponse.model_validate(user_table)


@router.post('/verify-email')
def verify_email(email: str, otp: int, db: Session = Depends(get_db)) -> dict:
    user_table = db.query(User).filter(User.email == email).first()
    if not user_table:
        raise HTTPException(status_code=404, detail='User not found')

    if user_table.is_verified:
        return {'message': 'User already verified'}

    email_verification_table = db.query(EmailVerification).filter(
        EmailVerification.user_id == user_table.id
    ).first()

    # === Check if verification record exists FIRST ===
    if not email_verification_table:
        raise HTTPException(status_code=400, detail='No verification record found')

    # === check otp expired and not expires ===
    if email_verification_table.is_used:
        raise HTTPException(status_code=400, detail='Otp already used')

    if (email_verification_table.expires_at and datetime.now(
            timezone.utc) > email_verification_table.expires_at):
        # cleanup expired otp
        email_verification_table.token = None
        email_verification_table.expires_at = None
        db.commit()
        raise HTTPException(status_code=400, detail='Otp Expired')

    if int(email_verification_table.token) != int(otp):
        email_verification_table.attempts += 1

        # Update max_attempts        
        if email_verification_table.attempts > email_verification_table.max_attempts:
            email_verification_table.max_attempts = email_verification_table.attempts

        db.commit()

        remaining = 5 - email_verification_table.attempts
        if remaining > 0:
            raise HTTPException(
                status_code=400,
                detail=f'Invalid Otp, {remaining} attempts remaining')
        else:
            email_verification_table.token = None
            db.commit()
            raise HTTPException(
                status_code=429,
                detail='Otp Expired, Please request a new otp')

    # === Success - verify user and cleanup ===
    user_table.is_verified = True
    email_verification_table.attempts = 0
    email_verification_table.token = None
    email_verification_table.expires_at = None
    email_verification_table.is_used = True
    email_verification_table.verified_at = datetime.now(timezone.utc)

    db.commit()

    return {'message': 'Email verified successfully'}
