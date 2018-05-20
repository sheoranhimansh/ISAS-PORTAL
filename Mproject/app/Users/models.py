from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = 'admin_table'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    #name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        #self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'email': self.email,
        }

    def __repr__(self):
        return "User<%d> %s" % (self.id, self.email)


class Faculty(db.Model):
    __tablename__ = 'faculty_table'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, name,email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'name': self.name,
        }

    def __repr__(self):
        return "User %s" % (self.name)




class Student(db.Model):
    __tablename__ = 'student_table'
    # Id = db.Column(db.Integer,autoincrement=True)
    name = db.Column(db.String(255),primary_key=True)
    email = db.Column(db.String(255))
    roll = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, name,email,roll, password):
        self.name = name
        self.email = email
        self.roll = roll
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'Roll' : self.roll,
            'name': self.name,
            'email': self.email,
        }

    def __repr__(self):
        return "User<%s> %s" % (self.roll, self.email)



class Course(db.Model):
    __tablename__ = 'courses_table'
    # Id = db.Column(db.Integer,autoincrement=True)
    name = db.Column(db.String(),primary_key=True)
    
    def __init__(self,name):
        self.name = name

    def to_dict(self):
        return {
            'name': self.name,
        }

    def __repr__(self):
        return " %s" % (self.name)
