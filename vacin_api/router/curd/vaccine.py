from sqlalchemy.orm import Session
from router import models, schemas, hashing
import sys
from router.dependencies import return_data
def create_vacxin(vacxin: schemas.Vacxin,db: Session):
    try:
        db_vacxin= models.Vacxin(
            Name = vacxin.Name,
            Production_by = vacxin.Production_by,
            Quantity = vacxin.Quantity,
            Time = vacxin.Time)
        db.add(db_vacxin)
        db.commit()
        db.refresh(db_vacxin)
        return return_data(db_vacxin,False,"Create done!")
    except:
        return return_data("",True,sys.exc_info()[0])
def update_vacxin(id: id, vacxin: schemas.Vacxin,db: Session):
    
    vc = db.query(models.Vacxin).filter(models.Vacxin.id == id)
    if not vc.first():
        return return_data("",True,"Not found")
    vc.update( {"Name": vacxin.Name,\
                "Production_by":vacxin.Production_by,\
                "Quantity":vacxin.Quantity,\
                "Time": vacxin.Time})
    db.commit()
    return return_data("",False,"Updated done!")

def delete_vaxin(db: Session,id: id):
    vacxin = db.query(models.Vacxin).filter(models.Vacxin.id==id)
    if not vacxin.first():
        return return_data("",True,"Not found")
    vacxin.delete(synchronize_session=False)
    db.commit()
    return return_data("",False,"Deleted done!")