from flask import Flask, render_template
from database import db
from flask_migrate import Migrate
from users import bp_Students

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MyKeY0192'
app.register_blueprint(bp_Students, url_prefix='/User')
db.init_app(app)

migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()