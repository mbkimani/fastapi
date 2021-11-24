from os import stat
from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy import schema

from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from ..database import get_db

from .. import models, schemas, utils, oauth2
from app import database

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix = "/login",
    tags = ['Authentication']
)

@router.post("/", response_model=schemas.Token)
def user_login(user_logins: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_logins.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user_logins.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    #create token, return token
    access_token = oauth2.create_access_token(data= {"current_user_id": user.id})
    return {"access_token":access_token, "token_type":"bearer"}