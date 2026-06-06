from fastapi import FastAPI, Depends, status, HTTPException, Response
from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import engine, get_db, SessionLocal
from . import models, schemas
from .utils import hash_password
from .routers import users, services, auth, bookings, invoices,payments

app = FastAPI()

#models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(services.router)
app.include_router(auth.router)
app.include_router(bookings.router)
app.include_router(payments.router)
app.include_router(invoices.router)




@app.get("/")
def root():
    return { 'messenge':'ok'}
    


