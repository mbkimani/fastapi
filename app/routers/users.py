from sqlalchemy.sql.functions import mode
from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserDisplay)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), ):

    #check id
    get_id = db.query(models.User).filter(models.User.email== user.email).first()

    if get_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already Exists")

    #hash password
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
    get_id = db.query(models.User).filter(models.User.id == id).first()
    if get_id==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    
    return get_id