from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    """
    blog index page
    """
    return {'data': {'name': 'Afonso'}}


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