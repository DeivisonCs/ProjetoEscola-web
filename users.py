from flask import Blueprint, render_template, request, redirect
from database import db
from models.tables import Students_Inf
from datetime import datetime

bp_Students = Blueprint("Students", __name__, template_folder="templates")

@bp_Students.route('/create', methods=["GET", "POST"])
def create():
    if request.method == 'GET':
        return render_template("add_student.html", show_alert=False)

    if request.method == 'POST':
        name = request.form.get("name")
        birth_date = request.form.get("birth_date")
        cpf = request.form.get("cpf")
        email = request.form.get("email")

        valid = valid_cad(name, birth_date, cpf, email)

        if valid == True:
            age = valid_age(birth_date)

            User = Students_Inf(name, age, cpf, email) 
            db.session.add(User)
            db.session.commit()
            
            return redirect("/")
        
        elif valid == 0:
            return render_template('add_student.html', mensage='Preencha todos os campos!', show_alert=True)

        elif valid == "Idade Inválida!":
            return render_template('add_student.html', mensage='Idade Inválida!', show_alert=True)
        
        elif valid == "CPF inválido":
            return render_template('add_student.html', mensage='CPF Inválido!', show_alert=True)

        elif valid == "CPF ja cadastrado":
            return render_template('add_student.html', mensage='CPF já Cadastrado!', show_alert=True)
        
        elif valid == "Email em Uso":
            return render_template('add_student.html', mensage='Email em Uso!', show_alert=True)
        


@bp_Students.route('/list')
def list_students():
    Students_all = Students_Inf.query.all()
    return render_template("list_students.html", Students_all=Students_all)


@bp_Students.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    User = Students_Inf.query.get(id)
    Users = Students_Inf.query.all()

    if request.method == 'GET':
        return render_template('update_student.html', User=User )
    
    if request.method == 'POST':
        name = request.form.get("name")
        age = request.form.get("birth_date")
        cpf = request.form.get("cpf")
        email = request.form.get("email")

        valid = valid_updt(User.id, name, age, cpf, email)
        
        if valid == True:
            User.name = name
            User.age = age
            User.cpf = cpf
            User.email = email

            db.session.add(User)
            db.session.commit()
            
            # User = Students_Inf.query.all()
            # return render_template("list_students.html", Students_all=User)
            return redirect("/User/list")
        
        elif valid == 0:
            return render_template('update_student.html', User=User, mensage='Preencha todos os campos!', show_alert=True)
        
        elif valid == "Idade Inválida!":
            return render_template('update_student.html', User=User, mensage='Idade Inválida!', show_alert=True)
        
        elif valid == "CPF inválido":
            return render_template('update_student.html', User=User, mensage='CPF Inválido!', show_alert=True)

        elif valid == "CPF ja cadastrado":
            return render_template('update_student.html', User=User, mensage='CPF já Cadastrado!', show_alert=True)
        
        elif valid == "Email em Uso":
            return render_template('update_student.html', User=User, mensage='Email em Uso!', show_alert=True)
    

@bp_Students.route('/remove/<int:id>', methods=['GET'])
def remove_student(id):
    User = Students_Inf.query.get(id)

    db.session.delete(User)
    db.session.commit()
    return redirect("/User/list")



# ------------------------ Validações -----------------------

# Validação do Cadastro de Novo Aluno
def valid_cad(name, birth_date, cpf, email):

    if name=="" or birth_date=="" or cpf=="" or email=="":
        return 0

    age = valid_age(birth_date)

    if age <= 0:
        return "Idade Inválida!"
    
    cpf_valid = valid_cpf(cpf)

    if cpf_valid == "CPF inválido":
        return "CPF inválido"
    
    if cpf_valid == "CPF ja cadastrado":
        return "CPF ja cadastrado"
    
    Users = Students_Inf.query.all()

    for user in Users:
        if user.email == email:
            return "Email em Uso"

    return True


def valid_updt(id, name, age, cpf, email):

    if name=="" or age=="" or cpf=="" or email=="":
        return 0

    if int(age) <= 0:
        return "Idade Inválida!"
    
    only_Num_CPF = ''.join(filter(str.isdigit, cpf))
    
    if len(only_Num_CPF) != 11:
        return "CPF inválido"

    else:
        Users = Students_Inf.query.all()

        for user in Users:
            no_Num_CPF = ''.join(filter(str.isdigit, user.cpf))

            if no_Num_CPF == only_Num_CPF and user.id != id:
                return "CPF ja cadastrado"
            
            elif user.email == email and user.id != id:
                return "Email em Uso"
    
    
    return True


def valid_cpf(cpf):
    only_Num_CPF = ''.join(filter(str.isdigit, cpf))
    
    if len(only_Num_CPF) != 11:
        return "CPF inválido"

    else:
        Users = Students_Inf.query.all()
        for user in Users:
            no_Num_CPF = ''.join(filter(str.isdigit, user.cpf))

            if no_Num_CPF == only_Num_CPF:
                return "CPF ja cadastrado"

    return True

def valid_age(birth_date):
    age = datetime.strptime(birth_date, "%Y-%m-%d")
    date_atual = datetime.now()
    diff = date_atual - age
    age = diff.days // 365

    return age

# 000.000.000-00