from fastapi import FastAPI
from blog.schemas import Blog
from . import models
from blog.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post('/blog')
def create(request: Blog):
    return request