from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': 'Afonso'}}


@app.get('/about')
def about():
    return {'data': {'name': 'about page'}}


@app.get('/blog/{id}')
def show(id):
    return {'data': {'id': id}} 


@app.get('/blog/{id}/comments')
def comments(id):
    return {'data': {'comments': []}}