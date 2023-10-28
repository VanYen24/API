from router.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def return_data(data, status,message):
    return { "status": not status,
            "message": message,
            "data":data}