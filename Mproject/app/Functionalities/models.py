from flask_sqlalchemy import SQLAlchemy
from app.Users.models import *
from app import db
from app.Users.models import *



class Semester(db.Model):
    __tablename__ = 'semester_table'
    # Id = db.Column(db.Integer,autoincrement=True)
    name=db.Column(db.String(1000),primary_key=True)

    def __init__(self,name):
        self.name=name

    def to_dict(self):
        return {
            'name':self.name
        }

    def __repr__(self):
        return "Todo<%s>" % (self.name)



class AddCourseToSem(db.Model):
    __tablename__ = 'coursesInSem_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sem_ids = db.Column(db.String(25),db.ForeignKey('semester_table.name'))
    course_ids = db.Column(db.String(25),db.ForeignKey('courses_table.name'))
    faculty=db.Column(db.String(255))

    def __init__(self, sem_ids,course_ids,faculty):
        self.sem_ids = sem_ids
        self.course_ids = course_ids
        self.faculty=faculty

    def to_dict(self):
        return {
            'course_id': self.course_ids,
            'sem_id': self.sem_ids,
            'faculty':self.faculty,
        }

    def __repr__(self):
        return "Course<%s> Sem<%s> Faculty<%d>" % (self.course_ids,self.sem_ids, self.faculty)

class AddStudentToCourse(db.Model):
    __tablename__ = 'studentincourse_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sem_ids = db.Column(db.String(25),db.ForeignKey('semester_table.name'))
    course_ids = db.Column(db.String(25),db.ForeignKey('courses_table.name'))
    roll = db.Column(db.String(25),db.ForeignKey('student_table.roll'))
    mid1 = db.Column(db.String(10))
    mid2 = db.Column(db.String(10))
    endsem = db.Column(db.String(10))
    attendance = db.Column(db.String(25))

    def __init__(self,  sem_ids, course_ids, roll, mid1, mid2, endsem,attendance):
        self.sem_ids = sem_ids
        self.course_ids = course_ids
        self.roll = roll
        self.mid1 = mid1
        self.mid2 = mid2
        self.endsem = endsem
        self.attendance=attendance

    # def to_dict(self):
    #     return {
    #         'roll': self.roll,
    #         'course_id': self.course_ids,
    #         'sem_id': self.sem_ids,
    #         'grade': self.grade,
    #         'attendance': self.attendance,
    #     }

    # def __repr__(self):
    #     return "Course<%s> Grade<%s> Attendance<%d>" % (self.course_ids,self.grade, self.attendance)
