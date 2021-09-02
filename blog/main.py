from fastapi import FastAPI
from . import models
from blog.database import engine, SessionLocal
from blog.routers.blog import router as blogRouter
from blog.routers.user import router as userRouter

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.include_router(blogRouter)
app.include_router(userRouter)
