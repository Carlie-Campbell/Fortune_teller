from flask import Flask, render_template, request, redirect, flash, session
from flask_app.models.user_model import User
from flask_app.models.fortune_model import Fortune
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)

# -------Home page----------------
@app.route('/') 
@app.route('/users')                          
def all_users():
    if 'in' not in session:
        session['in'] = ''
    return render_template('main.html')  

@app.route('/log')
def log():
    return render_template('login.html')


@app.route('/reg')
def register():
    return render_template('register.html')

# --------Register route-------------
@app.route('/users/register', methods=['POST'])
def reg_user():
# ----validate user is in system-------
    if not User.validator(request.form):
        return redirect('/')
    
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
# -------make sure stored pass is hashed-------
    data = {
        **request.form,
        'password': hashed_pass,
    }
    # --creates logged_user id, stores info in session---
    logged_user_id = User.create(data)
    session['user_id'] = logged_user_id
    session['first_name'] = request.form['first_name']
    return redirect('/dashboard')

# ------------Login route ----------
@app.route('/users/login', methods=['POST'])
def log_user():
    # ------makes sure email from form is in system----
    data = {
        'email':request.form['email']
    }
    potential_user = User.get_by_email(data)
    # ------if not flashes/redirects home--------
    if not potential_user:
        flash('Invalid Credentials', 'log')
        print('User not found')
        return redirect('/')
    
    # ------------Bcrypt hash----verifies pass or flashes/redirects
    if not bcrypt.check_password_hash(potential_user.password, request.form['password']):
        flash('Invalid Credentials', 'log')
        print('Invalid password')
        return redirect('/')
    # -------stores name/id in session and redirects to dashb---------
    session['user_id'] = potential_user.id
    session['first_name'] = potential_user.first_name
    return redirect('/dashboard')

# -------------logout------------
@app.route('/users/logout')
def logout():
    del session['user_id']
    del session['first_name']
    return redirect('/')