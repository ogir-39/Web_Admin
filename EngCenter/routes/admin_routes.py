from flask import Blueprint, render_template

from EngCenter import inject_admin_view

admin_bp = Blueprint('my_admin', __name__, template_folder='../templates/admin')


@admin_bp.route('/revenue')
def revenue():
    return render_template('revenue.html')
