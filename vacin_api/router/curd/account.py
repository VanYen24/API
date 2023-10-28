from re import M
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from router import models, schemas, hashing,token
import sys
from ..dependencies import return_data

def create_account(acc: schemas.CreateAccount, db :Session):
    try: 
        db_acc= models.Account(
            username = acc.username,
            password = hashing.Hash.bcrypt(acc.password),
            id_role = acc.role,
            active_acc = True)
        db.add(db_acc)
        db.commit()
        db.refresh(db_acc)
        id = db.query(models.Account).filter(models.Account.username==acc.username).first()
        db_token = models.User_token(user_token ="dathn",
                                id_account = id.id_account)
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
        return return_data("",False,"Create done!")
    except:
        return return_data("",True,"Account already exists")
def delete_account(id :id, db:Session):
    acc = db.query(models.Account).filter(models.Account.id_account==id).first()
    if not acc:
        return return_data("",True,"Not found")
    acc.active_acc = 0
    db.commit()
    return return_data("",False,f"Deleted id: {id} done!")