from typing import List, Optional
from fastapi import APIRouter, FastAPI, Header
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.functions import mode
from router.dependencies import get_db,return_data
from router.database import engine
from router import models,schemas,oaut2
from router.curd import user as curd
from fastapi.security import OAuth2PasswordBearer


router = APIRouter( prefix="/organization",tags=['Organizations'])

models.Base.metadata.create_all(engine)

@router.get("/show_all_organization")
def show(db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    role = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    if role.id_role==1 or role.id_role==2:
        check = db.query(models.Organization)\
                .join(models.Account)\
                .group_by(models.Organization.id_account)\
                .having(models.Account.active_acc==False)
        return return_data(check.all(),False,"")
    return return_data("",True,"no permission")
@router.get("/show_detail_organization/{id_organization}")
def show(id_organization,db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    role = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    if role.id_role==1 or role.id_role==2:
        return return_data(db.query(models.Organization).filter(models.Organization.id_organization==id_organization).first(),False,"")

    return return_data("",True,"no permission")


@router.post("/approve_organization/{id_organization}")
def show(id_organization,db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    role = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    if role.id_role==1 or role.id_role==2:
        id_account = db.query(models.Organization).filter(models.Organization.id_organization==id_organization).first()
        db_acc = db.query(models.Account).filter(models.Account.id_account == id_account.id_account)
        db_acc.update( {"active_acc": True})
        db.commit()
        return return_data("",False,"Approved!")
    return return_data("",True,"no permission")

@router.get("/show_category_organization")
def show(db:Session = Depends(get_db)):
    return return_data(db.query(models.Category_organization).all(),True,"no permission")