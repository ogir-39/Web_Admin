from flask import redirect, url_for, render_template, current_app
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.menu import MenuLink
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from sqlalchemy import func

from EngCenter import db, app, services
from EngCenter.services import admin_services
from EngCenter.models.models import Course, User, Bill, Enrollment, Classroom, BillEnum
from EngCenter.services.admin_services import get_model_name
from EngCenter.templates import admin


class DashboardView(BaseView):
    @expose('/')
    def create_course(self):
        create_course_url = url_for('course.create_view')
        return self.render('index.html', create_course_url=create_course_url)

    def create_user(self):
        create_user_url = url_for('user.create_view')
        return self.render('index.html', create_user_url=create_user_url)

    def create_class(self):
        create_class_url = url_for('classroom.create_view')
        return self.render('index.html', create_class_url=create_class_url)

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        total_students = admin_services.getToTalStudents()
        monthly_revenue = admin_services.getMonthlyRevenue()
        total_classrooms = admin_services.getTotalClassrooms()
        total_teachers = admin_services.getTotalTeachers()
        return self.render("/admin/index.html",total_students = total_students,
                           monthly_revenue = monthly_revenue, total_teachers = total_teachers, total_classrooms= total_classrooms)

class SharedView(ModelView):
    list_template = 'admin/model/list.html'
    create_template = 'admin/model/create.html'
    edit_template = 'admin/model/edit.html'
    delete_template = 'admin/model/delete.html'
    extra_css = ['/static/admin/css/model_view.css']

class CourseView(SharedView):
    column_searchable_list = ['name','age','level']
    column_labels = {
        'name': 'Tên khoá học',
        'fee' : 'Học phí',
        'age' : 'Độ tuổi',
        'level' : 'Trình độ',
        'duration_hour' : 'Thời gian',
        'course_description': 'Mô tả khoá học'
    }

class UserView(SharedView):
    column_list = ['name','email','gender','phone_number','dob','address','status','type']
    column_searchable_list = ['name','email','gender','phone_number','dob','address','status','type']
    column_labels = {
        'name' : 'Họ tên',
        'gender' : 'Giới tính',
        'phone_number' : 'Số điện thoại',
        'dob' : 'Ngày sinh',
        'address' : 'Địa chỉ',
        'status' : 'Trạng thái',
        'type' : 'Vai trò'
    }

class ClassView(SharedView):
    column_list = ['name','course','teacher','start_date','end_date','max_student']
    column_searchable_list = ['name','start_date','end_date','max_student']
    column_labels = {
        'name' : 'Tên lớp học',
        'course' : 'Khoá học',
        'teacher' : 'Giáo viên phụ trách',
        'start_date' : 'Ngày bắt đầu',
        'end_date' : 'Ngày kết thúc',
        'max_student' : 'Số lượng học sinh tối đa'
    }
    column_formatters = {
        'course': get_model_name,
        'teacher': get_model_name
    }



admin = Admin(app=app, theme=Bootstrap4Theme(),index_view=MyAdminIndexView())

category_QLDuLieu= 'Quản lý dữ liệu'

admin.add_view(CourseView(Course, db.session,category=category_QLDuLieu,name="Khoá học"))
admin.add_view(UserView(User, db.session,category=category_QLDuLieu,name="Tài khoản"))
admin.add_view(ClassView(Classroom,db.session,category=category_QLDuLieu,name="Lớp học"))

category_ThongKe= 'Thống kê'

# admin.add_view(ModelView(Bill, db.session, category=category_ThongKe,name="Doanh thu"))

