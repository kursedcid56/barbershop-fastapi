from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import SessionLocal, get_db
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from typing import Optional, List


router = APIRouter(
    prefix="/bookings",
    tags=['Bookings']
)
#Admin/Staff
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.BookingOut)
def create_booking(booking: schemas.BookingCreate,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(oauth2.allow_all)):
    service  = db.query(models.Service).filter(models.Service.id == booking.service_id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service with id:{id} not exist")
    
    booking_data = booking.model_dump()
    booking_data["user_id"] = current_user.id

    new_booking = models.Bookings(**booking_data)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    return new_booking

@router.get("/", response_model=List[schemas.BookingOut])
def get_booking(db: Session = Depends(get_db),
                 current_user: models.User = Depends(oauth2.allow_staff_and_admin)):
    list = db.query(models.Bookings).all()

    return list

@router.get("/me", response_model=List[schemas.BookingOut])
def get_me( db:Session = Depends(get_db),
           current_user: models.User = Depends(oauth2.allow_all)):
    me = db.query(models.Bookings).filter(models.Bookings.user_id == current_user.id).all()
    if not me: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"You don't have any schedule yet")
    
    return me


@router.get("/{id}", response_model= schemas.BookingOut)
def get_booking(id:int, db:Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.allow_staff_and_admin)):
    get_booking_query = db.query(models.Bookings).filter(models.Bookings.id == id).first()
    if not get_booking_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Booking with id:{id} does not exist")
    
    return get_booking_query

@router.patch("/{id}/status", response_model=schemas.BookingOut)
def update_booking_update(id:int,status_update: schemas.BookingStateUpdate,
                          db:Session = Depends(get_db),
                          current_user: models.User = Depends(oauth2.allow_staff_and_admin)):
    booking_query = db.query(models.Bookings).filter(models.Bookings.id == id).first()

    if not booking_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Booking with id:{id} does not exist")
    booking_query.status = status_update.status

    db.commit()
    db.refresh(booking_query)
    
    return booking_query



#CUSTOMER


@router.put('/{id}' ,response_model= schemas.BookingOut)
def update_booking(id: int,booking:schemas.BookingUpdate,db: Session = Depends(get_db),
                   current_user:models.User = Depends(oauth2.allow_all)):
    booking_query = db.query(models.Bookings).filter(models.Bookings.id == id)
    booking_in_db = booking_query.first()

    if not booking_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Booking with id:{id} does not exist")
    
    if booking_in_db.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you're not allowed")
                            

    booking_query.update(booking.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return booking_query.first()
@router.delete('/{id}')
def delete_booking(id:int, db:Session = Depends(get_db),
                   current_user: models.User = Depends(oauth2.allow_all)):
    delete_query = db.query(models.Bookings).filter(models.Bookings.id == id)
    delete_indb = delete_query.first()
    if not delete_indb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Booking with id:{id} does not exist")
    
    if delete_indb.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You're not allowed")
    
    delete_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




