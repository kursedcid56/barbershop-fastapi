from  .. import models, schemas, utils, oauth2
from ..utils import hash_password
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import  SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import List
router = APIRouter(
    prefix="/services",
    tags=['Service']
)

@router.get("/", response_model=List[schemas.ServiceOut])
def root(db:Session = Depends(get_db)):
    service = db.query(models.Service).all()
    return service

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ServiceBase)
def create_service(service: schemas.ServiceCreate, db:Session = Depends(get_db), 
                   current_user: models.User = Depends(oauth2.allow_admin_only)):
    new_service = models.Service(**service.model_dump())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service

@router.get("/{id}", response_model=schemas.ServiceResponse)
def get_service(id: int, db: Session = Depends(get_db), 
                current_user: models.User = Depends(oauth2.allow_all)):
    service = db.query(models.Service).filter(models.Service.id == id).first()
    if service == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"service with id: {id} does not exist")
    return service

@router.put("/{id}",response_model=schemas.ServiceResponse)
def update_service(id: int,service: schemas.ServiceUpdate ,db: Session = Depends(get_db), 
                   current_user: models.User = Depends(oauth2.allow_admin_only)):
    service_query = db.query(models.Service).filter(models.Service.id == id)

    service_in_db = service_query.first()
    if service_in_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service whith id: {id} does not exist")
    service_query.update(service.model_dump(), synchronize_session = False)

    db.commit()
    return service_query.first()
@router.delete("/{id}")
def delete_service(id: int,db: Session = Depends(get_db),
                   current_user: models.User = Depends(oauth2.allow_admin_only)):
    deleted_service = db.query(models.Service).filter(models.Service.id == id)

    service_in_db = deleted_service.first()
    if service_in_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service with id:{id} does not exist")
    deleted_service.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 




