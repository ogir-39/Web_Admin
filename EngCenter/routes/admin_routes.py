from flask import Blueprint, render_template

admin_bp = Blueprint('my_admin', __name__, template_folder='../templates/admin')

@admin_bp.route('/admin/statistic_revenue/', methods=['GET'])
def revenue():
    return render_template('statistic_revenue.html')
