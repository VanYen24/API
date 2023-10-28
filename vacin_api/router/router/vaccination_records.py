from typing import List, Optional
from fastapi import APIRouter, FastAPI, Header, Query
from fastapi.param_functions import Depends
from sqlalchemy.orm import query
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import Null, and_
from sqlalchemy.sql.expression import null, true
from sqlalchemy.sql.functions import mode
from router.dependencies import get_db,return_data
from router.database import engine
from router import models,schemas,oaut2
from router.curd import user as curd
from fastapi.security import OAuth2PasswordBearer
from datetime import date

router = APIRouter(prefix="/vaccination_records",tags=['Vaccination_records'])

models.Base.metadata.create_all(engine)

@router.get("/show_all_schedule_injections")
def show(db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    try:
        info = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
        if info.id_role==3:
            place = db.query(models.Permission_place).filter(models.Permission_place.id_account==id_acc).first()
            check = db.query(models.Schedule_injections)\
                    .join(models.DangKyTiem)\
                    .group_by(models.Schedule_injections.id_dangkytiem)\
                    .having(models.DangKyTiem.id_vaccine_place == place.id_vaccination_place)
            #db_ = db.query(models.Schedule_injections).filter(models.Schedule_injections.date==date)
            db_ = check.filter(models.Schedule_injections.is_active==True)
            lis =[]
            for i in range(0,db_.count()):
                db_dangkytiem = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_dangkytiem==db_[i].id_dangkytiem).first()
                db_user = db.query(models.User).filter(models.User.id_user==db_dangkytiem.id_user).first()
                data = {"id_dangkytiem":db_[i].id_dangkytiem,
                        "full_name":db_user.name_user,
                        "email": db_user.email,
                        "identify": db_user.indentify,
                        "number_of_times": db_dangkytiem.number_of_times,
                        "name_vaccine":db.query(models.Vacxin).filter(models.Vacxin.id ==db_[i].id_vaccine).first().Name,
                        "date_time": db_[i].date,
                        "phone_number": db_user.phone_number
                }
                lis.append(data)
            return return_data(lis,False,"")
        return return_data("",True,"No permission")
    except:
        return return_data("",True,"")

@router.post("/create_vaccination_records")
def create(id: schemas.injections,db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    try:
        info = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
        if info.id_role==3:
            for i in id.id_dangkytiem:
                id_user = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_dangkytiem==i).first().id_user
                db_ = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==id_user)
                if not db_.first():
                    db_= models.Vaccination_records(
                            id_user = id_user,
                            status  = 1)
                    db.add(db_)
                    db.commit()
                    db.refresh(db_)
                else:
                    db_.update({"status":db_.first().status+1})
                    db.commit()
                    
                tmp = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==id_user).first()
                db_= models.Vaccination_records_detail(
                        id_vaccination_record = tmp.id_vaccination_record,
                        id_vaccine_place = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_dangkytiem==i).first().id_vaccine_place,
                        id_vaccine = db.query(models.Schedule_injections).filter(models.Schedule_injections.id_dangkytiem==i).first().id_vaccine,
                        injection_date = db.query(models.Schedule_injections).filter(models.Schedule_injections.id_dangkytiem==i).first().date,
                        blood_pressure =0,
                        level_response=0,
                        heart_rate=0,
                        status = tmp.status,
                        note = "")
                        
                db.add(db_)
                db.commit()
                db.refresh(db_)

                db_ = db.query(models.Schedule_injections).filter(models.Schedule_injections.id_dangkytiem==i)
                db_.update({"is_active":False})
                db.commit()

                db_ = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_dangkytiem==i)
                db_.update({"is_active":False})
                db.commit()
            return return_data("",False,"Done!!!")
        return return_data("",True,"No permission")
    except:
        return return_data("",True,"")

@router.post("/update_vaccination_records_detail_{id}")
def create(id,request : schemas.Vaccination_records_detail,db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    try:
        info = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
        if info.id_role==3:
            info = db.query(models.Vaccination_records_detail).filter(models.Vaccination_records_detail.id_vaccination_records_detail==id)
            if not info.first():
                return return_data("",True,"Not found")
            info.update({"blood_pressure":request.blood_pressure,
                        "level_response": request.level_response,
                        "heart_rate": request.heart_rate,
                        "note": request.note
                        })
            db.commit()
            return return_data("",False,"Updated")
        return return_data("",True,"No permission")
    except:
        return return_data("",True,"")

@router.get("/show_all_vaccination_records")
def show(db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    try:
        info = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
        if info.id_role==3:
            place = db.query(models.Permission_place).filter(models.Permission_place.id_account==id_acc).first()
            db_detail = db.query(models.Vaccination_records_detail).filter(models.Vaccination_records_detail.id_vaccine_place==place.id_vaccination_place)
            #db_detail = db_detail.filter(models.Vaccination_records_detail.status==number_time)
            lis =[]
            for i in range(0,db_detail.count()):
                db_ =  db.query(models.Vaccination_records).filter(models.Vaccination_records.id_vaccination_record==db_detail[i].id_vaccination_record).first()
                db_user = db.query(models.User).filter(models.User.id_user==db_.id_user).first()

                data ={"id_user":db_.id_user,
                        "fullname_user":db_user.name_user,
                        "email": db_user.email,
                        "indentify": db_user.indentify,
                        "id_vaccine": db_detail[i].id_vaccine,
                        "name_vaccine": db.query(models.Vacxin).filter(models.Vacxin.id==db_detail[i].id_vaccine).first().Name,
                        "date": db_detail[i].injection_date,
                        "number_of_times": db_detail[i].status,
                        "id_vaccination_records_detail":db_detail[i].id_vaccination_records_detail,
                        "blood_pressure":db_detail[i].blood_pressure,
                        "level_response":db_detail[i].level_response,
                        "heart_rate":db_detail[i].heart_rate,
                        "note":db_detail[i].note
                        }
                lis.append(data)
            return return_data(lis,False,"")
        return return_data("",True,"No permission")
    except:
        return return_data("",True,"")
