import lorem
import random
import datetime
import os
from dotenv import load_dotenv

from flask import Flask, render_template, request
from models import db, Class, Student, Subject, Grades


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

#db = SQLAlchemy(app)


db.init_app(app)


@app.route('/populate_students/', methods=('POST', 'GET'))
def populate_students():
    if Class.query.count() == 0:
        return "There are no classes - classes must be created first"
    if Student.query.count() == 0:
        students_to_add = []
        for _ in range(40):
            name = lorem.sentence().split(" ")[:3]
            for _ in range(4):
                class_idx = random.randint(1, 4)
                print(class_idx)
                student_count = Student.query.filter_by(class_id=class_idx).count()
                if student_count <= 10:
                    student = {'name': name, 'class_id': class_idx}
                    students_to_add.append(student)
                else:
                    continue
        if students_to_add:
            db.session.bulk_insert_mappings(Student, students_to_add)    
            db.session.commit()
            return "Students created"
        else:
            return "non stduents to add"
    else:
        return "Students already exist"


@app.route('/create_classes/', methods=('POST', 'GET'))
def create_classes():
    if Class.query.count() != 0:
        return "Classes already exist"
    else:
        classes_to_add = []
        for idx in range(4):
            class_ = {'name' : f'Class {idx+1}'} 
            classes_to_add.append(class_)
        if classes_to_add:
            db.session.bulk_insert_mappings(Class, classes_to_add)
            db.session.commit()
            return "Classes created"
        else: 
            return "no classes to add"


@app.route('/classes', methods=('GET', 'POST'))
def classes():
    if request.method == 'POST':
        new_class_name = request.form['new_class_name']
        new_class = Class(name=new_class_name)
        db.session.add(new_class)
        db.session.commit()

    classes = Class.query.all()
    return render_template('classes.html', classes=classes)


@app.route('/classes/<int:class_id>/students', methods=('GET', 'POST'))
def students_in_class(class_id):
    if request.method == 'POST':
        new_student_name = request.form['new_student_name']
        new_student = Student(name=new_student_name, class_id=class_id)
        db.session.add(new_student)
        db.session.commit()
    
    class_ = Class.query.get(class_id)
    students = Student.query.filter_by(class_id=class_id).all()
    return render_template('students_in_class.html', class_=class_, students=students)

@app.route('/create_subjects', methods=['GET'])
def create_subjects():
    if Subject.query.count() != 0:
        return "Subjects already exist"
    else:
        subjects_to_to_add = []
        for _ in range(6):
            sentence = lorem.sentence().split(" ")
            length = len(sentence)
            index_1 = random.randint(0, length-1)
            index_2 = random.randint(0, length-1)
            title = sentence[index_1].upper() + ' ' + sentence[index_2].upper()
            subject = {'name': title}
            subjects_to_to_add.append(subject)
        if subjects_to_to_add:
            db.session.bulk_insert_mappings(Subject, subjects_to_to_add)
            db.session.commit()
            return "Subjects created"
        else:
            return "no subjects to add"
        
@app.route('/subjects', methods=('GET', 'POST'))
def subjects():
    if request.method == 'POST':
        new_subject_name = request.form['new_subject_name']
        new_subject = Subject(name=new_subject_name)
        db.session.add(new_subject)
        db.session.commit()
    
    subjects = Subject.query.all()
    return render_template('subjects.html', subjects=subjects)
    


@app.route('/generate_grades', methods=['GET'])
def generate_grades():
    def generate_random_date(start_date, end_date):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        time_between_dates = end_date - start_date
        time_between_dates_in_days = time_between_dates.days

        random_number_of_days = random.randrange(time_between_dates_in_days)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        return random_date.strftime("%Y-%m-%d")

    start_date = '2024-01-01'
    end_date = '2024-02-29'
    for student in Student.query.all():
        for subject in Subject.query.all():
            for _ in range(5):
                date = generate_random_date(start_date, end_date)
                grade = random.randint(0, 100)
                grade_obj = Grades(student_id=student.id, subject_id=subject.id, date=date, grade=grade)
                db.session.add(grade_obj)
        print(Grades.query.all())
    db.session.commit()
    return "Grades created"


def get_dates_for_grades(grades: Grades) -> tuple[list[datetime.datetime], dict[datetime.datetime, str]]:
    dates = []
    for grade in grades:
        dates.append(grade.date)
    dates = sorted(set(dates))
    formated_dates = {date: date.strftime('%d-%m-%Y') for date in dates}
    return dates, formated_dates


@app.route('/grades/subjects/<int:subject_id>/classes/<int:class_id>', methods=['GET'])
def show_grades_for_subject(subject_id, class_id):
    students = Student.query.filter_by(class_id=class_id).all()
    grades = Grades.query.filter(Grades.student_id.in_([student.id for student in students]), Grades.subject_id == subject_id)
    subject = Subject.query.get(subject_id)

    dates, formated_dates = get_dates_for_grades(grades)

    students_grades = {}
    for student in students:
        students_grades[student.name] = {}
        for date in dates:
            grade = grades.filter(Grades.student_id == student.id, Grades.date == date).first()
            if grade:
                students_grades[student.name][date] = grade.grade
    return render_template('grades.html', the_class=Class.query.get(class_id), students=students, 
                           dates=formated_dates, students_grades=students_grades, subject=subject)


@app.route('/grades/student/<int:student_id>', methods=['GET'])
def show_student_grades(student_id):

    student = Student.query.get(student_id)
    if student is None:
        return "Student not found"

    student_grades = Grades.query.filter_by(student_id=student_id)

    dates, formated_dates = get_dates_for_grades(student_grades)

    grades = {}
    for subject in Subject.query.all():
        grades[subject.name] = {}
        for date in dates:
            grade = student_grades.filter_by(subject_id=subject.id, date=date).first()
            if grade:
                grades[subject.name][date] = grade.grade

    return render_template('student_grades.html', student=student, dates=formated_dates, grades=grades, subjects=Subject.query.all())


@app.route('/add_student_grade', methods=['POST'])
def add_student_grade():
    new_grade = request.form.get('grade')
    student_id = request.form.get('student')
    subject_id = request.form.get('subject')
    date = request.form.get('date')

    grade = Grades(student_id=student_id, subject_id=subject_id, date=date, grade=new_grade)
    db.session.add(grade)
    db.session.commit()
    return "Grade added successfully"


if __name__ == "__main__":
    app.run(debug=True)
