from flask import Blueprint, request, session, jsonify,render_template,flash,redirect
from app import db, requires_auth
# from .models import Semester
# from .models import AddCourseToSem
# from .models import AddStudentToCourse
from app.Users.models import *
from app.Functionalities.models import *
from validate_email import validate_email

mod_todo = Blueprint('todo', __name__)


@mod_todo.route('/admin',methods=['GET','POST'])
@requires_auth
def add1():
    if request.method=='GET':
        aid=session['user_id']
        us=Admin.query.filter(aid==Admin.id).first()
        if us is None:
            session.pop('user_id')
            return redirect('/login')
        semester=Semester.query.all()
        course=Course.query.all()
        faculty=Faculty.query.all()
        return render_template('admin.html',semesters=semester,courses=course,faculty=faculty)
    else:
        if request.form['button']=='Change Credentials':
            sem1=request.form['sem3']
            cour1=request.form['cour3']
            qu=AddStudentToCourse.query.filter(cour1==AddStudentToCourse.course_ids,sem1==AddStudentToCourse.sem_ids).all()
            return redirect('/viewCourse/%s/%s'%(sem1,cour1))


        # elif request.form['button']=='Attendance':
        #     sem1=request.form['sem4']
        #     cour1=request.form['cour4']
        #     qu=AddStudentToCourse.query.filter(cour1==AddStudentToCourse.course_ids,sem1==AddStudentToCourse.sem_ids).all()
        #     return redirect('/viewCourse/%s/%s'%(qu.sem_ids,qu.course_ids))



        elif request.form['button']=='Add Course':
            sem1 = request.form['sem2']
            course1 = request.form['cour2']
            faculty1=request.form['faculty2']
            check1=AddCourseToSem.query.filter(AddCourseToSem.sem_ids==sem1,AddCourseToSem.course_ids==course1).first()
            if check1 is None:
                cour=AddCourseToSem(sem1,course1,faculty1)
                db.session.add(cour)
                db.session.commit()
                return redirect('/admin')
            else:
                return jsonify(success=True,message="Course already in this semester"),400
            # return redirect('/admin')            

        elif request.form['button']=='Add Semester':
            name1=request.form['sem1']
            sem2=Semester.query.filter(Semester.name==name1).first()
            if sem2 is None:
                semester1=Semester(name1)
                db.session.add(semester1)
                db.session.commit()
                return redirect('/admin')
            else:
                return jsonify(success=False,message="Sem already registered"),400

            # return redirect('/admin')


@mod_todo.route('/faculty/<name>',methods=['GET','POST'])
@requires_auth
def add2(name):
    if request.method=='GET':
        aid=session['user_id']
        us=Faculty.query.filter(aid==Faculty.name).first()
        if us is None or name!=aid:
            session.pop('user_id')
            return redirect('/login')
        user=AddCourseToSem.query.filter(AddCourseToSem.faculty==name).all()
        return render_template('faculty.html',users=user)
    else:
        sem1=request.form['sem1']
        cour1=request.form['cour1']
        return redirect('/viewCourse/%s/%s'%(sem1,cour1))

@mod_todo.route('/students/<roll>', methods=['GET','POST'])
@requires_auth
def individual_stud(roll):
    if request.method == 'GET':
        # aid=session['user_id']
        us=Student.query.filter(roll==Student.roll).first()
        if us is None:
            session.pop('user_id')
            return redirect('/login')
        sem=Semester.query.all()
        student = AddStudentToCourse.query.filter(AddStudentToCourse.roll == roll).all()
        list1=[]
        for i in sem:
            list=[]
            for j in student:
                if (i.name)==(j.sem_ids):
                    h={}
                    h["course_ids"] = j.course_ids
                    h["mid1"] = j.mid1
                    h["mid2"] = j.mid2
                    h["endsem"] = j.endsem
                    h["attendance"] = j.attendance
                    list.append(h)
            if list:
                list1.append(list)

        return render_template('students.html',students=list1)

        # sem1=request.form['sem1']
        # qu=AddCourseToSem.query.filter(AddCourseToSem.sem_ids==sem1).all()
        # for i in qu:
        #     u1=AddStudentToCourse(sem1,i.course_ids,roll,0,0,0,0)
        #     db.session.add(u1)
        # try:
        #     db.session.commit()
        # except IntegrityError as e:
        #     return jsonify(success=False, message="This email already exists"), 400
        # return redirect('/students/%s'%(roll))


@mod_todo.route('/viewCourse/<semname>/<coursename>', methods=['GET','POST'])
@requires_auth
def individual_student_op(semname,coursename):
    if request.method == 'GET':
        semncourse = AddStudentToCourse.query.filter(AddStudentToCourse.course_ids == coursename,AddStudentToCourse.sem_ids == semname).all()
        # l=[]
        # for t in semncourse:
        #     l.append(semncourse.roll)
        return render_template('editcredentials.html',semncourse=semncourse)

# @mod_todo.route('/editcredentials', methods=['POST'])
# @requires_auth
# def individual():
    else:
        if request.form['button']=='Grade':
            stud1=request.form['stud1']
            grade1=request.form['mid1']
            grade2=request.form['mid2']
            grade3=request.form['endsem']
            qu=AddStudentToCourse.query.filter(AddStudentToCourse.roll==stud1,AddStudentToCourse.course_ids==coursename,AddStudentToCourse.sem_ids==semname).first()
            qu.mid1=grade1  
            qu.mid2=grade2
            qu.endsem=grade3
            db.session.commit()
            return redirect('/viewCourse/%s/%s'%(semname,coursename))

        elif request.form['button']=='Attendance':
            stud1=request.form['stud2']
            attendance1=request.form['attendance2']
            qu=AddStudentToCourse.query.filter(AddStudentToCourse.roll==stud1,AddStudentToCourse.course_ids==coursename,AddStudentToCourse.sem_ids==semname).first()
            qu.attendance=attendance1
            db.session.commit()
            return redirect('/viewCourse/%s/%s'%(semname,coursename))

        elif request.form['button']=='View':
            stud1=request.form['stud3']
            return redirect('students/%s'%(stud1))
