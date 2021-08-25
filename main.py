from typing import Optional
from fastapi import FastAPI
from typing import Optional
from models import Blog

app = FastAPI()


@app.get('/')
def index():
    """
    blog index page
    """
    return {'data': {'name': 'Afonso'}}


@app.get('/blog')
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    """
    blogs page
    """
    if published:
        return {'data': {'blogs': f'{limit} published blogs from the database'}}
    else:
        return {'data': {'blogs': f'{limit} unpublished blogs from the database'}}


@app.get('/about')
def about():
    """
    blog about page
    """
    return {'data': {'name': 'about page'}}


@app.get('/blog/{id}')
def show(id: int):
    """
    get blog with id = id
    """
    return {'data': {'id': id}} 


@app.get('/blog/{id}/comments')
def comments(id: int):
    """
    fetch comments of blog with id = id
    """
    return {'data': {'comments': []}}


@app.post('/blog')
def create_blog(request: Blog):
    return {'data': {'message': f'Blog was created with {request.title} title.'}}