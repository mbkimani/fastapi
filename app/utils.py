# hashing for the passwords
from passlib.context import CryptContext
from fastapi import status, Depends, HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):

    return pwd_context.verify(plain_password, hashed_password)
    