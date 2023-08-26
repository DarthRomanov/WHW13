from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import db
from ..database.models import User

router = APIRouter()

@router.post("/verify/")
def verify_email(token: str):
    """
    Verify Email

    Verifies the user's email address based on the provided verification token.

    Args:
        token (str): The verification token received via email.

    Returns:
        dict: A dictionary with a success message if verification is successful.
    
    Raises:
        HTTPException: If the user is not found or verification fails.
    """
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.verified = True
    db.commit()
    
    return {"message": "Email verified successfully"}
