from pydantic import BaseModel
from typing import Optional

class ContactBase(BaseModel):
    """
    Contact Base Schema

    Represents the base schema for a contact.

    Attributes:
        first_name (str): First name of the contact.
        last_name (str): Last name of the contact.
        email (str): Email address of the contact.
        phone_number (str): Phone number of the contact.
        birthday (str, optional): Birthday of the contact (in string format).
        additional_data (str, optional): Additional data about the contact.
    """
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: Optional[str] = None
    additional_data: Optional[str] = None

class ContactCreate(ContactBase):
    """
    Contact Create Schema

    Represents the schema for creating a new contact based on the ContactBase.

    Inherits:
        ContactBase (class): The base schema for a contact.
    """
    pass

class ContactUpdate(ContactBase):
    """
    Contact Update Schema

    Represents the schema for updating an existing contact based on the ContactBase.

    Inherits:
        ContactBase (class): The base schema for a contact.
    """
    pass

class ContactResponse(ContactBase):
    """
    Contact Response Schema

    Represents the schema for a contact response, including the contact's ID.

    Inherits:
        ContactBase (class): The base schema for a contact.
    """
    id: int

class ContactListResponse(ContactBase):
    """
    Contact List Response Schema

    Represents the schema for a contact in a list response, including the contact's ID.

    Inherits:
        ContactBase (class): The base schema for a contact.
    """
    id: int

class ContactSearchResponse(ContactBase):
    """
    Contact Search Response Schema

    Represents the schema for a contact in a search response, including the contact's ID.

    Inherits:
        ContactBase (class): The base schema for a contact.
    """
    id: int

class UserCreate(BaseModel):
    """
    User Create Schema

    Represents the schema for creating a new user.

    Attributes:
        email (str): Email address of the user.
        password (str): Password of the user.
    """
    email: str
    password: str

class Token(BaseModel):
    """
    Token Schema

    Represents the schema for an access token.

    Attributes:
        access_token (str): The access token.
        token_type (str): The type of the token.
    """
    access_token: str
    token_type: str