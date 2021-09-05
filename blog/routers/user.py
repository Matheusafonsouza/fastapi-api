from fastapi import APIRouter
from blog.schemas import User as UserSchema, ShowUser
from fastapi import status, Depends, Response
from sqlalchemy.orm import Session
from blog.repositories import user as user_repository
from typing import List
from blog.database import get_db
from blog.oauth2 import get_current_user


router = APIRouter(
    prefix='/user',
    tags=['tags']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(
    request: UserSchema,
    db: Session = Depends(get_db)
):
    return user_repository.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(
    id,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    return user_repository.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(
    id,
    request: UserSchema,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    return user_repository.update(id, request, db)


@router.get('/', response_model=List[ShowUser])
def get_all(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    return user_repository.get_all(db)


@router.get('/{id}', response_model=ShowUser)
def show(
    id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    return user_repository.show(id, db)
