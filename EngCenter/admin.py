from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.menu import MenuLink
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user

from EngCenter import db, app
from EngCenter.models.models import Course, User, Bill, Enrollment


class MyAdminIndexView(AdminIndexView):
    pass

class CourseView(ModelView):
    list_template = 'admin/model/list.html'
    create_template = 'admin/model/create.html'
    extra_css = ['css/list.css']

class UserView(ModelView):
    list_template = 'admin/model/list.html'

class BillView(ModelView):
    list_template = 'admin/model/list.html'

class EnrollmentView(ModelView):
    list_template = 'admin/model/list.html'

admin = Admin(app=app, theme=Bootstrap4Theme())

category_QLDuLieu= 'Quản lý dữ liệu'

admin.add_view(CourseView(Course, db.session,category=category_QLDuLieu))
admin.add_view(UserView(User, db.session,category=category_QLDuLieu))

category_ThongKe= 'Thống kê'

admin.add_view(BillView(Bill, db.session,category=category_ThongKe))
admin.add_view(EnrollmentView(Enrollment, db.session,category=category_ThongKe))

