"""
User Routes

This module defines routes related to user registration, management, and authentication.

It includes functionality for user registration, email verification, updating avatars, and creating password reset tokens.

Functions:
    generate_verification_token(): Generates a verification token for email confirmation.
    send_verification_email(email: str, verification_token: str): Sends an email with the verification token.
    upload_avatar_to_cloudinary(avatar: UploadFile) -> str: Uploads an avatar image to Cloudinary and returns the URL.
    create_password_reset_token(db: Session, user_id: int, token: str): Creates a password reset token for a user.

Routes:
    POST /register: Endpoint to register a new user.
    PUT /users/{user_id}/avatar: Endpoint to update a user's avatar.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from jose import jwt
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from datetime import datetime, timedelta
import secrets
import string
from typing import List
from cloudinary.uploader import upload
from decouple import config

from ..database import db
from ..database.models import User
from ..schemas import UserCreate, UserResponse
from ..conf.config import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD_NAME
from ..database.models import PasswordResetToken

router = APIRouter()
user_router = APIRouter()


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"
VERIFICATION_TOKEN_EXPIRE_HOURS = 48  # Тривалість токену верифікації у годинах

# Функція для генерації токену верифікації
def generate_verification_token():
    """
    Generate Verification Token

    Generates a verification token for email confirmation.

    Returns:
        str: The generated verification token in hexadecimal format.
    """
    return secrets.token_hex(3)  # Генеруємо 6 символів (3 байта) у шістнадцятковому форматі

# Функція для надсилання листа для підтвердження
def send_verification_email(email: str, verification_token: str):
    """
    Send Verification Email

    Sends an email with the provided verification token for email confirmation.

    Args:
        email (str): The recipient's email address.
        verification_token (str): The verification token to include in the email.
    """
    conf = ConnectionConfig(
        MAIL_USERNAME = "arh.romanov@meta.ua",
        MAIL_PASSWORD = "Iruluf98",
        MAIL_FROM = "arh.romanov@meta.ua",
        MAIL_PORT = 587,
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_TLS = True,
        MAIL_SSL = False,
        USE_CREDENTIALS = True
    )

    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=f"Your verification code: {verification_token}"
    )

    fm = FastMail(conf)
    fm.send_message(message)

@router.post("/register/", response_model=User)
def register_user(user_data: UserCreate, db: Session = Depends(db.get_db)):
    """
    Register User

    Registers a new user, performs email verification, and sends a verification email.

    Args:
        user_data (UserCreate): User registration data.
        db (Session): SQLAlchemy database session.

    Returns:
        User: The newly registered user.
    """
    # Перевірка, чи користувач з таким email вже існує
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User with this email already exists")
    
    # Створення нового користувача
    new_user = User(email=user_data.email)
    new_user.set_password(user_data.password)  # Встановлення хешованого пароля
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Генерація та збереження токену верифікації
    verification_token = generate_verification_token()
    new_user.verification_token = verification_token
    new_user.verification_token_expires = datetime.utcnow() + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)
    db.commit()
    
    # Відправка листа для підтвердження
    send_verification_email(new_user.email, verification_token)
    
    return new_user


@user_router.put("/users/{user_id}/avatar/", response_model=UserResponse)
def update_user_avatar(user_id: int, avatar: UploadFile = File(...), db: Session = Depends(db.get_db)):
    """
    Update User Avatar

    Updates the avatar of a user.

    Args:
        user_id (int): ID of the user.
        avatar (UploadFile): Avatar image to upload.
        db (Session): SQLAlchemy database session.

    Returns:
        UserResponse: The updated user profile.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Ось тут використовуйте функцію завантаження аватару
    cloudinary_url = upload_avatar_to_cloudinary(avatar)

    user.avatar_url = cloudinary_url
    db.commit()
    db.refresh(user)
    return user


def upload_avatar_to_cloudinary(avatar: UploadFile) -> str:
    """
    Upload Avatar to Cloudinary

    Uploads the provided avatar image to Cloudinary.

    Args:
        avatar (UploadFile): Avatar image to upload.

    Returns:
        str: URL of the uploaded avatar.
    """
    response = upload(avatar.file, api_key=CLOUDINARY_API_KEY, api_secret=CLOUDINARY_API_SECRET, cloud_name=CLOUDINARY_CLOUD_NAME)
    return response['url']

def create_password_reset_token(db: Session, user_id: int, token: str):
    """
    Create Password Reset Token

    Creates a password reset token for a user.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): ID of the user.
        token (str): Token string for password reset.

    Returns:
        PasswordResetToken: The created password reset token.
    """
    expires_at = datetime.utcnow() + timedelta(hours=1)  # Припустимо, токен дійсний годину
    password_reset_token = PasswordResetToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(password_reset_token)
    db.commit()
    db.refresh(password_reset_token)
    return password_reset_token