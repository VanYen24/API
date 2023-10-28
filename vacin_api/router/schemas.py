from datetime import date
from fastapi.param_functions import Query
from pydantic import BaseModel
from typing import Optional, List
from fastapi import File,UploadFile

class vaccination_place(BaseModel):
    name_place: str
    id_sub_district :int
    id_district : int
    id_city: int 
    number_table: int
    address: str
    curator :str
class account(BaseModel):
    username: str
    password: str
class Vacxin(BaseModel):
    Name: str
    Production_by :str
    Quantity : int
    Time: int 
class TokenData(BaseModel):
    username: Optional[str]=None

class SignUp(BaseModel):
    email: str
    password: str
class Verify_Otp(BaseModel):
    otp: int
    email:str
class CreateAccount(BaseModel):
    username: str
    password:str
    role: int =1
    id_place: int
class User(BaseModel):
    phone_number: str
    name_user: str
    address: str
    indentify:str
    insurance: str
    gender:str
    dob: int
    id_district: int
    id_city:int
    id_sub_district:int
class Set_role_place(BaseModel):
    id_vaccination_place: int
    id_account: int
class SignUpOrgan(BaseModel):
    id_category_organization:int
    name_organization:str
    tax_number:str
    address:str
    representative_name:str
    regency:str
    dob:date
    phone_number:str
    email:str
    password:str
class Organization(BaseModel):
    id_category_organization:int
    name_organization:str
    tax_number:str
    address:str
    representative_name:str
    regency:str
    dob:int
    phone_number:str
    email:str
    id_account:int
class Registration_vaccination(BaseModel):
    id_vaccine_place :int
    id_priority : int
    is_sick: bool
    note: str
    number_of_times: int
class Schedule_injections(BaseModel):
    id_dangkytiem: List[int] =Query([])
    date: int
    id_vaccine: int

class Vaccination_records_detail(BaseModel):
    blood_pressure : int
    level_response : int
    heart_rate : int
    note : str
class reports(BaseModel):
    date_from: int=0
    date_to : int=0
    status:  int=0
    number_of_time: int=0
    id_vaccine: int=0
    age_from : int=0
    age_to: int =0
class injections(BaseModel):
    id_dangkytiem: List[int] =Query([])
class reports_manager(BaseModel):
    id_district: int =0
    id_sub_district: int =0
    id_vaccination_place: int =0
    date_from: int=0
    date_to : int=0
    status:  int=0                                                                                                                                                                                                                                                                                                                                                                                                                                      
    number_of_time: int=0
    id_vaccine: int=0
    age_from : int=0
    age_to: int =0
class show_feedback(BaseModel):
    inject_date: int=0
    id_vaccine: int=0
class forget_pass(BaseModel):
    email: str
class change_pass(BaseModel):
    old_pass: str
    new_pass: str