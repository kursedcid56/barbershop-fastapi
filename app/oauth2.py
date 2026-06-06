from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from . import database, models
from typing import List
#SECRECT_KEY
#Algorithm
#Expritation time

oau2th_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRECT_KEY ="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded = jwt.encode(to_encode, SECRECT_KEY, algorithm=ALGORITHM)

    return encoded

def verify_access_token(token: str, credentials_exception) -> schemas.TokenData:
    try:
        payload = jwt.decode(token, SECRECT_KEY, algorithms=[ALGORITHM])
        
        id: str = payload.get("user_id")

        if id is None:
            raise  credentials_exception        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise  credentials_exception

    return token_data  
    

def get_current_user(token: str = Depends(oau2th_schema), db: Session = Depends(database.get_db)) -> models.User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"could not validate credentials", 
                                          headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == int(token.id)).first()

    if user is None:
        raise credentials_exception

    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not Allowed")
        
        return current_user

allow_admin_only = RoleChecker(["admin"])             
allow_staff_and_admin = RoleChecker(["admin","staff"])
allow_all = RoleChecker(["admin","staff", "customer"])