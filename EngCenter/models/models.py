
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.mysql import DECIMAL, DOUBLE
from sqlalchemy.dialects.mssql import TINYINT
from EngCenter import app, db

class User(db.Model):
    id = Column(String(10), primary_key=True)
    fullname = Column(String(250), nullable=False)
    email = Column(String(100), nullable=False)
    gender = Column(Integer, nullable=False, default=0)
    phone_number = Column(String(10), unique=True)
    dob = Column(DateTime, nullable=False)
    address = Column(String(250))
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(30), nullable=False)
    status = Column(TINYINT, default=1)

class Admin(User):
    id = Column(String(10), ForeignKey(User.id) ,primary_key=True)

class Student(User):
    id = Column(String(10), ForeignKey(User.id) ,primary_key=True)

class Teacher(User):
    id = Column(String(10), ForeignKey(User.id) ,primary_key=True)

class Cashier(User):
    id = Column(String(10), ForeignKey(User.id) ,primary_key=True)

class AgeEnum(enum.Enum):
    KIDS = 0
    TEEN = 1
    ADULT = 2

class SkillEnum(enum.Enum):
    BEGINNER = 0
    INTERMEDIATE = 1
    ADVANCED = 2

class Course(db.Model):
    id = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=False)
    fee = Column(DECIMAL(10, 2), nullable=False)
    age = Column(Enum(AgeEnum), nullable=False)
    level = Column(Enum(SkillEnum), nullable=False)
    duration_hour = Column(String(10), nullable=False)
    course_description = Column(String(250))

class Schedule(enum.Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class Classroom(db.Model):
    id = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    class_schedule = Column(Enum(Schedule), nullable=False)
    max_student = Column(Integer, nullable=False)
    teacher_id = Column(String(10), ForeignKey(Teacher.id), nullable=False)
    course_id = Column(String(10), ForeignKey(Course.id), nullable=False)

class GradeComponent(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    weight = Column(DOUBLE, nullable=False)
    course_id = Column(String(10), ForeignKey(Course.id), nullable=False)

class EnrollEnum(enum.Enum):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2

class Enrollment(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    register_date = Column(DateTime, nullable=False, default=datetime.now)
    status = Column(Enum(EnrollEnum), nullable=False)
    student_id = Column(String(10), ForeignKey(Student.id), nullable=False)
    class_id = Column(String(10), ForeignKey(Classroom.id), nullable=False)

class Score(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(DOUBLE, nullable=False)
    enrollment_id = Column(Integer, ForeignKey(Enrollment.id), nullable=False)
    grade_id = Column(Integer, ForeignKey(GradeComponent.id), nullable=False)

class BillEnum(enum.Enum):
    UNPAID = 0
    PAID = 1

class Bill(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    status = Column(Enum(BillEnum), nullable=False)
    enrollment_id = Column(Integer, ForeignKey(Enrollment.id), nullable=False)
    cashier_id = Column(String(10), ForeignKey(Cashier.id), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
