from flask import Blueprint, render_template

from EngCenter.services import admin_services

main_bp = Blueprint('main', __name__, template_folder='../templates/main')

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/tmp')
def tmp():
    return render_template('tmp.html')

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')

@admin_bp.route('/admin')
def index():
    total_students = admin_services.getToTalStudents()
    return render_template('index.html',total_students = total_students)
