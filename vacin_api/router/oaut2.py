from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from router import token
from router.dependencies import get_db,return_data
from router import models,schemas
from sqlalchemy.orm.session import Session

def get_current_user(data: str,db:Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    tmp = db.query(models.User_token).filter(models.User_token.user_token==data).first()
    if not tmp:
        raise credentials_exception
    else:
        return tmp.id_account