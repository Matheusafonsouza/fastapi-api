from fastapi import APIRouter
from blog.schemas import Blog as BlogSchema, ShowBlog
from fastapi import status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from blog.models import Blog
from typing import List
from blog.database import get_db


router = APIRouter()

@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: BlogSchema, db: Session = Depends(get_db)):
    title = request.title
    body = request.body

    blog = Blog(
        title=title,
        body=body,
        user_id=2
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)

    return blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with the id {id} does not exists.'
        )
    
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request: BlogSchema, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with the id {id} does not exists.'
        )
    
    blog.update(request.dict())
    db.commit()
    return 'updated'


@router.get('/blog', response_model=List[ShowBlog], tags=['blogs'])
def list_all(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs


@router.get('/blog/{id}', response_model=ShowBlog, tags=['blogs'])
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with the id {id} does not exists.'
        )
    return blog