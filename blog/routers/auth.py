from fastapi import Depends
from sqlalchemy.orm import Session
from blog.schemas import Login
from fastapi import APIRouter
from blog.database import get_db
from blog.repositories import auth

router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)


@router.post('/login')
def login(request: Login, db: Session = Depends(get_db)):
    return auth.login(request, db)
