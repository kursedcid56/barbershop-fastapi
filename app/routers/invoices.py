from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import SessionLocal, get_db
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from typing import Optional, List


router = APIRouter(
    prefix="/invoices",
    tags=["Invoice"]
)


@router.get("/revenue")
def revenue(db:Session = Depends(get_db), current_user:models.User = Depends(oauth2.allow_admin_only)):
    query = db.query(models.Invoices).filter(models.Invoices.status == "paid").all()
    revenue = sum(i.total_amount for i in query) 
    
    return {"total_revenue": revenue, "total_invoices_paid": len(query)}


@router.get("/{id}", response_model= schemas.InvoiceOut)
def get_invoice(id:int ,db:Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.allow_all)):
    query = db.query(models.Invoices).filter(models.Invoices.id == id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invoice with id:{id} does not exist")
    return query



            


