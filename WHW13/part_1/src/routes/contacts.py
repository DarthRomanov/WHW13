"""
Contacts Routes

This module contains routes and functions related to managing contacts.

Modules:
    db: Database related functions.

Functions:
    create_contact(contact: ContactCreate, db: Session = Depends(db.get_db)) -> Contact:
        Create a new contact.

    get_all_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)) -> List[Contact]:
        Get a list of all contacts.

    get_contact(contact_id: int, db: Session = Depends(db.get_db)) -> Contact:
        Get a specific contact by ID.

    update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(db.get_db)) -> Contact:
        Update a contact.

    delete_contact(contact_id: int, db: Session = Depends(db.get_db)) -> dict:
        Delete a contact.

    search_contacts(query: Optional[str] = None, db: Session = Depends(db.get_db)) -> List[Contact]:
        Search contacts based on a query.

    upcoming_birthdays(db: Session = Depends(db.get_db)) -> List[Contact]:
        Get contacts with upcoming birthdays.

Endpoints:
    /contacts:
        POST: Create a new contact.
        GET: Get a list of all contacts.

    /contacts/{contact_id}:
        GET: Get a specific contact by ID.
        PUT: Update a contact.
        DELETE: Delete a contact.

    /contacts/search/:
        GET: Search contacts based on a query.

    /contacts/birthday/:
        GET: Get contacts with upcoming birthdays.

Note:
    This module handles routes for creating, retrieving, updating, and deleting contacts,
    as well as searching for contacts and retrieving upcoming birthdays.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi_limiter import limiter, FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from datetime import datetime, timedelta

from ..repository import contacts
from ..database import db
from ..database.models import Contact, User
from ..schemas import ContactCreate, ContactUpdate, ContactResponse, ContactSearchResponse
from ..routes.token import get_current_user_from_token


router = APIRouter()

@router.post("/contacts/", response_model=ContactResponse)
@limiter.limit("10 per minute")  # Додати обмеження до цього маршруту
def create_contact(contact: ContactCreate, db: Session = Depends(db.get_db)):
    """Create a new contact."""
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/contacts/", response_model=List[ContactResponse])
@limiter.limit("10 per minute")  # Додати обмеження до цього маршруту
def get_all_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)):
    """Get a list of all contacts."""
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return contacts

@router.get("/contacts/{contact_id}", response_model=ContactResponse)
@limiter.limit("10 per minute")  # Додати обмеження до цього маршруту
def get_contact(contact_id: int, db: Session = Depends(db.get_db)):
    """Get a specific contact by ID."""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/contacts/{contact_id}", response_model=ContactResponse)
@limiter.limit("10 per minute")  # Додати обмеження до цього маршруту
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(db.get_db)):
    """Update a specific contact by ID."""
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/contacts/{contact_id}")
@limiter.limit("10 per minute")  # Додати обмеження до цього маршруту
def delete_contact(contact_id: int, db: Session = Depends(db.get_db)):
    """Delete a specific contact by ID."""
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted"}

@router.get("/contacts/search/", response_model=List[ContactSearchResponse])
@limiter.limit("10 per minute")  # Додати обмеження до цього маршруту
def search_contacts(query: Optional[str] = None, db: Session = Depends(db.get_db)):
    """Search contacts based on a query."""
    if query:
        contacts = db.query(Contact).filter(
            Contact.first_name.ilike(f"%{query}%") |
            Contact.last_name.ilike(f"%{query}%") |
            Contact.email.ilike(f"%{query}%")
        ).all()
    else:
        contacts = db.query(Contact).all()
    return contacts

@router.get("/contacts/birthday/", response_model=List[ContactSearchResponse])
@limiter.limit("10 per minute")  # Додати обмеження до цього маршруту
def upcoming_birthdays(db: Session = Depends(db.get_db)):
    """Get contacts with upcoming birthdays."""
    today = datetime.now()
    next_week = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        Contact.birthday >= today.date(),
        Contact.birthday <= next_week.date()
    ).all()
    return contacts

