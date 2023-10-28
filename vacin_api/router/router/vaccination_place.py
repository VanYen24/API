from fastapi import APIRouter, FastAPI, Header
from typing import List, Optional
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from router.dependencies import get_db, return_data
from router.database import engine
from router import models,schemas, oaut2
from router.curd import vaccination_place as curd
import sqlalchemy

router = APIRouter( prefix="/vaccination_place",tags=['Vaccination_place'])

models.Base.metadata.create_all(engine)

@router.get("/show_city")
def show(db: Session = Depends(get_db)):
    return return_data(db.query(models.City).all(),False,"")
@router.get("/show_district")
def show(db: Session = Depends(get_db)):
    return return_data(db.query(models.District).all(),False,"")
@router.get("/show_district_{id_city}")
def show(id_city,db: Session = Depends(get_db)):
    return return_data(db.query(models.District).filter(models.District.id_city==id_city).all(),False,"")
@router.get("/show_sub_district_{id_district}")
def show(id_district,db: Session = Depends(get_db)):
    return return_data(db.query(models.Sub_district).filter(models.Sub_district.id_district==id_district).all(),False,"")


@router.get("/show_vaccination_place_")
def show(db: Session = Depends(get_db)):
    db_ = db.query(models.Vaccination_place)
    lis =[]
    for i in range(0,db_.count()):
        data = {"id_vaccination_place":db_[i].id_vaccination_place,
                "name_place": db_[i].name_place,
                "number_table": db_[i].number_table,
                "curator": db_[i].curator,
                "address": db_[i].address,
                "id_city": db_[i].id_city,
                "id_district": db_[i].id_district,
                "id_sub_district": db_[i].id_sub_district,
                "name_city": db.query(models.City).filter(models.City.id_city==db_[i].id_city).first().name_city,
                "name_district": db.query(models.District).filter(models.District.id_district==db_[i].id_district).first().name_district,
                "name_sub_district": db.query(models.Sub_district).filter(models.Sub_district.id_sub_district==db_[i].id_sub_district).first().name_sub_district
        }
        lis.append(data)
    return return_data(lis,False,"")


@router.get("/show_vaccination_place_{city}")
def show(id,db: Session = Depends(get_db)):
    return db.query(models.Vaccination_place)\
            .filter(models.Vaccination_place.id_city==id).all()
@router.get("/show_vaccination_place_{district}")
def show(id,db: Session = Depends(get_db)):
    return db.query(models.Vaccination_place)\
            .filter(models.Vaccination_place.id_district==id).all()
@router.get("/show_vaccination_place_{sub_district}")
def show(id,db: Session = Depends(get_db)):
    return db.query(models.Vaccination_place)\
            .filter(models.Vaccination_place.id_sub_district==id).all()


@router.post("/create_vaccination_place")
def create(vp: schemas.vaccination_place, db: Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    return curd.create_vaccination_place(vp=vp , db=db)
@router.delete("/detele_vaccination_place")
def delete(id, db:Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    return curd.delete_vaccination_place(id=id, db=db)

@router.put("/update_vaccination_place")
def update(id, vac: schemas.vaccination_place, db:Session=Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    return curd.update_vaccination_place(id=id,vac=vac,db=db)


