from fastapi import APIRouter, FastAPI, Header
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from router.dependencies import get_db,return_data
from router.database import engine
from router import models,schemas,oaut2
from router.curd import vaccine as curd
from typing import Optional

router = APIRouter( prefix="/vaccine",tags=['Vaccine'])

models.Base.metadata.create_all(engine)

@router.post("/create")
def create(vacxin: schemas.Vacxin,db: Session = Depends(get_db),token: Optional[str] = Header("")):

    id_acc = oaut2.get_current_user(token,db=db)
    return curd.create_vacxin(vacxin=vacxin,db =db)

@router.get("/show_all")
def show(db: Session = Depends(get_db)):
    return return_data(db.query(models.Vacxin).all(),False,"")

@router.get("/show_{id}")
def show(id,db: Session = Depends(get_db)):
    return return_data(db.query(models.Vacxin).filter(models.Vacxin.id ==id),False,"")

@router.put("/update")
def update(id, vacxin: schemas.Vacxin,db: Session = Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    return curd.update_vacxin(id=id,vacxin=vacxin,db =db)

@router.delete("/delete")
def delete(id, db:Session=Depends(get_db),token: Optional[str] = Header("")):
    id_acc = oaut2.get_current_user(token,db=db)
    return curd.delete_vaxin(db =db, id=id)
