from typing import List, Optional
from fastapi import APIRouter, FastAPI, Header, Query
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

router = APIRouter( prefix="/injections",tags=['Injections'])

models.Base.metadata.create_all(engine)

@router.post("/registration_vaccination")
def create(request: schemas.Registration_vaccination ,db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    role = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
    if role.id_role!=5:
        return return_data("",True,"No permission")

    id_user = db.query(models.User).filter(models.User.id_account==id_acc).first().id_user
    check = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==id_user).first()
    db_ = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_user==id_user)
    Somui = request.number_of_times
    if Somui ==1:
        info = db_.filter(models.DangKyTiem.number_of_times==1)
        if not info.first():
            check = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==id_user).first()
            if check:
                return return_data("",True,"You have injected the number 1")
            db_= models.DangKyTiem(
                    id_vaccine_place  = request.id_vaccine_place,
                    id_priority = request.id_priority,
                    date = int(datetime.datetime.now().timestamp()),
                    is_sick = request.is_sick,
                    note = request.note,
                    status = False,
                    number_of_times = request.number_of_times,
                    id_user = id_user,
                    is_active = True)
            db.add(db_)
            db.commit()
            db.refresh(db_)
            return return_data("",False,"Create done!")
        else:
            check = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==id_user).first()
            if check:
                return return_data("",True,"You have injected the number 1")
            info.update({   "id_vaccine_place":request.id_vaccine_place,
                            "id_priority":request.id_priority,
                            "date": int(datetime.datetime.now().timestamp()),
                            "is_sick":request.is_sick,
                            "note": request.note,
                            "status":False,
                            "number_of_times":request.number_of_times,
                            "is_active": True,
            })
            db.commit()
            db_ = db.query(models.Schedule_injections).filter(models.Schedule_injections.id_dangkytiem==info.first().id_dangkytiem)
            if db_.first():
                db_.delete()
                db.commit()
            return return_data("",False,"Create done!")

    elif Somui ==2:
        info = db_.filter(models.DangKyTiem.number_of_times==2)
        db_ = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==id_user).first()
        if not db_:
            return return_data("",True,"You have not injected the number 1")
        if not info.first():
            check = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==id_user).first()
            if check.status==2:
                return return_data("",True,"You have injected the number 2")
            db_= models.DangKyTiem(
                        id_vaccine_place  = request.id_vaccine_place,
                        id_priority = request.id_priority,
                        date = int(datetime.datetime.now().timestamp()),
                        is_sick = request.is_sick,
                        note = request.note,
                        status = False,
                        number_of_times = request.number_of_times,
                        id_user = id_user,
                        is_active = True)
            db.add(db_)
            db.commit()
            db.refresh(db_)
            return return_data("",False,"Create done!")
        else:
            check = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==id_user).first()
            if check.status==2:
                return return_data("",True,"You have injected the number 2")
            info.update({   "id_vaccine_place":request.id_vaccine_place,
                            "id_priority":request.id_priority,
                            "date": int(datetime.datetime.now().timestamp()),
                            "is_sick":request.is_sick,
                            "note": request.note,
                            "status":False,
                            "number_of_times":request.number_of_times,
                            "is_active": True,
            })
            db.commit()
            db_ = db.query(models.Schedule_injections).filter(models.Schedule_injections.id_dangkytiem==info.first().id_dangkytiem)
            if db_.first():
                db_.delete()
                db.commit()
            return return_data("",False,"Create done!")
    elif Somui >2:
        info = db_.filter(models.DangKyTiem.number_of_times==Somui)
        db_ = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==id_user).first()
        if not db_:
            return return_data("",True,"You have not injected the number 1")
        if not info.first():
            check = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==id_user).first()
            if check.status !=Somui-1:
                return return_data("",True,"You can register numnber inject other")
            db_= models.DangKyTiem(
                        id_vaccine_place  = request.id_vaccine_place,
                        id_priority = request.id_priority,
                        date = int(datetime.datetime.now().timestamp()),
                        is_sick = request.is_sick,
                        note = request.note,
                        status = False,
                        number_of_times = request.number_of_times,
                        id_user = id_user,
                        is_active = True)
            db.add(db_)
            db.commit()
            db.refresh(db_)
            return return_data("",False,"Create done!")
        else:
            check = db.query(models.Vaccination_records).filter(models.Vaccination_records.id_user==id_user).first()
            if check.status !=Somui-1:
                return return_data("",True,"You can register numnber inject other")
            info.update({   "id_vaccine_place":request.id_vaccine_place,
                            "id_priority":request.id_priority,
                            "date": int(datetime.datetime.now().timestamp()),
                            "is_sick":request.is_sick,
                            "note": request.note,
                            "status":False,
                            "number_of_times":request.number_of_times,
                            "is_active": True,
            })
            db.commit()
            db_ = db.query(models.Schedule_injections).filter(models.Schedule_injections.id_dangkytiem==info.first().id_dangkytiem)
            if db_.first():
                db_.delete()
                db.commit()
            return return_data("",False,"Create done!")


@router.get("/search_registration")
def show(db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    try:
        id_user = db.query(models.User).filter(models.User.id_account==id_acc).first().id_user
        info = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_user == id_user)
        info = info.filter(models.DangKyTiem.is_active==True).first()
        if not info:
            return return_data("",True,"You are not registered")
        else:
            return return_data({"id_dangkytiem":info.id_dangkytiem,
                                "id_vaccine_place":info.id_vaccine_place,
                                "id_priority": info.id_priority,
                                "date":info.date,
                                "is_sick":info.is_sick,
                                "note":info.note,
                                "status": info.status,
                                "number_of_times":info.number_of_times,
                                "id_user":info.id_user,
                                "is_active": info.is_active,
                                "name_vaccine_place": db.query(models.Vaccination_place).filter(models.Vaccination_place.id_vaccination_place==info.id_vaccine_place).first().name_place
                                },False,"")
    except:
        return return_data("",True,"")

@router.get("/search_schedule_injections")
def show(db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    try:
        id_user = db.query(models.User).filter(models.User.id_account==id_acc).first().id_user
        info = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_user == id_user)
        info = info.filter(models.DangKyTiem.is_active == True).first()
        if not info:
            return return_data(info,True,"You are not registered")
        Lichtiem = db.query(models.Schedule_injections).filter(models.Schedule_injections.id_dangkytiem==info.id_dangkytiem).first()
        if not Lichtiem or Lichtiem.is_active==False:
            return return_data("",True,"Waiting for approval")
        else:
            return return_data({"Date": Lichtiem.date,
                                "id_vaccine": Lichtiem.id_vaccine,
                                "Vaccine": db.query(models.Vacxin).filter(models.Vacxin.id==Lichtiem.id_vaccine).first().Name,
                                "id_vaccine_place":info.id_vaccine_place,
                                "name_vaccine_place": db.query(models.Vaccination_place).filter(models.Vaccination_place.id_vaccination_place==info.id_vaccine_place).first().name_place
                                },False,"")
    except:
        return return_data("",True,"")

@router.get("/show_registration_vaccination")
def show(db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    try:
        info = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
        if info.id_role==3:
            place = db.query(models.Permission_place).filter(models.Permission_place.id_account==id_acc).first()
            status = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_vaccine_place==place.id_vaccination_place)
            status = status.filter(models.DangKyTiem.is_active==True)
            db_ = status.filter(models.DangKyTiem.status==False)
            #db_ = db_.filter(models.DangKyTiem.number_of_times==id)
            lis =[]
            for i in range(0,db_.count()):
                db_organ = db.query(models.Dangkytiem_Organization).filter(models.Dangkytiem_Organization.id_dangkytiem==db_[i].id_dangkytiem)
                # if db_organ.first():
                #     continue
                data ={
                    "id_dangkytiem": db_[i].id_dangkytiem,
                    "id_vaccine_place": db_[i].id_vaccine_place,
                    "id_priority": db_[i].id_priority,
                    "date": db_[i].date,
                    "is_sick": db_[i].is_sick,
                    "note": db_[i].note,
                    "status": db_[i].status,
                    "number_of_times": db_[i].number_of_times,
                    "id_user": db_[i].id_user,
                    "is_active": db_[i].is_active,
                    "email": db.query(models.User).filter(models.User.id_user==db_[i].id_user).first().email,
                    "name_vaccine_place": db.query(models.Vaccination_place).filter(models.Vaccination_place.id_vaccination_place==db_[i].id_vaccine_place).first().name_place
                }
                lis.append(data)
            return return_data(lis,False,"")
        return return_data("",True,"No permission")
    except:
        return return_data("",True,"")
@router.get("/show_registration_vaccination_organization")
def show(db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    try:
        info = db.query(models.Account).filter(models.Account.id_account==id_acc).first()
        if info.id_role==3:
            place = db.query(models.Permission_place).filter(models.Permission_place.id_account==id_acc).first()
            status = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_vaccine_place==place.id_vaccination_place)
            status = status.filter(models.DangKyTiem.is_active==True)
            db_ = status.filter(models.DangKyTiem.status==False)
            #db_ = db_.filter(models.DangKyTiem.number_of_times==id)
            lis =[]
            for i in range(0,db_.count()):
                db_organ = db.query(models.Dangkytiem_Organization).filter(models.Dangkytiem_Organization.id_dangkytiem==db_[i].id_dangkytiem)
                if not db_organ.first():
                    continue
                data ={
                    "id_dangkytiem": db_[i].id_dangkytiem,
                    "id_vaccine_place": db_[i].id_vaccine_place,
                    "id_priority": db_[i].id_priority,
                    "date": db_[i].date,
                    "is_sick": db_[i].is_sick,
                    "note": db_[i].note,
                    "status": db_[i].status,
                    "number_of_times": db_[i].number_of_times,
                    "id_user": db_[i].id_user,
                    "is_active": db_[i].is_active,
                    "email": db.query(models.User).filter(models.User.id_user==db_[i].id_user).first().email,
                    "name_vaccine_place": db.query(models.Vaccination_place).filter(models.Vaccination_place.id_vaccination_place==db_[i].id_vaccine_place).first().name_place
                }
                lis.append(data)
            return return_data(lis,False,"")
        return return_data("",True,"No permission")
    except:
        return return_data("",True,"")
@router.post("/schedule_injections")
def create(request: schemas.Schedule_injections,db:Session = Depends(get_db),token: Optional[str] = Header("")):
    # request  :{id_dangkytiem: List[int] =Query([])
    #           date: int
    #           id_vaccine: int}

    id_acc = oaut2.get_current_user(token,db=db) # Kiểm tra token và lấy id của token
    try:
        info = db.query(models.Account).filter(models.Account.id_account==id_acc).first() #Lấy thông tin tài khoản
        if info.id_role==3:
            dt_obj = datetime.datetime.fromtimestamp(request.date) # lấy timestamp của request.date
            hour = dt_obj.hour 
            minute = dt_obj.minute
            second =  dt_obj.second
            request.date = request.date-hour*3600-minute*60-second # đưa về chuẩn timestamp tại 0hour 0minute 0second
            place = db.query(models.Permission_place).filter(models.Permission_place.id_account==id_acc).first() #Lấy ra điểm tiêm theo account
            table = db.query(models.Vaccination_place).filter(models.Vaccination_place.id_vaccination_place==place.id_vaccination_place).first().number_table
            # table: số bàn tiêm tại điểm tiêm
            split = 10 # khoảng cách giữa 2 người tiêm (phút)
            before= [0]*(240//split) #mảng kiểm tra ghế trống vào buổi sáng của ngày
            after = before   # #mảng kiểm tra ghế trống vào buổi sáng của chiều
            db_date = db.query(models.Schedule_injections).filter(models.Schedule_injections.date>request.date)
            db_date = db_date.filter(models.Schedule_injections.date<request.date+86400) # lấy ra bản ghi có ngày trùng với request.date
            if table * len(before)*2 - db_date.count() < len(request.id_dangkytiem): #kiểm tra số lượng lượt xếp lịch với số lượng ghê trống
                return return_data("",True,"Overload!!!!") #nếu quá trả về quá tải
            else:
                for i in range(0,db_date.count()): # duyệt 1 vòng bản ghi để check chỗ trống lưu vào 2 mảng 
                    tmp = db_date[i].date - request.date
                    if tmp <= 39600:
                        tmp -= 25200
                        before[tmp//(60*split)]+=1
                    else:
                        tmp -= 46800
                        after[tmp//(60*split)]+=1
            checkpoint1 =0 #đánh dáu thời điểm  từ đây trở về trước đã full chỗ tại buổi sáng
            checkpoint2 = 0  #đánh dáu thời điểm  từ đây trở về trước đã full chỗ tại buổi chiều
            for id in request.id_dangkytiem:
                if checkpoint1 < len(before):
                    for i in range(checkpoint1,len(before)):
                        if before[i] < table:       # nếu tại thời điểm đó vẫn còn chỗ khởi tạo lịch tiêm cho đối tượng tại thời điểm này
                            date_ = request.date + 25200 + i*60*split
                            before[i]+=1            #dánh dấu tại đây vừa thêm 1 dối tượng
                            db_= models.Schedule_injections(                     #tạo lịch tiêm mới
                                        id_dangkytiem = id,
                                        date  = date_,
                                        id_vaccine  = request.id_vaccine,
                                        is_active = True)
                            db.add(db_)
                            db.commit()
                            db.refresh(db_)
                            db_ = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_dangkytiem==id)
                            db_.update({"status":True})
                            db.commit()
                            break
                        else:
                            checkpoint1=i+1
                else:
                    for i in range(checkpoint2,len(after)):  #tương tự như buổi sáng
                        if after[i] < table:
                            date_ = request.date + 46800 + i*60*split
                            after[i]+=1
                            db_= models.Schedule_injections(
                                        id_dangkytiem = id,
                                        date  = date_,
                                        id_vaccine  = request.id_vaccine,
                                        is_active = True)
                            db.add(db_)
                            db.commit()
                            db.refresh(db_)
                            db_ = db.query(models.DangKyTiem).filter(models.DangKyTiem.id_dangkytiem==id)
                            db_.update({"status":True})
                            db.commit()
                            break
                        else:
                            checkpoint2=i+1
            return return_data("",False,"Updated done!")
        return return_data("",True,"No permission")
    except:
        return return_data("",True,"")