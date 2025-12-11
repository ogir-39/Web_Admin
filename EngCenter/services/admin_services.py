from datetime import datetime
from sqlalchemy import func, and_
from dateutil.relativedelta import relativedelta  # Cần cài đặt (pip install python-dateutil)

from EngCenter import db, app
from EngCenter.models.models import Bill, BillEnum, Student


def getMonthlyRevenue():
    # 1. Định nghĩa khoảng thời gian bằng Python
    # Lấy ngày đầu tiên của tháng hiện tại (00:00:00)
    start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Lấy ngày đầu tiên của tháng tiếp theo (tháng hiện tại + 1)
    start_of_next_month = start_of_month + relativedelta(months=+1)

    query = (
        db.session.query(func.sum(Bill.unit_price))
        .filter(
            # 1. Đã thanh toán
            Bill.status == BillEnum.PAID,

            # 2. Ngày hóa đơn phải >= ngày đầu tháng hiện tại
            Bill.create_date >= start_of_month,

            # 3. Ngày hóa đơn phải < ngày đầu tháng tiếp theo
            Bill.create_date < start_of_next_month
        )
    )

    print(query)
    result = query.scalar()
    return result if result is not None else 0

def getToTalStudents():
    query = db.session.query(func.count(Student.id)) .filter()
    result = query.scalar()
    return result if result is not None else 0

if __name__ == '__main__':
    with app.app_context():
        print(getToTalStudents())