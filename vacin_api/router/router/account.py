from typing import List, Optional
from fastapi import APIRouter, FastAPI, Header
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from router.dependencies import get_db,return_data
from router.database import engine
from router import models,schemas,oaut2
from router.curd import account as curd
from fastapi.security import OAuth2PasswordBearer


router = APIRouter( prefix="/account",tags=['Account'])

models.Base.metadata.create_all(engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/show_account")
def show(db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    role = db.query(models.Account).filter(models.Account.id_account==id_acc).first()

    if role.id_role !=1:
        return return_data("",True,"no permission")
    return return_data(db.query(models.Account).filter(models.Account.active_acc==True).all(),False,"")

@router.post("/create_account")
def create(acc : schemas.CreateAccount, db:Session=Depends(get_db),token: Optional[str] = Header("")):
    if token !="dathn":
        try:
            id_acc = oaut2.get_current_user(token,db=db)
            role = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
            if role.id_role !=1:
                return return_data("",True,"no permission")
            curd.create_account(acc=acc, db=db)
            if acc.role ==3:
                db_ = db.query(models.Account).filter(models.Account.username == acc.username).first()
                check = db.query(models.Permission_place).filter(models.Permission_place.id_account==db_.id_account)
                if check.first():
                    check.update({"id_vaccination_place":acc.id_place})
                    db.commit()

                else:
                    db_role= models.Permission_place(
                        id_vaccination_place = acc.id_place,
                        id_account = db_.id_account)
                    db.add(db_role)
                    db.commit()
                    db.refresh(db_role)
            return return_data("",False,"create done!")
        except:
            return return_data("",True,"")
    return curd.create_account(acc=acc, db=db)


@router.delete("/delete_account")
def delete(id, db:Session=Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    if id == id_acc:
        return return_data("",True,"You cannot delete the account")
    role = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    if role.id_role !=1:
        return return_data("",True,"no permission")
    user = db.query(models.Account).filter(models.Account.id_account==id).first()
    if user.active_acc !=1:
        return return_data("",True,"Account has been deleted")
    # print(role.active_acc)
    return curd.delete_account(id=id, db=db)


