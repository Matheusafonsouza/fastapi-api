from fastapi import APIRouter
from blog.schemas import User as UserSchema, ShowUser
from fastapi import status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from blog.models import User
from typing import List
from blog.database import get_db
from passlib.hash import pbkdf2_sha256


router = APIRouter()

@router.post('/user', status_code=status.HTTP_201_CREATED, tags=['users'])
def create(request: UserSchema, db: Session = Depends(get_db)):
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


@router.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['users'])
def destroy(id, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} does not exists.'
        )
    
    user.delete(synchronize_session=False)
    db.commit()
    return 'done'


@router.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['users'])
def update(id, request: UserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} does not exists.'
        )
    
    user.update(request.dict())
    db.commit()
    return 'updated'


@router.get('/user', response_model=List[ShowUser], tags=['users'])
def list_all(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get('/user/{id}', response_model=ShowUser, tags=['users'])
def show(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} does not exists.'
        )
    return user