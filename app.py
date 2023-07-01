from flask import Flask, render_template, request, redirect, url_for, session, g, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker
from form import RegisterForm, LoginForm
from flask import Blueprint
from flask_login import LoginManager
from flask_login import UserMixin
from flask import Blueprint
from flask import flash, redirect, render_template, request, jsonify, Blueprint, abort
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user,logout_user




SECRET_KEY = "some secret key"
app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databas_new2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db1 = SQLAlchemy(app)

todos = db1.relationship('TodoItem', backref='owner')


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(email):
    users= Users.query.filter_by(email=email).first()
    #Users.get_id(email)
    print(users)
    return users

class Users(db1.Model, UserMixin):
    __tablename__ = 'userssd'
    #id = db1.Column(db1.Integer, nullable=False, autoincrement=True)
    first_name = db1.Column(db1.String(255))
    last_name = db1.Column(db1.String(255))
    email = db1.Column(db1.String, unique = True, primary_key = True)
    password = db1.Column(db1.String(255))

    def __init__(self, email, first_name):
        self.email=email
        self.first_name=first_name

    def __repr__(self):
        return self.email
        #return f'Users{self.first_name}{self.email}'
    
    def get_id(self):
        return (self.email).encode('utf-8')


class Todo(db1.Model):
    __tablename__ = 'todoss'
    email = db1.Column(db1.String, primary_key=True)
    title = db1.Column(db1.String(100))
    summary= db1.Column(db1.String(1000))
    type_of_place= db1.Column(db1.String(100))
    #visited_on=db.Column(db.DateTime, default=datetime.utcnow)
    Expenditure = db1.Column(db1.Float)
    todo_owner = db1.Column(db1.String,db1.ForeignKey('userssd.email'))

    def __repr__(self):
        return f'Task{self.title}{self.summary}'

todos = db1.relationship('TodoItem', backref='owner')


todo = Blueprint('tasks', __name__)
# @todo.route('/home')
# def home():
#     return "Welcome Home."




@app.route('/register', methods = ['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit:
            users = Users(first_name =form.first_name.data,
                        last_name =form.last_name.data,
                        email =form.email.data,
                        password = generate_password_hash(form.password.data)
                        )
            db1.session.add(users)
            db1.session.commit()
            login_user(users)
            return redirect('/login')


use =[]
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit:
        users = Users.query.filter_by(email = form.email.data).first()
        print(users)
        use.append(users)
        #print(check_password_hash(str(users.password), str(form.password.data)))
        #if users.password == form.password:
        if users and check_password_hash(users.password, form.password.data):
            print("check into user")
            login_user(users)
            
            return redirect(url_for("home"))
        flash("Invalid details")
            
    return render_template('login.html', form=form)
    # if(request.method == 'POST'):
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    #     login = Users.query.filter_by(email=email, password=password).first()
    #     if login:
    #         login_user(login)
    #         return redirect(url_for("home"))
    #     flash("Invalid details")
    # return render_template("login.html")

# @app.route('/logout', methods = ['POST','GET'])
# def logout():
#     logout_user()
#     return redirect('/home')



@app.route("/")
def home():
    todo_list = Todo.query.all()
    #print(todo_list)
    print(current_user)
    print(users)
    print(load_user(email='hjy@123.com'))
    #todo_list = Todo.query.filter_by(email='hjy@1123.com') 
    #todo_list = Todo.query.filter_by(todo_owner='hjy@123.com')
    print(todo_list)
    return render_template("base.html", todo_list=todo_list, is_logged_in=current_user.is_authenticated)



@app.route("/add", methods=["POST"])
def add():
    #users = current_user
    print(use)
    email = request.form.get("email")
    title = request.form.get("title")
    summary=request.form.get("summary")
    type_of_place =request.form.get("type_of_place")
    #Expenditure=request.form.get("Expenditure")
    todo_owners=load_user(email='hjy@123.com')
    todo_owner = email

    #print(todo_owner)
    new_todo = Todo(email='hjy@123.com',title='satyaaalatest',summary='coola',type_of_place='Nonesa',Expenditure=110.31, todo_owner='hjy@123.com')
    db1.session.add(new_todo)
    db1.session.commit()
    print("committed")
    #return redirect('/todos')
    return redirect(url_for("home"))

# @todo.route('/todos')
# def todos():
    
#     todos = Todo.query.filter_by(todo_owner = current_user.email)
#     print(todos)
#     return render_template('todos.html', todos = todos)

@app.route("/update/<int:todo_id>", methods=["POST","GET"])
def update(todo_id):
    users=current_user
    todo = Todo.query.filter_by(id=todo_id).first()
    if request.method == 'GET':
        title = request.form.get("title")
        summary=request.form.get("summary")
        type_of_place =request.form.get("type_of_place")
        Expenditure=request.form.get("Expenditure")
        db1.session.commit()
        return (render_template("update.html", todo=todo))
    

    if request.method == 'POST':
        todo.title = request.form.get("title")
        todo.summary=request.form.get("summary")
        todo.type_of_places =request.form.get("type_of_place")
        todo.Expenditure=request.form.get("Expenditure")
        db1.session.commit()    #Edit
        print(db1.session.commit())
        print("user updated sucess")
        return redirect(url_for("home"))



@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id, todo_owner = current_user.id).first()
    db1.session.delete(todo)
    db1.session.commit()
    return redirect(url_for("home"))


@app.route('/logout')
def logout():
    session.pop('user')         
    return redirect('/login')

@todo.route('/users')
def users():
    users = Users.query.all()
    print(users)

    res = {}
    for user in users:
        res = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password':user.password

        }
    return jsonify(res), user.email

app.register_blueprint(todo)

if __name__ == "__main__":
    with app.app_context():
        db1.create_all()
        db1.create_all()
        app.run(debug=True, port=7000)
