from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder

from schemas import SignUpModel, LoginMadel
from database import session, engine
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT

auth_rooter = APIRouter(prefix="/auth")
session = session(bind=engine)


@auth_rooter.get('/')
async def auth():
    return {"massage": "Auth rooter"}


@auth_rooter.get('/signup')
async def signup():
    return {"massage": "Register page"}


@auth_rooter.post('/signup', status_code=status.HTTP_200_OK)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu emaildan oldin ro'yxatdan o'tkazilgan")

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu username mavjud")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),  # pip install werkzeug | shifirlash uchun
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    session.add(new_user)
    session.commit()
    return user


@auth_rooter.get('/login')
async def login():
    return {"massage": "Login page"}


@auth_rooter.post('/login', status_code=status.HTTP_200_OK)
async def login(user: LoginMadel, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)
        response = {
            "access": access_token,
            "refresh": refresh_token
        }

        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parol yoki username xato")

