"""
Database Models Module

This module defines SQLAlchemy models for the database tables used in the application.

Classes:
    Contact (Base): Represents a contact in the database with details such as name, email, and phone number.
    Tag (Base): Represents a tag associated with contacts.
    User (Base): Represents a user with email, hashed password, and related contacts.
    PasswordResetToken (Base): Represents a token for resetting user passwords.

Note:
    This module defines the database models that are used to structure the data in the application.
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func, BooleanDefaultFalse
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from datetime import timedelta

from .db import Base

class Contact(Base):
    """Represents a contact in the database."""
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, index=True, nullable=False)
    birthday = Column(Date)
    additional_data = Column(String)

    # Зв'язок з тегами (якщо вам потрібно)
    # tags = relationship("Tag", secondary=contact_m2m_tag, back_populates="contacts")

class Tag(Base):
    """Represents a tag associated with contacts."""
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    # Зв'язок з контактами (якщо вам потрібно)
    # contacts = relationship("Contact", secondary=contact_m2m_tag, back_populates="tags")

class User(Base):
    """Represents a user with email, hashed password, and related contacts."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    contacts = relationship("Contact", back_populates="owner")
    verified = Column(BooleanDefaultFalse)
    avatar_url = Column(String)

    def set_password(self, password):
        """Sets the hashed password for the user."""
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the hashed password of the user."""
        return check_password_hash(self.hashed_password, password)
    
class PasswordResetToken(Base):
    """Represents a token for resetting user passwords."""
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime, default=func.now() + timedelta(hours=1))