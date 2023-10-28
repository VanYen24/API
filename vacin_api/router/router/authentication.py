from fastapi import APIRouter, FastAPI, status, HTTPException
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from router.dependencies import get_db, return_data
from router.database import engine
from router import models,schemas,token,hashing,oaut2
from router.hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm
from router.curd import account as curd
from typing import List, Optional
from fastapi import APIRouter, FastAPI, Header

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(request: schemas.account, db: Session = Depends(get_db)):
    acc = db.query(models.Account).filter(models.Account.username == request.username).first()
    if not acc:
        return return_data("",True,"Account does not exist!")
    if not Hash.verify(acc.password,request.password):
        return return_data("",True,"Incorrect password")
    if acc.active_acc==False:
        return return_data({"is_active":False},True,"Account has not been activated")
    access_token = token.create_access_token(data={"sub": acc.username})
    db_token = db.query(models.User_token).filter(models.User_token.id_account == acc.id_account)
    db_token.update( {"user_token": access_token})
    db.commit()
    return return_data(access_token,False,"Login")


@router.post("/sign_up")
def sign_up(request: schemas.SignUp,db: Session = Depends(get_db)):
    email = request.email
    check = db.query(models.Account).filter(models.Account.username==email)
    if check.first():
        return return_data("",True,"Registration failed")
    if verify_otp:
        acc = schemas.CreateAccount
        acc.username = request.email
        acc.password = request.password
        acc.role = 5
        curd.create_account(acc=acc,db=db)

        up = db.query(models.Account).filter(models.Account.username == request.email)
        
        up.update({"active_acc": False})
        db.commit()
        return return_data("",False,"Registration done!")
    else:
        return return_data("",True,"Registration failed")
# @router.post("/sign_up_organization")
# def sign_up_organization(request: schemas.SignUpOrgan,db: Session = Depends(get_db)):
#     email = request.email
#     check = db.query(models.Account).filter(models.Account.username==email)
#     if check.first():
#         return return_data("",True,"Registration failed")
#     if verify_otp:
#         check = db.query(models.Organization).filter(models.Organization.phone_number==request.phone_number)
#         if check.first():
#             return return_data("phone number already exists",True,"Registration failed")
#         check = db.query(models.Organization).filter(models.Organization.tax_number==request.tax_number)
#         if check.first():
#             return return_data("Tax number already exists",True,"Registration failed")
#         acc = schemas.CreateAccount
#         acc.username = request.email
#         acc.password = request.password
#         acc.role = 4
#         curd.create_account(acc=acc,db=db)
#         up = db.query(models.Account).filter(models.Account.username == request.email)
        
#         up.update({"active_acc": False})
#         db.commit()
#         id = db.query(models.Account).filter(models.Account.username==request.email).first()
#         db_organ= models.Organization(
#                 id_category_organization = request.id_category_organization,
#                 address = request.address,
#                 id_account = id.id_account,
#                 regency =request.regency,
#                 email = request.email,
#                 name_organization = request.name_organization,
#                 representative_name = request.representative_name,
#                 phone_number = request.phone_number,
#                 tax_number= request.tax_number,
#                 dob =request.dob)
#         db.add(db_organ)
#         db.commit()
#         db.refresh(db_organ)
#         return return_data("",False,"Registration done!")
#     else:
#         return return_data("",True,"Registration failed")
@router.get("/send_otp")
def send_opt(email: str,db: Session = Depends(get_db)):
    pass_w = "anhdat290620"
    
    import smtplib
    import random
    otp = random.randint(10000,99999)
    # smtp = smtplib.SMTP('smtp.gmail.com', 587)
    # smtp.starttls()
    # smtp.login('a33586@thanglong.edu.vn', pass_w)

    # msg = smtplib.SMTPMessage()
    # msg['Subject'] = 'Test email from Python'
    # msg['From'] = 'a33586@thanglong.edu.vn'
    # msg['To'] = email
    # msg.add_header('Content-Type', 'text/plain')

    # # Set the message body
    # msg.set_payload('This is a test email sent from Python.')

    # # Send the email
    # smtp.send_message(msg)

    # # Close the SMTP session
    # smtp.quit()
    # return return_data("",False,"")


    sender = "a33586@thanglong.edu.vn"
    receiver = email
    password = pass_w
    body = f"Verification code is: {otp}"

    message = f"""

    {body}

    """
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender,password)
        server.sendmail(sender, receiver, message)
        check = db.query(models.OTP).filter(models.OTP.email==email)
        if check.first():
            check.update( {"otp": otp})
            db.commit()
            return return_data("",False,"")
        else:
            db_otp= models.OTP(
                email = email,
                otp = otp)
            db.add(db_otp)
            db.commit()
            db.refresh(db_otp)
            return return_data("",False,"")
    except:
        return return_data("",True,"Send OTP done")

@router.post("/verify_otp")
def verify_otp(otp: schemas.Verify_Otp,db: Session = Depends(get_db)):
    db_otp =db.query(models.OTP).filter(models.OTP.email == otp.email).first()
    if db_otp is None:
        return return_data("",True,"Email not exists")
    if db_otp.otp == otp.otp:
        up = db.query(models.Account).filter(models.Account.username == otp.email)
        if up is None:
            return return_data("",True,"Email hasn't been ")
        # print(up)
        if up.first().id_role==5:
            up.update({"active_acc": True})
            db.commit()
        return return_data("",False,"Successful")
    else:
        return return_data("",True,"Wrong otp")
# @router.post("/forget_pass")
# def forget_pass(email: schemas.forget_pass,db: Session = Depends(get_db)):
#     check = db.query(models.Account).filter(models.Account.username==email.email)
#     if not check.first():
#         return return_data("",True,"You are not registered")
#     else:
#         import smtplib
#         import random
#         otp = random.randint(10000,99999)
#         import smtplib
#         sender = "projectvaccine12@gmail.com"
#         receiver = email.email
#         password = "mailproject@123"
#         body = f"Now your password is: {otp}"

#         message = f"""

#         {body}

#         """

#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         try:
#             server.login(sender,password)
#             server.sendmail(sender, receiver, message)
#             check.update({"password":hashing.Hash.bcrypt(str(otp))})
#             db.commit()
#             return return_data("",False,"")
#         except smtplib.SMTPAuthenticationError:
#             return return_data("",True,"")
# @router.post("/change_pass")
# def change_pass(request: schemas.change_pass,db: Session = Depends(get_db),token: Optional[str] = Header("")):
#     id_acc = oaut2.get_current_user(token,db=db)
#     role = db.query(models.Account).filter(models.Account.id_account==id_acc)
    
#     if not Hash.verify(role.first().password,request.old_pass):
#         return return_data("",True,"Wrong password")
#     else:
#         role.update({"password":hashing.Hash.bcrypt(str(request.new_pass))})
#         db.commit()
#         return return_data("",False,"")
