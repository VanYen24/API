from logging import info
import re
from typing import List, Optional
from fastapi import APIRouter, FastAPI, Header
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import null, true
from sqlalchemy.sql.functions import current_date, mode
from router.dependencies import get_db,return_data
from router.database import engine
from router import models,schemas,oaut2
from router.curd import user as curd
from fastapi.security import OAuth2PasswordBearer
from datetime import date
import datetime
import time
router = APIRouter( prefix="/reports",tags=['Reports'])

models.Base.metadata.create_all(engine)

@router.post("/show_reports")
def create(request: schemas.reports_manager,db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    info =  info = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    if info.id_role!=3 and info.id_role!=2:
        return return_data("",True,"No permission")
    if request.date_from!=0:
        dt_obj = datetime.datetime.fromtimestamp(request.date_from)
        hour = dt_obj.hour
        minute = dt_obj.minute
        second =  dt_obj.second
        request.date_from = request.date_from-hour*3600-minute*60-second
    if request.date_to!=0:
        dt_obj = datetime.datetime.fromtimestamp(request.date_to)
        hour = dt_obj.hour
        minute = dt_obj.minute
        second =  dt_obj.second
        request.date_to = request.date_to-hour*3600-minute*60-second
    place =[]
    if info.id_role==3:
        place.append(db.query(models.Permission_place).filter(models.Permission_place.id_account==id_acc).first().id_vaccination_place)
    else:
        if request.id_vaccination_place!=0:
            place.append(request.id_vaccination_place)
        elif request.id_sub_district!=0:
            db_ = db.query(models.Vaccination_place).filter(models.Vaccination_place.id_sub_district==request.id_sub_district)
            for i in range(0,db_.count()):
                place.append(db_[i].id_vaccination_place)
        elif request.id_district!=0:
            db_ = db.query(models.Vaccination_place).filter(models.Vaccination_place.id_district==request.id_district)
            for i in range(0,db_.count()):
                place.append(db_[i].id_vaccination_place)
        else:
            db_ = db.query(models.Vaccination_place)
            for i in range(0,db_.count()):
                place.append(db_[i].id_vaccination_place)
    lis1,lis2 =[],[]
    for place in place:
        if request.status==2:
            db_detail = db.query(models.Vaccination_records_detail).filter(models.Vaccination_records_detail.id_vaccine_place==place)
            if request.date_from!=0:
                db_detail = db_detail.filter(models.Vaccination_records_detail.injection_date>request.date_from)
            if request.date_to!=0:
                db_detail = db_detail.filter(models.Vaccination_records_detail.injection_date < request.date_to+3600*24)
            if request.number_of_time!=0:
                db_detail = db_detail.filter(models.Vaccination_records_detail.status==request.number_of_time)
            if request.id_vaccine!=0:
                db_detail = db_detail.filter(models.Vaccination_records_detail.id_vaccine==request.id_vaccine)
            for i in range(0,db_detail.count()):
                db_record = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_vaccination_record==db_detail[i].id_vaccination_record).first()
                db_user = db.query(models.User).filter(models.User.id_user== db_record.id_user).first()
                dt_object = datetime.datetime.fromtimestamp(db_user.dob)
                age = datetime.datetime.today().year - dt_object.year
                if request.age_from!=0:
                    if age < request.age_from:
                        continue
                if request.age_to!=0:
                    if age > request.age_to:
                        continue
                if info.id_role ==3:
                    data = {"id_user":db_user.id_user,
                            "name_user": db_user.name_user,
                            "email": db_user.email,
                            "indentify": db_user.indentify,
                            "phone_number": db_user.phone_number,
                            "dob": db_user.dob,
                            "status": 2,
                            "date": db_detail[i].injection_date,
                            "id_vaccine": db_detail[i].id_vaccine,
                            "name_vaccine": db.query(models.Vacxin).filter(models.Vacxin.id==db_detail[i].id_vaccine).first().Name,
                            "number_of_times": db_detail[i].status,
                    }
                else:
                    data = {"id_user":db_user.id_user,
                            "name_user": db_user.name_user,
                            "email": db_user.email,
                            "indentify": db_user.indentify,
                            "phone_number": db_user.phone_number,
                            "dob": db_user.dob,
                            "status": 2,
                            "date": db_detail[i].injection_date,
                            "id_vaccine": db_detail[i].id_vaccine,
                            "name_vaccine": db.query(models.Vacxin).filter(models.Vacxin.id==db_detail[i].id_vaccine).first().Name,
                            "number_of_times": db_detail[i].status,
                            "id_vaccination_place": place,
                            "name_vaccination_place": db.query(models.Vaccination_place).filter(models.Vaccination_place.id_vaccination_place==place).first().name_place
                    }
                lis2.append(data)
            # return return_data(lis2,False,"")
        if request.status==1:
            db_dangkytiem = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_vaccine_place==place)
            db_dangkytiem = db_dangkytiem.filter(models.DangKyTiem.is_active==True)
            if request.number_of_time!=0:
                db_dangkytiem = db_dangkytiem.filter(models.DangKyTiem.number_of_times==request.number_of_time)
            for i in range(0,db_dangkytiem.count()):
                if request.date_from!=0 or request.date_to!=0 or request.id_vaccine!=0:
                    break
                db_user = db.query(models.User).filter(models.User.id_user==db_dangkytiem[i].id_user).first()
                dt_object = datetime.datetime.fromtimestamp(db_user.dob)
                age = datetime.datetime.today().year - dt_object.year
                if request.age_from!=0:
                    if age < request.age_from:
                        continue
                if request.age_to!=0:
                    if age > request.age_to:
                        continue
                if info.id_role ==3:
                    data = {"id_user":db_user.id_user,
                            "name_user": db_user.name_user,
                            "email": db_user.email,
                            "indentify": db_user.indentify,
                            "phone_number": db_user.phone_number,
                            "dob": db_user.dob,
                            "status": 1,
                            "date":None,
                            "id_vaccine": None,
                            "name_vaccine":None,
                            "number_of_times": db_dangkytiem[i].number_of_times
                    }
                else:
                    data = {"id_user":db_user.id_user,
                            "name_user": db_user.name_user,
                            "email": db_user.email,
                            "indentify": db_user.indentify,
                            "phone_number": db_user.phone_number,
                            "dob": db_user.dob,
                            "status": 1,
                            "date":None,
                            "id_vaccine": None,
                            "name_vaccine":None,
                            "number_of_times": db_dangkytiem[i].number_of_times,
                            "id_vaccination_place": place,
                            "name_vaccination_place": db.query(models.Vaccination_place).filter(models.Vaccination_place.id_vaccination_place==place).first().name_place
                    }
                lis2.append(data)
            # return return_data(lis2,False,"")
        if request.status==0:
            db_detail = db.query(models.Vaccination_records_detail).filter(models.Vaccination_records_detail.id_vaccine_place==place)
            if request.date_from!=0:
                db_detail = db_detail.filter(models.Vaccination_records_detail.injection_date>request.date_from)
            if request.date_to!=0:
                db_detail = db_detail.filter(models.Vaccination_records_detail.injection_date < request.date_to+3600*24)
            if request.number_of_time!=0:
                db_detail = db_detail.filter(models.Vaccination_records_detail.status==request.number_of_time)
            if request.id_vaccine!=0:
                db_detail = db_detail.filter(models.Vaccination_records_detail.id_vaccine==request.id_vaccine)
            for i in range(0,db_detail.count()):
                db_record = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_vaccination_record==db_detail[i].id_vaccination_record).first()
                db_user = db.query(models.User).filter(models.User.id_user== db_record.id_user).first()
                dt_object = datetime.datetime.fromtimestamp(db_user.dob)
                age = datetime.datetime.today().year - dt_object.year
                if request.age_from!=0:
                    if age < request.age_from:
                        continue
                if request.age_to!=0:
                    if age > request.age_to:
                        continue
                if info.id_role ==3:
                    data = {"id_user":db_user.id_user,
                            "name_user": db_user.name_user,
                            "email": db_user.email,
                            "indentify": db_user.indentify,
                            "phone_number": db_user.phone_number,
                            "dob": db_user.dob,
                            "status": 2,
                            "date": db_detail[i].injection_date,
                            "id_vaccine": db_detail[i].id_vaccine,
                            "name_vaccine": db.query(models.Vacxin).filter(models.Vacxin.id==db_detail[i].id_vaccine).first().Name,
                            "number_of_times": db_detail[i].status,
                    }
                else:
                    data = {"id_user":db_user.id_user,
                            "name_user": db_user.name_user,
                            "email": db_user.email,
                            "indentify": db_user.indentify,
                            "phone_number": db_user.phone_number,
                            "dob": db_user.dob,
                            "status": 2,
                            "date": db_detail[i].injection_date,
                            "id_vaccine": db_detail[i].id_vaccine,
                            "name_vaccine": db.query(models.Vacxin).filter(models.Vacxin.id==db_detail[i].id_vaccine).first().Name,
                            "number_of_times": db_detail[i].status,
                            "id_vaccination_place": place,
                            "name_vaccination_place": db.query(models.Vaccination_place).filter(models.Vaccination_place.id_vaccination_place==place).first().name_place
                    }
                lis2.append(data)
            db_dangkytiem = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_vaccine_place==place)
            db_dangkytiem = db_dangkytiem.filter(models.DangKyTiem.is_active==True)
            if request.number_of_time!=0:
                db_dangkytiem = db_dangkytiem.filter(models.DangKyTiem.number_of_times==request.number_of_time)
            for i in range(0,db_dangkytiem.count()):
                if request.date_from!=0 or request.date_to!=0 or request.id_vaccine!=0:
                    break
                db_user = db.query(models.User).filter(models.User.id_user==db_dangkytiem[i].id_user).first()
                dt_object = datetime.datetime.fromtimestamp(db_user.dob)
                age = datetime.datetime.today().year - dt_object.year
                if request.age_from!=0:
                    if age < request.age_from:
                        continue
                if request.age_to!=0:
                    if age > request.age_to:
                        continue
                if info.id_role ==3:
                    data = {"id_user":db_user.id_user,
                            "name_user": db_user.name_user,
                            "email": db_user.email,
                            "indentify": db_user.indentify,
                            "phone_number": db_user.phone_number,
                            "dob": db_user.dob,
                            "status": 1,
                            "date":None,
                            "id_vaccine": None,
                            "name_vaccine":None,
                            "number_of_times": db_dangkytiem[i].number_of_times
                    }
                else:
                    data = {"id_user":db_user.id_user,
                            "name_user": db_user.name_user,
                            "email": db_user.email,
                            "indentify": db_user.indentify,
                            "phone_number": db_user.phone_number,
                            "dob": db_user.dob,
                            "status": 1,
                            "date":None,
                            "id_vaccine": None,
                            "name_vaccine":None,
                            "number_of_times": db_dangkytiem[i].number_of_times,
                            "id_vaccination_place": place,
                            "name_vaccination_place": db.query(models.Vaccination_place).filter(models.Vaccination_place.id_vaccination_place==place).first().name_place
                    }
                lis2.append(data)
    return return_data(lis2,False,"")
@router.get("/show_report_injection")
def show(db:Session = Depends(get_db)):
    current_date = datetime.datetime.now()
    timestamp_date = int(current_date.timestamp())-current_date.hour*3600-current_date.minute*60-current_date.second
    last_month=  timestamp_date - 3600*24*30
    list_date = []
    lis_count = [0]*31
    timestamp = last_month
    for i in range(0,31):
        
        db_= db.query(models.Vaccination_records_detail).filter(models.Vaccination_records_detail.injection_date>=timestamp)
        timestamp = last_month +(i+1)*3600*24
        db_date =  db_.filter(models.Vaccination_records_detail.injection_date<timestamp)
        
        date = datetime.datetime.fromtimestamp(last_month+ i*3600*24)
        list_date.append(str(date.date()))
        lis_count[i]+=db_date.count()
    return return_data({"date_time":list_date,
                        "injected":lis_count},False,"")
@router.get("/show_report_vaccine")
def show(db:Session = Depends(get_db)):
    db_vaccine = db.query(models.Vacxin)            
    list_vaccine=[]
    list_count =[]
    for i in range(0,db_vaccine.count()):
        list_vaccine.append(db_vaccine[i].Name)
        db_record = db.query(models.Vaccination_records_detail).filter(models.Vaccination_records_detail.id_vaccine==db_vaccine[i].id)
        list_count.append(db_record.count())
    return return_data({"name_vaccine":list_vaccine,
                        "number_vaccine":list_count},False,"")

@router.get("/show_number")
def show(db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    db_acc = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    if db_acc.id_role!=3:
        return return_data("",True,"No permission")
    place = db.query(models.Permission_place).filter(models.Permission_place.id_account==id_acc).first().id_vaccination_place
    db_detail = db.query(models.Vaccination_records_detail)
    solieutiem = db_detail.count()
    db_detail = db_detail.filter(models.Vaccination_records_detail.id_vaccine_place==place)
    nguoitiem = db_detail.count()
    db_dangky = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_vaccine_place==place)
    dangky = db_dangky.count()
    return return_data({"so_lieu_tiem": solieutiem,
                        "da_tiem": nguoitiem,
                        "dang_ky" :dangky},False,"")

