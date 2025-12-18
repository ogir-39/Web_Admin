from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/engdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

from EngCenter.services.admin_services import format_large_number
app.jinja_env.filters["large_number"] = format_large_number

#


from EngCenter.routes.main_routes import main_bp


app.register_blueprint(main_bp)


@app.template_filter('get_score')
def get_score_filter(scores, grade_name):
    if not scores:
        return ""
    for s in scores:
        if s.grade_component.name == grade_name:
            return "{:.2f}".format(s.score)
    return ""

@app.template_filter('calculate_total')
def calculate_total_filter(scores):
    total = 0
    if not scores: return 0
    for s in scores:
        total += s.score * s.grade_component.weight
    return round(total, 2)

@app.template_filter('format_number')
def format_number_filter(number):
    token = []
    s = str(number)
    for n in range(0,len(s),2):
        token.append(s[n:n + 2])

    final_text = "".join(token)
    return final_text

@app.template_filter('color_level')
def color_filter(text):
    if(text.__eq__("BEGINNER")):
        return "bg-beginner"
    elif(text.__eq__("INTERMEDIATE")):
        return "bg-intermediate"
    else:
        return "bg-advance"



