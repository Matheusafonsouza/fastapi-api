from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from blog.schemas import Blog as BlogSchema, User as UserSchema, ShowUser, ShowBlog
from . import models
from blog.database import engine, SessionLocal
from sqlalchemy.orm import Session
from blog.models import Blog, User

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close( )

app = FastAPI()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: BlogSchema, db: Session = Depends(get_db)):
    title = request.title
    body = request.body

    blog = Blog(
        title=title,
        body=body,
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)

    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
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


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
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


@app.get('/blog', response_model=List[ShowBlog])
def list_all(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs


@app.get('/blog/{id}', response_model=ShowBlog)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with the id {id} does not exists.'
        )
    return blog

@app.post('/user', status_code=status.HTTP_201_CREATED)
def create(request: UserSchema, db: Session = Depends(get_db)):
    name = request.name
    email = request.email
    password = request.password

    user = User(
        name=name,
        email=email,
        password=password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT)
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


@app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED)
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


@app.get('/user', response_model=List[ShowUser])
def list_all(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.get('/user/{id}', response_model=ShowUser)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} does not exists.'
        )
    return user