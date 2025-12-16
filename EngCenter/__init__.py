from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/engdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

from EngCenter.services.admin_services import format_large_number
app.jinja_env.filters["large_number"] = format_large_number

@app.context_processor
def inject_admin_view():
    return dict(
        admin_view={
            'admin_view_url': '/admin/',
            'admin_view_name': 'ENGLISH CENTER'
        }
    )

from EngCenter.routes.main_routes import main_bp
app.register_blueprint(main_bp)



