from typing import List, Optional
from fastapi import APIRouter, FastAPI, Header
from fastapi.param_functions import Depends, Form
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import null, text, true
from sqlalchemy.sql.functions import mode
from router.dependencies import get_db,return_data
from router.hashing import Hash
from router.database import engine
from router import models,schemas,oaut2,hashing
from router.curd import user as curd
from fastapi.security import OAuth2PasswordBearer
from datetime import date
import datetime
import time
router = APIRouter( prefix="/users",tags=['Users'])

models.Base.metadata.create_all(engine)

@router.get("/show_myinfo")
def show(db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    info = db.query(models.User).filter(models.User.id_account==id_acc).first()
    role = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    if not info:
        return return_data({"id_user":0,
            "name_user": "",
            "role":   role.id_role,
            "email": role.username,
            "phone_number": "",
            "indentify": "",
            "gender": "",
            "insurance": "",
            "dob": int(datetime.datetime.now().timestamp()),
            "address": "",
            "id_city": 1,
            "id_district": 0,
            "id_sub_district": 0},False,"")
    return return_data({"id_user": info.id_user,
            "name_user": info.name_user,
            "role":   role.id_role,
            "email": info.email,
            "phone_number": info.phone_number,
            "indentify": info.indentify,
            "gender": info.gender,
            "insurance": info.insurance,
            "dob": info.dob,
            "address": info.address,
            "id_city": info.id_city,
            "id_district": info.id_district,
            "id_sub_district": info.id_sub_district},False,"")

@router.post("/create_myinfo")
def create(request: schemas.User,db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    role = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    info = db.query(models.User).filter(models.User.id_account==id_acc)
    if role.id_role!=4:
        if not info.first():
            dictrict = db.query(models.Sub_district).filter(models.Sub_district.id_sub_district==request.id_sub_district).first().id_district
            db_user= models.User(
                    phone_number = request.phone_number,
                    name_user  = request.name_user,
                    email  = role.username,
                    address  = request.address,
                    indentify  = request.indentify,
                    insurance = request.insurance,
                    gender = request.gender,
                    dob = request.dob,
                    id_account = id_acc,
                    id_district = dictrict,
                    id_city = db.query(models.District).filter(models.District.id_district==dictrict).first().id_city,
                    id_sub_district = request.id_sub_district)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return return_data("",False,"Create done!")
        else:
            db_user = db.query(models.User).filter(models.User.id_account == id_acc)
            db_user.update({"phone_number" : request.phone_number,
                            "name_user" : request.name_user,
                            "email": role.username,
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
    return "ko co quyen"

@router.get("/show_vaccination_place")
def show(db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    info = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    if info.id_role !=3:
        return return_data("",True,"No permission")
    db_ = db.query(models.Permission_place).filter(models.Permission_place.id_account==id_acc).first()
    db_ = db.query(models.Vaccination_place).filter(models.Vaccination_place.id_vaccination_place==db_.id_vaccination_place).first()
    return return_data(db_,False,"")

@router.get("/my_vaccinations_record")
def show(db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    info = db.query(models.User).filter(models.User.id_account==id_acc).first()
    db_ = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==info.id_user).first()
    if not db_:
        return return_data("",True,"You don't have vaccination record")
    else:
        db_detail = db.query(models.Vaccination_records_detail).filter(models.Vaccination_records_detail.id_vaccination_record==db_.id_vaccination_record)
        lis =[]
        for i in range(0,db_detail.count()):
            data = {"id_vaccine":db_detail[i].id_vaccine,
                    "name_vaccine":db.query(models.Vacxin).filter(models.Vacxin.id == db_detail[i].id_vaccine).first().Name,
                    "id_vaccine_place":db_detail[i].id_vaccine_place,
                    "name_vaccine_place": db.query(models.Vaccination_place).filter(models.Vaccination_place.id_vaccination_place==db_detail[i].id_vaccine_place).first().name_place,
                    "injection_date":db_detail[i].injection_date,
                    "blood_pressure":db_detail[i].blood_pressure,
                    "level_response": db_detail[i].level_response,
                    "heart_rate":db_detail[i].heart_rate,
                    "note":db_detail[i].note,
                    "number_of_times":db_detail[i].status,
                    "id_vaccination_records_detail": db_detail[i].id_vaccination_records_detail
                    }
            lis.append(data)
        return return_data(lis,False,"")
@router.post("/change_pass")
def change_pass(request: schemas.change_pass,db: Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    role = db.query(models.Account).filter(models.Account.id_account==id_acc)
    
    if not Hash.verify(role.first().password,request.old_pass):
        return return_data("",True,"Wrong password")
    else:
        role.update({"password":hashing.Hash.bcrypt(str(request.new_pass))})
        db.commit()
        return return_data("",False,"")

    