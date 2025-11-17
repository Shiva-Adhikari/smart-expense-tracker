from tests.test_db import client, get_db
from src.schemas.authentication import UserRegister
from src.models.authentication import User, EmailVerification
from sqlalchemy import select


class TestRegister:
    def test_user_register_successfully(self):
        user = UserRegister(
            email = "one@example.com",
            username = "one_user",
            password = "SecurePass123",
            is_active = True
        )
        response = client.post('/api/v1/authentication/register', json=user.model_dump())

        # Check status
        assert response.status_code == 200

        # Check response structure
        data = response.json()
        assert data['message'] == 'Register successful'
        assert 'user' in data

        # Check user data
        assert data['user']['email'] == 'one@example.com'
        assert data['user']['username'] == 'one_user'
        assert data['user']['is_verified'] == False      # Should be False initially
        assert 'password' not in data['user']   # Password should not be in response!


    def test_user_register_duplicate_email(self):
        # First registration - should succeed
        user = UserRegister(
            email = "one@example.com",
            username = "one_user",
            password = "SecurePass123",
            is_active = True
        )
        response = client.post('/api/v1/authentication/register', json=user.model_dump())

        # Check status
        assert response.status_code == 200

        # Manually verify the user (simulate email verification)
        db = next(get_db())
        user_in_db = db.scalars(
            select(User).filter(User.email == 'one@example.com')
        ).first()
        user_in_db.is_verified = True
        db.commit()
        db.close()

        # Try register again with same email - should fail with 409 (duplicate)
        user = UserRegister(
            email = "one@example.com",
            username = "two_user",
            password = "SecurePass123",
            is_active = True
        )
        response = client.post('/api/v1/authentication/register', json=user.model_dump())

        # Check status
        assert response.status_code == 409  # Conflict
        assert response.json()['detail'] == 'Email already exists'


    def test_user_register_duplicate_username(self):
        # First registration - should succeed
        user = UserRegister(
            email = "three@example.com",
            username = "three_user",
            password = "SecurePass123",
            is_active = True
        )
        response = client.post('/api/v1/authentication/register', json=user.model_dump())

        # Check status
        assert response.status_code == 200

        # Manually verify the user (simulate email verification)
        db = next(get_db())
        user_in_db = db.scalars(
            select(User).filter(User.username == 'three_user')
        ).first()
        user_in_db.is_verified = True
        db.commit()
        db.close()

        # Try register again with same email - should fail with 409 (duplicate)
        user = UserRegister(
            email = "four@example.com",
            username = "three_user",
            password = "SecurePass123",
            is_active = True
        )
        response = client.post('/api/v1/authentication/register', json=user.model_dump())

        # Check status
        assert response.status_code == 409  # Conflict
        assert response.json()['detail'] == 'Username already exists'


    def test_user_register_delete_unverified_user(self):
        # First registration - should succeed
        user = UserRegister(
            email = "five@example.com",
            username = "five_user",
            password = "SecurePass123",
            is_active = True,
            is_verified = False
        )
        response = client.post('/api/v1/authentication/register', json=user.model_dump())

        # Check status
        assert response.status_code == 200
        assert response.json()['user']['is_verified'] == False

        # Manually register the user with same username
        db = next(get_db())
        user_in_db = db.scalars(
            select(User).filter(User.username == 'five_user')
        ).first()
        assert user_in_db is not None
        assert user_in_db.is_verified == False
        db.close()

        # ==================

        # Second time registration - same second username
        user2 = UserRegister(
            email = "five@example.com",
            username = "five_user",
            password = "SecurePass123",
            is_active = True,
        )
        response2 = client.post('/api/v1/authentication/register', json=user2.model_dump())

        # Should succeed (old unverified user was deleted)
        assert response2.status_code == 200
        assert response2.json()['message'] == 'Register successful'
        assert response2.json()['user']['is_verified'] == False

        # Verify only ONE user exists(old one was deleted, new one created)
        db = next(get_db())
        all_users = db.scalars(
            select(User).filter(User.username == 'five_user')
        ).all()
        assert len(all_users) == 1  # Only one user should exist
        db.close()
