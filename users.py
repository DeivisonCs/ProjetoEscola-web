from flask import Blueprint, render_template, request, redirect
from database import db
from models.tables import Students_Inf

bp_Students = Blueprint("Students", __name__, template_folder="templates")

@bp_Students.route('/create', methods=["GET", "POST"])
def create():
    if request.method == 'GET':
        return render_template("add_student.html")

    if request.method == 'POST':
        name = request.form.get("name")
        age = request.form.get("age")
        cpf = request.form.get("cpf")
        email = request.form.get("email")

        User = Students_Inf(name, age, cpf, email) 
        db.session.add(User)
        db.session.commit()
        return "Dados Cadastrados"


@bp_Students.route('/list')
def list_students():
    Students_all = Students_Inf.query.all()
    return render_template("list_students.html", Students_all=Students_all)


@bp_Students.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    User = Students_Inf.query.get(id)

    if request.method == 'GET':
        return render_template('update_student.html', User=User )
    
    if request.method == 'POST':
        User.name = request.form.get("name")
        User.age = request.form.get("age")
        User.cpf = request.form.get("cpf")
        User.email = request.form.get("email")

        db.session.add(User)
        db.session.commit()

        User = Students_Inf.query.all()
        return render_template("list_students.html", Students_all=User)
    

@bp_Students.route('/remove/<int:id>', methods=['GET'])
def remove_student(id):
    User = Students_Inf.query.get(id)

    db.session.delete(User)
    db.session.commit()
    return redirect("list_students.html")