from blog.repositories import blog
from fastapi import APIRouter
from blog.schemas import Blog as BlogSchema, ShowBlog
from fastapi import status, Depends
from sqlalchemy.orm import Session
from typing import List
from blog.database import get_db


router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: BlogSchema, db: Session = Depends(get_db)):
    return blog.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    return blog.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: BlogSchema, db: Session = Depends(get_db)):
    return blog.update(id, request, db)


@router.get('/', response_model=List[ShowBlog])
def get_all(db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.get('/{id}', response_model=ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    return blog.show(id, db)
