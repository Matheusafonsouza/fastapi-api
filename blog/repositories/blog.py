from sqlalchemy.orm.session import Session
from fastapi import status, HTTPException
from blog.models import Blog
from blog.schemas import Blog as BlogSchema


def get_all(db: Session):
    blogs = db.query(Blog).all()
    return blogs


def show(id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with the id {id} does not exists.'
        )
    return blog


def update(id: int, request: BlogSchema, db: Session):
    blog = db.query(Blog).filter(Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with the id {id} does not exists.'
        )

    blog.update(request.dict())
    db.commit()
    return 'updated'


def destroy(id: int,  db: Session):
    blog = db.query(Blog).filter(Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with the id {id} does not exists.'
        )

    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


def create(request: BlogSchema, db: Session):
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
