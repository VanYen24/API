from re import M
from router.curd import account
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from router import models, schemas, hashing,token
import sys
from ..dependencies import return_data

def create_profile(id_acc,request: schemas.User, db :Session):
    db_user= models.User(
                    phone_number = request.phone_number,
                    name_user  = request.name_user,
                    email  = request.email,
                    address  = request.address,
                    indentify  = request.indentify,
                    insurance = request.insurance,
                    gender = request.gender,
                    dob = request.dob,
                    id_account = id_acc,
                    id_district = request.id_district,
                    id_city = request.id_city,
                    id_sub_district = request.id_sub_district)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return return_data("",False,"Create done!")

def update_profile(id_acc,request: schemas.User, db :Session):
    db_user = db.query(models.User).filter(models.User.id_account == id_acc)
    db_user.update({"phone_number" : request.phone_number,
                    "name_user" : request.name_user,
                    "email": request.email,
                    "address": request.address,
                    "indentify": request.indentify,
                    "insurance": request.insurance,
                    "gender": request.gender,
                    "dob": request.dob,
                    "id_account": id_acc,
                    "id_district" : request.id_district,
                    "id_city" : request.id_city,
                    "id_sub_district" : request.id_sub_district})
    db.commit()
    return return_data("",False,"Updated done!")
