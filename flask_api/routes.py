from flask import render_template, url_for,flash,redirect,request,jsonify, make_response 
from flask_api import app,db,bcrypt
from flask_api.forms import RegistrationForm, LoginForm
from flask_api.models import User,Todo
from flask_login import login_user,current_user,logout_user,login_required
import uuid
import jwt 
from datetime import datetime, timedelta 
from functools import wraps 




def token_required(f): 
    @wraps(f) 
    def decorated(*args, **kwargs): 
        token = None
        
        if 'x-access-token' in request.headers: 
            token = request.headers['x-access-token'] 
       
        if not token: 
            return jsonify({'message' : 'Token is missing !!'}), 401
   
        try: 
          
            data = jwt.decode(token, app.config['SECRET_KEY']) 
            current_user = User.query.filter_by(public_id = data['public_id']) .first() 
        except: 
            return jsonify({ 
                'message' : 'Token is invalid !!'
            }), 401
        
        return  f(current_user, *args, **kwargs) 

    return decorated
   


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/base")
def base():
    return render_template('base.html')

@app.route("/register" , methods=['GET' , 'POST'])
def register():
  if current_user.is_authenticated:
        return redirect(url_for('home'))
  form =  RegistrationForm()

  if form.validate_on_submit():

      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      user = User(name=form.name.data, username=form.username.data , password=hashed_password)
      db.session.add(user)
      db.session.commit()
      flash(f'{form.name.data} votre compte à été crée', 'success')
      
      return redirect(url_for('login'))
    
  return render_template('register.html' , title='Register' , form=form)



@app.route("/login" , methods=['GET' , 'POST'])
def login():

  if current_user.is_authenticated:
      return redirect(url_for('home'))
  form =  LoginForm()
    
  if form.validate_on_submit():
     user =  User.query.filter_by(username=form.username.data).first()
     if user and bcrypt.check_password_hash(user.password, form.password.data):
      
        login_user(user , remember=form.remember.data)
        token = jwt.encode({ 
            'username': form.username.data, 
            'exp' : datetime.utcnow() + timedelta(minutes = 30) 
        }, app.config['SECRET_KEY']) 

       # return make_response(jsonify({'token' : token.decode('UTF-8')}), 201) 
        return redirect(url_for('home'))

     else:
      
         flash('Oups ! echec  de connexion verifier votre username ou votre mot de passe' , 'danger') 
         make_response( 
        'Could not verify', 
        403, 
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'} 
    ) 
        
  return render_template('login.html' , title='Login' , form=form )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html' , title='Account')

@app.route("/about")
@login_required
def about():
    todoList = Todo.query.all()
    return render_template('todo.html' , todoList=todoList) 

@app.route("/add", methods=["POST"])
def add():
    content = request.form.get("content")
    newTodo = Todo(content=content, status=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for('about'))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.status = not todo.status
    db.session.commit()
    return redirect(url_for('about'))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('about'))

@app.route("/addList", methods=["POST"])
def addList():
    content = request.form.get("content")
    newTodo = ListTodo(content=content, status=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for('about'))
