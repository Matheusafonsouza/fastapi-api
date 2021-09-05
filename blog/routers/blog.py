from blog.repositories import blog as blog_repository
from fastapi import APIRouter
from blog.schemas import Blog as BlogSchema, ShowBlog
from fastapi import status, Depends
from blog.schemas import User as UserSchema
from sqlalchemy.orm import Session
from typing import List
from blog.database import get_db
from blog.oauth2 import get_current_user


router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(
    request: BlogSchema,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    return blog_repository.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(
    id,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    return blog_repository.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(
        id,
        request: BlogSchema,
        db: Session = Depends(get_db),
        current_user: UserSchema = Depends(get_current_user)
):
    return blog_repository.update(id, request, db)


@router.get('/', response_model=List[ShowBlog])
def get_all(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    return blog_repository.get_all(db)


@router.get('/{id}', response_model=ShowBlog)
def show(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    return blog_repository.show(id, db)
