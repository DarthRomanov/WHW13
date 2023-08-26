"""
Users Repository

This module provides database operations related to user management.

Functions:
    get_user_by_email(db: Session, email: str) -> User:
        Retrieve a user based on their email.

Note:
    This module contains functions for retrieving user information from the database.
"""

from sqlalchemy.orm import Session
from ..database.models import User

def get_user_by_email(db: Session, email: str):
    """Retrieve a user based on their email."""
    return db.query(User).filter(User.email == email).first()
