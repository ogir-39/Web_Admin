from flask import render_template
from EngCenter import app, admin, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        app.run(debug=True)
