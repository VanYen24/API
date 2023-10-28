from enum import unique
from typing import Text
from pydantic.main import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import INTEGER, TIMESTAMP, Date

from router.database import Base

class Vacxin(Base):
    __tablename__ = "vacxin"

    id = Column(Integer, primary_key=True,autoincrement=True)
    Name = Column(String)
    Production_by = Column(String)
    Quantity = Column(Integer)
    Time = Column(Integer)
    
class Vaccination_place(Base):
    __tablename__ = "vaccination_place"

    id_vaccination_place = Column(Integer, primary_key=True,autoincrement=True)
    name_place = Column(String)
    id_sub_district = Column(Integer,ForeignKey('sub_district.id_sub_district'))
    id_district = Column(Integer,ForeignKey('district.id_district'))
    id_city = Column(Integer,ForeignKey('city.id_city'))
    number_table = Column(Integer)
    address = Column(String)
    curator = Column(String)

    sub_district = relationship("Sub_district", back_populates="vaccination_place_sub_district")
    district = relationship("District", back_populates="vaccination_place_district")
    city = relationship("City", back_populates="vaccination_place")

class Sub_district(Base):
    __tablename__ = "sub_district"
    id_sub_district = Column(Integer, primary_key=True,autoincrement=True)
    name_sub_district = Column(String)
    id_district = Column(Integer)
    vaccination_place_sub_district = relationship("Vaccination_place", back_populates="sub_district")

class District(Base):
    __tablename__ = "district"
    id_district = Column(Integer, primary_key=True,autoincrement=True)
    name_district = Column(String)
    id_city = Column(Integer)

    vaccination_place_district = relationship("Vaccination_place", back_populates="district")
class City(Base):
    __tablename__ = "city"
    id_city = Column(Integer, primary_key=True,autoincrement=True)
    name_city = Column(String)

    vaccination_place = relationship("Vaccination_place", back_populates="city")
"""
class User(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True,autoincrement=True)
    phone_number = Column(String,unique=True)
    password  = Column(String)
    name_user  = Column(String)
    email  = Column(String,unique=True)
    address  = Column(String)
    indentify  = Column(String,unique=True)
    insurance = Column(String,unique=True)
    gender = Column(String)
    dob = Column(DateTime)
    id_permission = Column(Integer,ForeignKey('permission_user.id_permission'))
    permission_user = relationship("Permission_user", back_populates="user")    

class Permission_user(Base):
    __tablename__ = 'permission_user'
    id_permission = Column(Integer, primary_key=True,autoincrement=True)
    name_permission = Column(String)

    user = relationship("User", back_populates="permission_user")
"""
class Account(Base):
    __tablename__ = 'account'
    id_account = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String,unique=True)
    password = Column(String)
    id_role = Column(Integer, ForeignKey('account_roles.id_role'))
    active_acc = Column(Boolean)

    account_roles = relationship("Account_roles", back_populates="account")
    user_token = relationship("User_token", back_populates="account")
    organization = relationship("Organization", back_populates="account")

class Account_roles(Base):
    __tablename__ = 'account_roles'
    id_role = Column(Integer, primary_key=True,autoincrement=True)
    name_role = Column(String)

    account = relationship("Account", back_populates="account_roles")

class User_token(Base):
    __tablename__ = 'user_token'
    id_user_token = Column(Integer, primary_key=True,autoincrement=True)
    user_token = Column(String)
    id_account = Column(Integer,ForeignKey('account.id_account'))

    account = relationship("Account", back_populates="user_token")

class OTP(Base):
    __tablename__ = 'otp'
    id_otp = Column(Integer, primary_key=True,autoincrement=True)
    email = Column(String,unique=True)
    otp = Column(Integer)
class User(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True,autoincrement=True)
    phone_number = Column(String)
    name_user  = Column(String)
    email  = Column(String,unique=True)
    address  = Column(String)
    indentify  = Column(String)
    insurance = Column(String)
    gender = Column(String)
    dob = Column(Integer)
    id_account = Column(Integer)
    id_district = Column(Integer)
    id_city = Column(Integer)
    id_sub_district = Column(Integer)

class Permission_place(Base):
    __tablename__ = "permission_place"

    id_permission_place = Column(Integer, primary_key=True,autoincrement=True)
    id_vaccination_place = Column(Integer)
    id_account  = Column(Integer)

class Organization(Base):
    __tablename__ = "organization"

    id_organization = Column(Integer, primary_key=True,autoincrement=True)
    id_category_organization = Column(Integer)
    name_organization  = Column(String)
    tax_number  = Column(String)
    address  = Column(String)
    representative_name  = Column(String)
    regency  = Column(String)
    dob  = Column(Integer)
    phone_number  = Column(String)
    email  = Column(String,unique=True)
    id_account  = Column(Integer,ForeignKey('account.id_account'))

    account = relationship("Account", back_populates="organization")
class Category_organization(Base):
    __tablename__ = "category_organization"

    id_catgory_organization = Column(Integer, primary_key=True,autoincrement=True)
    name_category_organization = Column(Integer)

class DangKyTiem(Base):
    __tablename__ = "dangkytiem"

    id_dangkytiem = Column(Integer, primary_key=True,autoincrement=True)
    id_vaccine_place = Column(Integer)
    id_priority = Column(Integer)
    date = Column(Integer)
    is_sick= Column(Boolean)
    note= Column(Text)
    status = Column(Boolean)
    number_of_times = Column(Integer)
    id_user = Column(Integer)
    is_active = Column(Boolean)

    schedule_injections = relationship("Schedule_injections", back_populates="dangkytiem")
class Dangkytiem_Organization(Base):
    __tablename__ = "dangkytiem_organization"

    id_dangkytiem_organization = Column(Integer, primary_key=True,autoincrement=True)
    id_dangkytiem = Column(Integer)
    id_organization = Column(Integer)

class Priority(Base):
    __tablename__ = "priority"

    id_priority = Column(Integer, primary_key=True,autoincrement=True)
    name_priority = Column(String)

class Schedule_injections(Base):
    __tablename__ = "schedule_injections"

    id_schedule_injections = Column(Integer, primary_key=True,autoincrement=True)
    id_dangkytiem = Column(Integer,ForeignKey('dangkytiem.id_dangkytiem'))
    date = Column(Integer)
    id_vaccine = Column(Integer)
    is_active = Column(Boolean)

    dangkytiem = relationship("DangKyTiem", back_populates="schedule_injections")

class Vaccination_records(Base):
    __tablename__ = "vaccination_records"

    id_vaccination_record = Column(Integer, primary_key=True,autoincrement=True)
    id_user = Column(Integer)
    status = Column(Integer)

class Vaccination_records_detail(Base):
    __tablename__ = "vaccination_records_detail"

    id_vaccination_records_detail = Column(Integer, primary_key=True,autoincrement=True)
    id_vaccination_record = Column(Integer)
    id_vaccine = Column(Integer)
    id_vaccine_place = Column(Integer)
    injection_date = Column(Integer)
    blood_pressure = Column(Integer)
    level_response = Column(Integer)
    heart_rate = Column(Integer)
    note = Column(Text)
    status = Column(Integer)
class Feedback(Base):
    __tablename__ = "feedback"

    id_feedback = Column(Integer, primary_key=True,autoincrement=True)
    id_user = Column(Integer)
    content_feedback = Column(Text)
    number_of_times = Column(Integer)
    date_time = Column(Integer)
    id_vaccine = Column(Integer)
    id_vaccination_place = Column(Integer)
    