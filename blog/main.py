from fastapi import FastAPI, Depends
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

@app.post('/blog')
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