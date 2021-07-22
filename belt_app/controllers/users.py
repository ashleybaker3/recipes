from belt_app import app
from flask import render_template, request, redirect, session, flash
from belt_app.models.users import User
from belt_app.models.recipes import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def validate():
    if not User.validate_registration(request.form):
        return redirect('/')
    
    hashed_password = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        "email" : request.form["email"],
        "password" : hashed_password
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')


@app.route('/login', methods = ['POST'])
def login():
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'email' : request.form['email']
    } 
    login_validation = User.validate_login(data)

    if not login_validation:
        return redirect('/')
    
    user_in_db = User.get_user_by_email(data)
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            flash('Invalid email/password.', "login_email")
            return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    logged_in_user = User.get_user_by_id(data)
    recipes = Recipe.get_all(data)
    print("*********************************")
    print(recipes)
    return render_template('/dashboard.html', logged_user = logged_in_user, recipes = recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')