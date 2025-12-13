from flask import Blueprint, render_template, current_app


admin_bp = Blueprint('my_admin', __name__, template_folder='../templates/admin')

@current_app.context_processor
def inject_admin_view():
    return dict(
        admin_view={
            'admin_view_url': '/admin/',
            'admin_view_name': 'ENGLISH CENTER'
        }
    )
@admin_bp.route('/admin/statistic_revenue/', methods=['GET'])
def revenue():
    return render_template('statistic_revenue.html',admin_view=inject_admin_view())
