from fastapi import FastAPI, Depends, status, Response, HTTPException
from blog.schemas import Blog as BlogSchema
from . import models
from blog.database import engine, SessionLocal
from sqlalchemy.orm import Session
from blog.models import Blog

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


@app.get('/blog')
def create(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs


@app.get('/blog/{id}')
def create(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with the id {id} does not exists.'
        )
    return blog