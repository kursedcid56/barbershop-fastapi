from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import SessionLocal, get_db
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from typing import Optional, List


router = APIRouter(
    prefix="/payments",
    tags=["Payment"]
)


@router.post("/", response_model=schemas.PaymentOut)
def payment( input: schemas.PaymenCreate,db: Session = Depends(get_db),
            current_user: models.User = Depends(oauth2.allow_staff_and_admin)):
    query = db.query(models.Invoices).filter(models.Invoices.id == input.invoice_id)
    invoice_in_db = query.first()

    if not invoice_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invoice with id:{id} does not exist")
    if invoice_in_db.status == "paid":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This Invoice was already paid")

    total = db.query(models.Payment).filter(models.Payment.invoice_id == input.invoice_id).all()
    total_paid = 0
    for i in total:
        total_paid += i.amount_paid
    total_paid += input.amount_paid
    
    if total_paid >= invoice_in_db.total_amount:
        invoice_in_db.status = schemas.StatusEnom.PAID
    else:
        invoice_in_db.status = schemas.StatusEnom.PARTIAL

    input_data = input.model_dump()
    new_payment = models.Payment(**input_data)
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment