from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': 'Afonso'}}

@app.get('/about')
def about():
    return {'data': {'name': 'about page'}}