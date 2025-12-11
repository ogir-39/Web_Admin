from flask import Blueprint, render_template

from EngCenter.services import admin_services

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')

@admin_bp.route('/')
def index():
    total_students = admin_services.getToTalStudents()
    return render_template('index.html',total_students = total_students)