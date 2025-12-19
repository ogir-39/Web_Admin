from calendar import month
from datetime import datetime

from flask import redirect, url_for, render_template, current_app, request
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.menu import MenuLink
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from pip._internal.utils._jaraco_text import _
from sqlalchemy import func
from werkzeug.debug import console

from EngCenter import db, app, services
from EngCenter.services import admin_services
from EngCenter.models.models import Course, User, Bill, Enrollment, Classroom, BillEnum, TeachingLog, ScheduleDetail
from EngCenter.services.admin_services import get_model_name, get_data_table
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
        selected_month = request.args.get('month', type=int, default=datetime.now().month)
        total_students = admin_services.get_total_students()
        monthly_revenue = admin_services.get_monthly_revenue(selected_month)
        total_classrooms = admin_services.get_total_classrooms()
        total_teachers = admin_services.get_total_teachers()
        return self.render("/admin/index.html",total_students = total_students,
                           monthly_revenue = monthly_revenue, total_teachers = total_teachers, total_classrooms= total_classrooms)

    @expose('/revenue')
    def revenue(self):
        selected_month = request.args.get('month', type=int, default=datetime.now().month)
        selected_year = request.args.get('year', type=int, default=datetime.now().year)
        chart_type=['line','bar']

        raw_annual_revenue_data = admin_services.get_annual_revenue(selected_year)
        annual_revenue_data = [item['total_revenue'] for item in raw_annual_revenue_data]

        report_data = admin_services.get_data_table(selected_month, selected_year)

        total_students = admin_services.get_total_students()
        monthly_revenue = admin_services.get_monthly_revenue(selected_month)
        total_classrooms = admin_services.get_total_classrooms()
        bill_years = admin_services.get_bill_year()
        total_annual_revenue = admin_services.get_total_annual_revenue(selected_year)
        highest_monthly_revenue = admin_services.get_highest_monthly_revenue(selected_year)
        lowest_monthly_revenue = admin_services.get_lowest_monthly_revenue(selected_year)
        quarterly_revenue=admin_services.get_quarterly_revenue(selected_year)

        months = [{'value': i, 'label': f'Tháng {i}', 'selected': i == selected_month} for i in range(1, 13)]
        return self.render("/admin/revenue.html",total_students = total_students,
                            monthly_revenue = monthly_revenue, total_classrooms= total_classrooms,
                            course_data=report_data,months_list=months, years_list=bill_years,
                            current_month=selected_month, selected_year=selected_year, quarterly_revenue=quarterly_revenue,
                            annual_revenue=annual_revenue_data, total_annual_revenue=total_annual_revenue,
                            highest_monthly_revenue=highest_monthly_revenue,lowest_monthly_revenue=lowest_monthly_revenue)

    @expose('/ccr')
    def ccr(self):
        selected_year = request.args.get('year', type=int, default=datetime.now().year)

        total_students = admin_services.get_total_students()
        quarterly_revenue=admin_services.get_quarterly_revenue(selected_year)
        total_passed_students = admin_services.get_total_passed_student()

        return self.render("/admin/ccr.html",total_students = total_students, quarterly_revenue=quarterly_revenue
                           ,total_passed_students=total_passed_students)


class SharedView(ModelView):
    can_delete = True
    action_disallowed_list = []



    column_display_pk = True

    list_template = 'admin/model/list.html'
    create_template = 'admin/model/create.html'
    edit_template = 'admin/model/edit.html'
    delete_template = 'admin/model/delete.html'
    extra_css = ['/static/admin/css/model_view.css']

class CourseView(SharedView):
    column_searchable_list = ['id','name','age','level']
    column_labels = {
        'id':'ID',
        'name': 'Tên khoá học',
        'fee' : 'Học phí',
        'age' : 'Độ tuổi',
        'level' : 'Trình độ',
        'duration_hour' : 'Thời gian',
        'course_description': 'Mô tả khoá học'
    }
    form_columns = ['id', 'name', 'fee', 'age', 'level','duration_hour', 'course_description']

class UserView(SharedView):
    column_list = ['id','name','email','gender','phone_number','dob','address','status','type']
    form_columns = ['id','name','username','password','email','gender','phone_number','dob','address','status','type']
    column_searchable_list = ['id','name','email','gender','phone_number','dob','address','status','type']
    column_labels = {
        'id' : 'ID',
        'name' : 'Họ tên',
        'gender' : 'Giới tính',
        'phone_number' : 'Số điện thoại',
        'dob' : 'Ngày sinh',
        'address' : 'Địa chỉ',
        'status' : 'Trạng thái',
        'type' : 'Vai trò',
        'password' : 'Mật khẩu'
    }

class ClassView(SharedView):
    column_list = ['id','name','course','teacher','start_date','end_date','max_student']
    form_columns = ['id','name','course','teacher','start_date','end_date','max_student']
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


class TeachingLogView(SharedView):
    list_template = 'admin/model/list_teachinglog.html'
    column_list = ['teacher','teacher_id','classroom','check_in_time','teaching_date','duration_hour','hour_rate_snapshot','status','admin_note']
    column_searchable_list = ['teacher_id']
    column_labels = {
        'teacher' : 'Giáo viên',
        'classroom' : 'Lớp học',
        'check_in_time' : 'Thời gian chấm công',
        'teaching_date' : 'Ngày dạy',
        'duration_hour' : 'Duration Hour',
        'hour_rate_snapshot' : 'Hour Rate Snapshot',
        'status' : 'Trạng thái',
        'admin_note' : 'Ghi chú'
    }

    column_formatters = {
        'classroom': get_model_name,
        'teacher': get_model_name
    }

    # Ghi đè phương thức get_query để thêm bộ lọc mặc định
    def get_query(self):
        # Chỉ lấy các bản ghi có status là PENDING
        return super(TeachingLogView, self).get_query().filter(
            self.model.status == 'PENDING' # Hoặc EnrollEnum.PENDING tùy cấu hình model
        )

    # Đừng quên ghi đè cả get_count_query để con số tổng (List 18) khớp với dữ liệu lọc
    def get_count_query(self):
        return super(TeachingLogView, self).get_count_query().filter(
            self.model.status == 'PENDING'
        )



admin = Admin(app=app, theme=Bootstrap4Theme(),index_view=MyAdminIndexView())

category_QLDuLieu= 'Quản lý dữ liệu'

admin.add_view(CourseView(Course, db.session,category=category_QLDuLieu,name="Khoá học"))
admin.add_view(UserView(User, db.session,category=category_QLDuLieu,name="Tài khoản"))
admin.add_view(ClassView(Classroom,db.session,category=category_QLDuLieu,name="Lớp học"))
admin.add_view(TeachingLogView(TeachingLog,db.session,category=category_QLDuLieu,name="Chấm công"))

