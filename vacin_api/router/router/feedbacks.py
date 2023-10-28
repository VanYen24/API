from typing import List, Optional
from fastapi import APIRouter, FastAPI, Header
from fastapi.param_functions import Depends, Form
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import null, text, true
from sqlalchemy.sql.functions import mode
from router.dependencies import get_db,return_data
from router.database import engine
from router import models,schemas,oaut2
from router.curd import user as curd
from fastapi.security import OAuth2PasswordBearer
from datetime import date
import datetime
import time
router = APIRouter( prefix="/feedbacks",tags=['Feedbacks'])

models.Base.metadata.create_all(engine)

@router.post("/feed_back_user")
def create(feedback: str = Form(...),db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    role = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    db_user = db.query(models.User).filter(models.User.id_account==id_acc).first()
    if role.id_role==5:
        check = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==db_user.id_user).first()
        if not check:
            return return_data("",True,"You don't inject")
        db_feedback = db.query(models.Feedback).filter(models.Feedback.id_user==db_user.id_user)
        if not db_feedback.first():
            db_feedback = models.Feedback(
                                    id_user = db_user.id_user,
                                    content_feedback = feedback,
                                    number_of_times = check.status,
                                    date_time = db.query(models.Vaccination_records_detail).filter(models.Vaccination_records_detail.id_vaccination_record==check.id_vaccination_record).filter(models.Vaccination_records_detail.status==check.status).first().injection_date,
                                    id_vaccine = db.query(models.Vaccination_records_detail).filter(models.Vaccination_records_detail.id_vaccination_record==check.id_vaccination_record).filter(models.Vaccination_records_detail.status==check.status).first().id_vaccine,
                                    id_vaccination_place = db.query(models.Vaccination_records_detail).filter(models.Vaccination_records_detail.id_vaccination_record==check.id_vaccination_record).filter(models.Vaccination_records_detail.status==check.status).first().id_vaccine_place
                                    )
            db.add(db_feedback)
            db.commit()
            db.refresh(db_feedback)
            return return_data("",False,"Create done!")
        else:
            if check.status != db_feedback.first().number_of_times:
                db_feedback = models.Feedback(
                                    id_user = db_user.id_user,
                                    content_feedback = feedback,
                                    number_of_times = check.status,
                                    date_time = db.query(models.Vaccination_records_detail).filter(models.Vaccination_records_detail.id_vaccination_record==check.id_vaccination_record).filter(models.Vaccination_records_detail.status==check.status).first().injection_date,
                                    id_vaccine = db.query(models.Vaccination_records_detail).filter(models.Vaccination_records_detail.id_vaccination_record==check.id_vaccination_record).filter(models.Vaccination_records_detail.status==check.status).first().id_vaccine,
                                    id_vaccination_place = db.query(models.Vaccination_records_detail).filter(models.Vaccination_records_detail.id_vaccination_record==check.id_vaccination_record).filter(models.Vaccination_records_detail.status==check.status).first().id_vaccine_place
                                )
                db.add(db_feedback)
                db.commit()
                db.refresh(db_feedback)
                return return_data("",False,"Create done!")
            else:
                db_feedback.update({"content_feedback":feedback})
                db.commit()
                return return_data("",False,"Create done!")
    return return_data("",True,"No permission")
@router.post("/show_feedback")
def create(feedback: schemas.show_feedback,db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    role = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    try:
        id_place = db.query(models.Permission_place).filter(models.Permission_place.id_account==id_acc).first().id_vaccination_place
        if feedback.inject_date!=0:
            dt_obj = datetime.datetime.fromtimestamp(feedback.inject_date)
            hour = dt_obj.hour
            minute = dt_obj.minute
            second =  dt_obj.second
            feedback.inject_date = feedback.inject_date-hour*3600-minute*60-second
        if role.id_role==3:
            db_feedback = db.query(models.Feedback).filter(models.Feedback.id_vaccination_place==id_place)
            if feedback.id_vaccine !=0:
                db_feedback = db_feedback.filter(models.Feedback.id_vaccine==feedback.id_vaccine)
            if feedback.inject_date!=0:
                db_feedback = db_feedback.filter(models.Feedback.date_time >= feedback.inject_date)
                db_feedback = db_feedback.filter(models.Feedback.date_time < feedback.inject_date+3600*24)
            lis =[]
            for i in range(0,db_feedback.count()):
                db_user = db.query(models.User).filter(models.User.id_user==db_feedback[i].id_user).first()
                data ={
                    "id_user":db_user.id_user,
                    "full_name":db_user.name_user,
                    "email":db_user.email,
                    "phone":db_user.phone_number,
                    "id_vaccine":db_feedback[i].id_vaccine,
                    "inject_date":db_feedback[i].date_time,
                    "feedback":db_feedback[i].content_feedback,
                    "number_inject":db_feedback[i].number_of_times,
                }
                lis.append(data)
            return return_data(lis,False,"")
        return return_data("",True,"No permission")
    except:
        return return_data("",True,"")
    