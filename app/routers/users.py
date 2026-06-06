from  .. import models, schemas, utils
from ..utils import hash_password
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import  SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import List
from .. import oauth2

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=List[schemas.UserOut])
def get_all_user(db:Session = Depends(get_db),
         current_user: models.User = Depends(oauth2.allow_admin_only)):
    user = db.query(models.User).all()

    return user

@router.get("/me")
def get_me(db:Session = Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    return current_user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.allow_staff_and_admin)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user

@router.put("/{id}", response_model=schemas.UserResponse)
def updatde_user(id: int, user: schemas.UserUpdate, db:Session = Depends(get_db),
                 current_user: models.User = Depends(oauth2.allow_staff_and_admin)):
    user_query = db.query(models.User).filter(models.User.id == id)
    
    user_in_db = user_query.first()
    if user_in_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id:  {id} not exist")
    user_query.update(user.model_dump(), synchronize_session=False)
    db.commit()

    return user_query.first()

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.allow_admin_only)):
    deleted_user = db.query(models.User).filter(models.User.id == id)

    user_in_db = deleted_user.first()

    if user_in_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    deleted_user.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

    
    