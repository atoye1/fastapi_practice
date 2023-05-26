from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException as HttpException

from database import get_db
from domain.user import user_crud
from domain.user.user_schema import UserCreate


router = APIRouter(
    prefix="/api/user",
)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create)
    print('user', user)
    if user:
        print('ERROR: User already exists')
        raise HttpException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    user_crud.create_user(db, user_create)
