from flask import Blueprint, request, session, jsonify,redirect,render_template,flash
from sqlalchemy.exc import IntegrityError
from app import db
from .models import Admin
from .models import Faculty
from .models import Student
from .models import Course
from app.Functionalities.models import *
import csv
import re

mod_user = Blueprint('user', __name__)

# @mod_user.route('/login', methods=['GET'])
# def check_login():
#     if 'user_id' in session:
#         user = Admin.query.filter(Admin.email == email).first()
#         if user is None:
#             user = Faculty.query.filter(Faculty.email == email).first()
#             if user is None:
#                 user = Student.query.filter(Student.email == email).first()
#                 if user is None:
#                     return jsonify(success=False), 401
#     return jsonify(success=True, user=user.to_dict())

@mod_user.route('/login', methods=['POST','GET'])
def login():
    if request.method=='GET':
        session.pop('user_id',None)
        return render_template('login.html')
    else:
        try:
            email = request.form['email']
            password = request.form['password']
        except KeyError as e:
            return jsonify(success=False, message="%s not sent in the request" % e.args), 400

        user = Admin.query.filter(Admin.email == email).first()
        p=1
        if user is None or not user.check_password(password):
            user = Faculty.query.filter(Faculty.email == email).first()
            p=2
            if user is None or not user.check_password(password):
                user = Student.query.filter(Student.email == email).first()
                p=3
                if user is None or not user.check_password(password):
                    return jsonify(success=False, message="Invalid Credentials"), 400

        
        if p is 1:
            session['user_id'] = user.id
            return redirect('/admin')
        if p is 2:
            session['user_id'] = user.name
            return redirect('/faculty/%s'%(user.name))
        if p is 3:
            session['user_id'] = user.roll
            return redirect('/students/%s'%(user.roll))

# @mod_user.route('/logout', methods=['POST'])
# def logout():
#     session.pop('user_id')
#     return jsonify(success=True)
#     return redirect

@mod_user.route('/register', methods=['GET','POST'])
def create_user():
    if request.method=='GET':
        session.pop('user_id',None)
        sem=Semester.query.all()
        return render_template('register.html',sem=sem)
    else:
        try:
            name = request.form['name']
            email = request.form['email']
            roll=request.form['roll']
            password = request.form['password']
        except KeyError as e:
            return jsonify(success=False, message="%s not sent in the request" % e.args), 400



    # if '@' not in email:
    #     return jsonify(success=False, message="Please enter a valid email"), 400

    # u = Student(name, email, password)
    # db.session.add(u)
    # try:
    #     db.session.commit()
    # except IntegrityError as e:
    #     return jsonify(success=False, message="This email already exists"), 400

    # return jsonify(success=True)


        if '@' not in email:
            return jsonify(success=False, message="Please enter a valid email"), 400

        s=Student.query.filter(Student.roll==roll).first()
        if s is None:
            u = Student(name, email,roll, password)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success=False, message="This email already exists"), 400
        else:
            stu=Student.query.filter(Student.roll==roll).first()
            if not stu.check_password(password):
                return jsonify(message="WRONG PASSWORD"),400
        sem=request.form['sem1']
        s=AddStudentToCourse.query.filter(AddStudentToCourse.sem_ids==sem,AddStudentToCourse.roll==roll).first()
        if s is None:
            qu=AddCourseToSem.query.filter(AddCourseToSem.sem_ids==sem).all()
            for i in qu:
                u1=AddStudentToCourse(sem,i.course_ids,roll,0,0,0,0)
                db.session.add(u1)
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success=False, message="This email already exists"), 400
        else:
            return jsonify(success=False,message="Already registered for this semester"),400

        session['user_id']=roll
        return redirect('/students/%s'%(roll))

@mod_user.route('/', methods=['GET','POST'])
def create_admin():
    if request.method=='GET':
        ad=Admin.query.filter(Admin.id==1).first()
        if ad is None:
            list="Abhishek"
            name=list
            email=list+"@"+"researchweb.iiit.ac.in"
            password=list+"24"
            u = Admin(email, password)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success=False, message="This email already exists"), 400

            with open('app/Users/a1.1.csv') as csvfile:
                readCSV1 = csv.reader(csvfile,delimiter = '\n')
                rows1 = []
                for row in readCSV1:
                    rows1.append(row)
        
                for i in rows1:
                    name=i[0]
                    u = Course(name)
                    db.session.add(u)
                try:
                    db.session.commit()
                except IntegrityError as e:
                    return jsonify(success=False, message="This email already exists"), 400

            with open('app/Users/a2.1.csv') as csvfile:
                readCSV2 = csv.reader(csvfile,delimiter = '\n')
                rows2 = []
                l=0
                for row in readCSV2:
                    l=l+1
                    rows2.append(row)

                for i in rows2:
                    name=i[0]
                    email=i[0]+"@"+"researchweb.iiit.ac.in"
                    password=i[0]+"24"
                    u = Faculty(name, email, password)
                    db.session.add(u)
                # try:
                    db.session.commit()
                # except IntegrityError as e:
                    # return jsonify(success=False, message="This email already exists"), 400
                j=0
                k=l/8
                i=0
                while i < l:
                    cour=rows1[i][0]
                    faculty=rows2[i][0]
                    if (i%13) == 0:
                        j=j+1
                    u=AddCourseToSem(j,cour,faculty)
                    db.session.add(u)
                    try:
                        db.session.commit()
                    except IntegrityError as e:
                        return jsonify(success=False, message="This email already exists"), 400
                    i=i+1


            i=1
            while i <= 8:
                u=Semester(i)
                db.session.add(u)
                try:
                        db.session.commit()
                except IntegrityError as e:
                        return jsonify(success=False, message="This email already exists"), 400
                i=i+1
            

        return render_template('index.html')
