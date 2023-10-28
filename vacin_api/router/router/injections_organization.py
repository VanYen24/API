from typing import List, Optional
from fastapi import APIRouter, FastAPI, Header, Query,File,UploadFile,Form
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null, true
from sqlalchemy.sql.functions import mode
from router.dependencies import get_db,return_data
from router.database import engine
from router import models,schemas,oaut2
from router.curd import user as curd
from fastapi.security import OAuth2PasswordBearer
import datetime
from router import models, schemas, hashing,token
import pandas as pd
router = APIRouter( prefix="/injections_organization",tags=['Injections_organization'])

models.Base.metadata.create_all(engine)

@router.post("/uploadfile")
def create_upload_file(number_of_times:  int = Form(...),id_vaccination_place: int = Form(...),file: UploadFile = File(...), db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    role = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    if role.id_role!=4:
        return return_data("",True,"No permission")
    data = pd.read_excel(file.file)
    líst_account=[]
    líst_user =[]
    list_dangkytiem =[]
    list_dangkytiem_organ =[]
    list_token =[]
    for index,row in data.iterrows():
        try:
            full_name = row[0]
            phone_number = row[1]
            email = row[2]
            address = row[3]
            indentify =row[4]
            insurance = row[5]
            gender = "male" if row[6]==1 else "female"
            dob = row[7].timestamp()
            id_priority = row[8]
            is_sick = row[9]
            note = row[10]
            print(email)
            db_acc = db.query(models.Account).filter(models.Account.username==email)
            if not db_acc.first():
                if number_of_times!=1:
                    db_=db.query(models.Dangkytiem_Organization).filter(models.Dangkytiem_Organization.id_dangkytiem_organization==0).first().id_dangkytiem
                db_acc= models.Account(
                    username = email,
                    password = hashing.Hash.bcrypt("1"),
                    id_role = 5,
                    active_acc = True)
                db.add(db_acc)
                db.commit()
                db.refresh(db_acc)
                id = db.query(models.Account).filter(models.Account.username==email).first()
                db_token = models.User_token(user_token ="dathn",
                                        id_account = id.id_account)
                db.add(db_token)
                db.commit()
                db.refresh(db_token)
                líst_account.append(id.id_account)
                db_token = db.query(models.User_token).filter(models.User_token.id_account==id.id_account).first().id_user_token
                list_token.append(db_token)
                db_user= models.User(
                        phone_number = phone_number,
                        name_user  = full_name,
                        email  = email,
                        address  = address,
                        indentify  = indentify,
                        insurance = insurance,
                        gender = gender,
                        dob = dob,
                        id_account = id.id_account,
                        id_district = None,
                        id_city = None,
                        id_sub_district = None)
                db.add(db_user)
                db.commit()
                db.refresh(db_user)            
                id_user = db.query(models.User).filter(models.User.email==email).first().id_user
                líst_user.append(id_user)

                db_= models.DangKyTiem(
                        id_vaccine_place  = id_vaccination_place,
                        id_priority = id_priority,
                        date = int(datetime.datetime.now().timestamp()),
                        is_sick = is_sick,
                        note = note,
                        status = False,
                        number_of_times = number_of_times,
                        id_user = id_user,
                        is_active = True)
                db.add(db_)
                db.commit()
                db.refresh(db_)
                id_dangkytiem = db_.id_dangkytiem
                list_dangkytiem.append(id_dangkytiem)
                db_ = models.Dangkytiem_Organization(
                        id_dangkytiem = id_dangkytiem,
                        id_organization = db.query(models.Organization).filter(models.Organization.id_account==id_acc).first().id_organization
                )
                db.add(db_)
                list_dangkytiem_organ.append(db_.id_dangkytiem_organization)
                db.commit()
                db.refresh(db_)
                return return_data("",False,"Create done!")
            else:
                if number_of_times==1:
                    db_user = db.query(models.User).filter(models.User.id_account==db_acc.first().id_account)
                    if not db_user.first():
                        db_user= models.User(
                                phone_number = phone_number,
                                name_user  = full_name,
                                email  = email,
                                address  = address,
                                indentify  = indentify,
                                insurance = insurance,
                                gender = gender,
                                dob = dob,
                                id_account = db_acc.first().id_account,
                                id_district = None,
                                id_city = None,
                                id_sub_district = None)
                        db.add(db_user)
                        db.commit()
                        db.refresh(db_user)            
                        id_user = db.query(models.User).filter(models.User.email==email).first().id_user
                        líst_user.append(id_user)

                        db_= models.DangKyTiem(
                                id_vaccine_place  = id_vaccination_place,
                                id_priority = id_priority,
                                date = int(datetime.datetime.now().timestamp()),
                                is_sick = is_sick,
                                note = note,
                                status = False,
                                number_of_times = number_of_times,
                                id_user = id_user,
                                is_active = True)
                        db.add(db_)
                        db.commit()
                        db.refresh(db_)
                        id_dangkytiem = db_.id_dangkytiem
                        list_dangkytiem.append(id_dangkytiem)
                        db_ = models.Dangkytiem_Organization(
                                id_dangkytiem = id_dangkytiem,
                                id_organization = db.query(models.Organization).filter(models.Organization.id_account==id_acc).first().id_organization
                        )
                        db.add(db_)
                        list_dangkytiem_organ.append(db_.id_dangkytiem_organization)
                        db.commit()
                        db.refresh(db_)
                    else:
                        db_dangkytiem = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_user==db_user.first().id_user)
                        if not db_dangkytiem.first():
                            db_= models.DangKyTiem(
                                    id_vaccine_place  = id_vaccination_place,
                                    id_priority = id_priority,
                                    date = int(datetime.datetime.now().timestamp()),
                                    is_sick = is_sick,
                                    note = note,
                                    status = False,
                                    number_of_times = number_of_times,
                                    id_user = db_user.first().id_user,
                                    is_active = True)
                            db.add(db_)
                            db.commit()
                            db.refresh(db_)
                            id_dangkytiem = db_.id_dangkytiem
                            list_dangkytiem.append(id_dangkytiem)
                            db_ = models.Dangkytiem_Organization(
                                    id_dangkytiem = id_dangkytiem,
                                    id_organization = db.query(models.Organization).filter(models.Organization.id_account==id_acc).first().id_organization
                            )
                            db.add(db_)
                            list_dangkytiem_organ.append(db_.id_dangkytiem_organization)
                            db.commit()
                            db.refresh(db_)
                        else:  
                            db_dangkytiem.update({"id_vaccine_place": id_vaccination_place,
                                            "id_priority" : id_priority,
                                            "date": int(datetime.datetime.now().timestamp()),
                                            "is_sick" : is_sick,
                                            "note":  note,
                                            "status": False,\
                                            "number_of_times": number_of_times,
                                            "id_user" : db_user.first().id_user,
                                            "is_active" : True})
                            db.commit()
                            id_dangkytiem =db_dangkytiem.first().id_dangkytiem
                            list_dangkytiem.append(id_dangkytiem)
                            db_dangky_tochuc = db.query(models.Dangkytiem_Organization).filter(models.Dangkytiem_Organization.id_dangkytiem==id_dangkytiem)
                            if not db_dangkytiem.first():
                                db_ = models.Dangkytiem_Organization(
                                        id_dangkytiem = id_dangkytiem,
                                        id_organization = db.query(models.Organization).filter(models.Organization.id_account==id_acc).first().id_organization
                                )
                                db.add(db_)
                                list_dangkytiem_organ.append(db_.id_dangkytiem_organization)
                                db.commit()
                                db.refresh(db_)
                else:
                    id_user = db.query(models.User).filter(models.User.email==email).first().id_user
                    db_record = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==id_user)
                    if not db_record.first():
                        db_=db.query(models.Dangkytiem_Organization).filter(models.Dangkytiem_Organization.id_dangkytiem_organization==0).first().id_dangkytiem
                    else:
                        if db_record.first().status!=1:  
                            db_=db.query(models.Dangkytiem_Organization).filter(models.Dangkytiem_Organization.id_dangkytiem_organization==0).first().id_dangkytiem
                        else:
                            db_dangkytiem = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_user==id_user)
                            db_dangkytiem = db_dangkytiem.filter(models.DangKyTiem.is_active==True)
                            if not db_dangkytiem.first():
                                db_= models.DangKyTiem(
                                        id_vaccine_place  = id_vaccination_place,
                                        id_priority = id_priority,
                                        date = int(datetime.datetime.now().timestamp()),
                                        is_sick = is_sick,
                                        note = note,
                                        status = False,
                                        number_of_times = number_of_times,
                                        id_user = id_user,
                                        is_active = True)
                                db.add(db_)
                                db.commit()
                                db.refresh(db_)
                                id_dangkytiem = db_.id_dangkytiem
                                list_dangkytiem.append(id_dangkytiem)
                                db_ = models.Dangkytiem_Organization(
                                        id_dangkytiem = id_dangkytiem,
                                        id_organization = db.query(models.Organization).filter(models.Organization.id_account==id_acc).first().id_organization
                                )
                                db.add(db_)
                                list_dangkytiem_organ.append(db_.id_dangkytiem_organization)
                                db.commit()
                                db.refresh(db_)
                            else:
                                db_dangkytiem.update({"id_vaccine_place": id_vaccination_place,
                                        "id_priority" : id_priority,
                                        "date": int(datetime.datetime.now().timestamp()),
                                        "is_sick" : is_sick,
                                        "note":  note,
                                        "status": False,
                                        "number_of_times": number_of_times,
                                        "id_user" : id_user,
                                        "is_active" : True})
                                db.commit()
                                id_dangkytiem =db_dangkytiem.first().id_dangkytiem
                                list_dangkytiem.append(id_dangkytiem)
                                db_ = models.Dangkytiem_Organization(
                                        id_dangkytiem = id_dangkytiem,
                                        id_organization = db.query(models.Organization).filter(models.Organization.id_account==id_acc).first().id_organization
                                )
                                db.add(db_)
                                list_dangkytiem_organ.append(db_.id_dangkytiem_organization)
                                db.commit()
                                db.refresh(db_)
        except:
            for i in líst_account:
                db_ = db.query(models.Account).filter(models.Account.id_account==i)
                db_.delete()
                db.commit()
            for i in líst_user:
                db_ = db.query(models.User).filter(models.User.id_user==i)
                db_.delete()
                db.commit()
            for i in list_dangkytiem:
                db_ = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_dangkytiem==19)
                db_.delete()
                db.commit()
            for i in list_dangkytiem_organ:
                db_ = db.query(models.Dangkytiem_Organization).filter(models.Dangkytiem_Organization.id_dangkytiem_organization==i)
                db_.delete()
                db.commit()
            for i in list_token:
                db_ = db.query(models.User_token).filter(models.User_token.id_user_token==20)
                db_.delete()
                db.commit()
            return return_data({"row_error":index+1},True,"")
    return return_data("",False,"")
@router.get("/show_inject_organization")
def show(db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    role = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    if role.id_role!=4:
        return return_data("",True,"No permission")
    db_organ = db.query(models.Dangkytiem_Organization)
    lis =[]
    for i in range(0,db_organ.count()):
        db_dangkytiem = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_dangkytiem==db_organ[i].id_dangkytiem).first()
        db_user = db.query(models.User).filter(models.User.id_user==db_dangkytiem.id_user).first()
        db_check = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==db_user.id_user).first()
        if not db_check or db_check.status < db_dangkytiem.number_of_times:
            data ={
                "id_user": db_user.id_user,
                "name_user": db_user.name_user,
                "email": db_user.email,
                "indentify":db_user.indentify,
                "phone_number": db_user.phone_number,
                "dob": db_user.dob,
                "number_of_times":db_dangkytiem.number_of_times,
                "status":0,
                "date_inject":"",
                "name_vaccine":"",
            }
            lis.append(data)
        else:
            # print(db_dangkytiem.id_dangkytiem)
            id_vaccine = db.query(models.Schedule_injections).filter(models.Schedule_injections.id_dangkytiem==db_dangkytiem.id_dangkytiem).first().id_vaccine
            data ={
                "id_user": db_user.id_user,
                "name_user": db_user.name_user,
                "email": db_user.email,
                "indentify":db_user.indentify,
                "phone_number": db_user.phone_number,
                "dob": db_user.dob,
                "number_of_times":db_dangkytiem.number_of_times,
                "status":1,
                "date_inject":db.query(models.Schedule_injections).filter(models.Schedule_injections.id_dangkytiem==db_dangkytiem.id_dangkytiem).first().date,
                "name_vaccine":db.query(models.Vacxin).filter(models.Vacxin.id==id_vaccine).first().Name,
            }
            lis.append(data)
    return return_data(lis,False,"")
import sys
import io
import pickle

@router.post("/upload")
async def create_upload_file(file: UploadFile = File(...), db:Session = Depends(get_db)):
    try:

        print(file.file)
        return file.file
    except Exception as e:
        return str(e)

