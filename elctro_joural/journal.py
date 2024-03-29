import lorem
import random
import datetime

from flask import Flask, render_template, request
import sqlalchemy
from models import db, Class, Student, Subject, Grades


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///journal'

db.init_app(app)


@app.route('/populate_students/', methods=('POST', 'GET'))
def populate_students():
    if Class.query.count() == 0:
        return "There are no classes - classes must be created first"
    if Student.query.count() == 0:
        for _ in range(40):
            name = lorem.sentence().split(" ")[:3]
            for _ in range(4):
                class_idx = random.randint(1, 4)
                print(class_idx)
                student_count = Student.query.filter_by(class_id=class_idx).count()
                if student_count <= 10:
                    student = Student(name=name, class_id=class_idx)
                    break
                else:
                    continue
            db.session.add(student)
        db.session.commit()
        return "Students created"
    else:
        return "Students already exist"


@app.route('/create_classes/', methods=('POST', 'GET'))
def create_classes():
    if Class.query.count() != 0:
        return "Classes already exist"
    else:
        for idx in range(4):
            class_name = f"Class {idx+1}"
            class_obj = Class(name=class_name)
            db.session.add(class_obj)
        db.session.commit()
        return "Classes created"


@app.route('/classes', methods=['GET'])
def classes():
    classes = Class.query.all()
    return render_template('classes.html', classes=classes)


@app.route('/create_subjects', methods=['GET'])
def create_subjects():
    if Subject.query.count() != 0:
        return "Subjects already exist"
    else:
        for _ in range(6):
            sentence = lorem.sentence().split(" ")
            length = len(sentence)
            index_1 = random.randint(0, length-1)
            index_2 = random.randint(0, length-1)
            title = sentence[index_1].upper() + ' ' + sentence[index_2].upper()
            subject = Subject(name=title)
            db.session.add(subject)
        db.session.commit()
        return "Subjects created"


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


@app.route('/grades/student/<int:student_id>', methods=['GET'])
def show_student_grades(student_id):

    student = Student.query.get(student_id)
    if student is None:
        return "Student not found"

    student_grades = Grades.query.filter_by(student_id=student_id)
    dates = []
    for grade in student_grades:
        dates.append(grade.date)

    dates = sorted(set(dates))
    formated_dates = {date: date.strftime('%d-%m-%Y') for date in dates}

    print(len(set(dates)))
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
