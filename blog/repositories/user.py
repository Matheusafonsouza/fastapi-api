from sqlalchemy.orm import Session
from passlib.hash import pbkdf2_sha256
from blog.schemas import User as UserSchema
from blog.models import User
from fastapi import status, HTTPException


def create(request: UserSchema, db: Session):
    name = request.name
    email = request.email
    hashed_password = pbkdf2_sha256.hash(request.password)

    user = User(
        name=name,
        email=email,
        password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def destroy(id, db: Session):
    user = db.query(User).filter(User.id == id)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} does not exists.'
        )

    user.delete(synchronize_session=False)
    db.commit()
    return 'done'


def update(id, request: UserSchema, db: Session):
    user = db.query(User).filter(User.id == id)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} does not exists.'
        )

    user.update(request.dict())
    db.commit()
    return 'updated'


def get_all(db: Session):
    users = db.query(User).all()
    return users


def show(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} does not exists.'
        )
    return user
