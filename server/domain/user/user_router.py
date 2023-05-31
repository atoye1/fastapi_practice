from datetime import timedelta, datetime
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException as HttpException

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = ' 4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03d'
ALGORITHM = 'HS256'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user",
)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print('get_currenet_user token: ', token)
    credentials_exception = HttpException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, username)
        if user is None:
            raise credentials_exception
        return user


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def create_user(user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create)
    print('user', user)
    if user:
        print('ERROR: User already exists')
        raise HttpException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    user_crud.create_user(db, user_create)


@router.get('/getUser')
def get_user():
    return get_current_user()


@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.get_user(db, form_data.username)
    if not user:
        raise HttpException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})
    if not pwd_context.verify(form_data.password, user.password):
        raise HttpException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})

    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}
