from fastapi import FastAPI
from blog.models import Blog

app = FastAPI()

@app.post('/blog')
def create(request: Blog):
    return request