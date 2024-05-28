from pydantic import BaseModel, Field
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    # class Config:
    #     orm_mode = True
    #     schema_extra = {
    #         "example": {
    #             'username': "diordev",
    #             'email': 'diordev@gmail.com',
    #             'password': 'diordev2004',
    #             'is_staff': False,
    #             'is_active': True
    #         }
    #     }


class Settings(BaseModel):
    # import secrets
    # secrets.token_hex()
    authjwt_secret_key: str = "a34d25fe87dc60712e7cd7303d0d17829a094e762dcb72311a4ceb325ff32800"


class LoginMadel(BaseModel):
    username: str
    password: str
