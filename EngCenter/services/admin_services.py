from calendar import month
from datetime import datetime, timezone
from itertools import groupby

import pytz
from dateutil.relativedelta import relativedelta
from flask import request
from sqlalchemy import func, literal_column, union_all, select, case
from sqlalchemy.orm import aliased

from EngCenter import db, app
from EngCenter.models.models import Bill, BillEnum, Student, Teacher, Classroom, Enrollment, Course, GradeComponent, \
    Score, EnrollEnum


def format_large_number(number):
    """Rút gọn số lớn thành Tr (Triệu) hoặc Tỉ."""

    # Đảm bảo đầu vào là một số và không phải None
    if number is None:
        return '0 VND'

    number = int(number)

    # 1 Tỷ = 1,000,000,000
    if number >= 1_000_000_000:
        # Làm tròn đến 2 chữ số thập phân
        ty = round(number / 1_000_000_000, 2)
        return f'{ty:.2f} tỉ'  # Ví dụ: 5.00 Tỉ

    # 1 Triệu = 1,000,000
    elif number >= 1_000_000:
        # Làm tròn đến 2 chữ số thập phân
        trieu = round(number / 1_000_000, 2)
        return f'{trieu:.2f} tr'  # Ví dụ: 500.00 Tr

    else:
        # Dưới 1 triệu, hiển thị định dạng số thường (có dấu phẩy)
        return f'{number:,.0f}'  # Ví dụ: 990,000 VND

def get_data_table(selected_month, selected_year):
    month_filter = func.month(Classroom.start_date).__eq__(selected_month)
    year_filter = func.year(Classroom.start_date).__eq__(selected_year)

    query = (
        db.session.query((Course.name),func.count(Classroom.course_id).label('ToTalClasses'),func.count(Enrollment.class_id).label('ToTalStudents'))
        .join(Classroom, (Classroom.course_id.__eq__(Course.id)) & month_filter & year_filter,isouter=True)
        .join(Enrollment, Enrollment.class_id==Classroom.id, isouter=True)
        .group_by(Course.name)
    )

    result = query.all()
    data = [{
        'coursename' : r.name,
        'totalclassrooms' : r.ToTalClasses,
        'totalstudents' : r.ToTalStudents
    } for r in result ]

    return data

def get_monthly_revenue(selected_month):
    start_of_month = datetime.now().replace(month=selected_month,day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_next_month = start_of_month + relativedelta(months=+1)
    query = (
        db.session.query(func.sum(Bill.unit_price))
        .filter(
            Bill.status == BillEnum.PAID,
            Bill.create_date >= start_of_month,
            Bill.create_date < start_of_next_month
        )
    )

    result = query.scalar()
    return result if result is not None else 0

def get_quarterly_revenue(selected_year):
    query = (db.session.query(func.quarter(Bill.create_date).label('quarter_number'),func.sum(Bill.unit_price).label('quarterly_revenue'))
            .filter((Bill.status == BillEnum.PAID),func.year(Bill.create_date) == selected_year)
            .group_by(func.quarter(Bill.create_date))
            .order_by(func.quarter(Bill.create_date).asc()))
    result = query.all()

    quarterly_data = [0, 0, 0, 0]

    for r in result:
        # quarter_number thường trả về 1, 2, 3, 4
        # Ta gán vào mảng theo chỉ số (index = quý - 1)
        index = int(r.quarter_number) - 1
        quarterly_data[index] = float(r.quarterly_revenue)

    return quarterly_data

def get_bill_year():
    query = db.session.query(func.year(Bill.create_date).label('years')).distinct()
    # return query.all()
    result = query.all()

    data = [
        {'years' : r.years}
        for r in result
    ]
    return data

def get_highest_monthly_revenue(selected_year):
    query = (db.session.query(func.month(Bill.create_date).label('month_number'))
                .filter((func.year(Bill.create_date) == selected_year) , Bill.status == BillEnum.PAID)
                .group_by(func.month(Bill.create_date))
                .order_by(func.sum(Bill.unit_price).desc())
                .limit(1))
    result = query.scalar()
    return result if result is not None else 0

def get_lowest_monthly_revenue(selected_year):
    query = (db.session.query(func.month(Bill.create_date).label('month_number'))
                .filter((func.year(Bill.create_date) == selected_year) , Bill.status == BillEnum.PAID)
                .group_by(func.month(Bill.create_date))
                .order_by(func.sum(Bill.unit_price).asc())
                .limit(1))
    result = query.scalar()
    return result if result is not None else 0

def get_annual_revenue(selected_year: int):
    # 1. TẠO CTE DANH SÁCH 12 THÁNG (Months_CTE)

    # Tạo danh sách các SELECT 1, SELECT 2, ..., SELECT 12
    # Sử dụng literal_column để tạo cột "month_number" có giá trị từ 1 đến 12
    month_selects = []
    for i in range(1, 13):
        # Tạo một SELECT statement đơn giản: SELECT i AS month_number
        month_selects.append(select(literal_column(str(i)).label('month_number')))

    # Kết hợp tất cả các SELECT thành một CTE bằng UNION ALL
    months_cte = union_all(*month_selects).cte("months")

    # 2. TÍNH DOANH THU THỰC TẾ THEO THÁNG (MonthlySales_CTE)
    monthly_sales = (
        db.session.query(
            func.month(Bill.create_date).label('month_number'),
            func.sum(Bill.unit_price).label('monthly_revenue')
        )
        .filter(
            Bill.status == BillEnum.PAID,  # Lọc trạng thái PAID
            func.year(Bill.create_date) == selected_year  # Lọc theo năm được chọn
        )
        .group_by(literal_column('month_number'))  # Group theo số tháng
        .cte('monthly_sales')
    )

    # 3. OUTER JOIN và Xử lý NULL (COALESCE)

    # Tạo bí danh (Alias) cho các CTE để sử dụng trong JOIN
    M = aliased(months_cte)
    MS = aliased(monthly_sales)

    query = (
        db.session.query(
            M.c.month_number,
            # Lấy Tên Tháng: Chuyển đổi số tháng (1->12) thành giá trị ngày tháng hợp lệ
            func.monthname(func.str_to_date(
                func.concat(selected_year, '-', M.c.month_number, '-01'),
                '%Y-%c-%d')
            ).label('month_name'),
            # Dùng COALESCE để thay thế giá trị NULL (tháng không có doanh thu) bằng 0
            func.coalesce(MS.c.monthly_revenue, 0).label('total_revenue')
        )
        # LEFT JOIN (outerjoin) danh sách 12 tháng với doanh thu thực tế
        .outerjoin(MS, M.c.month_number == MS.c.month_number)
        .order_by(M.c.month_number)
    )

    result = query.all()

    # 4. CHUYỂN ĐỔI KẾT QUẢ SANG LIST OF DICTS
    data = [
        {
            'month_number': r.month_number,
            'month_name': r.month_name,
            'total_revenue': r.total_revenue
        } for r in result
    ]

    return data

def get_total_annual_revenue(selected_year: int):
    query = db.session.query(func.sum(Bill.unit_price)).filter(func.year(Bill.create_date) == selected_year)
    result = query.scalar()
    return result if result is not None else 0

def get_total_students():
    query = db.session.query(func.count(Student.id)) .filter()
    result = query.scalar()
    return result if result is not None else 0

def get_total_teachers():
    query = db.session.query(func.count(Teacher.id)) .filter()
    result = query.scalar()
    return result if result is not None else 0

def get_total_classrooms():
    query = db.session.query(func.count(Classroom.id)) .filter()
    result = query.scalar()
    return result if result is not None else 0

def get_total_passed_student():
    t = (db.session.query(Course.name,Enrollment.student_id,Enrollment.id,func.sum(GradeComponent.weight*Score.score).label('Score'))
                .filter((Course.id == GradeComponent.course_id) & (Enrollment.id == Score.enrollment_id)
                & (Score.grade_id == GradeComponent.id == GradeComponent.student_id) & (Enrollment.status==EnrollEnum.APPROVED))
                .group_by(Course.name,Enrollment.student_id,Enrollment.id)).subquery()

    query = (db.session.query(t.c.name,func.count(case((t.c.Score>=8,t.c.id))).label('Pass')
                              ,func.count(case((t.c.Score<8,t.c.id))).label('Fail'))
             .group_by(t.c.name))

    result = query.all()

    data = [{
        'course_name' : r.name,
        'pass':r.Pass,
        'fail':r.Fail
    } for r in result
    ]
    return data


def get_model_name(view, context, model, name):
    model_object = getattr(model, name)

    if model_object:
        # Trả về tên khóa học (course.name)
        return model_object.name

    # Trả về giá trị trống nếu không có khóa học nào được liên kết
    return "N/A"

if __name__=="__main__":
    with app.app_context():
        print("")