from sqlalchemy.orm import Session
from router import models, schemas, hashing
import sys
from router.dependencies import return_data
def create_vaccination_place(vp: schemas.vaccination_place,db: Session):
    try:
        db_vp= models.Vaccination_place(
            name_place = vp.name_place,
            id_sub_district = vp.id_sub_district,
            id_district = vp.id_district,
            id_city = vp.id_city,
            number_table = vp.number_table,
            address = vp.address,
            curator = vp.curator)
        db.add(db_vp)
        db.commit()
        db.refresh(db_vp)
        return return_data(db_vp,False,"Create done!")
    except:
        return return_data("",True,sys.exc_info()[0])
      
def update_vaccination_place(id: id, vac: schemas.vaccination_place,db: Session):
    
    vp = db.query(models.Vaccination_place).filter(models.Vaccination_place.id_vaccination_place == id)
    if not vp.first():
        return return_data("",True,"Not found")
    vp.update({"name_place": vac.name_place, \
                "id_sub_district": vac.id_sub_district, \
                "id_district": vac.id_district, \
                "id_city": vac.id_city,\
                "number_table": vac.number_table,\
                "address": vac.address, \
                "curator": vac.curator})
    db.commit()
    return return_data("",False,"Updated done!")
def delete_vaccination_place(id: id, db: Session):
    vp = db.query(models.Vaccination_place).filter(models.Vaccination_place.id_vaccination_place==id)
    if not vp.first():
        return return_data("",True,"Not found")
    vp.delete(synchronize_session=False)
    db.commit()
    return return_data("",False,"Deleted done!")