from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import Column,INT ,String,JSON,DateTime
from flask_login import UserMixin
from controller import db
from datetime import datetime

base = declarative_base()


    
class Add_SubUsers(base):
    __tablename__ = 'add_subusers'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000))
    useremail = db.Column(db.String(100), unique=True)


#Admin authentication table
class Admin(UserMixin, db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


# Table for addind questions 
class feedback_questions(base):
    __tablename__ = 'feedback_questions_tbl'
    id = db.Column(db.Integer, primary_key=True)
    question=db.Column(db.String(25), nullable=True)
    question_type  = db.Column(db.String(25))
    # multiple_opt =  db.Column(db.JSON(50), nullable=True)



class feedback_formCreation(base):
    __tablename__ = 'feedback_formCreation'
    formID =    db.Column(db.Integer, primary_key=True)
    formName =  db.Column(db.String(50))
    questions = db.Column(db.JSON(50), nullable=True)
    created = db.Column(db.DateTime, default= datetime.now())
    
    # multiple_opt =  db.Column(db.JSON(50), nullable=True)


class questions_tbl(base):
    __tablename__ = 'questions_tbl'
    questionID =    db.Column(db.Integer, primary_key=True)
    questions =  db.Column(db.String(50))
    question_type = db.Column(db.String(50))
    options =   db.Column(db.JSON(50), nullable=True)    
















 
       



    









