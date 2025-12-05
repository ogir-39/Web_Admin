from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.menu import MenuLink
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from sqlalchemy import func

from EngCenter import db, app
from EngCenter.models.models import Course, User, Bill, Enrollment, Classroom, BillEnum


def get_model_name(view, context, model, name):
    """Lấy tên khóa học từ đối tượng Course liên quan."""

    # Giả định: Cột Foreign Key trong Model Class của bạn là 'course'
    # và đối tượng Course có thuộc tính là 'name'
    model_object = getattr(model, name)  # Lỗi xảy ra ở đây vì 'model' (Classroom) không có thuộc tính 'course'

    if model_object:
        # Trả về tên khóa học (course.name)
        return model_object.name

    # Trả về giá trị trống nếu không có khóa học nào được liên kết
    return "N/A"


def get_total_revenue():
    """Tính tổng doanh thu từ Bill ở trạng thái PAID."""

    # Chúng ta cần tham gia 4 bảng: Bill -> Enrollment -> Classroom -> Course
    # và chỉ lấy Bill có trạng thái PAID

    total_revenue = db.session.query(
        func.sum(Course.fee)  # Tổng hợp cột fee từ Course
    ).select_from(Bill).join(
        Enrollment, Bill.enrollment_id == Enrollment.id  # 1. Bill -> Enrollment
    ).join(
        Classroom, Enrollment.class_id == Classroom.id  # 2. Enrollment -> Classroom
    ).join(
        Course, Classroom.course_id == Course.id  # 3. Classroom -> Course
    ).filter(
        Bill.status == BillEnum.PAID  # 4. Lọc Bill đã thanh toán
    ).scalar()  # Lấy giá trị tổng duy nhất

    # Trả về 0 nếu kết quả là None (chưa có doanh thu)
    return total_revenue if total_revenue is not None else 0

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

    def index(self):
        # 🎯 Tính toán tổng doanh thu
        revenue = get_total_revenue()

        # Định dạng tiền tệ (tùy chọn)
        revenue_display = "{:,.0f}".format(revenue)

        # Truyền vào template
        return self.render('index.html', total_revenue=revenue_display)

class MyAdminIndexView(AdminIndexView):
    pass

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




admin = Admin(app=app, theme=Bootstrap4Theme())

category_QLDuLieu= 'Quản lý dữ liệu'

admin.add_view(CourseView(Course, db.session,category=category_QLDuLieu,name="Khoá học"))
admin.add_view(UserView(User, db.session,category=category_QLDuLieu,name="Tài khoản"))
admin.add_view(ClassView(Classroom,db.session,category=category_QLDuLieu,name="Lớp học"))

category_ThongKe= 'Thống kê'

