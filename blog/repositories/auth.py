from blog.schemas import Login
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from blog.models import User
from passlib.hash import pbkdf2_sha256


def login(request: Login, db: Session):
    password = request.password
    email = request.email

    err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'Invalid email/password.'
    )

    if not email or not password:
        raise err

    user = db.query(User).filter(User.email == email).first()
    print(user.password)
    print(password)
    if not user or not pbkdf2_sha256.verify(password, user.password):
        raise err

    return user
