from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.menu import MenuLink
from flask_admin.theme import Bootstrap4Theme
from unicodedata import category
from flask_login import current_user, logout_user

from EngCenter import db, app
from EngCenter.models.models import Course, User, Bill, Enrollment


class MyAdminIndexView(AdminIndexView):
    pass

class CourseView(ModelView):
    list_template = 'admin/model/course_list.html'

admin = Admin(app=app, name="E-COMMERCE", theme=Bootstrap4Theme())

category_QLDuLieu= 'Quản lý dữ liệu'

admin.add_view(CourseView(Course, db.session,category=category_QLDuLieu))
admin.add_view(ModelView(User, db.session,category=category_QLDuLieu))

category_ThongKe= 'Thống kê'

admin.add_view(ModelView(Bill, db.session,category=category_ThongKe))
admin.add_view(ModelView(Enrollment, db.session,category=category_ThongKe))

