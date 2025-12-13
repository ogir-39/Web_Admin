from calendar import month
from datetime import datetime, timezone
import pytz
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from EngCenter import db, app
from EngCenter.models.models import Bill, BillEnum, Student, Teacher, Classroom


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

def getMonthlyRevenue():
    # Lấy ngày đầu tiên của tháng hiện tại (00:00:00)
    start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Lấy ngày đầu tiên của tháng tiếp theo (tháng hiện tại + 1)
    start_of_next_month = start_of_month + relativedelta(months=+1)
    query = (
        db.session.query(func.sum(Bill.unit_price))
        .filter(
            Bill.status == BillEnum.PAID,
            Bill.create_date >= start_of_month,
            Bill.create_date < start_of_next_month
        )
    )
    print(f"Kiểm tra phạm vi truy vấn (UTC): Từ {start_of_month} đến {start_of_next_month}")
    print(query)
    result = query.scalar()
    return result if result is not None else 0

def getToTalStudents():
    query = db.session.query(func.count(Student.id)) .filter()
    result = query.scalar()
    return result if result is not None else 0

def getTotalTeachers():
    query = db.session.query(func.count(Teacher.id)) .filter()
    result = query.scalar()
    return result if result is not None else 0

def getTotalClassrooms():
    query = db.session.query(func.count(Classroom.id)) .filter()
    result = query.scalar()
    return result if result is not None else 0

def get_model_name(view, context, model, name):
    model_object = getattr(model, name)

    if model_object:
        # Trả về tên khóa học (course.name)
        return model_object.name

    # Trả về giá trị trống nếu không có khóa học nào được liên kết
    return "N/A"

if __name__ == '__main__':
    with app.app_context():
        print(getMonthlyRevenue())