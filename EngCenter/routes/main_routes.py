from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__, template_folder='../templates/main')

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/tmp')
def tmp():
    return render_template('tmp.html')