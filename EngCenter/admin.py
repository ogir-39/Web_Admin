from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.menu import MenuLink
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user

from EngCenter import db, app
from EngCenter.models.models import Course, User, Bill, Enrollment, Classroom


class MyAdminIndexView(AdminIndexView):
    pass

class SharedView(ModelView):
    list_template = 'admin/model/list.html'
    create_template = 'admin/model/create.html'
    edit_template = 'admin/model/edit.html'
    delete_template = 'admin/model/delete.html'
    extra_css = ['/static/admin/css/model_view.css']

class CourseView(SharedView):
    column_searchable_list = ["name"]
    column_labels = {
        'name': 'Tên khoá học',
        'fee' : 'Học phí',
        'age' : 'Độ tuổi',
        'level' : 'Trình độ',
        'duration hour' : 'Thời gian',
        'course_description': 'Mô tả khoá học'
    }

class UserView(SharedView):
    column_list = ['fullname','email','gender','phone_number','dob','address','status','type']
    column_searchable_list = ['fullname','email','gender','phone_number','dob','address','status','type']
    column_labels = {
        'fullname' : 'Họ tên',
        'gender' : 'Giới tính',
        'phone_number' : 'Số điện thoại',
        'dob' : 'Ngày sinh',
        'address' : 'Địa chỉ',
        'status' : 'Trạng thái',
        'type' : 'Vai trò'
    }

class ClassView(SharedView):
    pass

class BillView(SharedView):
    pass

class EnrollmentView(SharedView):
    pass


admin = Admin(app=app, theme=Bootstrap4Theme())

category_QLDuLieu= 'Quản lý dữ liệu'

admin.add_view(CourseView(Course, db.session,category=category_QLDuLieu,name="Khoá học", endpoint='course'))
admin.add_view(UserView(User, db.session,category=category_QLDuLieu,name="Tài khoản"))
admin.add_view(ClassView(Classroom,db.session,category=category_QLDuLieu,name="Lớp học"))

category_ThongKe= 'Thống kê'

admin.add_view(BillView(Bill, db.session,category=category_ThongKe,name="Hoá đơn"))
admin.add_view(EnrollmentView(Enrollment, db.session,category=category_ThongKe,name="Đăng ký"))

